"""Fixed sizing helpers."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Price, Quantity, Money


def fixed_quantity(qty: Quantity) -> Quantity:
    return Decimal(qty)


def fixed_notional(notional: Money, price: Price) -> Quantity:
    """Size by notional value at a given price."""
    if price == 0:
        raise ZeroDivisionError("price must be non-zero")
    return Decimal(notional) / Decimal(price)
