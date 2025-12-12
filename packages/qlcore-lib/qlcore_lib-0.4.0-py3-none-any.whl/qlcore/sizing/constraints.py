"""Position sizing constraints."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Quantity


def apply_position_limits(
    desired_qty: Quantity,
    max_position: Quantity | None = None,
    max_notional: Decimal | None = None,
    price: Decimal | None = None,
) -> Quantity:
    qty = Decimal(desired_qty)
    if max_position is not None:
        qty = max(-Decimal(max_position), min(Decimal(max_position), qty))
    if max_notional is not None and price is not None:
        limit_qty = Decimal(max_notional) / Decimal(price)
        qty = max(-limit_qty, min(limit_qty, qty))
    return qty
