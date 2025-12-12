"""Unrealized PnL helpers."""

from __future__ import annotations

from ..core.protocols import BasePosition
from ..core.types import Money, Price
from ..positions.metrics import unrealized_pnl as calc_unrealized


def unrealized_pnl(position: BasePosition, mark_price: Price) -> Money:
    return calc_unrealized(position, mark_price)
