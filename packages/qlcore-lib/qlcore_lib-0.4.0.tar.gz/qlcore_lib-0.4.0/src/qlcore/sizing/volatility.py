"""Volatility-based sizing (e.g., ATR sizing)."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money, Price, Quantity


def atr_position_size(
    equity: Money, atr: Price, risk_multiple: Decimal = Decimal("1")
) -> Quantity:
    """Size inversely proportional to ATR (higher volatility -> smaller size)."""
    if atr <= 0:
        raise ValueError("ATR must be positive")
    return (Decimal(equity) * risk_multiple) / Decimal(atr)
