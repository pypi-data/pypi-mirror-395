from decimal import Decimal

from qlcore.portfolio import Portfolio
from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.core.enums import OrderSide, PositionSide


def test_portfolio_multi_currency_cash_and_ledger():
    portfolio = Portfolio()

    usd_fill = Fill(
        order_id="usd1",
        instrument_id="BTC-USD",
        side=OrderSide.BUY,
        quantity=Decimal("1"),
        price=Decimal("10000"),
        fee=Decimal("10"),
        timestamp_ms=0,
    )
    eur_fill = Fill(
        order_id="eur1",
        instrument_id="ETH-EUR",
        side=OrderSide.BUY,
        quantity=Decimal("2"),
        price=Decimal("2000"),
        fee=Decimal("2"),
        timestamp_ms=1,
    )

    portfolio.apply_fill(usd_fill)
    portfolio.apply_fill(eur_fill)

    # Create funding event with correct field names
    funding_event = FundingEvent(
        instrument_id="BTC-USD",
        rate=Decimal("0.0001"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("10000"),
    )
    portfolio.apply_funding(funding_event, fills=[usd_fill])

    balance = portfolio.account.balance

    # Cash outflow from BUY fills plus funding payment
    # BUY 1 BTC @ 10000 with fee 10 = -10010
    # BUY 2 ETH @ 2000 with fee 2 = -4002
    # Funding for 1 BTC long @ rate 0.0001 = -1 (long pays when rate > 0)
    # Total = -10010 - 4002 - 1 = -14013
    assert balance == Decimal("-14013")
    assert len(portfolio.ledger.entries) == 3  # 2 fills + 1 funding


def test_perp_funding_uses_quote_currency_and_updates_position():
    portfolio = Portfolio()

    perp_fill = Fill(
        order_id="perp1",
        instrument_id="BTC-USDT-PERP",
        side=OrderSide.BUY,
        quantity=Decimal("1"),
        price=Decimal("10000"),
        fee=Decimal("0"),
        timestamp_ms=0,
    )

    portfolio.apply_fill(perp_fill)

    funding_event = FundingEvent(
        instrument_id="BTC-USDT-PERP",
        rate=Decimal("0.0001"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("10000"),
    )

    portfolio.apply_funding(funding_event, fills=[perp_fill])

    key = ("BTC-USDT-PERP", PositionSide.LONG)
    assert key in portfolio.positions
    assert portfolio.positions[key].realized_pnl == Decimal("-1")

    # Cash debit should hit the quote currency (USDT), not a fake "PERP" bucket.
    assert portfolio.account.balances["USDT"] == Decimal("-10001")
    assert "PERP" not in portfolio.account.balances
