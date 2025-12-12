"""Currency conversion helpers."""

from __future__ import annotations

from decimal import Decimal


def convert(amount: Decimal, rate: Decimal) -> Decimal:
    """Convert an amount using a quote/base rate."""
    return Decimal(amount) * Decimal(rate)
