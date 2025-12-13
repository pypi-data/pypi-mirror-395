"""
ZeroQuant Python SDK for agentic DeFi vaults.
"""

__version__ = "0.3.0"

from .client import ZeroQuantClient
from .models import (
    VaultConfig,
    SwapParams,
    ExecuteParams,
    ExecuteBatchParams,
    TransactionResult,
    GasEstimate,
    AgentSession,
    CreateSessionParams,
)
from .intents.swap import SwapIntent
from .exceptions import (
    ZeroQuantError,
    NotConnectedError,
    ReadOnlyError,
    ValidationError,
    TransactionError,
    ContractError,
)
from .retry import (
    RetryConfig,
    with_retry,
    with_retry_async,
    retry_async,
    retry_sync,
)

# Order management
from .orders import (
    Order,
    OrderFill,
    OrderFees,
    CreateOrderParams,
    OrderSide,
    OrderType,
    TimeInForce,
    OrderStatus,
    OrderQueryParams,
    PlaceOrderResult,
    CancelOrderResult,
    OrderStats,
    MinimumViableOrder,
    ExchangeOrderResponse,
    InternalOrderState,
    MVORecord,
    MVOManager,
    OrderManager,
)

# TEE integration
from .tee import (
    TEEPlatform,
    AttestationStatus,
    TCBVersion,
    AMDSEVReport,
    TEEAttestation,
    TrustedMeasurement,
    EffectiveLimits,
    AttestationResult,
    AMDSEVClient,
    # Intel TDX
    IntelTDXClient,
    TDXQuote,
    TDReport,
    TDInfo,
    TDXTCBInfo,
)

# Position tracking
from .positions import (
    Position,
    PositionSide,
    PositionUpdate,
    PositionSnapshot,
    PositionTracker,
)

# Exchange adapters (CEX routing)
from .exchange_adapters import (
    SupportedExchange,
    ExchangeCredentials,
    ExchangeConfig,
    ValidationRules,
    ValidationResult,
    ValidationError as ExchangeValidationError,
    RouteOrderRequest,
    RouteOrderResponse,
    CancelOrderRequest,
    CancelOrderResponse,
    QueryOrdersRequest,
    MarketData,
    BaseExchangeAdapter,
    BinanceAdapter,
    CoinbaseAdapter,
    KrakenAdapter,
    ExchangeRouter,
    RouterConfig,
    RouterStats,
    create_router,
    create_agent_router,
)

__all__ = [
    # Client
    "ZeroQuantClient",
    # Models
    "VaultConfig",
    "SwapParams",
    "ExecuteParams",
    "ExecuteBatchParams",
    "TransactionResult",
    "GasEstimate",
    "AgentSession",
    "CreateSessionParams",
    # Intents
    "SwapIntent",
    # Exceptions
    "ZeroQuantError",
    "NotConnectedError",
    "ReadOnlyError",
    "ValidationError",
    "TransactionError",
    "ContractError",
    # Retry utilities
    "RetryConfig",
    "with_retry",
    "with_retry_async",
    "retry_async",
    "retry_sync",
    # Order management
    "Order",
    "OrderFill",
    "OrderFees",
    "CreateOrderParams",
    "OrderSide",
    "OrderType",
    "TimeInForce",
    "OrderStatus",
    "OrderQueryParams",
    "PlaceOrderResult",
    "CancelOrderResult",
    "OrderStats",
    "MinimumViableOrder",
    "ExchangeOrderResponse",
    "InternalOrderState",
    "MVORecord",
    "MVOManager",
    "OrderManager",
    # TEE integration
    "TEEPlatform",
    "AttestationStatus",
    "TCBVersion",
    "AMDSEVReport",
    "TEEAttestation",
    "TrustedMeasurement",
    "EffectiveLimits",
    "AttestationResult",
    "AMDSEVClient",
    # Intel TDX
    "IntelTDXClient",
    "TDXQuote",
    "TDReport",
    "TDInfo",
    "TDXTCBInfo",
    # Position tracking
    "Position",
    "PositionSide",
    "PositionUpdate",
    "PositionSnapshot",
    "PositionTracker",
    # Exchange adapters
    "SupportedExchange",
    "ExchangeCredentials",
    "ExchangeConfig",
    "ValidationRules",
    "ValidationResult",
    "ExchangeValidationError",
    "RouteOrderRequest",
    "RouteOrderResponse",
    "CancelOrderRequest",
    "CancelOrderResponse",
    "QueryOrdersRequest",
    "MarketData",
    "BaseExchangeAdapter",
    "BinanceAdapter",
    "CoinbaseAdapter",
    "KrakenAdapter",
    "ExchangeRouter",
    "RouterConfig",
    "RouterStats",
    "create_router",
    "create_agent_router",
]
