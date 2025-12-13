"""
Binance Exchange Adapter
Routes orders to Binance spot/futures API
"""

import hmac
import hashlib
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


class BinanceAdapter(BaseExchangeAdapter):
    """Binance exchange adapter for spot trading."""

    def __init__(
        self,
        testnet: bool = False,
        base_url: Optional[str] = None,
        timeout: int = 30000,
    ):
        """
        Initialize Binance adapter.

        Args:
            testnet: Use testnet API
            base_url: Custom API endpoint
            timeout: Request timeout in ms
        """
        config = ExchangeConfig(
            exchange=SupportedExchange.BINANCE,
            testnet=testnet,
            base_url=base_url,
            timeout=timeout,
        )
        super().__init__(config)

        self.base_url = (
            "https://testnet.binance.vision/api/v3"
            if testnet
            else (base_url or "https://api.binance.com/api/v3")
        )
        self._client = httpx.AsyncClient(timeout=timeout / 1000)

    @property
    def exchange(self) -> SupportedExchange:
        return SupportedExchange.BINANCE

    @property
    def display_name(self) -> str:
        return "Binance"

    def to_exchange_format(self, order: MinimumViableOrder) -> Dict[str, Any]:
        """Convert MVO to Binance order format."""
        symbol = order.symbol or f"{order.base_asset}/{order.quote_asset}"
        binance_order: Dict[str, Any] = {
            "symbol": self.to_exchange_symbol(symbol),
            "side": "BUY" if order.side and order.side.upper() == "BUY" else "SELL",
            "type": self._map_order_type(order),
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }

        # Add quantity
        if order.original_quantity_base is not None:
            binance_order["quantity"] = str(order.original_quantity_base)

        # Add price for limit orders
        if order.original_price is not None and order.original_price > 0:
            binance_order["price"] = str(order.original_price)

        # Add time in force for limit orders
        if binance_order["type"] == "LIMIT":
            binance_order["timeInForce"] = self._map_time_in_force(order.time_in_force)

        return binance_order

    def from_exchange_format(self, response: Dict[str, Any]) -> ExchangeOrderResponse:
        """Convert Binance response to standard format."""
        # Calculate fees from fills
        total_fee = 0.0
        fee_asset = ""
        if "fills" in response and response["fills"]:
            for fill in response["fills"]:
                total_fee += float(fill.get("commission", 0))
                fee_asset = fill.get("commissionAsset", "")

        # Calculate average price
        average_price = 0.0
        if "fills" in response and response["fills"]:
            total_value = sum(
                float(f["price"]) * float(f["qty"])
                for f in response["fills"]
            )
            total_qty = sum(float(f["qty"]) for f in response["fills"])
            average_price = total_value / total_qty if total_qty > 0 else 0
        elif float(response.get("executedQty", 0)) > 0:
            average_price = (
                float(response.get("cummulativeQuoteQty", 0)) /
                float(response["executedQty"])
            )

        return ExchangeOrderResponse(
            exchange_order_id=str(response.get("orderId", "")),
            is_maker=response.get("type") == "LIMIT",
            order_type=response.get("type", "").lower() if response.get("type") else None,
            average_price=average_price or None,
            executed_quantity_base=float(response.get("executedQty", 0)) or None,
            status=self._map_status(response.get("status", "")),
            amount_executed_quote=float(response.get("cummulativeQuoteQty", 0)) or None,
            fee_paid=total_fee or None,
            fee_asset=fee_asset or None,
            average_entry_price=average_price,
        )

    def to_exchange_symbol(self, symbol: str) -> str:
        """Convert symbol to Binance format (ETH/USDC -> ETHUSDC)."""
        return symbol.replace("/", "").upper()

    def from_exchange_symbol(self, symbol: str) -> str:
        """Convert from Binance symbol format."""
        quote_assets = ["USDT", "USDC", "BUSD", "BTC", "ETH", "BNB"]
        for quote in quote_assets:
            if symbol.endswith(quote):
                base = symbol[:-len(quote)]
                return f"{base}/{quote}"
        return symbol

    async def _submit_to_exchange(
        self,
        order: Dict[str, Any],
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Submit order to Binance."""
        params = urlencode(order)
        signature = self._sign(params, credentials.api_secret)
        signed_params = f"{params}&signature={signature}"

        response = await self._client.post(
            f"{self.base_url}/order",
            params=signed_params,
            headers={"X-MBX-APIKEY": credentials.api_key},
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Binance error: {error.get('msg', response.text)}")

        return response.json()

    async def _cancel_on_exchange(
        self,
        order_id: str,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Cancel order on Binance."""
        params = urlencode({
            "symbol": self.to_exchange_symbol(symbol),
            "orderId": int(order_id),
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        })
        signature = self._sign(params, credentials.api_secret)
        signed_params = f"{params}&signature={signature}"

        response = await self._client.delete(
            f"{self.base_url}/order",
            params=signed_params,
            headers={"X-MBX-APIKEY": credentials.api_key},
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Binance cancel error: {error.get('msg', response.text)}")

        return response.json()

    async def _query_from_exchange(
        self,
        request: QueryOrdersRequest,
    ) -> List[Dict[str, Any]]:
        """Query orders from Binance."""
        params: Dict[str, Any] = {
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }

        if request.symbol:
            params["symbol"] = self.to_exchange_symbol(request.symbol)
        if request.limit:
            params["limit"] = request.limit

        query_string = urlencode(params)
        signature = self._sign(query_string, request.credentials.api_secret)
        signed_params = f"{query_string}&signature={signature}"

        endpoint = "openOrders" if request.open_only else "allOrders"
        response = await self._client.get(
            f"{self.base_url}/{endpoint}",
            params=signed_params,
            headers={"X-MBX-APIKEY": request.credentials.api_key},
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Binance query error: {error.get('msg', response.text)}")

        return response.json()

    async def get_market_data(
        self,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Optional[MarketData]:
        """Get market data from Binance."""
        try:
            exchange_symbol = self.to_exchange_symbol(symbol)

            # Fetch exchange info and price
            info_resp, price_resp = await asyncio.gather(
                self._client.get(f"{self.base_url}/exchangeInfo", params={"symbol": exchange_symbol}),
                self._client.get(f"{self.base_url}/ticker/price", params={"symbol": exchange_symbol}),
            )

            if info_resp.status_code != 200 or price_resp.status_code != 200:
                return None

            exchange_info = info_resp.json()
            price_data = price_resp.json()

            symbol_info = exchange_info.get("symbols", [{}])[0]
            if not symbol_info:
                return None

            # Parse filters
            lot_size_filter = next(
                (f for f in symbol_info.get("filters", []) if f["filterType"] == "LOT_SIZE"),
                {},
            )
            price_filter = next(
                (f for f in symbol_info.get("filters", []) if f["filterType"] == "PRICE_FILTER"),
                {},
            )

            return MarketData(
                symbol=symbol,
                current_price=float(price_data.get("price", 0)),
                min_order_size=float(lot_size_filter.get("minQty", 0)) or None,
                max_order_size=float(lot_size_filter.get("maxQty", 0)) or None,
                step_size=float(lot_size_filter.get("stepSize", 0)) or None,
                tick_size=float(price_filter.get("tickSize", 0)) or None,
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
        """Create signature headers."""
        signature = self._sign(body, credentials.api_secret)
        return {
            "X-MBX-APIKEY": credentials.api_key,
            "signature": signature,
        }

    def _sign(self, query_string: str, secret: str) -> str:
        """Sign a query string with HMAC SHA256."""
        return hmac.new(
            secret.encode(),
            query_string.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _map_order_type(self, order: MinimumViableOrder) -> str:
        """Map MVO to Binance order type."""
        if order.original_price is None or order.original_price == 0:
            return "MARKET"
        return "LIMIT"

    def _map_time_in_force(self, tif: Optional[str]) -> str:
        """Map time in force to Binance format."""
        if tif:
            tif_lower = tif.lower()
            if tif_lower == "ioc":
                return "IOC"
            elif tif_lower == "fok":
                return "FOK"
        return "GTC"

    def _map_status(self, status: str) -> Optional[str]:
        """Map Binance status to standard status."""
        status_map = {
            "NEW": "open",
            "PARTIALLY_FILLED": "partially_filled",
            "FILLED": "filled",
            "CANCELED": "cancelled",
            "REJECTED": "rejected",
            "EXPIRED": "expired",
        }
        return status_map.get(status, status.lower() if status else None)

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()


# Import asyncio for parallel requests
import asyncio
