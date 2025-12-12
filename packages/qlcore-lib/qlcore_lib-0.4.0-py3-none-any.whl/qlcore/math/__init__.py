"""Math helpers (precision, rounding, returns, stats)."""

from .precision import ctx
from .rounding import round_price_to_tick, round_qty_to_lot, quantize_fee
from .returns import (
    simple_return,
    log_return,
    cumulative_return,
    annualized_return,
    returns_from_prices,
)
from .stats import mean, stddev, variance
from .volatility import realized_volatility, annualize_volatility

__all__ = [
    "ctx",
    "round_price_to_tick",
    "round_qty_to_lot",
    "quantize_fee",
    "simple_return",
    "log_return",
    "cumulative_return",
    "annualized_return",
    "returns_from_prices",
    "mean",
    "stddev",
    "variance",
    "realized_volatility",
    "annualize_volatility",
]
