"""Integration tests simulating realistic trading scenarios."""

from decimal import Decimal
from qlcore.portfolio import Portfolio
from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.core.enums import OrderSide, PositionSide
from qlcore.pnl import calculate_portfolio_pnl, PnLMode
from qlcore.risk import max_drawdown


def test_realistic_trading_day():
    """Simulate a realistic trading day with 100 fills, funding, and PnL calculation."""
    portfolio = Portfolio()

    # Deposit initial capital
    portfolio.account.deposit(Decimal("10000"))

    # Simulate 100 fills alternating buy/sell
    fills = []
    base_price = Decimal("10000")

    for i in range(100):
        side = OrderSide.BUY if i % 2 == 0 else OrderSide.SELL
        price = base_price + Decimal(i % 10) * Decimal("10")

        fill = Fill(
            order_id=f"o{i}",
            instrument_id="BTC-PERP",
            side=side,
            quantity=Decimal("0.1"),
            price=price,
            fee=Decimal("0.5"),
            timestamp_ms=i * 1000,
        )
        fills.append(fill)
        portfolio.apply_fill(fill)

    # Apply funding event
    funding = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.0001"),
        period_start_ms=0,
        period_end_ms=100000,
        index_price=Decimal("10050"),
    )
    portfolio.apply_funding(funding, fills=fills)

    # Calculate final PnL
    marks = {"BTC-PERP": Decimal("10100")}
    pnl = calculate_portfolio_pnl(
        portfolio=portfolio,
        marks=marks,
        fills=fills,
        funding_events=[funding],
        mode=PnLMode.BOTH,
    )

    # Assertions
    assert len(portfolio.positions) <= 1  # At most one position (could be flat)
    assert pnl.total is not None
    assert pnl.fees > 0  # Should have paid fees
    assert len(portfolio.ledger.entries) > 0

    # Verify account balance is reasonable
    equity = portfolio.account.equity + pnl.unrealized
    assert equity > Decimal("0")  # Should have positive equity


def test_position_flip_with_pnl():
    """Test position flip from LONG to SHORT with correct PnL accounting."""
    portfolio = Portfolio()

    # Open LONG position
    buy_fill = Fill(
        "o1", "BTC-USD", OrderSide.BUY, Decimal("2"), Decimal("100"), Decimal("2"), 0
    )
    portfolio.apply_fill(buy_fill)

    # Check position
    assert len(portfolio.positions) == 1
    key = ("BTC-USD", PositionSide.LONG)
    assert key in portfolio.positions
    assert portfolio.positions[key].size == Decimal("2")

    # Flip to SHORT
    sell_fill = Fill(
        "o2",
        "BTC-USD",
        OrderSide.SELL,
        Decimal("3"),
        Decimal("110"),
        Decimal("3"),
        1000,
    )
    portfolio.apply_fill(sell_fill)

    # Check flipped position
    assert len(portfolio.positions) == 1
    short_key = ("BTC-USD", PositionSide.SHORT)
    assert short_key in portfolio.positions
    short_pos = portfolio.positions[short_key]
    assert short_pos.size == Decimal("1")

    # Verify realized PnL from closing LONG
    # Sold 2 @ 110, bought @ 100, profit = 2 * (110 - 100) = 20
    assert short_pos.realized_pnl == Decimal("20")

    # Verify fees accumulated
    total_fees = Decimal("2") + Decimal("3")
    assert short_pos.fees == total_fees


def test_equity_curve_calculation():
    """Test tracking equity curve over multiple trades."""
    portfolio = Portfolio()
    portfolio.account.deposit(Decimal("1000"))

    equity_curve = []
    prices = [
        Decimal("100"),
        Decimal("105"),
        Decimal("103"),
        Decimal("110"),
        Decimal("108"),
    ]

    # Open position
    buy_fill = Fill(
        "o1", "BTC-USD", OrderSide.BUY, Decimal("1"), prices[0], Decimal("1"), 0
    )
    portfolio.apply_fill(buy_fill)

    # Track equity at each price point
    for i, mark_price in enumerate(prices):
        pnl = calculate_portfolio_pnl(
            portfolio=portfolio, marks={"BTC-USD": mark_price}, mode=PnLMode.BOTH
        )
        equity = portfolio.account.equity + pnl.total.unrealized
        equity_curve.append(equity)

    # Calculate max drawdown
    dd, peak = max_drawdown(equity_curve)

    # Assertions
    assert len(equity_curve) == 5
    assert all(e > Decimal("0") for e in equity_curve)  # All positive
    assert dd <= Decimal("0")  # Drawdown is negative
    assert peak == max(equity_curve)


