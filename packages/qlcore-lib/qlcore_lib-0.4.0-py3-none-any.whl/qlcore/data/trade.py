"""Trade tick structure."""

from __future__ import annotations

from dataclasses import dataclass
from ..core.enums import OrderSide
from ..core.types import Price, Quantity, TimestampMs


@dataclass(frozen=True)
class Trade:
    instrument_id: str
    side: OrderSide
    price: Price
    quantity: Quantity
    timestamp_ms: TimestampMs
