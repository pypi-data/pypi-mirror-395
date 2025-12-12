"""Funding rate series element."""

from __future__ import annotations

from dataclasses import dataclass
from ..core.types import Rate, Price, TimestampMs


@dataclass(frozen=True)
class FundingRate:
    instrument_id: str
    rate: Rate
    index_price: Price
    timestamp_ms: TimestampMs
