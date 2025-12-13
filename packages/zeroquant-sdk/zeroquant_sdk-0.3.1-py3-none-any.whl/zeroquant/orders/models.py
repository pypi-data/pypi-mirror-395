"""
Order Management Models for ZeroQuant Python SDK
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Callable
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class OrderSide(str, Enum):
    """Order side (buy or sell)."""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"


class TimeInForce(str, Enum):
    """Time in force for orders."""
    GTC = "gtc"  # Good til cancelled
    IOC = "ioc"  # Immediate or cancel
    FOK = "fok"  # Fill or kill


class OrderStatus(str, Enum):
    """Order status lifecycle."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    CONFIRMING = "confirming"
    OPEN = "open"
    PARTIAL_FILL = "partial_fill"
    FILLED = "filled"
    CANCELLED = "cancelled"
    FAILED = "failed"


class OrderFees(BaseModel):
    """Fee breakdown for an order."""

    total: int = Field(default=0, description="Total fees in quote token (scaled)")
    protocol: int = Field(default=0, description="Protocol fees")
    network: int = Field(default=0, description="Network/gas fees")
    maker_rebate: int = Field(default=0, description="Maker rebate if applicable")
    fee_asset: Optional[str] = Field(None, description="Asset fees are paid in")


class OrderFill(BaseModel):
    """Individual fill for an order.

    Supports both on-chain fill format and position tracking format.
    For position tracking, use: fill_id, symbol, side, quantity, price, fee, timestamp
    For on-chain fills, use: id, order_id, amount, price, fees, timestamp
    """

    # Core fields with aliases for compatibility
    id: Optional[str] = Field(None, alias="fill_id", description="Fill ID")
    order_id: Optional[str] = Field(None, description="Parent order ID")
    amount: Optional[int] = Field(None, description="Fill amount in base token (scaled)")
    price: float = Field(description="Fill price")
    fees: OrderFees = Field(default_factory=OrderFees, description="Fees for this fill")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    timestamp: int = Field(description="Fill timestamp (unix ms)")
    protocol: Optional[str] = Field(None, description="DEX protocol used")

    # Position tracking fields
    symbol: Optional[str] = Field(None, description="Trading pair symbol (e.g., ETH/USDC)")
    side: Optional[str] = Field(None, description="Fill side (buy/sell)")
    quantity: Optional[float] = Field(None, description="Fill quantity (human-readable)")
    fee: Optional[float] = Field(None, description="Fee amount (human-readable)")

    model_config = {"populate_by_name": True}


class Order(BaseModel):
    """Complete order representation."""

    id: str = Field(description="Unique order ID")
    vault_address: str = Field(description="Vault address")
    base_token: str = Field(description="Base token address")
    quote_token: str = Field(description="Quote token address")
    side: OrderSide = Field(description="Order side")
    type: OrderType = Field(description="Order type")
    status: OrderStatus = Field(description="Current status")
    time_in_force: TimeInForce = Field(default=TimeInForce.GTC, description="Time in force")

    amount: int = Field(description="Original order amount (base token, scaled)")
    filled_amount: int = Field(default=0, description="Filled amount (base token, scaled)")
    price: Optional[int] = Field(None, description="Limit price (scaled by 1e6)")
    average_fill_price: Optional[int] = Field(None, description="Average fill price (scaled by 1e6)")

    fees: OrderFees = Field(default_factory=OrderFees, description="Total fees")
    fills: List[OrderFill] = Field(default_factory=list, description="Individual fills")

    reduce_only: bool = Field(default=False, description="Reduce-only order")
    client_order_id: Optional[str] = Field(None, description="Client-provided order ID")

    created_at: int = Field(description="Creation timestamp (unix ms)")
    updated_at: int = Field(description="Last update timestamp (unix ms)")
    submitted_at: Optional[int] = Field(None, description="Submission timestamp")
    filled_at: Optional[int] = Field(None, description="Completion timestamp")
    cancelled_at: Optional[int] = Field(None, description="Cancellation timestamp")

    tx_hash: Optional[str] = Field(None, description="Submission transaction hash")
    error: Optional[str] = Field(None, description="Error message if failed")

    @property
    def remaining_amount(self) -> int:
        """Get remaining unfilled amount."""
        return self.amount - self.filled_amount

    @property
    def fill_percentage(self) -> float:
        """Get fill percentage (0-100)."""
        if self.amount == 0:
            return 0.0
        return (self.filled_amount / self.amount) * 100

    @property
    def is_open(self) -> bool:
        """Check if order is still open."""
        return self.status in [OrderStatus.PENDING, OrderStatus.SUBMITTED,
                               OrderStatus.CONFIRMING, OrderStatus.OPEN,
                               OrderStatus.PARTIAL_FILL]

    @property
    def is_complete(self) -> bool:
        """Check if order is complete (filled, cancelled, or failed)."""
        return self.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.FAILED]


class CreateOrderParams(BaseModel):
    """Parameters for creating a new order."""

    base_token: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Base token address")
    quote_token: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Quote token address")
    side: OrderSide = Field(description="Order side")
    type: OrderType = Field(description="Order type")
    amount: int = Field(gt=0, description="Order amount in base token (scaled)")
    price: Optional[int] = Field(None, ge=0, description="Limit price (scaled by 1e6)")
    time_in_force: TimeInForce = Field(default=TimeInForce.GTC, description="Time in force")
    reduce_only: bool = Field(default=False, description="Reduce-only order")
    client_order_id: Optional[str] = Field(None, description="Client-provided order ID")

    @field_validator('price')
    @classmethod
    def validate_price_for_limit(cls, v, info):
        """Limit orders require a price."""
        # Note: This runs before type is available in some Pydantic versions
        # Full validation should be done at order creation time
        return v


class OrderQueryParams(BaseModel):
    """Parameters for querying orders."""

    vault_address: Optional[str] = Field(None, description="Filter by vault address")
    base_token: Optional[str] = Field(None, description="Filter by base token")
    quote_token: Optional[str] = Field(None, description="Filter by quote token")
    side: Optional[OrderSide] = Field(None, description="Filter by side")
    status: Optional[List[OrderStatus]] = Field(None, description="Filter by status")
    start_time: Optional[int] = Field(None, description="Start timestamp (unix ms)")
    end_time: Optional[int] = Field(None, description="End timestamp (unix ms)")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Result offset")


class PlaceOrderResult(BaseModel):
    """Result of placing an order."""

    success: bool = Field(description="Whether order was placed successfully")
    order_id: Optional[str] = Field(None, description="Order ID if successful")
    order: Optional[Order] = Field(None, description="Full order object")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    error: Optional[str] = Field(None, description="Error message if failed")


class CancelOrderResult(BaseModel):
    """Result of cancelling an order."""

    success: bool = Field(description="Whether cancellation was successful")
    order_id: str = Field(description="Order ID")
    cancelled_at: Optional[int] = Field(None, description="Cancellation timestamp")
    filled_amount: int = Field(default=0, description="Amount filled before cancellation")
    error: Optional[str] = Field(None, description="Error message if failed")


class OrderStats(BaseModel):
    """Aggregate order statistics."""

    total_orders: int = Field(default=0, description="Total orders")
    filled_orders: int = Field(default=0, description="Fully filled orders")
    cancelled_orders: int = Field(default=0, description="Cancelled orders")
    failed_orders: int = Field(default=0, description="Failed orders")
    open_orders: int = Field(default=0, description="Currently open orders")
    total_volume: int = Field(default=0, description="Total volume (quote token)")
    total_fees: int = Field(default=0, description="Total fees paid")
    average_fill_price: Optional[int] = Field(None, description="Average fill price")
