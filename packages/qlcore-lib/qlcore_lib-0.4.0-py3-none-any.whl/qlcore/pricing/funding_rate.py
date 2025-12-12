"""Funding rate estimation helpers."""

from __future__ import annotations

from decimal import Decimal


def annualize_rate(period_rate: Decimal, periods_per_year: int = 365 * 3) -> Decimal:
    """Approximate annualized funding given a per-period rate."""
    return (Decimal(1) + Decimal(period_rate)) ** Decimal(periods_per_year) - Decimal(1)
