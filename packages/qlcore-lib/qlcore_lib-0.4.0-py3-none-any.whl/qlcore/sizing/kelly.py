"""Kelly criterion sizing."""

from __future__ import annotations

from decimal import Decimal


def kelly_fraction(win_rate: Decimal, win_loss_ratio: Decimal) -> Decimal:
    """Calculate the Kelly fraction of bankroll to risk per trade.

    The Kelly criterion determines the optimal bet size to maximize
    long-term growth rate. The result can be negative (don't bet),
    or > 1 (use leverage).

    Args:
        win_rate: Probability of winning (0 to 1)
        win_loss_ratio: Average win / average loss ratio

    Returns:
        Fraction of bankroll to risk (can be negative or > 1)

    Raises:
        ValueError: If win_loss_ratio is not positive

    Example:
        >>> from decimal import Decimal
        >>> # 60% win rate, 1.5:1 reward/risk
        >>> kelly = kelly_fraction(Decimal("0.6"), Decimal("1.5"))
        >>> float(kelly)  # ~33% of bankroll
        0.33...

        >>> # 50% win rate, 2:1 reward/risk
        >>> kelly = kelly_fraction(Decimal("0.5"), Decimal("2"))
        >>> float(kelly)  # 25% of bankroll
        0.25

        >>> # Use half-Kelly for reduced volatility
        >>> half_kelly = kelly / 2
    """
    p = Decimal(win_rate)
    q = Decimal(1) - p
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")
    return p - (q / Decimal(win_loss_ratio))
