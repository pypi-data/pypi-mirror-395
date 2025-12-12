"""Rounding helpers (tick/lot/fee quantization)."""

from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from ..core.types import Price, Quantity, Money


def _to_decimal(value: Money | Price | Quantity) -> Decimal:
    """Ensure incoming numeric values are Decimal."""
    return value if isinstance(value, Decimal) else Decimal(value)


def round_price_to_tick(price: Price, tick_size: Decimal) -> Price:
    """Round a price down to the nearest valid tick."""
    if tick_size <= 0:
        raise ValueError("tick_size must be positive")
    dec_price = _to_decimal(price)
    ticks = (dec_price / tick_size).to_integral_value(rounding=ROUND_DOWN)
    return ticks * tick_size


def round_qty_to_lot(qty: Quantity, lot_size: Decimal) -> Quantity:
    """Round a quantity down to the nearest valid lot size."""
    if lot_size <= 0:
        raise ValueError("lot_size must be positive")
    dec_qty = _to_decimal(qty)
    lots = (dec_qty / lot_size).to_integral_value(rounding=ROUND_DOWN)
    return lots * lot_size


def quantize_fee(fee: Money, precision: int | None = None) -> Money:
    """Quantize a fee to the desired precision using HALF_UP rounding."""
    dec_fee = _to_decimal(fee)
    if precision is None:
        return dec_fee
    quant = Decimal(10) ** -precision
    return dec_fee.quantize(quant, rounding=ROUND_HALF_UP)
