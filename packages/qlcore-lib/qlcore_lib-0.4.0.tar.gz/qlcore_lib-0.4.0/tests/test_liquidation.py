from decimal import Decimal

from qlcore.core.enums import PositionSide
from qlcore.risk.liquidation import (
    calculate_isolated_liquidation_price,
    calculate_cross_liquidation_price,
)
from qlcore.margin.requirements import MarginSchedule, MarginLevel


def test_isolated_long_liquidation_price():
    price = calculate_isolated_liquidation_price(
        side=PositionSide.LONG,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        wallet_margin=Decimal("20"),
        maintenance_margin_rate=Decimal("0.1"),
    )
    # numerator = 100 - 20, denominator = 1 - 0.1 = 0.9 -> 80/0.9
    assert price == Decimal("88.88888888888888888888888889")


def test_no_liquidation_when_wallet_sufficient():
    price = calculate_isolated_liquidation_price(
        side=PositionSide.LONG,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        wallet_margin=Decimal("200"),
        maintenance_margin_rate=Decimal("0.1"),
    )
    assert price is None


def test_cross_uses_equity_as_wallet():
    price = calculate_cross_liquidation_price(
        portfolio_equity=Decimal("50"),
        position_notional=Decimal("100"),
        side=PositionSide.SHORT,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        maintenance_margin_rate=Decimal("0.1"),
    )
    assert price == Decimal("136.3636363636363636363636364")


def test_liquidation_with_safety_buffer():
    price = calculate_isolated_liquidation_price(
        side=PositionSide.LONG,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        wallet_margin=Decimal("10"),
        maintenance_margin_rate=Decimal("0.1"),
        safety_buffer=Decimal("10"),
    )
    assert price > Decimal("100")


def test_liquidation_with_margin_schedule():
    schedule = MarginSchedule(
        levels=(
            MarginLevel(
                notional_threshold=Decimal("0"),
                initial=Decimal("0.1"),
                maintenance=Decimal("0.05"),
            ),
            MarginLevel(
                notional_threshold=Decimal("50"),
                initial=Decimal("0.2"),
                maintenance=Decimal("0.15"),
            ),
        )
    )
    price = calculate_isolated_liquidation_price(
        side=PositionSide.LONG,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        wallet_margin=Decimal("10"),
        maintenance_margin_rate=Decimal("0.1"),
        margin_schedule=schedule,
    )
    # higher maintenance -> closer liquidation price (should be higher than schedule-less)
    assert price > Decimal("100")
