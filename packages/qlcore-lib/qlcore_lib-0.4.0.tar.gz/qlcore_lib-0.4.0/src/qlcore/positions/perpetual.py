"""Perpetual swap position implementation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Sequence

from .base import BasePositionImpl
from .cost_basis import CostBasisMethod
from ..core.types import Money, TimestampMs
from ..events.fill import Fill
from ..events.funding import FundingEvent


@dataclass(frozen=True)
class PerpetualPosition(BasePositionImpl):
    """Perpetual swap position with funding tracking.

    Extends BasePositionImpl with funding-specific fields to track
    cumulative funding payments received or paid over the position's lifetime.

    Attributes:
        accumulated_funding: Total funding P&L accumulated (positive = received, negative = paid)
        last_funding_timestamp_ms: Timestamp of the last applied funding event

    Example:
        >>> pos = PerpetualPosition.flat("BTC-PERP")
        >>> pos = pos.apply_fill(fill)
        >>> pos = pos.apply_funding(funding_event)
        >>> print(pos.funding_pnl)
    """

    accumulated_funding: Money = Decimal(0)
    last_funding_timestamp_ms: TimestampMs = TimestampMs(0)

    @staticmethod
    def flat(instrument_id: str) -> "PerpetualPosition":
        """Create an empty perpetual position."""
        zero = Decimal(0)
        return PerpetualPosition(
            instrument_id=instrument_id,
            side=BasePositionImpl.flat(instrument_id).side,
            size=zero,
            entry_value=zero,
            realized_pnl=zero,
            fees=zero,
            lots=(),
            cost_basis_method=CostBasisMethod.FIFO,
            unrealized_pnl=zero,
            last_update_ms=TimestampMs(0),
            accumulated_funding=zero,
            last_funding_timestamp_ms=TimestampMs(0),
        )

    @property
    def funding_pnl(self) -> Money:
        """Cumulative funding P&L (positive = received, negative = paid)."""
        return self.accumulated_funding

    @property
    def total_realized_pnl(self) -> Money:
        """Total realized P&L including trading and funding."""
        return Decimal(self.realized_pnl) + Decimal(self.accumulated_funding)

    def apply_fill(self, fill: Fill) -> "PerpetualPosition":
        """Apply fill and preserve perpetual-specific fields."""
        base_result = super().apply_fill(fill)
        return PerpetualPosition(
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
            accumulated_funding=self.accumulated_funding,
            last_funding_timestamp_ms=self.last_funding_timestamp_ms,
        )

    def apply_funding(
        self, event: FundingEvent, fills: Sequence[Fill] | None = None
    ) -> "PerpetualPosition":
        """Apply funding event and accumulate funding P&L.

        Args:
            event: Funding event to apply
            fills: Optional fills during funding period for time segmentation

        Returns:
            New PerpetualPosition with updated funding accumulator

        Note:
            Unlike BasePositionImpl.apply_funding which adds funding to realized_pnl,
            this tracks funding separately in accumulated_funding for clearer attribution.
        """
        from ..pnl.funding import calculate_funding_payment

        funding_payment = calculate_funding_payment(
            position=self,
            event=event,
            fills=fills or (),
            fills_applied=True,
        )

        return replace(
            self,
            accumulated_funding=Decimal(self.accumulated_funding) + funding_payment,
            last_funding_timestamp_ms=TimestampMs(event.period_end_ms),
            last_update_ms=TimestampMs(event.period_end_ms),
        )

    @classmethod
    def from_base(
        cls,
        base: BasePositionImpl,
        *,
        accumulated_funding: Money = Decimal(0),
        last_funding_timestamp_ms: TimestampMs = TimestampMs(0),
    ) -> "PerpetualPosition":
        """Convert a BasePositionImpl to PerpetualPosition.

        Args:
            base: Base position to convert
            accumulated_funding: Initial funding accumulator value
            last_funding_timestamp_ms: Initial last funding timestamp

        Returns:
            New PerpetualPosition with all base position data preserved
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
            accumulated_funding=accumulated_funding,
            last_funding_timestamp_ms=last_funding_timestamp_ms,
        )
