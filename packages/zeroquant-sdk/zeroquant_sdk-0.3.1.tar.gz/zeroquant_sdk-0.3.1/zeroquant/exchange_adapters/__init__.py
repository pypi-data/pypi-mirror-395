"""
Exchange Adapters Module

Provides an agnostic order validation and routing layer for centralized exchanges.
Routes orders through validation, then forwards to exchanges with original credentials.

Supported Exchanges:
- Binance (spot)
- Coinbase (Advanced Trade)
- Kraken

Example:
    import os
    from zeroquant.exchange_adapters import (
        ExchangeRouter,
        ExchangeCredentials,
        RouteOrderRequest,
        SupportedExchange,
        create_agent_router,
    )
    from zeroquant.orders import MinimumViableOrder

    # Create router with agent limits
    router = create_agent_router(
        daily_limit_usd=50000,
        per_tx_limit_usd=10000,
    )

    # Route an order
    result = await router.route_order(
        RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=2.5,
                original_price=2000,
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key=os.environ["BINANCE_KEY"],
                api_secret=os.environ["BINANCE_SECRET"],
            ),
        )
    )
"""

from .types import (
    SupportedExchange,
    ExchangeCredentials,
    ExchangeConfig,
    ValidationRules,
    ValidationResult,
    ValidationError,
    RouteOrderRequest,
    RouteOrderResponse,
    CancelOrderRequest,
    CancelOrderResponse,
    QueryOrdersRequest,
    MarketData,
)
from .base_adapter import BaseExchangeAdapter
from .binance import BinanceAdapter
from .coinbase import CoinbaseAdapter
from .kraken import KrakenAdapter
from .router import (
    ExchangeRouter,
    RouterConfig,
    RouterStats,
    create_router,
    create_agent_router,
)

__all__ = [
    # Types
    "SupportedExchange",
    "ExchangeCredentials",
    "ExchangeConfig",
    "ValidationRules",
    "ValidationResult",
    "ValidationError",
    "RouteOrderRequest",
    "RouteOrderResponse",
    "CancelOrderRequest",
    "CancelOrderResponse",
    "QueryOrdersRequest",
    "MarketData",
    # Base adapter
    "BaseExchangeAdapter",
    # Exchange adapters
    "BinanceAdapter",
    "CoinbaseAdapter",
    "KrakenAdapter",
    # Router
    "ExchangeRouter",
    "RouterConfig",
    "RouterStats",
    "create_router",
    "create_agent_router",
]
