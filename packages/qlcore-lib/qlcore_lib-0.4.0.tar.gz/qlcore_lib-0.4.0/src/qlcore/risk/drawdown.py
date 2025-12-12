"""Drawdown calculations."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Tuple


def max_drawdown(equity_curve: Iterable[Decimal]) -> Tuple[Decimal, Decimal]:
    """Return (max_drawdown, peak) where drawdown is expressed as negative decimal."""
    peak = Decimal("-Infinity")
    max_dd = Decimal(0)
    for value in equity_curve:
        val = Decimal(value)
        if val > peak:
            peak = val
        if peak > 0:
            dd = (val - peak) / peak
            max_dd = min(max_dd, dd)
    return max_dd, peak
