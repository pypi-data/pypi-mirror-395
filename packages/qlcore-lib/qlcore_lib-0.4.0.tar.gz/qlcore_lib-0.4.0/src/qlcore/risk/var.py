"""Value at Risk (VaR) utilities."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable


def historical_var(returns: Iterable[Decimal], confidence: float = 0.95) -> Decimal:
    """Simple historical VaR (positive number representing loss)."""
    sorted_rets = sorted(Decimal(r) for r in returns)
    if not sorted_rets:
        return Decimal(0)
    index = int((1 - confidence) * len(sorted_rets))
    index = max(0, min(index, len(sorted_rets) - 1))
    return -sorted_rets[index]
