from decimal import Decimal
import pytest

from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.events.fee import FeeEvent
from qlcore.core.enums import OrderSide
from qlcore.core.exceptions import ValidationError


def test_fill_validation():
    """Test fill event validation."""
    # Valid fill
    fill = Fill(
        order_id="o1",
        instrument_id="BTC-USD",
        side=OrderSide.BUY,
        quantity=Decimal("1"),
        price=Decimal("10000"),
        fee=Decimal("10"),
        timestamp_ms=0,
    )
    assert fill.instrument_id == "BTC-USD"

    # Invalid: empty order_id
    with pytest.raises(ValidationError, match="order_id"):
        Fill(
            "",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )

    # Invalid: zero quantity
    with pytest.raises(ValidationError, match="quantity"):
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("0"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )

    # Invalid: negative fee
    with pytest.raises(ValidationError):
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("-10"),
            0,
        )


def test_funding_event_validation():
    """Test funding event validation."""
    # Valid funding
    event = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.0001"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("10000"),
    )
    assert event.rate == Decimal("0.0001")

    # Invalid: end before start
    with pytest.raises(ValidationError, match="must be >="):
        FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("0.0001"),
            period_start_ms=1000,
            period_end_ms=500,
            index_price=Decimal("10000"),
        )

    # Invalid: extreme rate
    with pytest.raises(ValidationError):
        FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("50"),
            period_start_ms=0,
            period_end_ms=1000,
            index_price=Decimal("10000"),
        )


def test_fee_event_validation():
    """Test fee event validation."""
    # Valid fee
    fee = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("10"),
        currency="USD",
        timestamp_ms=0,
    )
    assert fee.currency == "USD"

    # Currency normalization
    fee = FeeEvent(
        instrument_id="BTC-USD",
        amount=Decimal("10"),
        currency="usd",
        timestamp_ms=0,
    )
    assert fee.currency == "USD"

    # Invalid: note too long
    with pytest.raises(ValidationError, match="note too long"):
        FeeEvent(
            instrument_id="BTC-USD",
            amount=Decimal("10"),
            currency="USD",
            timestamp_ms=0,
            note="x" * 501,
        )
