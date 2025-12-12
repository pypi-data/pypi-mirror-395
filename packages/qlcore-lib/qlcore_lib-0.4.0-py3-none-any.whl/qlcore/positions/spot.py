"""Spot position implementation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Sequence

from .base import BasePositionImpl
from ..events.fill import Fill
from ..positions.cost_basis import CostBasisMethod
from ..core.exceptions import InvalidFillError


@dataclass(frozen=True)
class SpotPosition(BasePositionImpl):
    """Spot positions reuse the generic BasePositionImpl behavior."""

    @classmethod
    def from_trades(
        cls,
        trades: Sequence[Fill],
        *,
        cost_basis_method: CostBasisMethod = CostBasisMethod.FIFO,
    ) -> "SpotPosition":
        """Build a SpotPosition from a sequence of fills."""
        if not trades:
            raise InvalidFillError("trades cannot be empty")
        instrument = trades[0].instrument_id
        pos: BasePositionImpl = BasePositionImpl.flat(instrument)
        pos = replace(pos, cost_basis_method=cost_basis_method)
        for fill in trades:
            if fill.instrument_id != instrument:
                raise InvalidFillError(
                    f"all trades must be for instrument {instrument}, got {fill.instrument_id}"
                )
            pos = pos.apply_fill(fill)

        return cls(
            instrument_id=pos.instrument_id,
            side=pos.side,
            size=pos.size,
            entry_value=pos.entry_value,
            realized_pnl=pos.realized_pnl,
            fees=pos.fees,
            lots=pos.lots,
            cost_basis_method=pos.cost_basis_method,
            unrealized_pnl=pos.unrealized_pnl,
            last_update_ms=pos.last_update_ms,
        )
