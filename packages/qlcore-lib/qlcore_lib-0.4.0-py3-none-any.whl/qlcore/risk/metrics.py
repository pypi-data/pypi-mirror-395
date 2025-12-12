"""Risk metrics (Sharpe, Sortino, etc.)."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from ..math.stats import mean, stddev


# Annualization factors for crypto (24/7, 365 days/year)
DAILY_PERIODS = 365  # Crypto trades every day
HOURLY_PERIODS = 365 * 24  # 8760 hours per year
WEEKLY_PERIODS = 52
EIGHT_HOURLY_PERIODS = 365 * 3  # 1095 funding periods (common 8h funding)


def sharpe_ratio(
    returns: Iterable[Decimal],
    risk_free: Decimal = Decimal(0),
    annualize: bool = False,
    periods_per_year: int = DAILY_PERIODS,
) -> Decimal | None:
    """Calculate the Sharpe ratio from a series of returns.

    The Sharpe ratio measures risk-adjusted return as the excess return
    per unit of volatility.

    Args:
        returns: Iterable of period returns (e.g., daily returns)
        risk_free: Risk-free rate for the same period (default: 0)
        annualize: If True, annualize the ratio (default: False)
        periods_per_year: Number of periods per year (default: 365 for daily)

    Returns:
        Sharpe ratio, or None if returns are empty or volatility is zero

    Example:
        >>> from decimal import Decimal
        >>> returns = [Decimal("0.01"), Decimal("0.02"), Decimal("-0.01"), Decimal("0.03")]
        >>> ratio = sharpe_ratio(returns)
        >>> ratio is not None
        True
        >>> float(ratio) > 0  # Positive returns = positive Sharpe
        True

        >>> # Annualized Sharpe (for daily returns)
        >>> ann_ratio = sharpe_ratio(returns, annualize=True)
        >>> float(ann_ratio) > float(ratio)  # Annualized is sqrt(365) larger
        True
    """
    rets = [Decimal(r) - risk_free for r in returns]
    if not rets:
        return None
    volatility = stddev(rets, sample=True)
    if volatility == 0:
        return None

    ratio = mean(rets) / volatility

    if annualize:
        # Annualize: multiply by sqrt(periods_per_year)
        ann_factor = Decimal(periods_per_year).sqrt()
        ratio = ratio * ann_factor

    return ratio


def sortino_ratio(
    returns: Iterable[Decimal],
    risk_free: Decimal = Decimal(0),
    target: Decimal = Decimal(0),
    annualize: bool = False,
    periods_per_year: int = DAILY_PERIODS,
) -> Decimal | None:
    """Calculate the Sortino ratio from a series of returns.

    The Sortino ratio is similar to Sharpe but only penalizes downside
    volatility, making it more appropriate when returns are asymmetric.

    Args:
        returns: Iterable of period returns
        risk_free: Risk-free rate for the same period (default: 0)
        target: Target return threshold (default: 0)
        annualize: If True, annualize the ratio (default: False)
        periods_per_year: Number of periods per year (default: 365 for daily)

    Returns:
        Sortino ratio, or None if returns are empty or downside deviation is zero

    Example:
        >>> from decimal import Decimal
        >>> returns = [Decimal("0.02"), Decimal("0.03"), Decimal("-0.01"), Decimal("0.01")]
        >>> ratio = sortino_ratio(returns)
        >>> ratio is not None
        True
        >>> float(ratio) > 0
        True

        >>> # Annualized Sortino
        >>> ann_ratio = sortino_ratio(returns, annualize=True)
    """
    rets = [Decimal(r) - risk_free for r in returns]
    if not rets:
        return None

    downside_moves = [min(Decimal(0), r - target) for r in rets]
    downside_sq = sum((d**2 for d in downside_moves if d < 0), Decimal(0))
    if downside_sq == 0:
        return None

    downside_dev = (downside_sq / Decimal(len(rets))).sqrt()
    if downside_dev == 0:
        return None

    ratio = mean(rets) / downside_dev

    if annualize:
        ann_factor = Decimal(periods_per_year).sqrt()
        ratio = ratio * ann_factor

    return ratio


def calmar_ratio(
    returns: Iterable[Decimal],
    max_drawdown: Decimal,
    periods_per_year: int = DAILY_PERIODS,
) -> Decimal | None:
    """Calculate the Calmar ratio (annualized return / max drawdown).

    Uses absolute value of max_drawdown since drawdowns are typically negative.

    Args:
        returns: Iterable of period returns
        max_drawdown: Maximum drawdown (negative or positive)
        periods_per_year: Number of periods per year (default: 365)

    Returns:
        Calmar ratio, or None if max_drawdown is zero

    Example:
        >>> from decimal import Decimal
        >>> returns = [Decimal("0.01")] * 100  # 1% daily for 100 days
        >>> calmar = calmar_ratio(returns, Decimal("-0.10"))  # 10% drawdown
        >>> calmar is not None
        True
    """
    rets = [Decimal(r) for r in returns]
    if not rets:
        return None

    mdd = abs(Decimal(max_drawdown))
    if mdd == 0:
        return None

    # Annualized return
    total_return = sum(rets)
    ann_return = total_return * (Decimal(periods_per_year) / Decimal(len(rets)))

    return ann_return / mdd


def information_ratio(
    portfolio_returns: Iterable[Decimal],
    benchmark_returns: Iterable[Decimal],
    annualize: bool = False,
    periods_per_year: int = DAILY_PERIODS,
) -> Decimal | None:
    """Calculate the Information Ratio (excess return / tracking error).

    Measures portfolio performance relative to a benchmark.

    Args:
        portfolio_returns: Portfolio period returns
        benchmark_returns: Benchmark period returns
        annualize: If True, annualize the ratio
        periods_per_year: Number of periods per year

    Returns:
        Information ratio, or None if tracking error is zero

    Example:
        >>> from decimal import Decimal
        >>> port_rets = [Decimal("0.02"), Decimal("0.01"), Decimal("-0.01")]
        >>> bench_rets = [Decimal("0.015"), Decimal("0.005"), Decimal("-0.005")]
        >>> ir = information_ratio(port_rets, bench_rets)
        >>> ir is not None
        True
    """
    port = [Decimal(r) for r in portfolio_returns]
    bench = [Decimal(r) for r in benchmark_returns]

    if len(port) != len(bench) or not port:
        return None

    # Active returns (excess over benchmark)
    active = [p - b for p, b in zip(port, bench)]

    tracking_error = stddev(active, sample=True)
    if tracking_error == 0:
        return None

    ratio = mean(active) / tracking_error

    if annualize:
        ann_factor = Decimal(periods_per_year).sqrt()
        ratio = ratio * ann_factor

    return ratio
