"""Base order definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..core.enums import OrderSide, OrderType, TimeInForce
from ..core.types import TimestampMs, Quantity, Price


@dataclass(frozen=True)
class BaseOrder:
    id: str
    instrument_id: str
    side: OrderSide
    type: OrderType
    quantity: Quantity
    price: Optional[Price]
    time_in_force: TimeInForce
    timestamp_ms: TimestampMs
