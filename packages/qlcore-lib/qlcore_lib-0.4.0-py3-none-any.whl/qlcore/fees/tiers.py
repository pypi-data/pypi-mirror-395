"""VIP tier definitions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class VipTier:
    name: str
    required_volume: Decimal
    maker_rate: Decimal
    taker_rate: Decimal
