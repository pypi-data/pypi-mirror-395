"""PnL attribution utilities."""

from __future__ import annotations

from decimal import Decimal
from typing import Mapping
from .calculator import PnLBreakdown


def total_by_instrument(
    breakdowns: Mapping[str, PnLBreakdown],
) -> Mapping[str, Decimal]:
    return {instrument: data.total for instrument, data in breakdowns.items()}


def component_by_instrument(
    breakdowns: Mapping[str, PnLBreakdown], component: str
) -> Mapping[str, Decimal]:
    """Return a specific PnL component per instrument key."""
    out: dict[str, Decimal] = {}
    for instrument, data in breakdowns.items():
        value = getattr(data, component, None)
        if value is None:
            raise AttributeError(f"PnLBreakdown has no component '{component}'")
        out[instrument] = Decimal(value)
    return out
