"""
Minimum Viable Order (MVO) Pattern for ZeroQuant Python SDK

Provides a simplified order management pattern matching existing exchange integrations.
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class MinimumViableOrder(BaseModel):
    """
    Minimum Viable Order - input parameters for placing an order.
    Matches existing exchange integration patterns.
    """

    symbol: Optional[str] = Field(None, description="Trading pair symbol (e.g., 'WETH/USDC')")
    exchange: Optional[str] = Field(None, description="Exchange identifier")
    base_asset: Optional[str] = Field(None, description="Base asset address")
    quote_asset: Optional[str] = Field(None, description="Quote asset address")
    contract_title: Optional[str] = Field(None, description="Contract title for futures")
    side: Optional[str] = Field(None, description="Order side ('buy' or 'sell')")
    time_in_force: Optional[str] = Field(None, description="Time in force")
    reduce_only: bool = Field(default=False, description="Reduce-only flag")
    original_price: Optional[float] = Field(None, description="Original order price")
    original_quantity_base: Optional[float] = Field(None, description="Original quantity in base asset")


class ExchangeOrderResponse(BaseModel):
    """
    Response data from exchange after order placement/update.
    """

    exchange_order_id: Optional[str] = Field(None, description="Exchange-assigned order ID")
    is_maker: bool = Field(default=False, description="Whether order is maker")
    order_type: Optional[str] = Field(None, description="Order type from exchange")
    average_price: Optional[float] = Field(None, description="Average fill price")
    executed_quantity_base: Optional[float] = Field(None, description="Executed quantity in base")
    status: Optional[str] = Field(None, description="Exchange order status")
    amount_executed_quote: Optional[float] = Field(None, description="Executed amount in quote")
    fee: Optional[float] = Field(None, description="Total fee")
    fee_paid: Optional[float] = Field(None, description="Fee paid")
    fee_rebate: Optional[float] = Field(None, description="Fee rebate")
    fee_asset: Optional[str] = Field(None, description="Asset fees paid in")
    realized_pnl: Optional[float] = Field(None, description="Realized PnL")
    average_entry_price: float = Field(default=0.0, description="Average entry price")


class InternalOrderState(BaseModel):
    """
    Internal state tracking for order lifecycle.
    """

    accepted: bool = Field(default=False, description="Order accepted by system")
    created: bool = Field(default=False, description="Order created on exchange")
    failed: bool = Field(default=False, description="Order failed")
    filled: bool = Field(default=False, description="Order fully filled")
    partially_filled: bool = Field(default=False, description="Order partially filled")
    new: bool = Field(default=True, description="Order is new")
    cancelled: bool = Field(default=False, description="Order cancelled")


class MVORecord(BaseModel):
    """
    Complete MVO record combining all order information.
    """

    id: str = Field(description="Internal order ID")
    order: MinimumViableOrder = Field(description="Original order parameters")
    exchange_response: ExchangeOrderResponse = Field(
        default_factory=ExchangeOrderResponse,
        description="Exchange response data"
    )
    internal_state: InternalOrderState = Field(
        default_factory=InternalOrderState,
        description="Internal state tracking"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")


class MVOManager:
    """
    Manager for MVO-pattern order tracking.

    Provides simplified order management matching existing exchange integration patterns.

    Example:
        manager = MVOManager()

        # Place order
        mvo = manager.place_order(MinimumViableOrder(
            symbol="WETH/USDC",
            side="buy",
            original_quantity_base=1.5,
            original_price=2450.50,
        ))

        # Mark accepted
        manager.mark_accepted(mvo.id)

        # Update from exchange
        manager.update_from_exchange(mvo.id, ExchangeOrderResponse(
            exchange_order_id="ext_123",
            status="partially_filled",
            executed_quantity_base=0.75,
        ))

        # Query orders
        open_orders = manager.get_all_open_orders()
    """

    def __init__(self):
        """Initialize MVO manager."""
        self._orders: Dict[str, MVORecord] = {}

    def place_order(self, order: MinimumViableOrder) -> MVORecord:
        """
        Place a new order.

        Args:
            order: Order parameters

        Returns:
            MVORecord with generated ID
        """
        order_id = f"mvo_{uuid.uuid4().hex[:12]}"

        record = MVORecord(
            id=order_id,
            order=order,
            exchange_response=ExchangeOrderResponse(),
            internal_state=InternalOrderState(new=True),
        )

        self._orders[order_id] = record
        return record

    def get_order(self, order_id: str) -> Optional[MVORecord]:
        """
        Get order by ID.

        Args:
            order_id: Order ID

        Returns:
            MVORecord or None if not found
        """
        return self._orders.get(order_id)

    def mark_accepted(self, order_id: str) -> bool:
        """
        Mark order as accepted by system.

        Args:
            order_id: Order ID

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        order.internal_state.accepted = True
        order.internal_state.new = False
        order.updated_at = datetime.utcnow()
        return True

    def mark_created(self, order_id: str) -> bool:
        """
        Mark order as created on exchange.

        Args:
            order_id: Order ID

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        order.internal_state.created = True
        order.updated_at = datetime.utcnow()
        return True

    def mark_failed(self, order_id: str) -> bool:
        """
        Mark order as failed.

        Args:
            order_id: Order ID

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        order.internal_state.failed = True
        order.internal_state.new = False
        order.updated_at = datetime.utcnow()
        return True

    def update_from_exchange(
        self,
        order_id: str,
        response: ExchangeOrderResponse
    ) -> bool:
        """
        Update order with exchange response data.

        Args:
            order_id: Order ID
            response: Exchange response data

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        # Update exchange response
        order.exchange_response = response

        # Update internal state based on status
        if response.status:
            status_lower = response.status.lower()

            if status_lower in ['filled', 'complete', 'executed']:
                order.internal_state.filled = True
                order.internal_state.partially_filled = False
            elif status_lower in ['partially_filled', 'partial']:
                order.internal_state.partially_filled = True
            elif status_lower in ['cancelled', 'canceled']:
                order.internal_state.cancelled = True
            elif status_lower in ['failed', 'rejected']:
                order.internal_state.failed = True

        order.updated_at = datetime.utcnow()
        return True

    def mark_filled(self, order_id: str) -> bool:
        """
        Mark order as fully filled.

        Args:
            order_id: Order ID

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        order.internal_state.filled = True
        order.internal_state.partially_filled = False
        order.updated_at = datetime.utcnow()
        return True

    def mark_cancelled(self, order_id: str) -> bool:
        """
        Mark order as cancelled.

        Args:
            order_id: Order ID

        Returns:
            True if successful
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        order.internal_state.cancelled = True
        order.updated_at = datetime.utcnow()
        return True

    def get_all_orders(self) -> List[MVORecord]:
        """
        Get all orders.

        Returns:
            List of all MVORecords
        """
        return list(self._orders.values())

    def get_all_open_orders(self) -> List[MVORecord]:
        """
        Get all open orders (not filled, cancelled, or failed).

        Returns:
            List of open MVORecords
        """
        return [
            order for order in self._orders.values()
            if not (order.internal_state.filled or
                    order.internal_state.cancelled or
                    order.internal_state.failed)
        ]

    def get_all_executed_orders(self, limit: Optional[int] = None) -> List[MVORecord]:
        """
        Get all executed (filled) orders.

        Args:
            limit: Maximum number of orders to return

        Returns:
            List of executed MVORecords
        """
        executed = [
            order for order in self._orders.values()
            if order.internal_state.filled
        ]

        # Sort by updated_at descending
        executed.sort(key=lambda x: x.updated_at, reverse=True)

        if limit:
            return executed[:limit]
        return executed

    def remove_order(self, order_id: str) -> bool:
        """
        Remove order from tracking.

        Args:
            order_id: Order ID

        Returns:
            True if removed
        """
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False

    def clear_completed_orders(self) -> int:
        """
        Remove all completed orders (filled, cancelled, failed).

        Returns:
            Number of orders removed
        """
        to_remove = [
            order_id for order_id, order in self._orders.items()
            if (order.internal_state.filled or
                order.internal_state.cancelled or
                order.internal_state.failed)
        ]

        for order_id in to_remove:
            del self._orders[order_id]

        return len(to_remove)
