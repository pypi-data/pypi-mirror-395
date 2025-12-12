"""Return calculation utilities."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable


def simple_return(current: Decimal, previous: Decimal) -> Decimal:
    """Calculate simple return (current / previous - 1).

    Example:
        >>> from decimal import Decimal
        >>> simple_return(Decimal("110"), Decimal("100"))
        Decimal('0.1')
    """
    if previous == 0:
        raise ZeroDivisionError("previous value must be non-zero")
    return (Decimal(current) / Decimal(previous)) - Decimal(1)


def log_return(current: Decimal, previous: Decimal) -> Decimal:
    """Calculate log return ln(current / previous).

    Example:
        >>> from decimal import Decimal
        >>> ret = log_return(Decimal("110"), Decimal("100"))
        >>> float(ret)  # ~0.0953
        0.09531...
    """
    if previous == 0:
        raise ZeroDivisionError("previous value must be non-zero")
    ratio = Decimal(current) / Decimal(previous)
    if ratio <= 0:
        raise ValueError("log return requires positive ratio")
    return ratio.ln()


def cumulative_return(returns: Iterable[Decimal]) -> Decimal:
    """Aggregate multiple period returns into a cumulative return.

    Example:
        >>> from decimal import Decimal
        >>> rets = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02")]
        >>> float(cumulative_return(rets))  # (1.1)(1.05)(0.98) - 1 = 0.1319
        0.1319
    """
    total = Decimal(1)
    for r in returns:
        total *= Decimal(1) + Decimal(r)
    return total - Decimal(1)


def annualized_return(
    total_return: Decimal,
    periods: int,
    periods_per_year: int = 365,
) -> Decimal:
    """Convert total return to annualized return (CAGR).

    Uses the formula: (1 + total_return)^(periods_per_year / periods) - 1

    Args:
        total_return: Total cumulative return (e.g., 0.50 for 50%)
        periods: Number of periods in the data (e.g., 180 days)
        periods_per_year: Periods per year (default: 365 days)

    Returns:
        Annualized (CAGR) return

    Example:
        >>> from decimal import Decimal
        >>> # 50% return over 2 years (730 days)
        >>> ann = annualized_return(Decimal("0.50"), 730, 365)
        >>> float(ann)  # ~22.5% per year
        0.224...

        >>> # 10% return over 1 quarter (90 days)
        >>> ann = annualized_return(Decimal("0.10"), 90, 365)
        >>> float(ann)  # ~47.7% annualized
        0.477...
    """
    if periods <= 0:
        raise ValueError("periods must be positive")

    growth_factor = Decimal(1) + Decimal(total_return)
    exponent = Decimal(periods_per_year) / Decimal(periods)

    # (1 + r)^exponent - 1
    return growth_factor**exponent - Decimal(1)


def returns_from_prices(prices: Iterable[Decimal]) -> list[Decimal]:
    """Calculate simple returns from a price series.

    Args:
        prices: Iterable of prices (at least 2 values)

    Returns:
        List of returns (length = len(prices) - 1)

    Example:
        >>> from decimal import Decimal
        >>> prices = [Decimal("100"), Decimal("110"), Decimal("105")]
        >>> rets = returns_from_prices(prices)
        >>> for r in rets:
        ...     print(round(float(r), 4))
        0.1
        -0.0455
    """
    price_list = [Decimal(p) for p in prices]
    if len(price_list) < 2:
        raise ValueError("need at least 2 prices to calculate returns")

    returns = []
    for i in range(1, len(price_list)):
        ret = simple_return(price_list[i], price_list[i - 1])
        returns.append(ret)

    return returns
