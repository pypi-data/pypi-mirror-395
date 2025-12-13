"""
Position Tracking Module

Provides real-time position tracking and P&L calculation.

Example:
    from zeroquant.positions import PositionTracker, Position

    tracker = PositionTracker()

    # Subscribe to position updates
    tracker.subscribe(lambda event: print(f"Position update: {event}"))

    # Update position from fill (fill is returned by the execution engine)
    # fill = {"symbol": "ETH/USDC", "side": "buy", "size": 1.5, "price": 2000}
    fill = execution_engine.get_fill()  # or from WebSocket event
    tracker.update_from_fill(fill)

    # Get current position
    position = tracker.get_position("ETH/USDC")
    print(f"Size: {position.size}, P&L: {position.unrealized_pnl}")
"""

from .models import (
    Position,
    PositionSide,
    PositionUpdate,
    PositionSnapshot,
)
from .tracker import PositionTracker

__all__ = [
    "Position",
    "PositionSide",
    "PositionUpdate",
    "PositionSnapshot",
    "PositionTracker",
]
