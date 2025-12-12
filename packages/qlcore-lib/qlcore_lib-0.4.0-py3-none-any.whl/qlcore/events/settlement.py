"""Settlement event for futures/options expirations."""

from __future__ import annotations

from dataclasses import dataclass
from ..core.types import Price, TimestampMs


@dataclass(frozen=True)
class SettlementEvent:
    instrument_id: str
    price: Price
    timestamp_ms: TimestampMs
