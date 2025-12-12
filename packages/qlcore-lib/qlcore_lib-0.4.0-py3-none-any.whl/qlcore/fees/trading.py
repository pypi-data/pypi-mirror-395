"""Trading fee models."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from ..core.types import Money, Rate
from ..math.rounding import quantize_fee
from .tiers import VipTier


@dataclass(frozen=True)
class FeeSchedule:
    maker_rate: Decimal
    taker_rate: Decimal


def calculate_fee(
    *, trade_value: Money, fee_rate: Rate, precision: int | None = None
) -> Money:
    """Return the fee for a given trade value and fee rate."""
    raw = trade_value * fee_rate
    return quantize_fee(raw, precision=precision)


def trade_fee(notional: Decimal, is_maker: bool, schedule: FeeSchedule) -> Decimal:
    rate = schedule.maker_rate if is_maker else schedule.taker_rate
    return calculate_fee(trade_value=Decimal(notional), fee_rate=rate)


# Backwards compatibility alias
def fee_for_trade(notional: Decimal, is_maker: bool, schedule: FeeSchedule) -> Decimal:
    return trade_fee(notional, is_maker, schedule)


def select_vip_tier(volume_30d: Decimal, tiers: Iterable[VipTier]) -> VipTier:
    """Pick the highest tier whose required_volume <= volume_30d."""
    best = None
    for tier in tiers:
        if volume_30d >= tier.required_volume:
            if best is None or tier.required_volume > best.required_volume:
                best = tier
    if best is None:
        raise ValueError(
            "no tier applicable; ensure a base tier with required_volume=0 exists"
        )
    return best
