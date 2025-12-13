"""
Exchange Adapter Types
Agnostic types for centralized exchange routing
"""

from enum import Enum
from typing import Optional, List, Dict, Any, Callable, Literal
from pydantic import BaseModel, Field

from ..orders.mvo import MinimumViableOrder, ExchangeOrderResponse


class SupportedExchange(str, Enum):
    """Supported centralized exchanges."""
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    OKX = "okx"
    BYBIT = "bybit"
    KUCOIN = "kucoin"
    GATE = "gate"
    HUOBI = "huobi"


class ExchangeCredentials(BaseModel):
    """
    Exchange credentials - passed through to exchange.
    These are NEVER stored by the router.
    """
    api_key: str = Field(description="API key")
    api_secret: str = Field(description="API secret")
    passphrase: Optional[str] = Field(None, description="Passphrase (required for some exchanges)")
    subaccount: Optional[str] = Field(None, description="Subaccount (optional)")


class ExchangeConfig(BaseModel):
    """Exchange configuration."""
    exchange: SupportedExchange = Field(description="Exchange identifier")
    testnet: bool = Field(default=False, description="Testnet/sandbox mode")
    base_url: Optional[str] = Field(None, description="Custom API endpoint")
    timeout: int = Field(default=30000, description="Request timeout in ms")
    rate_limit_max_requests: Optional[int] = Field(None, description="Max requests per window")
    rate_limit_window_ms: Optional[int] = Field(None, description="Rate limit window in ms")


class ValidationError(BaseModel):
    """Validation error detail."""
    code: str = Field(description="Error code")
    message: str = Field(description="Human-readable message")
    field: Optional[str] = Field(None, description="Field that failed validation")
    value: Optional[Any] = Field(None, description="Current value")
    limit: Optional[Any] = Field(None, description="Expected/limit value")


class ValidationResult(BaseModel):
    """Result of order validation."""
    valid: bool = Field(description="Whether order passed validation")
    errors: List[ValidationError] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Warnings (non-blocking)")
    adjusted_order: Optional[MinimumViableOrder] = Field(None, description="Adjusted order if modified")


class ValidationRules(BaseModel):
    """Order validation rules for agent limits."""
    max_order_value_usd: Optional[float] = Field(None, description="Maximum order value in USD")
    max_position_size: Optional[float] = Field(None, description="Maximum position size in base asset")
    allowed_pairs: Optional[List[str]] = Field(None, description="Allowed trading pairs")
    blocked_pairs: Optional[List[str]] = Field(None, description="Blocked trading pairs")
    allowed_order_types: Optional[List[str]] = Field(None, description="Allowed order types")
    daily_limit_usd: Optional[float] = Field(None, description="Daily spending limit (USD)")
    daily_spent_usd: Optional[float] = Field(None, description="Current daily spent (USD)")
    per_tx_limit_usd: Optional[float] = Field(None, description="Per-transaction limit (USD)")
    require_reduce_only: bool = Field(default=False, description="Require reduce-only")
    max_leverage: Optional[float] = Field(None, description="Maximum leverage allowed")

    class Config:
        extra = "allow"


class RouteOrderRequest(BaseModel):
    """Order routing request."""
    order: MinimumViableOrder = Field(description="Order to route")
    exchange: SupportedExchange = Field(description="Target exchange")
    credentials: ExchangeCredentials = Field(description="Exchange credentials")
    validation_rules: Optional[ValidationRules] = Field(None, description="Agent validation rules")
    skip_validation: bool = Field(default=False, description="Skip validation")
    dry_run: bool = Field(default=False, description="Validate only, don't submit")


class RouteOrderResponse(BaseModel):
    """Order routing response."""
    success: bool = Field(description="Whether routing succeeded")
    validation: ValidationResult = Field(description="Validation result")
    exchange_response: Optional[ExchangeOrderResponse] = Field(None, description="Exchange response")
    raw_response: Optional[Dict[str, Any]] = Field(None, description="Exchange-specific raw response")
    error: Optional[str] = Field(None, description="Error if failed")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    timestamp: int = Field(description="Timestamp")
    request_id: str = Field(description="Request ID for tracking")


class CancelOrderRequest(BaseModel):
    """Cancel order request."""
    order_id: str = Field(description="Order ID to cancel")
    exchange_order_id: Optional[str] = Field(None, description="Exchange order ID")
    symbol: str = Field(description="Trading pair symbol")
    exchange: SupportedExchange = Field(description="Target exchange")
    credentials: ExchangeCredentials = Field(description="Exchange credentials")


class CancelOrderResponse(BaseModel):
    """Cancel order response."""
    success: bool = Field(description="Whether cancellation succeeded")
    order_id: Optional[str] = Field(None, description="Cancelled order ID")
    error: Optional[str] = Field(None, description="Error if failed")
    timestamp: int = Field(description="Timestamp")


class QueryOrdersRequest(BaseModel):
    """Query orders request."""
    exchange: SupportedExchange = Field(description="Exchange to query")
    credentials: ExchangeCredentials = Field(description="Exchange credentials")
    symbol: Optional[str] = Field(None, description="Trading pair symbol")
    order_ids: Optional[List[str]] = Field(None, description="Order IDs to query")
    open_only: bool = Field(default=False, description="Query open orders only")
    limit: Optional[int] = Field(None, description="Limit results")


class MarketData(BaseModel):
    """Market data for validation."""
    symbol: str = Field(description="Trading pair symbol")
    current_price: float = Field(description="Current price")
    volume_24h: Optional[float] = Field(None, description="24h volume")
    min_order_size: Optional[float] = Field(None, description="Min order size")
    max_order_size: Optional[float] = Field(None, description="Max order size")
    price_precision: Optional[int] = Field(None, description="Price precision")
    quantity_precision: Optional[int] = Field(None, description="Quantity precision")
    tick_size: Optional[float] = Field(None, description="Tick size")
    step_size: Optional[float] = Field(None, description="Step size")
