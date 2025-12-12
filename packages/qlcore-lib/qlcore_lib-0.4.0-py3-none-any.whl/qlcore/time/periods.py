"""Simple time period helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimePeriod:
    start_ms: int
    end_ms: int

    def __post_init__(self) -> None:
        if self.end_ms < self.start_ms:
            raise ValueError("end_ms must be >= start_ms")

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    def contains(self, timestamp_ms: int) -> bool:
        return self.start_ms <= timestamp_ms <= self.end_ms
