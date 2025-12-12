"""Trailing-stop order implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseOrder
from ..state import OrderState, OrderStatus
from ...core.enums import OrderType, TimeInForce
from ...core.exceptions import ValidationError
from ...utils.validation import ensure_positive


@dataclass(frozen=True)
class TrailingStopOrder(BaseOrder):
    trail_amount: Decimal | None = None

    def __post_init__(self) -> None:
        if self.trail_amount is None:
            raise ValidationError("Trailing-stop orders require a trail_amount")
        ensure_positive(self.trail_amount, "trail_amount")
        object.__setattr__(self, "type", OrderType.TRAILING_STOP)
        object.__setattr__(self, "time_in_force", TimeInForce.GTC)
        object.__setattr__(self, "price", None)

    def initial_state(self) -> OrderState:
        return OrderState(
            order_id=self.id,
            status=OrderStatus.NEW,
            cumulative_filled_qty=Decimal(0),
            total_quantity=self.quantity,
        )
