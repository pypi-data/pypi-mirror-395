"""
Position Tracker for ZeroQuant Python SDK
"""

import time
from typing import Optional, Dict, Any, Set, Callable, List

from ..orders.models import OrderFill
from .models import Position, PositionSide, PositionUpdate, PositionSnapshot


PositionEventListener = Callable[[PositionUpdate], None]


class PositionTracker:
    """
    Real-time position tracker.

    Tracks positions across multiple trading pairs,
    calculates P&L, and emits position update events.

    Example:
        tracker = PositionTracker()

        # Subscribe to updates
        unsubscribe = tracker.subscribe(lambda update: print(update))

        # Process fills
        tracker.update_from_fill(fill)

        # Get position
        pos = tracker.get_position("ETH/USDC")

        # Update prices
        tracker.update_price("ETH/USDC", 2100.0)

        # Get snapshot
        snapshot = tracker.get_snapshot()

        # Cleanup
        unsubscribe()
    """

    def __init__(self):
        """Initialize position tracker."""
        self._positions: Dict[str, Position] = {}
        self._listeners: Set[PositionEventListener] = set()
        self._total_realized_pnl: float = 0.0

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        return self._positions.get(symbol)

    def get_all_positions(self) -> Dict[str, Position]:
        """Get all positions."""
        return dict(self._positions)

    def get_open_positions(self) -> Dict[str, Position]:
        """Get all non-flat positions."""
        return {
            symbol: pos
            for symbol, pos in self._positions.items()
            if not pos.is_flat()
        }

    def update_from_fill(self, fill: OrderFill) -> PositionUpdate:
        """
        Update position from an order fill.

        Args:
            fill: The order fill to process

        Returns:
            PositionUpdate event
        """
        symbol = fill.symbol
        timestamp = int(time.time() * 1000)

        # Get or create position
        position = self._positions.get(symbol)
        if position is None:
            position = Position(
                symbol=symbol,
                created_at=timestamp,
                updated_at=timestamp,
            )
            self._positions[symbol] = position

        # Determine fill direction
        fill_size = fill.quantity
        if fill.side.lower() == "sell":
            fill_size = -fill_size

        old_signed_size = position.signed_size
        new_signed_size = old_signed_size + fill_size

        # Calculate realized P&L if reducing position
        realized_pnl = 0.0
        if (old_signed_size > 0 and fill_size < 0) or (old_signed_size < 0 and fill_size > 0):
            # Reducing position
            reduce_size = min(abs(old_signed_size), abs(fill_size))
            price_diff = fill.price - position.entry_price
            if old_signed_size < 0:
                price_diff = -price_diff  # Short position
            realized_pnl = price_diff * reduce_size
            position.realized_pnl += realized_pnl
            self._total_realized_pnl += realized_pnl

        # Update entry price (weighted average for increases)
        if abs(new_signed_size) > abs(old_signed_size):
            # Increasing position - calculate weighted average
            if abs(new_signed_size) > 0:
                old_value = abs(old_signed_size) * position.entry_price
                new_value = abs(fill_size) * fill.price
                position.entry_price = (old_value + new_value) / abs(new_signed_size)
        elif new_signed_size != 0 and (
            (old_signed_size > 0 and new_signed_size < 0) or
            (old_signed_size < 0 and new_signed_size > 0)
        ):
            # Flipped sides - new entry price
            position.entry_price = fill.price

        # Update position
        position.signed_size = new_signed_size
        position.size = abs(new_signed_size)
        position.updated_at = timestamp

        # Update side
        if new_signed_size > 0:
            position.side = PositionSide.LONG
        elif new_signed_size < 0:
            position.side = PositionSide.SHORT
        else:
            position.side = PositionSide.FLAT
            position.entry_price = 0.0

        # Update P&L with current price
        if fill.price > 0:
            position.update_pnl(fill.price)

        # Determine update type
        if old_signed_size == 0:
            update_type = "opened"
        elif new_signed_size == 0:
            update_type = "closed"
        elif abs(new_signed_size) > abs(old_signed_size):
            update_type = "increased"
        else:
            update_type = "decreased"

        # Create update event
        update = PositionUpdate(
            type=update_type,
            symbol=symbol,
            position=position.model_copy(),
            fill_price=fill.price,
            fill_size=fill.quantity,
            realized_pnl=realized_pnl if realized_pnl != 0 else None,
            timestamp=timestamp,
        )

        # Emit event
        self._emit(update)

        return update

    def update_price(self, symbol: str, price: float) -> Optional[PositionUpdate]:
        """
        Update mark price for a position.

        Args:
            symbol: Trading pair symbol
            price: Current mark price

        Returns:
            PositionUpdate if position exists, None otherwise
        """
        position = self._positions.get(symbol)
        if position is None or position.is_flat():
            return None

        position.update_pnl(price)
        position.updated_at = int(time.time() * 1000)

        update = PositionUpdate(
            type="price_update",
            symbol=symbol,
            position=position.model_copy(),
            timestamp=position.updated_at,
        )

        self._emit(update)
        return update

    def update_prices(self, prices: Dict[str, float]) -> List[PositionUpdate]:
        """
        Update mark prices for multiple positions.

        Args:
            prices: Dictionary of symbol -> price

        Returns:
            List of position updates
        """
        updates = []
        for symbol, price in prices.items():
            update = self.update_price(symbol, price)
            if update:
                updates.append(update)
        return updates

    def set_position(self, position: Position) -> None:
        """
        Set a position directly (e.g., from API sync).

        Args:
            position: Position to set
        """
        self._positions[position.symbol] = position

    def close_position(self, symbol: str, close_price: float) -> Optional[PositionUpdate]:
        """
        Close a position at a given price.

        Args:
            symbol: Trading pair symbol
            close_price: Price to close at

        Returns:
            PositionUpdate if position existed
        """
        position = self._positions.get(symbol)
        if position is None or position.is_flat():
            return None

        # Calculate realized P&L
        price_diff = close_price - position.entry_price
        if position.is_short():
            price_diff = -price_diff
        realized_pnl = price_diff * position.size

        position.realized_pnl += realized_pnl
        self._total_realized_pnl += realized_pnl

        # Reset position
        old_position = position.model_copy()
        position.side = PositionSide.FLAT
        position.size = 0.0
        position.signed_size = 0.0
        position.entry_price = 0.0
        position.unrealized_pnl = 0.0
        position.notional_value = 0.0
        position.updated_at = int(time.time() * 1000)

        update = PositionUpdate(
            type="closed",
            symbol=symbol,
            position=position.model_copy(),
            fill_price=close_price,
            fill_size=old_position.size,
            realized_pnl=realized_pnl,
            timestamp=position.updated_at,
        )

        self._emit(update)
        return update

    def get_snapshot(self) -> PositionSnapshot:
        """Get snapshot of all positions."""
        total_unrealized = 0.0
        total_realized = 0.0
        total_notional = 0.0
        total_margin = 0.0

        for position in self._positions.values():
            total_unrealized += position.unrealized_pnl
            total_realized += position.realized_pnl
            total_notional += position.notional_value
            if position.margin:
                total_margin += position.margin

        return PositionSnapshot(
            positions={s: p.model_copy() for s, p in self._positions.items()},
            total_unrealized_pnl=total_unrealized,
            total_realized_pnl=total_realized,
            total_notional=total_notional,
            total_margin=total_margin,
            timestamp=int(time.time() * 1000),
        )

    def clear(self) -> None:
        """Clear all positions."""
        self._positions.clear()
        self._total_realized_pnl = 0.0

    def subscribe(self, listener: PositionEventListener) -> Callable[[], None]:
        """
        Subscribe to position updates.

        Args:
            listener: Callback function for updates

        Returns:
            Unsubscribe function
        """
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def _emit(self, update: PositionUpdate) -> None:
        """Emit position update to all listeners."""
        for listener in self._listeners:
            try:
                listener(update)
            except Exception:
                pass
