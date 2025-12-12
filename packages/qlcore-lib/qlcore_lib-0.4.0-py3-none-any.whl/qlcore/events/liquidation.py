"""Liquidation event."""

from __future__ import annotations

from dataclasses import dataclass
from ..core.enums import PositionSide
from ..core.types import Price, Quantity, TimestampMs


@dataclass(frozen=True)
class LiquidationEvent:
    instrument_id: str
    side: PositionSide
    price: Price
    quantity: Quantity
    timestamp_ms: TimestampMs
