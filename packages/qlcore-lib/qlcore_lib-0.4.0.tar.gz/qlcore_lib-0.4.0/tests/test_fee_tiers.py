from decimal import Decimal

from qlcore.fees.trading import FeeSchedule, fee_for_trade, select_vip_tier
from qlcore.fees.tiers import VipTier


def test_fee_for_trade_maker_taker():
    schedule = FeeSchedule(maker_rate=Decimal("0.0002"), taker_rate=Decimal("0.0004"))
    fee_maker = fee_for_trade(Decimal("10000"), True, schedule)
    fee_taker = fee_for_trade(Decimal("10000"), False, schedule)
    assert fee_maker == Decimal("2")
    assert fee_taker == Decimal("4")


def test_select_vip_tier():
    tiers = [
        VipTier(
            name="base",
            required_volume=Decimal("0"),
            maker_rate=Decimal("0.0004"),
            taker_rate=Decimal("0.0006"),
        ),
        VipTier(
            name="vip1",
            required_volume=Decimal("1000000"),
            maker_rate=Decimal("0.0002"),
            taker_rate=Decimal("0.0005"),
        ),
    ]
    tier = select_vip_tier(Decimal("1500000"), tiers)
    assert tier.name == "vip1"
