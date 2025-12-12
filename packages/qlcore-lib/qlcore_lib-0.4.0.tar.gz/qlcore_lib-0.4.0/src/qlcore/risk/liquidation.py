"""Liquidation price calculations."""

from __future__ import annotations

from decimal import Decimal

from ..core.types import Money, Price, Quantity
from ..core.enums import PositionSide
from ..core.exceptions import ValidationError
from ..margin.requirements import MarginSchedule


def _maintenance_margin_rate(
    margin_schedule: MarginSchedule,
    size: Quantity,
    entry_price: Price,
) -> Decimal:
    """Return maintenance margin rate for a given position size/notional.

    The schedule is expressed in terms of notional thresholds, so we convert
    the current position into notional using the entry price.
    """
    notional = abs(Decimal(size) * Decimal(entry_price))
    req = margin_schedule.for_notional(notional)
    mmr = Decimal(req.maintenance)

    if mmr < 0 or mmr >= 1:
        raise ValidationError(
            f"maintenance margin rate from schedule must be in [0, 1), got {mmr}"
        )

    return mmr


def _solve_liquidation_price(
    *,
    sign: Decimal,
    entry_price: Price,
    size: Quantity,
    wallet: Money,
    mmr: Decimal,
    fee_buffer: Money,
    safety_margin: Money = Money(0),
) -> Price | None:
    """Solve for the liquidation price.

    At liquidation we equate account equity with required maintenance margin:

        wallet + sign * size * (price - entry_price)
            = mmr * price * size + fee_buffer + safety_margin

    Rearranging:

        (sign - mmr) * size * price
            = -wallet + sign * size * entry_price + fee_buffer + safety_margin

        price = (
            -wallet + sign * size * entry_price + fee_buffer + safety_margin
        ) / ((sign - mmr) * size)

    If the resulting price is non-positive, there is no meaningful liquidation
    price in the valid price domain and ``None`` is returned.

    Degenerate configurations (e.g. zero size or sign == mmr) also yield None.
    """
    if size <= 0:
        return None

    size_dec = Decimal(size)
    if size_dec <= 0:
        return None

    denom = (sign - mmr) * size_dec
    if denom == 0:
        # Degenerate configuration: maintenance margin rate equals the signed
        # price sensitivity. Treat as "no finite liquidation price".
        return None

    numer = (
        -Decimal(wallet)
        + sign * size_dec * Decimal(entry_price)
        + Decimal(fee_buffer)
        + Decimal(safety_margin)
    )

    price = numer / denom
    if price <= 0:
        # Would only liquidate at non-positive price; treat as "no liquidation".
        return None

    return Price(price)


def isolated_liquidation_price(
    *,
    side: PositionSide,
    entry_price: Price,
    size: Quantity,
    wallet_margin: Money,
    maintenance_margin_rate: Decimal,
    fee_buffer: Money = Money(0),
    safety_buffer: Money = Money(0),
    margin_schedule: MarginSchedule | None = None,
) -> Price | None:

    if size <= 0:
        return None

    if entry_price <= 0:
        raise ValidationError(f"entry_price must be positive, got {entry_price}")

    if maintenance_margin_rate < 0 or maintenance_margin_rate >= 1:
        raise ValidationError(
            f"maintenance_margin_rate must be in [0, 1), got {maintenance_margin_rate}"
        )

    sign = Decimal(1) if side == PositionSide.LONG else Decimal(-1)
    mmr = Decimal(maintenance_margin_rate)
    if margin_schedule is not None:
        mmr = _maintenance_margin_rate(margin_schedule, size, entry_price)

    return _solve_liquidation_price(
        sign=sign,
        entry_price=entry_price,
        size=size,
        wallet=wallet_margin,
        mmr=mmr,
        fee_buffer=fee_buffer,
        safety_margin=Money(safety_buffer),
    )


def cross_liquidation_price(
    *,
    portfolio_equity: Money,
    position_notional: Money,
    side: PositionSide,
    entry_price: Price,
    size: Quantity,
    maintenance_margin_rate: Decimal,
    fee_buffer: Money = Money(0),
) -> Price | None:
    if size <= 0:
        return None

    if entry_price <= 0:
        raise ValidationError(f"entry_price must be positive, got {entry_price}")

    if maintenance_margin_rate < 0 or maintenance_margin_rate >= 1:
        raise ValidationError(
            f"maintenance_margin_rate must be in [0, 1), got {maintenance_margin_rate}"
        )

    sign = Decimal(1) if side == PositionSide.LONG else Decimal(-1)
    mmr = Decimal(maintenance_margin_rate)

    return _solve_liquidation_price(
        sign=sign,
        entry_price=entry_price,
        size=size,
        wallet=portfolio_equity,
        mmr=mmr,
        fee_buffer=fee_buffer,
        safety_margin=Money(0),
    )


def calculate_isolated_liquidation_price(**kwargs) -> Price | None:
    """Backward-compatible alias for isolated_liquidation_price()."""
    return isolated_liquidation_price(**kwargs)


def calculate_cross_liquidation_price(**kwargs) -> Price | None:
    """Backward-compatible alias for cross_liquidation_price()."""
    return cross_liquidation_price(**kwargs)
