"""Volatility utilities built on top of decimal stats."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from .stats import stddev


def realized_volatility(
    returns: Iterable[Decimal], periods_per_year: int = 365
) -> Decimal:
    """Compute annualized realized volatility from a series of returns."""
    per_period_std = stddev(returns, sample=True)
    return annualize_volatility(per_period_std, periods_per_year=periods_per_year)


def annualize_volatility(vol: Decimal, periods_per_year: int = 365) -> Decimal:
    """Scale per-period volatility to an annualized figure."""
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return Decimal(periods_per_year).sqrt() * Decimal(vol)
