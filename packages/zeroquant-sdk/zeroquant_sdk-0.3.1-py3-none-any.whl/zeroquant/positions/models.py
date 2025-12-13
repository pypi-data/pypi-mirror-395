"""
Position Models for ZeroQuant Python SDK
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator


class PositionSide(str, Enum):
    """Position side."""
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"


class Position(BaseModel):
    """Current position state."""

    symbol: str = Field(description="Trading pair symbol")
    side: PositionSide = Field(default=PositionSide.FLAT, description="Position side")
    size: float = Field(default=0.0, description="Position size (absolute value)")
    signed_size: float = Field(default=0.0, description="Signed size (negative for short)")
    entry_price: float = Field(default=0.0, description="Average entry price")
    mark_price: Optional[float] = Field(None, description="Current mark price")
    liquidation_price: Optional[float] = Field(None, description="Liquidation price")
    unrealized_pnl: float = Field(default=0.0, description="Unrealized P&L")
    realized_pnl: float = Field(default=0.0, description="Realized P&L")
    margin: Optional[float] = Field(None, description="Required margin")
    leverage: float = Field(default=1.0, description="Leverage multiplier")
    notional_value: float = Field(default=0.0, description="Notional value")
    created_at: int = Field(description="Position creation timestamp")
    updated_at: int = Field(description="Last update timestamp")

    @field_validator('size')
    @classmethod
    def size_must_be_non_negative(cls, v: float) -> float:
        """Validate that size is non-negative."""
        if v < 0:
            raise ValueError('size must be non-negative')
        return v

    @field_validator('leverage')
    @classmethod
    def leverage_must_be_positive(cls, v: float) -> float:
        """Validate that leverage is strictly positive."""
        if v <= 0:
            raise ValueError('leverage must be strictly positive')
        return v

    @model_validator(mode='after')
    def validate_consistency(self) -> 'Position':
        """Validate cross-field consistency."""
        # FLAT implies size == 0
        if self.side == PositionSide.FLAT and self.size != 0:
            raise ValueError('FLAT position must have size == 0')
        # Non-FLAT implies size > 0
        if self.side != PositionSide.FLAT and self.size == 0:
            raise ValueError('Non-FLAT position must have size > 0')
        # signed_size sign must match side
        if self.side == PositionSide.LONG and self.signed_size < 0:
            raise ValueError('LONG position must have non-negative signed_size')
        if self.side == PositionSide.SHORT and self.signed_size > 0:
            raise ValueError('SHORT position must have non-positive signed_size')
        if self.side == PositionSide.FLAT and self.signed_size != 0:
            raise ValueError('FLAT position must have signed_size == 0')
        return self

    def update_pnl(self, current_price: float) -> None:
        """Update unrealized P&L based on current price."""
        self.mark_price = current_price
        if self.size > 0 and self.entry_price > 0:
            price_diff = current_price - self.entry_price
            self.unrealized_pnl = price_diff * self.signed_size
            self.notional_value = current_price * self.size

    def is_long(self) -> bool:
        """Check if position is long."""
        return self.side == PositionSide.LONG

    def is_short(self) -> bool:
        """Check if position is short."""
        return self.side == PositionSide.SHORT

    def is_flat(self) -> bool:
        """Check if position is flat."""
        return self.side == PositionSide.FLAT or self.size == 0


class PositionUpdate(BaseModel):
    """Position update event."""

    type: str = Field(description="Update type: opened, increased, decreased, closed, liquidated")
    symbol: str = Field(description="Trading pair symbol")
    position: Position = Field(description="Current position state")
    fill_price: Optional[float] = Field(None, description="Fill price that caused update")
    fill_size: Optional[float] = Field(None, description="Fill size that caused update")
    realized_pnl: Optional[float] = Field(None, description="Realized P&L from this update")
    timestamp: int = Field(description="Update timestamp")


class PositionSnapshot(BaseModel):
    """Snapshot of all positions."""

    positions: Dict[str, Position] = Field(default_factory=dict, description="Positions by symbol")
    timestamp: int = Field(description="Snapshot timestamp")

    @property
    def total_unrealized_pnl(self) -> float:
        """Total unrealized P&L computed from positions."""
        return sum(pos.unrealized_pnl for pos in self.positions.values())

    @property
    def total_realized_pnl(self) -> float:
        """Total realized P&L computed from positions."""
        return sum(pos.realized_pnl for pos in self.positions.values())

    @property
    def total_notional(self) -> float:
        """Total notional value computed from positions."""
        return sum(pos.notional_value for pos in self.positions.values())

    @property
    def total_margin(self) -> float:
        """Total margin used computed from positions."""
        return sum(pos.margin or 0.0 for pos in self.positions.values())

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position by symbol."""
        return self.positions.get(symbol)

    def get_open_positions(self) -> Dict[str, Position]:
        """Get all non-flat positions."""
        return {
            symbol: pos
            for symbol, pos in self.positions.items()
            if not pos.is_flat()
        }
