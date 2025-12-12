"""Formatting helpers for display."""

from __future__ import annotations

from decimal import Decimal


def format_decimal(value: Decimal, precision: int = 2) -> str:
    quant = Decimal(10) ** -precision
    return str(Decimal(value).quantize(quant))


def format_percent(rate: Decimal, precision: int = 2) -> str:
    return f"{format_decimal(rate * Decimal(100), precision)}%"
