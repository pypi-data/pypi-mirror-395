"""Fee calculation engine."""

from ..core.types import Money, Rate
from ..math.rounding import quantize_fee


def calculate_fee(
    *, trade_value: Money, fee_rate: Rate, precision: int | None = None
) -> Money:
    """Return the fee for a given trade value and fee rate."""
    raw = trade_value * fee_rate
    return quantize_fee(raw, precision=precision)
