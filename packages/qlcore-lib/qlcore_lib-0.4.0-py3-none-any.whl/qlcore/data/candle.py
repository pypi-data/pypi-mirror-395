"""OHLCV candle structure."""

from __future__ import annotations

from dataclasses import dataclass
from ..core.types import Price, Quantity, TimestampMs


@dataclass(frozen=True)
class Candle:
    instrument_id: str
    start_ms: TimestampMs
    end_ms: TimestampMs
    open: Price
    high: Price
    low: Price
    close: Price
    volume: Quantity
