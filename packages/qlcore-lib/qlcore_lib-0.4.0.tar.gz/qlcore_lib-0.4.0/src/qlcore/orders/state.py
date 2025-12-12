"""Order state machine and transitions."""

from enum import Enum
from dataclasses import dataclass
from ..core.types import Quantity
from ..core.exceptions import ValidationError


class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"


@dataclass
class OrderState:
    order_id: str
    status: OrderStatus
    cumulative_filled_qty: Quantity
    total_quantity: Quantity

    def apply_fill(self, fill_qty: Quantity) -> "OrderState":
        """Return a new state after applying a partial or full fill."""
        if fill_qty <= 0:
            raise ValidationError("fill quantity must be positive")
        new_cum = self.cumulative_filled_qty + fill_qty
        if new_cum > self.total_quantity:
            raise ValidationError("fill exceeds order quantity")
        if new_cum == self.total_quantity:
            new_status = OrderStatus.FILLED
        else:
            new_status = OrderStatus.PARTIALLY_FILLED
        return OrderState(
            order_id=self.order_id,
            status=new_status,
            cumulative_filled_qty=new_cum,
            total_quantity=self.total_quantity,
        )

    def cancel(self) -> "OrderState":
        """Return a new state representing a canceled order."""
        return OrderState(
            order_id=self.order_id,
            status=OrderStatus.CANCELED,
            cumulative_filled_qty=self.cumulative_filled_qty,
            total_quantity=self.total_quantity,
        )
