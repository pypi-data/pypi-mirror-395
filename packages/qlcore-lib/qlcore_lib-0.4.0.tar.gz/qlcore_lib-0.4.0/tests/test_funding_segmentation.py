from decimal import Decimal

from qlcore.events.funding import FundingEvent
from qlcore.core.enums import OrderSide
from qlcore.positions.base import BasePositionImpl
from qlcore.events.fill import Fill
from qlcore.pnl.funding import calculate_funding_payment


def test_funding_segments_by_fills():
    pos = BasePositionImpl.flat("BTC-PERP")
    # Open 2 size long
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-PERP",
            OrderSide.BUY,
            Decimal("2"),
            Decimal("100"),
            Decimal("0"),
            0,
        )
    )

    fills = [
        # reduce to 1 at t=500
        Fill(
            "o2",
            "BTC-PERP",
            OrderSide.SELL,
            Decimal("1"),
            Decimal("100"),
            Decimal("0"),
            500,
        ),
    ]

    event = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.01"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("100"),
    )

    payment = calculate_funding_payment(position=pos, event=event, fills=fills)

    # For first 500ms: size 2, for next 500ms: size 1, rate=1%, index=100
    # payment = -(2*100*0.01*0.5) -(1*100*0.01*0.5) = -1.5
    assert payment == Decimal("-1.5")
