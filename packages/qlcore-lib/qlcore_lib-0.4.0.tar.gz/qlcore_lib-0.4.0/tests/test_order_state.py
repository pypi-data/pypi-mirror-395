from decimal import Decimal

from qlcore.orders.state import OrderState, OrderStatus
from qlcore.core.exceptions import ValidationError


def test_partial_and_full_fill():
    state = OrderState(
        order_id="o1",
        status=OrderStatus.NEW,
        cumulative_filled_qty=Decimal(0),
        total_quantity=Decimal("5"),
    )
    state = state.apply_fill(Decimal("2"))
    assert state.status == OrderStatus.PARTIALLY_FILLED
    assert state.cumulative_filled_qty == Decimal("2")

    state = state.apply_fill(Decimal("3"))
    assert state.status == OrderStatus.FILLED
    assert state.cumulative_filled_qty == Decimal("5")


def test_overfill_rejected():
    state = OrderState(
        order_id="o2",
        status=OrderStatus.NEW,
        cumulative_filled_qty=Decimal("4"),
        total_quantity=Decimal("5"),
    )
    try:
        state.apply_fill(Decimal("2"))
        assert False, "expected ValidationError"
    except ValidationError:
        pass


def test_cancel_preserves_cum_qty():
    state = OrderState(
        order_id="o3",
        status=OrderStatus.PARTIALLY_FILLED,
        cumulative_filled_qty=Decimal("1"),
        total_quantity=Decimal("3"),
    )
    canceled = state.cancel()
    assert canceled.status == OrderStatus.CANCELED
    assert canceled.cumulative_filled_qty == Decimal("1")
