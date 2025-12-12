"""Market order implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseOrder
from ..state import OrderState, OrderStatus
from ...core.enums import OrderType, TimeInForce
from ...core.exceptions import ValidationError


@dataclass(frozen=True)
class MarketOrder(BaseOrder):
    def __post_init__(self) -> None:
        if self.price is not None:
            raise ValidationError("Market orders should not define price")
        object.__setattr__(self, "type", OrderType.MARKET)
        object.__setattr__(self, "time_in_force", TimeInForce.IOC)

    def initial_state(self) -> OrderState:
        return OrderState(
            order_id=self.id,
            status=OrderStatus.NEW,
            cumulative_filled_qty=Decimal(0),
            total_quantity=self.quantity,
        )
