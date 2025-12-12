"""Futures position implementation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Sequence

from .base import BasePositionImpl
from .cost_basis import CostBasisMethod
from ..core.enums import PositionSide
from ..core.types import Money, Price, TimestampMs
from ..events.fill import Fill
from ..events.settlement import SettlementEvent


@dataclass(frozen=True)
class FuturesPosition(BasePositionImpl):
    """Futures position with expiration and settlement support.

    Extends BasePositionImpl with futures-specific fields for tracking
    contract expiration and handling settlement at expiry.

    Attributes:
        expiry_ms: Contract expiration timestamp in milliseconds (None if not set)
        settlement_price: Price at which position was settled (None if not yet settled)
        is_settled: Whether the position has been settled

    Example:
        >>> pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1725289600000)
        >>> pos = pos.apply_fill(fill)
        >>> if pos.is_expired(current_time_ms):
        ...     pos = pos.settle(settlement_event)
    """

    expiry_ms: TimestampMs | None = None
    settlement_price: Price | None = None
    is_settled: bool = False

    @staticmethod
    def flat(
        instrument_id: str,
        expiry_ms: TimestampMs | None = None,
    ) -> "FuturesPosition":
        """Create an empty futures position.

        Args:
            instrument_id: Instrument identifier
            expiry_ms: Optional contract expiration timestamp
        """
        zero = Decimal(0)
        return FuturesPosition(
            instrument_id=instrument_id,
            side=PositionSide.LONG,
            size=zero,
            entry_value=zero,
            realized_pnl=zero,
            fees=zero,
            lots=(),
            cost_basis_method=CostBasisMethod.FIFO,
            unrealized_pnl=zero,
            last_update_ms=TimestampMs(0),
            expiry_ms=expiry_ms,
            settlement_price=None,
            is_settled=False,
        )

    def is_expired(self, current_time_ms: TimestampMs) -> bool:
        """Check if contract has expired.

        Args:
            current_time_ms: Current timestamp in milliseconds

        Returns:
            True if expiry_ms is set and current time is at or past expiry
        """
        if self.expiry_ms is None:
            return False
        return current_time_ms >= self.expiry_ms

    def time_to_expiry(self, current_time_ms: TimestampMs) -> int | None:
        """Calculate time until expiration in milliseconds.

        Args:
            current_time_ms: Current timestamp in milliseconds

        Returns:
            Milliseconds until expiration, 0 if expired, None if no expiry set
        """
        if self.expiry_ms is None:
            return None
        remaining = int(self.expiry_ms) - int(current_time_ms)
        return max(0, remaining)

    def time_to_expiry_hours(self, current_time_ms: TimestampMs) -> float | None:
        """Calculate time until expiration in hours.

        Args:
            current_time_ms: Current timestamp in milliseconds

        Returns:
            Hours until expiration, 0 if expired, None if no expiry set
        """
        ms = self.time_to_expiry(current_time_ms)
        if ms is None:
            return None
        return ms / (1000 * 60 * 60)

    def apply_fill(self, fill: Fill) -> "FuturesPosition":
        """Apply fill and preserve futures-specific fields."""
        base_result = super().apply_fill(fill)
        return FuturesPosition(
            instrument_id=base_result.instrument_id,
            side=base_result.side,
            size=base_result.size,
            entry_value=base_result.entry_value,
            realized_pnl=base_result.realized_pnl,
            fees=base_result.fees,
            lots=base_result.lots,
            cost_basis_method=base_result.cost_basis_method,
            unrealized_pnl=base_result.unrealized_pnl,
            last_update_ms=base_result.last_update_ms,
            expiry_ms=self.expiry_ms,
            settlement_price=self.settlement_price,
            is_settled=self.is_settled,
        )

    def settle(self, event: SettlementEvent) -> "FuturesPosition":
        """Settle the position at the settlement price.

        This closes the position and realizes P&L based on the settlement price.
        After settlement, the position size becomes 0 and is_settled becomes True.

        Args:
            event: Settlement event with price and timestamp

        Returns:
            New FuturesPosition with position closed and P&L realized

        Raises:
            ValueError: If position is already settled or size is 0
        """
        if self.is_settled:
            raise ValueError("Position is already settled")
        if self.size == 0:
            raise ValueError("Cannot settle a flat position")

        # Calculate P&L from settlement
        # For LONG: profit = (settlement_price - avg_entry) * size
        # For SHORT: profit = (avg_entry - settlement_price) * size
        avg_entry = self.avg_entry_price or Decimal(0)
        settlement_price = Decimal(event.price)

        if self.side == PositionSide.LONG:
            settlement_pnl = (settlement_price - avg_entry) * Decimal(self.size)
        else:
            settlement_pnl = (avg_entry - settlement_price) * Decimal(self.size)

        return FuturesPosition(
            instrument_id=self.instrument_id,
            side=self.side,
            size=Decimal(0),  # Position is closed
            entry_value=Decimal(0),
            realized_pnl=Decimal(self.realized_pnl) + settlement_pnl,
            fees=self.fees,
            lots=(),  # Clear lots
            cost_basis_method=self.cost_basis_method,
            unrealized_pnl=Decimal(0),
            last_update_ms=TimestampMs(event.timestamp_ms),
            expiry_ms=self.expiry_ms,
            settlement_price=event.price,
            is_settled=True,
        )

    @classmethod
    def from_base(
        cls,
        base: BasePositionImpl,
        *,
        expiry_ms: TimestampMs | None = None,
    ) -> "FuturesPosition":
        """Convert a BasePositionImpl to FuturesPosition.

        Args:
            base: Base position to convert
            expiry_ms: Contract expiration timestamp

        Returns:
            New FuturesPosition with all base position data preserved
        """
        return cls(
            instrument_id=base.instrument_id,
            side=base.side,
            size=base.size,
            entry_value=base.entry_value,
            realized_pnl=base.realized_pnl,
            fees=base.fees,
            lots=base.lots,
            cost_basis_method=base.cost_basis_method,
            unrealized_pnl=base.unrealized_pnl,
            last_update_ms=base.last_update_ms,
            expiry_ms=expiry_ms,
            settlement_price=None,
            is_settled=False,
        )
