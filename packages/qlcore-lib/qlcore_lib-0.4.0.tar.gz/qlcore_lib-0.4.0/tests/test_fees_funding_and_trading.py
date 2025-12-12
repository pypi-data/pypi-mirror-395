from decimal import Decimal


from qlcore.fees.funding import funding_fee
from qlcore.fees.trading import FeeSchedule, fee_for_trade


def test_funding_fee_basic():
    assert funding_fee(Decimal("1000"), Decimal("0.001")) == Decimal("1.000")


def test_fee_for_trade_maker_taker():
    schedule = FeeSchedule(
        maker_rate=Decimal("0.0002"),
        taker_rate=Decimal("0.0004"),
    )
    maker = fee_for_trade(Decimal("10000"), is_maker=True, schedule=schedule)
    taker = fee_for_trade(Decimal("10000"), is_maker=False, schedule=schedule)
    assert maker == Decimal("2.0000")
    assert taker == Decimal("4.0000")

    # Negative notional just yields negative fee (no validation enforced)
    negative_fee = fee_for_trade(Decimal("-1"), is_maker=True, schedule=schedule)
    assert negative_fee < 0
