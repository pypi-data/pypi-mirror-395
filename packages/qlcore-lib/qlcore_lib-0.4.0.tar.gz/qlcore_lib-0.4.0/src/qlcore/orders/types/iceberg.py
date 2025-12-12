"""Iceberg order implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseOrder
from ..state import OrderState, OrderStatus
from ...core.enums import OrderType, TimeInForce
from ...core.exceptions import ValidationError
from ...utils.validation import ensure_positive


@dataclass(frozen=True)
class IcebergOrder(BaseOrder):
    display_quantity: Decimal | None = None

    def __post_init__(self) -> None:
        if self.price is None:
            raise ValidationError("Iceberg orders require a price")
        if self.display_quantity is None:
            raise ValidationError("display_quantity is required for iceberg orders")
        ensure_positive(self.display_quantity, "display_quantity")
        if self.display_quantity > self.quantity:
            raise ValidationError("display_quantity cannot exceed total quantity")
        object.__setattr__(self, "type", OrderType.ICEBERG)
        object.__setattr__(self, "time_in_force", TimeInForce.GTC)

    def initial_state(self) -> OrderState:
        return OrderState(
            order_id=self.id,
            status=OrderStatus.NEW,
            cumulative_filled_qty=Decimal(0),
            total_quantity=self.quantity,
        )
