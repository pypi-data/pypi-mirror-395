from decimal import Decimal

from qlcore.positions.base import BasePositionImpl
from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.core.enums import OrderSide
from qlcore.pnl import (
    calculate_funding_payment,
    calculate_portfolio_pnl,
    PnLMode,
)
from qlcore.portfolio import Portfolio


def test_funding_payment_short_receives_when_rate_positive():
    """Short positions should receive funding when rate is positive."""
    pos = BasePositionImpl.flat("BTC-PERP")
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-PERP",
            OrderSide.SELL,
            Decimal("1"),
            Decimal("100"),
            Decimal("0"),
            0,
        )
    )

    event = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.01"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("100"),
    )

    payment = calculate_funding_payment(position=pos, event=event)
    assert payment > 0  # Short receives payment when rate > 0
    assert payment == Decimal("1.0")


def test_funding_payment_uses_fills_applied_flag():
    """When fills already applied to position, funding should rewind to start size."""
    pos = BasePositionImpl.flat("BTC-PERP")
    fill_open = Fill(
        "o1",
        "BTC-PERP",
        OrderSide.BUY,
        Decimal("2"),
        Decimal("100"),
        Decimal("0"),
        0,
    )
    pos = pos.apply_fill(fill_open)

    # Apply reduction; position now 1, but funding should consider 2->1 change
    fill_reduce = Fill(
        "o2",
        "BTC-PERP",
        OrderSide.SELL,
        Decimal("1"),
        Decimal("100"),
        Decimal("0"),
        500,
    )
    pos = pos.apply_fill(fill_reduce)

    event = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.01"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("100"),
    )

    payment = calculate_funding_payment(
        position=pos, event=event, fills=[fill_reduce], fills_applied=True
    )
    # First half size 2, second half size 1 => -(2*100*0.01*0.5) -(1*100*0.01*0.5) = -1.5
    assert payment == Decimal("-1.5")


def test_portfolio_pnl_includes_fee_only_breakdown():
    """Aggregate PnL should include fees even when no positions remain."""
    portfolio = Portfolio()

    # No positions or marks; only fees should be aggregated
    pnl = calculate_portfolio_pnl(
        portfolio=portfolio,
        marks={},
        fills=(
            Fill(
                "o1",
                "BTC-USD",
                OrderSide.BUY,
                Decimal("0.1"),
                Decimal("10000"),
                Decimal("5"),
                0,
            ),
        ),
        funding_events=(),
        fee_events=(),
        slippage_events=(),
        mode=PnLMode.BOTH,
    )

    assert pnl.total.fees == Decimal("5")
    assert pnl.fees == Decimal("5")
