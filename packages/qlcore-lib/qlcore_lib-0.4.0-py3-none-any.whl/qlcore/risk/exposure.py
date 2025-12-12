"""Exposure calculations."""

from __future__ import annotations

from decimal import Decimal


def net_exposure(long_notional: Decimal, short_notional: Decimal) -> Decimal:
    """Return net exposure (long - short)."""
    return Decimal(long_notional) - Decimal(short_notional)


def gross_exposure(long_notional: Decimal, short_notional: Decimal) -> Decimal:
    """Return gross exposure (sum of notionals)."""
    return abs(Decimal(long_notional)) + abs(Decimal(short_notional))
