"""Stop-limit order implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseOrder
from ..state import OrderState, OrderStatus
from ...core.enums import OrderType, TimeInForce
from ...core.exceptions import ValidationError
from ...core.types import Price


@dataclass(frozen=True)
class StopLimitOrder(BaseOrder):
    stop_price: Price | None = None

    def __post_init__(self) -> None:
        if self.price is None:
            raise ValidationError("Stop-limit orders require a limit price")
        stop = self.stop_price if self.stop_price is not None else self.price
        if stop is None:
            raise ValidationError("Stop-limit orders require a stop price")
        object.__setattr__(self, "stop_price", stop)
        object.__setattr__(self, "type", OrderType.STOP_LIMIT)
        object.__setattr__(self, "time_in_force", TimeInForce.GTC)

    def initial_state(self) -> OrderState:
        return OrderState(
            order_id=self.id,
            status=OrderStatus.NEW,
            cumulative_filled_qty=Decimal(0),
            total_quantity=self.quantity,
        )