def test_multi_instrument_portfolio():
    """Test portfolio with multiple instruments."""
    portfolio = Portfolio()

    portfolio.account.deposit(Decimal("10000"))

    # Trade BTC
    btc_fill = Fill(
        "o1",
        "BTC-USD",
        OrderSide.BUY,
        Decimal("0.5"),
        Decimal("10000"),
        Decimal("5"),
        0,
    )
    portfolio.apply_fill(btc_fill)

    # Trade ETH
    eth_fill = Fill(
        "o2",
        "ETH-USD",
        OrderSide.BUY,
        Decimal("10"),
        Decimal("200"),
        Decimal("2"),
        1000,
    )
    portfolio.apply_fill(eth_fill)

    # Verify positions
    assert len(portfolio.positions) == 2
    assert ("BTC-USD", PositionSide.LONG) in portfolio.positions
    assert ("ETH-USD", PositionSide.LONG) in portfolio.positions

    # Calculate equity
    marks = {"BTC-USD": Decimal("10500"), "ETH-USD": Decimal("220")}

    pnl = calculate_portfolio_pnl(portfolio=portfolio, marks=marks, mode=PnLMode.BOTH)

    equity = portfolio.account.equity + pnl.total.unrealized

    assert equity > Decimal("0")
    assert len(portfolio.ledger.entries) == 2  # Two fills recorded


def test_funding_with_position_size_changes():
    """Test funding calculation when position size changes during funding period."""
    portfolio = Portfolio()

    # Open position with 2 BTC
    fill1 = Fill(
        "o1", "BTC-PERP", OrderSide.BUY, Decimal("2"), Decimal("10000"), Decimal("2"), 0
    )
    portfolio.apply_fill(fill1)

    # Reduce to 1 BTC at midpoint
    fill2 = Fill(
        "o2",
        "BTC-PERP",
        OrderSide.SELL,
        Decimal("1"),
        Decimal("10000"),
        Decimal("1"),
        500,
    )
    portfolio.apply_fill(fill2)

    # Apply funding over period containing both fills
    funding = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.01"),  # 1% funding rate
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("10000"),
    )

    portfolio.apply_funding(funding, fills=[fill1, fill2])

    # Position should still be open
    assert len(portfolio.positions) == 1

    # Funding payment should be time-weighted
    # First half: 2 BTC * 10000 * 0.01 * 0.5 = -100
    # Second half: 1 BTC * 10000 * 0.01 * 0.5 = -50
    # Total: -150
    expected_funding = Decimal("-150")

    # Check ledger has funding entry
    funding_entries = [
        e for e in portfolio.ledger.entries if e.description == "FUNDING"
    ]
    assert len(funding_entries) == 1
    assert funding_entries[0].amount == expected_funding


def test_fee_accumulation():
    """Test that fees accumulate correctly across multiple fills."""
    portfolio = Portfolio()

    fills = [
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("100"),
            Decimal("1"),
            0,
        ),
        Fill(
            "o2",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("105"),
            Decimal("1.5"),
            1000,
        ),
        Fill(
            "o3",
            "BTC-USD",
            OrderSide.SELL,
            Decimal("1"),
            Decimal("110"),
            Decimal("2"),
            2000,
        ),
    ]

    for fill in fills:
        portfolio.apply_fill(fill)

    # Check position
    pos = portfolio.positions[("BTC-USD", PositionSide.LONG)]

    # Total fees should be sum of all fill fees
    expected_fees = Decimal("1") + Decimal("1.5") + Decimal("2")
    assert pos.fees == expected_fees

    # Verify ledger has all fills
    assert len(portfolio.ledger.entries) == 3
