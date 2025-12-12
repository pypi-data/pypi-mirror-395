"""Position-level metrics helpers."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money, Price
from ..core.protocols import BasePosition
from ..core.enums import PositionSide


def mark_to_market(position: BasePosition, mark_price: Price) -> Money:
    """Return mark-to-market value (signed)."""
    if position.size == 0 or position.avg_entry_price is None:
        return Decimal(0)
    signed_size = (
        position.size if position.side == PositionSide.LONG else -position.size
    )
    return signed_size * mark_price


def unrealized_pnl(position: BasePosition, mark_price: Price) -> Money:
    """Compute unrealized PnL using average entry price."""
    if position.size == 0 or position.avg_entry_price is None:
        return Decimal(0)
    signed_size = (
        position.size if position.side == PositionSide.LONG else -position.size
    )
    return (mark_price - position.avg_entry_price) * signed_size


def leverage(position: BasePosition, equity: Money) -> Decimal | None:
    """Return position leverage given portfolio equity."""
    equity_value = Decimal(equity)
    if equity_value == 0:
        return None
    notional = Decimal(position.notional)
    return abs(notional) / abs(equity_value)
