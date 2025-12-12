"""Limit order implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseOrder
from ..state import OrderState, OrderStatus
from ...core.enums import OrderType, TimeInForce
from ...core.exceptions import ValidationError


@dataclass(frozen=True)
class LimitOrder(BaseOrder):
    def __post_init__(self) -> None:
        if self.price is None:
            raise ValidationError("Limit orders require a limit price")
        object.__setattr__(self, "type", OrderType.LIMIT)
        # FIXED: Removed duplicate GTC check
        if self.time_in_force not in (
            TimeInForce.GTC,
            TimeInForce.FOK,
            TimeInForce.IOC,
            TimeInForce.POST_ONLY,
        ):
            object.__setattr__(self, "time_in_force", TimeInForce.GTC)

    def initial_state(self) -> OrderState:
        return OrderState(
            order_id=self.id,
            status=OrderStatus.NEW,
            cumulative_filled_qty=Decimal(0),
            total_quantity=self.quantity,
        )
