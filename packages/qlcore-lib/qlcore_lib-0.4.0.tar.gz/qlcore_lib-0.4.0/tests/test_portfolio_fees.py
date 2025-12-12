from decimal import Decimal

from qlcore.events.fee import FeeEvent
from qlcore.portfolio import Portfolio


def test_portfolio_fee_application():
    """Test fee application to portfolio.

    FIXED: Corrected test expectations to match fixed signed_amount logic.

    A positive fee amount (e.g., Decimal("5")) represents a fee paid.
    The signed_amount property returns negative (outflow).
    When applied to account, the balance should decrease (become negative).
    """
    portfolio = Portfolio()

    # Test 1: Regular fee (positive amount = fee paid)
    fee = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("5"),  # FIXED: Positive amount (fee paid)
        currency="USD",
        timestamp_ms=0,
        note="trading fee",
    )
    portfolio.apply_fee(fee)

    # signed_amount returns -5 (outflow)
    # Account balance should be -5 (cash reduced)
    assert portfolio.account.balances["USD"] == Decimal("-5")
    assert len(portfolio.ledger.entries) == 1
    assert portfolio.ledger.entries[0].amount == Decimal("-5")

    # Test 2: Maker rebate (negative amount = fee received)
    portfolio2 = Portfolio()
    rebate = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("-3"),  # Negative amount (rebate received)
        currency="USD",
        timestamp_ms=1,
        note="maker rebate",
    )
    portfolio2.apply_fee(rebate)

    # signed_amount returns +3 (inflow from rebate)
    # Account balance should be +3 (cash increased)
    assert portfolio2.account.balances["USD"] == Decimal("3")
    assert portfolio2.ledger.entries[0].amount == Decimal("3")


def test_fee_event_signed_amount():
    """Test that FeeEvent.signed_amount returns correct sign."""

    # Regular fee: positive amount -> negative signed_amount (outflow)
    fee = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("10"),
        currency="USD",
        timestamp_ms=0,
    )
    assert fee.signed_amount == Decimal("-10")

    # Rebate: negative amount -> positive signed_amount (inflow)
    rebate = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("-5"),
        currency="USD",
        timestamp_ms=0,
    )
    assert rebate.signed_amount == Decimal("5")
