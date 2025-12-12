"""Funding fee helpers."""

from __future__ import annotations

from decimal import Decimal


def funding_fee(notional: Decimal, rate: Decimal) -> Decimal:
    return Decimal(notional) * Decimal(rate)
