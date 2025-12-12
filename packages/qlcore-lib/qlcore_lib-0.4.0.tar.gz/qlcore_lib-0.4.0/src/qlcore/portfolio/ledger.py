"""Transaction ledger."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..core.types import Money, TimestampMs


@dataclass(frozen=True)
class LedgerEntry:
    description: str
    amount: Money
    currency: str
    timestamp_ms: TimestampMs
    instrument_id: str | None = None
    meta: Dict[str, Any] = field(default_factory=dict)


class Ledger:
    def __init__(self) -> None:
        self.entries: List[LedgerEntry] = []

    def record(self, entry: LedgerEntry) -> None:
        self.entries.append(entry)
