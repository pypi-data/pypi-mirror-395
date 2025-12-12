"""Funding event structure."""

from dataclasses import dataclass
from ..core.types import Rate, Price, TimestampMs
from ..utils.validation import (
    ensure_valid_price,
    ensure_valid_rate,
    ensure_valid_timestamp,
    ensure_valid_timestamp_order,
    sanitize_instrument_id,
)


@dataclass(frozen=True)
class FundingEvent:
    instrument_id: str
    rate: Rate
    period_start_ms: TimestampMs
    period_end_ms: TimestampMs
    index_price: Price

    def __post_init__(self) -> None:
        instrument_id = sanitize_instrument_id(self.instrument_id)
        object.__setattr__(self, "instrument_id", instrument_id)

        ensure_valid_rate(self.rate, "rate", allow_negative=True)
        ensure_valid_price(self.index_price, "index_price")
        ensure_valid_timestamp(self.period_start_ms, "period_start_ms")
        ensure_valid_timestamp(self.period_end_ms, "period_end_ms")
        ensure_valid_timestamp_order(
            self.period_start_ms,
            self.period_end_ms,
            start_name="period_start_ms",
            end_name="period_end_ms",
        )
