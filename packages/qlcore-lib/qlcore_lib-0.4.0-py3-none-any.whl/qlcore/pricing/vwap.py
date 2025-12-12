"""VWAP calculation."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Tuple
from ..core.types import Price, Quantity


def vwap(data: Iterable[Tuple[Price, Quantity]]) -> Price:
    """Calculate Volume-Weighted Average Price.

    VWAP is the average price weighted by volume, commonly used
    as a trading benchmark.

    Args:
        data: Iterable of (price, quantity) tuples

    Returns:
        Volume-weighted average price

    Raises:
        ValueError: If total quantity is zero

    Example:
        >>> from decimal import Decimal
        >>> trades = [
        ...     (Decimal("100"), Decimal("10")),   # 10 @ $100
        ...     (Decimal("102"), Decimal("20")),   # 20 @ $102
        ...     (Decimal("99"), Decimal("5")),     # 5 @ $99
        ... ]
        >>> price = vwap(trades)
        >>> float(price)
        101.0

        >>> # VWAP is weighted toward larger trades
        >>> # (10*100 + 20*102 + 5*99) / 35 = 101.0
    """
    total_value = Decimal(0)
    total_qty = Decimal(0)
    for price, qty in data:
        total_value += Decimal(price) * Decimal(qty)
        total_qty += Decimal(qty)
    if total_qty == 0:
        raise ValueError("vwap requires positive total quantity")
    return total_value / total_qty
