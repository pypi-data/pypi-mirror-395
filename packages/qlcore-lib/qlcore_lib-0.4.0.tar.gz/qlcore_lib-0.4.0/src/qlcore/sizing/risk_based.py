"""Risk-based sizing."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money, Price, Quantity


def risk_per_trade(
    equity: Money, risk_fraction: Decimal, stop_distance: Price
) -> Quantity:
    """Size so that loss to stop_distance equals a fraction of equity."""
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    return (Decimal(equity) * Decimal(risk_fraction)) / Decimal(stop_distance)
