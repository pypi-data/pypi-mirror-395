"""Percent-of-equity sizing."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money, Price, Quantity


def percent_of_equity(equity: Money, percent: Decimal, price: Price) -> Quantity:
    """Calculate position size as a percentage of equity.

    A simple sizing method that allocates a fixed percentage of
    account equity to each position.

    Args:
        equity: Total account equity
        percent: Percentage to allocate (e.g., 0.02 for 2%)
        price: Current asset price

    Returns:
        Quantity to buy/sell

    Raises:
        ZeroDivisionError: If price is zero

    Example:
        >>> from decimal import Decimal
        >>> # Allocate 2% of $10,000 equity at $100/share
        >>> qty = percent_of_equity(Decimal("10000"), Decimal("0.02"), Decimal("100"))
        >>> float(qty)
        2.0

        >>> # Allocate 5% of $50,000 equity at $250/share
        >>> qty = percent_of_equity(Decimal("50000"), Decimal("0.05"), Decimal("250"))
        >>> float(qty)
        10.0
    """
    if price == 0:
        raise ZeroDivisionError("price must be non-zero")
    return (Decimal(equity) * Decimal(percent)) / Decimal(price)
