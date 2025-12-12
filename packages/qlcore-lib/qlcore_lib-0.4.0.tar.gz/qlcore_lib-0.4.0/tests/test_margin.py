from decimal import Decimal

from qlcore.margin.requirements import (
    MarginRequirements,
    MarginLevel,
    MarginSchedule,
    calculate_initial_margin,
    calculate_maintenance_margin,
)
from qlcore.margin.utilization import margin_utilization
from qlcore.margin.cross import free_margin
from qlcore.margin.isolated import IsolatedMargin


def test_margin_calculations():
    req = MarginRequirements(initial=Decimal("0.1"), maintenance=Decimal("0.05"))
    assert calculate_initial_margin(Decimal("1000"), req) == Decimal("100")
    assert calculate_maintenance_margin(Decimal("1000"), req) == Decimal("50")
    assert margin_utilization(Decimal("100"), Decimal("200")) == Decimal("0.5")
    assert free_margin(Decimal("200"), Decimal("50")) == Decimal("150")

    iso = IsolatedMargin(wallet=Decimal("100"), requirement=Decimal("40"))
    assert iso.free == Decimal("60")

    schedule = MarginSchedule(
        levels=(
            MarginLevel(
                notional_threshold=Decimal("0"),
                initial=Decimal("0.1"),
                maintenance=Decimal("0.05"),
            ),
            MarginLevel(
                notional_threshold=Decimal("10000"),
                initial=Decimal("0.2"),
                maintenance=Decimal("0.1"),
            ),
        )
    )

    # tiered lookup by notional
    req_big = schedule.for_notional(Decimal("20000"))
    assert req_big.initial == Decimal("0.2")
    assert req_big.maintenance == Decimal("0.1")

    # tiered lookup by size * price
    req_big_by_size = schedule.for_size(size=Decimal("2"), price=Decimal("10000"))
    assert req_big_by_size.initial == Decimal("0.2")
    assert req_big_by_size.maintenance == Decimal("0.1")

    # convenience rate helpers (size + price)
    init_rate = schedule.get_initial_margin_rate(
        size=Decimal("2"), price=Decimal("10000")
    )
    maint_rate = schedule.get_maintenance_margin_rate(
        size=Decimal("2"), price=Decimal("10000")
    )
    assert init_rate == Decimal("0.2")
    assert maint_rate == Decimal("0.1")

    # convenience rate helpers (explicit notional)
    init_rate_notional = schedule.get_initial_margin_rate(notional=Decimal("20000"))
    maint_rate_notional = schedule.get_maintenance_margin_rate(
        notional=Decimal("20000")
    )
    assert init_rate_notional == Decimal("0.2")
    assert maint_rate_notional == Decimal("0.1")
