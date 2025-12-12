"""Margin utilization metrics."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money


def margin_utilization(used_margin: Money, equity: Money) -> Decimal:
    if equity == 0:
        return Decimal(0)
    return Decimal(used_margin) / Decimal(equity)
