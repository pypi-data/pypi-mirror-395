"""
Coinbase Exchange Adapter
Routes orders to Coinbase Advanced Trade API
"""

import hmac
import hashlib
import time
import secrets
from typing import Optional, List, Dict, Any

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


class CoinbaseAdapter(BaseExchangeAdapter):
    """Coinbase exchange adapter for Advanced Trade API."""

    def __init__(
        self,
        testnet: bool = False,
        base_url: Optional[str] = None,
        timeout: int = 30000,
    ):
        """
        Initialize Coinbase adapter.

        Args:
            testnet: Use sandbox API
            base_url: Custom API endpoint
            timeout: Request timeout in ms
        """
        config = ExchangeConfig(
            exchange=SupportedExchange.COINBASE,
            testnet=testnet,
            base_url=base_url,
            timeout=timeout,
        )
        super().__init__(config)

        self.base_url = (
            "https://api-sandbox.coinbase.com/api/v3/brokerage"
            if testnet
            else (base_url or "https://api.coinbase.com/api/v3/brokerage")
        )
        self._client = httpx.AsyncClient(timeout=timeout / 1000)

    @property
    def exchange(self) -> SupportedExchange:
        return SupportedExchange.COINBASE

    @property
    def display_name(self) -> str:
        return "Coinbase"

    def to_exchange_format(self, order: MinimumViableOrder) -> Dict[str, Any]:
        """Convert MVO to Coinbase order format."""
        client_order_id = f"zq_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
        symbol = order.symbol or f"{order.base_asset}/{order.quote_asset}"
        product_id = self.to_exchange_symbol(symbol)

        coinbase_order: Dict[str, Any] = {
            "client_order_id": client_order_id,
            "product_id": product_id,
            "side": "BUY" if order.side and order.side.upper() == "BUY" else "SELL",
            "order_configuration": {},
        }

        # Market order
        if order.original_price is None or order.original_price == 0:
            coinbase_order["order_configuration"]["market_market_ioc"] = {
                "base_size": str(order.original_quantity_base) if order.original_quantity_base else "0",
            }
        else:
            # Limit order - determine time in force
            tif = order.time_in_force.lower() if order.time_in_force else "gtc"

            if tif == "fok":
                coinbase_order["order_configuration"]["limit_limit_fok"] = {
                    "base_size": str(order.original_quantity_base or 0),
                    "limit_price": str(order.original_price),
                }
            elif tif == "gtd":
                from datetime import datetime, timedelta
                end_time = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
                coinbase_order["order_configuration"]["limit_limit_gtd"] = {
                    "base_size": str(order.original_quantity_base or 0),
                    "limit_price": str(order.original_price),
                    "end_time": end_time,
                    "post_only": False,
                }
            else:  # GTC default
                coinbase_order["order_configuration"]["limit_limit_gtc"] = {
                    "base_size": str(order.original_quantity_base or 0),
                    "limit_price": str(order.original_price),
                    "post_only": False,
                }

        return coinbase_order

    def from_exchange_format(self, response: Dict[str, Any]) -> ExchangeOrderResponse:
        """Convert Coinbase response to standard format."""
        return ExchangeOrderResponse(
            exchange_order_id=response.get("order_id"),
            is_maker=response.get("order_type") == "LIMIT",
            order_type=response.get("order_type", "").lower() if response.get("order_type") else None,
            average_price=float(response.get("average_filled_price", 0)) or None,
            executed_quantity_base=float(response.get("filled_size", 0)) or None,
            status=self._map_status(response.get("status", "")),
            amount_executed_quote=float(response.get("total_value_after_fees", 0)) or None,
            fee_paid=float(response.get("total_fees", 0)) or None,
            average_entry_price=float(response.get("average_filled_price", 0)) or 0,
        )

    def to_exchange_symbol(self, symbol: str) -> str:
        """Convert symbol to Coinbase format (ETH/USDC -> ETH-USDC)."""
        return symbol.replace("/", "-").upper()

    def from_exchange_symbol(self, symbol: str) -> str:
        """Convert from Coinbase symbol format."""
        return symbol.replace("-", "/")

    async def _submit_to_exchange(
        self,
        order: Dict[str, Any],
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Submit order to Coinbase."""
        import json
        body = json.dumps(order)
        timestamp = str(int(time.time()))
        method = "POST"
        path = "/api/v3/brokerage/orders"

        headers = self._create_signature(method, path, body, credentials)
        headers["Content-Type"] = "application/json"
        headers["CB-ACCESS-TIMESTAMP"] = timestamp

        response = await self._client.post(
            f"{self.base_url}/orders",
            content=body,
            headers=headers,
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Coinbase error: {error.get('message', response.text)}")

        return response.json()

    async def _cancel_on_exchange(
        self,
        order_id: str,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Cancel order on Coinbase."""
        import json
        body = json.dumps({"order_ids": [order_id]})
        timestamp = str(int(time.time()))
        method = "POST"
        path = "/api/v3/brokerage/orders/batch_cancel"

        headers = self._create_signature(method, path, body, credentials)
        headers["Content-Type"] = "application/json"
        headers["CB-ACCESS-TIMESTAMP"] = timestamp

        response = await self._client.post(
            f"{self.base_url}/orders/batch_cancel",
            content=body,
            headers=headers,
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Coinbase cancel error: {error.get('message', response.text)}")

        return response.json()

    async def _query_from_exchange(
        self,
        request: QueryOrdersRequest,
    ) -> List[Dict[str, Any]]:
        """Query orders from Coinbase."""
        params = []
        if request.symbol:
            params.append(f"product_id={self.to_exchange_symbol(request.symbol)}")
        if request.open_only:
            params.append("order_status=PENDING,OPEN")
        if request.limit:
            params.append(f"limit={request.limit}")

        query_string = f"?{'&'.join(params)}" if params else ""
        timestamp = str(int(time.time()))
        method = "GET"
        path = f"/api/v3/brokerage/orders/historical/batch{query_string}"

        headers = self._create_signature(method, path, "", request.credentials)
        headers["CB-ACCESS-TIMESTAMP"] = timestamp

        response = await self._client.get(
            f"{self.base_url}/orders/historical/batch{query_string}",
            headers=headers,
        )

        if response.status_code != 200:
            error = response.json()
            raise Exception(f"Coinbase query error: {error.get('message', response.text)}")

        data = response.json()
        return data.get("orders", [])

    async def get_market_data(
        self,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Optional[MarketData]:
        """Get market data from Coinbase."""
        try:
            product_id = self.to_exchange_symbol(symbol)
            timestamp = str(int(time.time()))
            method = "GET"
            path = f"/api/v3/brokerage/products/{product_id}"

            headers = self._create_signature(method, path, "", credentials)
            headers["CB-ACCESS-TIMESTAMP"] = timestamp

            response = await self._client.get(
                f"{self.base_url}/products/{product_id}",
                headers=headers,
            )

            if response.status_code != 200:
                return None

            product = response.json()

            return MarketData(
                symbol=symbol,
                current_price=float(product.get("price", 0)),
                min_order_size=float(product.get("base_min_size", 0)) or None,
                max_order_size=float(product.get("base_max_size", 0)) or None,
                step_size=float(product.get("base_increment", 0)) or None,
                tick_size=float(product.get("quote_increment", 0)) or None,
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
        """Create Coinbase signature headers."""
        timestamp = str(int(time.time()))
        message = timestamp + method + path + body
        signature = hmac.new(
            credentials.api_secret.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

        return {
            "CB-ACCESS-KEY": credentials.api_key,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
        }

    def _map_status(self, status: str) -> Optional[str]:
        """Map Coinbase status to standard status."""
        status_map = {
            "PENDING": "open",
            "OPEN": "open",
            "FILLED": "filled",
            "CANCELLED": "cancelled",
            "EXPIRED": "expired",
            "FAILED": "failed",
        }
        return status_map.get(status.upper() if status else "", status.lower() if status else None)

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
