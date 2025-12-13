"""
Tests for ZeroQuant Position Tracking Module
"""

import pytest
import time

from zeroquant.positions import (
    Position,
    PositionSide,
    PositionUpdate,
    PositionSnapshot,
    PositionTracker,
)
from zeroquant.orders.models import OrderFill


class TestPositionModels:
    """Test position model classes."""

    def test_position_side_enum(self):
        """Test PositionSide enum values."""
        assert PositionSide.LONG == "long"
        assert PositionSide.SHORT == "short"
        assert PositionSide.FLAT == "flat"

    def test_position_creation(self):
        """Test Position creation."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.LONG,
            size=2.5,
            signed_size=2.5,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        assert position.symbol == "ETH/USDC"
        assert position.side == PositionSide.LONG
        assert position.size == 2.5
        assert position.entry_price == 2000.0

    def test_position_is_long(self):
        """Test is_long method."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.LONG,
            size=1.0,
            signed_size=1.0,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        assert position.is_long() is True
        assert position.is_short() is False
        assert position.is_flat() is False

    def test_position_is_short(self):
        """Test is_short method."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.SHORT,
            size=1.0,
            signed_size=-1.0,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        assert position.is_long() is False
        assert position.is_short() is True
        assert position.is_flat() is False

    def test_position_is_flat(self):
        """Test is_flat method."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.FLAT,
            size=0.0,
            signed_size=0.0,
            entry_price=0.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        assert position.is_flat() is True
        assert position.is_long() is False
        assert position.is_short() is False

    def test_position_update_pnl(self):
        """Test P&L update."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.LONG,
            size=2.0,
            signed_size=2.0,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        position.update_pnl(2100.0)

        assert position.mark_price == 2100.0
        assert position.unrealized_pnl == 200.0  # (2100 - 2000) * 2
        assert position.notional_value == 4200.0  # 2100 * 2

    def test_position_update_pnl_short(self):
        """Test P&L update for short position."""
        position = Position(
            symbol="ETH/USDC",
            side=PositionSide.SHORT,
            size=2.0,
            signed_size=-2.0,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        position.update_pnl(1900.0)

        assert position.mark_price == 1900.0
        assert position.unrealized_pnl == 200.0  # (1900 - 2000) * -2

    def test_position_snapshot_creation(self):
        """Test PositionSnapshot creation."""
        pos1 = Position(
            symbol="ETH/USDC",
            side=PositionSide.LONG,
            size=1.0,
            signed_size=1.0,
            entry_price=2000.0,
            unrealized_pnl=100.0,
            notional_value=2100.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        snapshot = PositionSnapshot(
            positions={"ETH/USDC": pos1},
            total_unrealized_pnl=100.0,
            total_realized_pnl=50.0,
            total_notional=2100.0,
            timestamp=int(time.time() * 1000),
        )

        assert snapshot.total_unrealized_pnl == 100.0
        assert snapshot.get_position("ETH/USDC") is not None

    def test_position_snapshot_get_open(self):
        """Test getting open positions from snapshot."""
        pos1 = Position(
            symbol="ETH/USDC",
            side=PositionSide.LONG,
            size=1.0,
            signed_size=1.0,
            entry_price=2000.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )
        pos2 = Position(
            symbol="BTC/USDC",
            side=PositionSide.FLAT,
            size=0.0,
            signed_size=0.0,
            entry_price=0.0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
        )

        snapshot = PositionSnapshot(
            positions={"ETH/USDC": pos1, "BTC/USDC": pos2},
            timestamp=int(time.time() * 1000),
        )

        open_positions = snapshot.get_open_positions()
        assert len(open_positions) == 1
        assert "ETH/USDC" in open_positions


class TestPositionTracker:
    """Test PositionTracker functionality."""

    def test_tracker_creation(self):
        """Test PositionTracker creation."""
        tracker = PositionTracker()

        assert len(tracker.get_all_positions()) == 0

    def test_update_from_buy_fill(self):
        """Test updating position from buy fill."""
        tracker = PositionTracker()

        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.5,
            fee=1.5,
            timestamp=int(time.time() * 1000),
        )

        update = tracker.update_from_fill(fill)

        assert update.type == "opened"
        assert update.position.side == PositionSide.LONG
        assert update.position.size == 1.5
        assert update.position.entry_price == 2000.0

    def test_update_from_sell_fill(self):
        """Test updating position from sell fill."""
        tracker = PositionTracker()

        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="sell",
            price=2000.0,
            quantity=1.5,
            fee=1.5,
            timestamp=int(time.time() * 1000),
        )

        update = tracker.update_from_fill(fill)

        assert update.type == "opened"
        assert update.position.side == PositionSide.SHORT
        assert update.position.size == 1.5
        assert update.position.signed_size == -1.5

    def test_increase_position(self):
        """Test increasing an existing position."""
        tracker = PositionTracker()

        # First buy
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)

        # Second buy
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="ETH/USDC",
            side="buy",
            price=2100.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        update = tracker.update_from_fill(fill2)

        assert update.type == "increased"
        assert update.position.size == 2.0
        # Weighted average: (1*2000 + 1*2100) / 2 = 2050
        assert update.position.entry_price == 2050.0

    def test_reduce_position(self):
        """Test reducing a position."""
        tracker = PositionTracker()

        # Open position
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=2.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)

        # Partial close
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="ETH/USDC",
            side="sell",
            price=2100.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        update = tracker.update_from_fill(fill2)

        assert update.type == "decreased"
        assert update.position.size == 1.0
        assert update.realized_pnl == 100.0  # (2100 - 2000) * 1

    def test_close_position(self):
        """Test closing a position completely."""
        tracker = PositionTracker()

        # Open position
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=2.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)

        # Full close
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="ETH/USDC",
            side="sell",
            price=2200.0,
            quantity=2.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        update = tracker.update_from_fill(fill2)

        assert update.type == "closed"
        assert update.position.is_flat() is True
        assert update.realized_pnl == 400.0  # (2200 - 2000) * 2

    def test_flip_position(self):
        """Test flipping from long to short."""
        tracker = PositionTracker()

        # Open long
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)

        # Sell more than position (flip to short)
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="ETH/USDC",
            side="sell",
            price=2100.0,
            quantity=2.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        update = tracker.update_from_fill(fill2)

        assert update.position.side == PositionSide.SHORT
        assert update.position.size == 1.0
        assert update.position.signed_size == -1.0
        # New entry price should be the flip price
        assert update.position.entry_price == 2100.0

    def test_update_price(self):
        """Test updating mark price."""
        tracker = PositionTracker()

        # Open position
        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill)

        # Update price
        update = tracker.update_price("ETH/USDC", 2150.0)

        assert update is not None
        assert update.position.mark_price == 2150.0
        assert update.position.unrealized_pnl == 150.0

    def test_update_prices_batch(self):
        """Test updating multiple prices."""
        tracker = PositionTracker()

        # Open positions
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="BTC/USDC",
            side="buy",
            price=50000.0,
            quantity=0.1,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)
        tracker.update_from_fill(fill2)

        # Update prices
        updates = tracker.update_prices({
            "ETH/USDC": 2100.0,
            "BTC/USDC": 51000.0,
        })

        assert len(updates) == 2

    def test_close_position_directly(self):
        """Test closing position with close_position method."""
        tracker = PositionTracker()

        # Open position
        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=2.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill)

        # Close position
        update = tracker.close_position("ETH/USDC", 2100.0)

        assert update is not None
        assert update.type == "closed"
        assert update.realized_pnl == 200.0
        assert update.position.is_flat()

    def test_get_snapshot(self):
        """Test getting position snapshot."""
        tracker = PositionTracker()

        # Open positions
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)

        # Update price
        tracker.update_price("ETH/USDC", 2100.0)

        snapshot = tracker.get_snapshot()

        assert len(snapshot.positions) == 1
        assert snapshot.total_unrealized_pnl == 100.0

    def test_event_subscription(self):
        """Test event subscription."""
        tracker = PositionTracker()
        events = []

        unsubscribe = tracker.subscribe(lambda e: events.append(e))

        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill)

        assert len(events) == 1
        assert events[0].type == "opened"

        unsubscribe()

        # No more events after unsubscribe
        tracker.update_price("ETH/USDC", 2100.0)
        assert len(events) == 1

    def test_clear_positions(self):
        """Test clearing all positions."""
        tracker = PositionTracker()

        fill = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill)

        assert len(tracker.get_all_positions()) == 1

        tracker.clear()

        assert len(tracker.get_all_positions()) == 0

    def test_get_open_positions(self):
        """Test getting only open positions."""
        tracker = PositionTracker()

        # Open and close a position
        fill1 = OrderFill(
            fill_id="fill_1",
            order_id="order_1",
            symbol="ETH/USDC",
            side="buy",
            price=2000.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        fill2 = OrderFill(
            fill_id="fill_2",
            order_id="order_2",
            symbol="ETH/USDC",
            side="sell",
            price=2100.0,
            quantity=1.0,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill1)
        tracker.update_from_fill(fill2)

        # Open another position
        fill3 = OrderFill(
            fill_id="fill_3",
            order_id="order_3",
            symbol="BTC/USDC",
            side="buy",
            price=50000.0,
            quantity=0.1,
            fee=1.0,
            timestamp=int(time.time() * 1000),
        )
        tracker.update_from_fill(fill3)

        open_positions = tracker.get_open_positions()

        assert len(open_positions) == 1
        assert "BTC/USDC" in open_positions
