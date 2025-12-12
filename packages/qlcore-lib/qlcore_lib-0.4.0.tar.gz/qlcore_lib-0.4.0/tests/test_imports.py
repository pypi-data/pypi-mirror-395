from decimal import Decimal

from qlcore.core.enums import OrderSide, PositionSide
from qlcore.events.fill import Fill
from qlcore.pnl import calculate_pnl, PnLMode
from qlcore.positions.base import BasePositionImpl


def test_basic_pnl_flow():
    pos = BasePositionImpl.flat("BTC-USD")
    pos = pos.apply_fill(
        Fill(
            "buy",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
    )
    pos = pos.apply_fill(
        Fill(
            "sell",
            "BTC-USD",
            OrderSide.SELL,
            Decimal("0.4"),
            Decimal("11000"),
            Decimal("4"),
            1,
        )
    )

    pnl = calculate_pnl(position=pos, mark_price=Decimal("10500"), mode=PnLMode.BOTH)

    assert pos.size == Decimal("0.6")
    assert pnl.realized == Decimal("400")
    assert pnl.unrealized == Decimal("300")
    # FIXED: Total PnL calculation
    # total = realized + unrealized - fees
    # total = 400 + 300 - 14 = 686
    assert pnl.total == Decimal("686")


def test_flip_allocates_fee_to_new_lot():
    pos = BasePositionImpl.flat("BTC-USD")
    pos = pos.apply_fill(
        Fill(
            "buy",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("100"),
            Decimal("1"),
            0,
        )
    )
    pos = pos.apply_fill(
        Fill(
            "sell-flip",
            "BTC-USD",
            OrderSide.SELL,
            Decimal("2"),
            Decimal("90"),
            Decimal("2"),
            1,
        )
    )
    assert pos.side == PositionSide.SHORT
    assert pos.size == Decimal("1")
    assert pos.realized_pnl == Decimal("-10")
    assert pos.lots[0].fee == Decimal("1")
    assert pos.entry_value == Decimal("-89")
    assert pos.fees == Decimal("3")
