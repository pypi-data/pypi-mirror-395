"""
Kraken Exchange Adapter
Routes orders to Kraken API
"""

import hmac
import hashlib
import base64
import time
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode

import httpx

from ..orders.mvo import MinimumViableOrder, ExchangeOrderResponse
from .types import (
    SupportedExchange,
    ExchangeCredentials,
    ExchangeConfig,
    QueryOrdersRequest,
    MarketData,
)
from .base_adapter import BaseExchangeAdapter


class KrakenAdapter(BaseExchangeAdapter):
    """Kraken exchange adapter for spot trading."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30000,
    ):
        """
        Initialize Kraken adapter.

        Args:
            base_url: Custom API endpoint
            timeout: Request timeout in ms
        """
        config = ExchangeConfig(
            exchange=SupportedExchange.KRAKEN,
            base_url=base_url,
            timeout=timeout,
        )
        super().__init__(config)

        self.base_url = base_url or "https://api.kraken.com"
        self._client = httpx.AsyncClient(timeout=timeout / 1000)

    @property
    def exchange(self) -> SupportedExchange:
        return SupportedExchange.KRAKEN

    @property
    def display_name(self) -> str:
        return "Kraken"

    def to_exchange_format(self, order: MinimumViableOrder) -> Dict[str, Any]:
        """Convert MVO to Kraken order format."""
        symbol = order.symbol or f"{order.base_asset}/{order.quote_asset}"
        kraken_order: Dict[str, Any] = {
            "nonce": int(time.time() * 1000),
            "pair": self.to_exchange_symbol(symbol),
            "type": "buy" if order.side and order.side.lower() == "buy" else "sell",
            "ordertype": "limit" if order.original_price else "market",
            "volume": str(order.original_quantity_base or 0),
        }

        # Add price for limit orders
        if order.original_price is not None and order.original_price > 0:
            kraken_order["price"] = str(order.original_price)

        # Add time in force
        if order.time_in_force:
            kraken_order["timeinforce"] = self._map_time_in_force(order.time_in_force)

        # Add reduce only
        if order.reduce_only:
            kraken_order["reduce_only"] = True

        return kraken_order

    def from_exchange_format(self, response: Dict[str, Any]) -> ExchangeOrderResponse:
        """Convert Kraken response to standard format."""
        # Handle query response format (order info)
        if "status" in response:
            return ExchangeOrderResponse(
                exchange_order_id=response.get("txid"),
                is_maker=response.get("descr", {}).get("ordertype") == "limit",
                order_type=response.get("descr", {}).get("ordertype"),
                average_price=float(response.get("price", 0)) or None,
                executed_quantity_base=float(response.get("vol_exec", 0)) or None,
                status=self._map_status(response.get("status", "")),
                amount_executed_quote=float(response.get("cost", 0)) or None,
                fee_paid=float(response.get("fee", 0)) or None,
                average_entry_price=float(response.get("price", 0)) or 0,
            )

        # Handle add order response format
        txid = None
        if "result" in response and "txid" in response["result"]:
            txid = response["result"]["txid"][0] if response["result"]["txid"] else None

        return ExchangeOrderResponse(
            exchange_order_id=txid,
            is_maker=False,
            status="open" if txid else "failed",
            average_entry_price=0,
        )

    def to_exchange_symbol(self, symbol: str) -> str:
        """Convert symbol to Kraken format."""
        normalized = symbol.replace("/", "").upper()

        # Kraken-specific mappings
        kraken_mappings = {
            "BTCUSD": "XXBTZUSD",
            "BTCUSDT": "XBTUSDT",
            "BTCUSDC": "XBTUSDC",
            "ETHUSD": "XETHZUSD",
            "ETHUSDT": "ETHUSDT",
            "ETHUSDC": "ETHUSDC",
            "ETHBTC": "XETHXXBT",
        }

        return kraken_mappings.get(normalized, normalized)

    def from_exchange_symbol(self, symbol: str) -> str:
        """Convert from Kraken symbol format."""
        reverse_mappings = {
            "XXBTZUSD": "BTC/USD",
            "XBTUSDT": "BTC/USDT",
            "XBTUSDC": "BTC/USDC",
            "XETHZUSD": "ETH/USD",
            "ETHUSDT": "ETH/USDT",
            "ETHUSDC": "ETH/USDC",
            "XETHXXBT": "ETH/BTC",
        }
        return reverse_mappings.get(symbol, symbol)

    async def _submit_to_exchange(
        self,
        order: Dict[str, Any],
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Submit order to Kraken."""
        path = "/0/private/AddOrder"
        post_data = urlencode(order)

        headers = self._create_signature("POST", path, post_data, credentials)
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = await self._client.post(
            f"{self.base_url}{path}",
            content=post_data,
            headers=headers,
        )

        data = response.json()

        if data.get("error") and len(data["error"]) > 0:
            raise Exception(f"Kraken error: {', '.join(data['error'])}")

        return data

    async def _cancel_on_exchange(
        self,
        order_id: str,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Cancel order on Kraken."""
        path = "/0/private/CancelOrder"
        post_data = urlencode({
            "nonce": int(time.time() * 1000),
            "txid": order_id,
        })

        headers = self._create_signature("POST", path, post_data, credentials)
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = await self._client.post(
            f"{self.base_url}{path}",
            content=post_data,
            headers=headers,
        )

        data = response.json()

        if data.get("error") and len(data["error"]) > 0:
            raise Exception(f"Kraken cancel error: {', '.join(data['error'])}")

        return data

    async def _query_from_exchange(
        self,
        request: QueryOrdersRequest,
    ) -> List[Dict[str, Any]]:
        """Query orders from Kraken."""
        path = "/0/private/OpenOrders" if request.open_only else "/0/private/ClosedOrders"
        post_data = urlencode({
            "nonce": int(time.time() * 1000),
            "trades": True,
        })

        headers = self._create_signature("POST", path, post_data, request.credentials)
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = await self._client.post(
            f"{self.base_url}{path}",
            content=post_data,
            headers=headers,
        )

        data = response.json()

        if data.get("error") and len(data["error"]) > 0:
            raise Exception(f"Kraken query error: {', '.join(data['error'])}")

        # Convert to list of orders
        orders = data.get("result", {}).get("open", {}) or data.get("result", {}).get("closed", {})
        return [{"txid": txid, **order_info} for txid, order_info in orders.items()]

    async def get_market_data(
        self,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Optional[MarketData]:
        """Get market data from Kraken."""
        try:
            pair = self.to_exchange_symbol(symbol)

            # Fetch asset pairs and ticker
            import asyncio
            pairs_resp, ticker_resp = await asyncio.gather(
                self._client.get(f"{self.base_url}/0/public/AssetPairs", params={"pair": pair}),
                self._client.get(f"{self.base_url}/0/public/Ticker", params={"pair": pair}),
            )

            if pairs_resp.status_code != 200 or ticker_resp.status_code != 200:
                return None

            pairs_data = pairs_resp.json()
            ticker_data = ticker_resp.json()

            if pairs_data.get("error") or ticker_data.get("error"):
                return None

            pair_info = list(pairs_data.get("result", {}).values())[0] if pairs_data.get("result") else {}
            ticker = list(ticker_data.get("result", {}).values())[0] if ticker_data.get("result") else {}

            if not pair_info or not ticker:
                return None

            return MarketData(
                symbol=symbol,
                current_price=float(ticker.get("c", [0])[0]),
                min_order_size=float(pair_info.get("ordermin", 0)) or None,
                price_precision=pair_info.get("pair_decimals"),
                quantity_precision=pair_info.get("lot_decimals"),
            )
        except Exception:
            return None

    def _create_signature(
        self,
        method: str,
        path: str,
        body: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, str]:
        """Create Kraken API signature."""
        # Parse nonce from body
        from urllib.parse import parse_qs
        params = parse_qs(body)
        nonce = params.get("nonce", [str(int(time.time() * 1000))])[0]

        # Create signature
        message = nonce + body
        message_hash = hashlib.sha256(message.encode()).digest()
        secret = base64.b64decode(credentials.api_secret)
        hmac_obj = hmac.new(secret, path.encode() + message_hash, hashlib.sha512)
        signature = base64.b64encode(hmac_obj.digest()).decode()

        return {
            "API-Key": credentials.api_key,
            "API-Sign": signature,
        }

    def _map_time_in_force(self, tif: Optional[str]) -> str:
        """Map time in force to Kraken format."""
        if tif:
            tif_lower = tif.lower()
            if tif_lower == "ioc":
                return "IOC"
            elif tif_lower == "gtd":
                return "GTD"
        return "GTC"

    def _map_status(self, status: str) -> Optional[str]:
        """Map Kraken status to standard status."""
        status_map = {
            "pending": "open",
            "open": "open",
            "closed": "filled",
            "canceled": "cancelled",
            "expired": "expired",
        }
        return status_map.get(status.lower() if status else "", status.lower() if status else None)

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
