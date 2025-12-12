"""Simple in-memory audit trail for user actions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import List, Any, Dict
from decimal import Decimal

from ..core.types import TimestampMs


class AuditEventType(str, Enum):
    FILL = "fill"
    FUNDING = "funding"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


@dataclass(frozen=True)
class AuditEvent:
    event_type: AuditEventType
    user_id: str
    instrument_id: str | None
    timestamp_ms: TimestampMs
    details: Dict[str, Any] = field(default_factory=dict)


class AuditTrail:
    """Lightweight audit trail for unit tests and examples."""

    def __init__(self):
        self.events: List[AuditEvent] = []

    def record_fill(
        self,
        user_id: str,
        order_id: str,
        instrument_id: str,
        side: str,
        quantity: Decimal,
        price: Decimal,
        fee: Decimal,
        timestamp_ms: int | None = None,
    ) -> None:
        """Record a fill event."""
        ts = TimestampMs(
            int(timestamp_ms if timestamp_ms is not None else time.time() * 1000)
        )
        event = AuditEvent(
            event_type=AuditEventType.FILL,
            user_id=user_id,
            instrument_id=instrument_id,
            timestamp_ms=ts,
            details={
                "order_id": order_id,
                "side": side,
                "quantity": str(quantity),
                "price": str(price),
                "fee": str(fee),
            },
        )
        self.events.append(event)

    def get_events_by_user(self, user_id: str) -> List[AuditEvent]:
        return [e for e in self.events if e.user_id == user_id]

    def get_events_by_instrument(self, instrument_id: str) -> List[AuditEvent]:
        return [e for e in self.events if e.instrument_id == instrument_id]
