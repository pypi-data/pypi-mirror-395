from decimal import Decimal

from qlcore.positions.base import BasePositionImpl
from qlcore.core.enums import OrderSide
from qlcore.events.fill import Fill
from qlcore.pnl import calculate_pnl, PnLMode


def test_spot_round_trip():
    pos = BasePositionImpl.flat("ETH-USD")
    pos = pos.apply_fill(
        Fill(
            "buy",
            "ETH-USD",
            OrderSide.BUY,
            Decimal("2"),
            Decimal("1000"),
            Decimal("2"),
            0,
        )
    )
    pos = pos.apply_fill(
        Fill(
            "sell",
            "ETH-USD",
            OrderSide.SELL,
            Decimal("1"),
            Decimal("1100"),
            Decimal("1"),
            1,
        )
    )

    pnl = calculate_pnl(position=pos, mark_price=Decimal("1200"), mode=PnLMode.BOTH)

    # Remaining size 1 @ avg price ~1000, realized on sold 1 minus fees
    assert pos.size == Decimal("1")
    assert pnl.realized > Decimal("90")
    assert pnl.unrealized == Decimal("200")
