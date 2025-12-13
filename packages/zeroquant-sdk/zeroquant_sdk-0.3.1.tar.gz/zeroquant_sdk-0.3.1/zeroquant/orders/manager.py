"""
Order Manager for ZeroQuant Python SDK

Provides full-featured order management with fill tracking.
"""

from typing import Optional, List, Dict, Callable, Any
from datetime import datetime
import uuid
import asyncio

from .models import (
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
)


# Type aliases for callbacks
OrderCallback = Callable[[Order], None]
FillCallback = Callable[[OrderFill], None]


class OrderManager:
    """
    Full-featured order manager with fill tracking and event subscriptions.

    Example:
        manager = OrderManager()

        # Create order
        order = manager.create_order("0xVault...", CreateOrderParams(
            base_token="0xWETH...",
            quote_token="0xUSDC...",
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            amount=1_000_000_000_000_000_000,  # 1 ETH
            price=2500_000_000,  # $2500
        ))

        # Update status
        manager.update_order_status(order.id, OrderStatus.SUBMITTED)
        manager.update_order_status(order.id, OrderStatus.OPEN)

        # Record fill
        manager.record_fill(order.id, {
            "amount": 500_000_000_000_000_000,
            "price": 2498_000_000,
            "fees": {"total": 1_250_000},
        })

        # Subscribe to updates
        manager.on_order_update(order.id, lambda o: print(f"Update: {o.status}"))
    """

    def __init__(self, ws_url: Optional[str] = None):
        """
        Initialize order manager.

        Args:
            ws_url: Optional WebSocket URL for real-time updates
        """
        self._orders: Dict[str, Order] = {}
        self._order_callbacks: Dict[str, List[OrderCallback]] = {}
        self._all_order_callbacks: List[OrderCallback] = []
        self._fill_callbacks: List[FillCallback] = []
        self._ws_url = ws_url
        self._connected = False

    def create_order(
        self,
        vault_address: str,
        params: CreateOrderParams
    ) -> Order:
        """
        Create a new order.

        Args:
            vault_address: Vault address
            params: Order parameters

        Returns:
            Created order

        Raises:
            ValueError: If limit order has no price
        """
        # Validate limit orders have price
        if params.type == OrderType.LIMIT and not params.price:
            raise ValueError("Limit orders require a price")

        order_id = f"order_{uuid.uuid4().hex[:12]}"
        now = int(datetime.utcnow().timestamp() * 1000)

        order = Order(
            id=order_id,
            vault_address=vault_address,
            base_token=params.base_token,
            quote_token=params.quote_token,
            side=params.side,
            type=params.type,
            status=OrderStatus.PENDING,
            time_in_force=params.time_in_force,
            amount=params.amount,
            filled_amount=0,
            price=params.price,
            fees=OrderFees(),
            fills=[],
            reduce_only=params.reduce_only,
            client_order_id=params.client_order_id,
            created_at=now,
            updated_at=now,
        )

        self._orders[order_id] = order
        self._notify_order_update(order)

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Get order by ID.

        Args:
            order_id: Order ID

        Returns:
            Order or None
        """
        return self._orders.get(order_id)

    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus,
        tx_hash: Optional[str] = None,
        error: Optional[str] = None,
    ) -> bool:
        """
        Update order status.

        Args:
            order_id: Order ID
            status: New status
            tx_hash: Transaction hash (for submitted/confirming)
            error: Error message (for failed)

        Returns:
            True if updated
        """
        order = self._orders.get(order_id)
        if not order:
            return False

        now = int(datetime.utcnow().timestamp() * 1000)
        order.status = status
        order.updated_at = now

        if tx_hash:
            order.tx_hash = tx_hash

        if status == OrderStatus.SUBMITTED:
            order.submitted_at = now
        elif status == OrderStatus.FILLED:
            order.filled_at = now
        elif status == OrderStatus.CANCELLED:
            order.cancelled_at = now
        elif status == OrderStatus.FAILED:
            order.error = error

        self._notify_order_update(order)
        return True

    def record_fill(
        self,
        order_id: str,
        fill_data: Dict[str, Any],
    ) -> Optional[OrderFill]:
        """
        Record a fill for an order.

        Args:
            order_id: Order ID
            fill_data: Fill data including amount, price, fees, etc.

        Returns:
            Created OrderFill or None if order not found
        """
        order = self._orders.get(order_id)
        if not order:
            return None

        fill_id = f"fill_{uuid.uuid4().hex[:8]}"
        now = int(datetime.utcnow().timestamp() * 1000)

        # Parse fees
        fees_data = fill_data.get('fees', {})
        if isinstance(fees_data, dict):
            fees = OrderFees(**fees_data)
        else:
            fees = OrderFees(total=fees_data)

        fill = OrderFill(
            id=fill_id,
            order_id=order_id,
            amount=fill_data.get('amount', 0),
            price=fill_data.get('price', 0),
            fees=fees,
            tx_hash=fill_data.get('tx_hash'),
            block_number=fill_data.get('block_number'),
            timestamp=fill_data.get('timestamp', now),
            protocol=fill_data.get('protocol'),
        )

        # Update order
        old_filled = order.filled_amount
        order.filled_amount += fill.amount
        order.fills.append(fill)
        order.updated_at = now

        # Update fees
        order.fees.total += fill.fees.total
        order.fees.protocol += fill.fees.protocol
        order.fees.network += fill.fees.network

        # Calculate new average fill price
        if order.average_fill_price is None:
            order.average_fill_price = fill.price
        else:
            old_value = order.average_fill_price * old_filled
            new_value = fill.price * fill.amount
            order.average_fill_price = (old_value + new_value) // order.filled_amount

        # Update status
        if order.filled_amount >= order.amount:
            order.status = OrderStatus.FILLED
            order.filled_at = now
        elif order.filled_amount > 0:
            order.status = OrderStatus.PARTIAL_FILL

        self._notify_order_update(order)
        self._notify_fill(fill)

        return fill

    def cancel_order(
        self,
        order_id: str,
        reason: Optional[str] = None
    ) -> CancelOrderResult:
        """
        Cancel an order.

        Args:
            order_id: Order ID
            reason: Cancellation reason

        Returns:
            Cancellation result
        """
        order = self._orders.get(order_id)

        if not order:
            return CancelOrderResult(
                success=False,
                order_id=order_id,
                error="Order not found",
            )

        if not order.is_open:
            return CancelOrderResult(
                success=False,
                order_id=order_id,
                filled_amount=order.filled_amount,
                error=f"Cannot cancel order in status: {order.status}",
            )

        now = int(datetime.utcnow().timestamp() * 1000)
        order.status = OrderStatus.CANCELLED
        order.cancelled_at = now
        order.updated_at = now

        self._notify_order_update(order)

        return CancelOrderResult(
            success=True,
            order_id=order_id,
            cancelled_at=now,
            filled_amount=order.filled_amount,
        )

    def get_orders(
        self,
        params: Optional[OrderQueryParams] = None
    ) -> List[Order]:
        """
        Get orders matching query parameters.

        Args:
            params: Query parameters

        Returns:
            List of matching orders
        """
        orders = list(self._orders.values())

        if not params:
            return orders

        if params.vault_address:
            orders = [o for o in orders if o.vault_address == params.vault_address]

        if params.base_token:
            orders = [o for o in orders if o.base_token == params.base_token]

        if params.quote_token:
            orders = [o for o in orders if o.quote_token == params.quote_token]

        if params.side:
            orders = [o for o in orders if o.side == params.side]

        if params.status:
            orders = [o for o in orders if o.status in params.status]

        if params.start_time:
            orders = [o for o in orders if o.created_at >= params.start_time]

        if params.end_time:
            orders = [o for o in orders if o.created_at <= params.end_time]

        # Sort by created_at descending
        orders.sort(key=lambda x: x.created_at, reverse=True)

        # Apply pagination
        start = params.offset
        end = start + params.limit
        return orders[start:end]

    def get_open_orders(self, vault_address: Optional[str] = None) -> List[Order]:
        """
        Get all open orders.

        Args:
            vault_address: Optional vault filter

        Returns:
            List of open orders
        """
        orders = [o for o in self._orders.values() if o.is_open]

        if vault_address:
            orders = [o for o in orders if o.vault_address == vault_address]

        return orders

    def get_filled_orders(
        self,
        vault_address: Optional[str] = None,
        limit: int = 100,
    ) -> List[Order]:
        """
        Get filled orders.

        Args:
            vault_address: Optional vault filter
            limit: Maximum orders to return

        Returns:
            List of filled orders
        """
        orders = [
            o for o in self._orders.values()
            if o.status == OrderStatus.FILLED
        ]

        if vault_address:
            orders = [o for o in orders if o.vault_address == vault_address]

        orders.sort(key=lambda x: x.filled_at or 0, reverse=True)
        return orders[:limit]

    def get_order_stats(self, vault_address: Optional[str] = None) -> OrderStats:
        """
        Get aggregate order statistics.

        Args:
            vault_address: Optional vault filter

        Returns:
            Order statistics
        """
        orders = list(self._orders.values())

        if vault_address:
            orders = [o for o in orders if o.vault_address == vault_address]

        stats = OrderStats()
        stats.total_orders = len(orders)

        total_fill_value = 0
        total_filled_amount = 0

        for order in orders:
            if order.status == OrderStatus.FILLED:
                stats.filled_orders += 1
            elif order.status == OrderStatus.CANCELLED:
                stats.cancelled_orders += 1
            elif order.status == OrderStatus.FAILED:
                stats.failed_orders += 1
            elif order.is_open:
                stats.open_orders += 1

            stats.total_fees += order.fees.total

            # Calculate volume from fills
            for fill in order.fills:
                fill_value = (fill.amount * fill.price) // 1_000_000
                stats.total_volume += fill_value
                total_fill_value += fill.price * fill.amount
                total_filled_amount += fill.amount

        if total_filled_amount > 0:
            stats.average_fill_price = total_fill_value // total_filled_amount

        return stats

    # Event subscription methods

    def on_order_update(
        self,
        order_id: str,
        callback: OrderCallback
    ) -> Callable[[], None]:
        """
        Subscribe to updates for a specific order.

        Args:
            order_id: Order ID
            callback: Callback function

        Returns:
            Unsubscribe function
        """
        if order_id not in self._order_callbacks:
            self._order_callbacks[order_id] = []

        self._order_callbacks[order_id].append(callback)

        def unsubscribe():
            if order_id in self._order_callbacks:
                self._order_callbacks[order_id].remove(callback)

        return unsubscribe

    def on_all_orders(self, callback: OrderCallback) -> Callable[[], None]:
        """
        Subscribe to all order updates.

        Args:
            callback: Callback function

        Returns:
            Unsubscribe function
        """
        self._all_order_callbacks.append(callback)

        def unsubscribe():
            self._all_order_callbacks.remove(callback)

        return unsubscribe

    def on_fill(self, callback: FillCallback) -> Callable[[], None]:
        """
        Subscribe to fill events.

        Args:
            callback: Callback function

        Returns:
            Unsubscribe function
        """
        self._fill_callbacks.append(callback)

        def unsubscribe():
            self._fill_callbacks.remove(callback)

        return unsubscribe

    def _notify_order_update(self, order: Order):
        """Notify subscribers of order update."""
        # Specific order callbacks
        if order.id in self._order_callbacks:
            for callback in self._order_callbacks[order.id]:
                try:
                    callback(order)
                except Exception:
                    pass  # Don't let callback errors break the manager

        # All order callbacks
        for callback in self._all_order_callbacks:
            try:
                callback(order)
            except Exception:
                pass

    def _notify_fill(self, fill: OrderFill):
        """Notify subscribers of fill event."""
        for callback in self._fill_callbacks:
            try:
                callback(fill)
            except Exception:
                pass
