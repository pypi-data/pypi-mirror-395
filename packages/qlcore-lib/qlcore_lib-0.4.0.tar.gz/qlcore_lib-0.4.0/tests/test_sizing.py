from decimal import Decimal

from qlcore.sizing.fixed import fixed_quantity, fixed_notional
from qlcore.sizing.percent import percent_of_equity
from qlcore.sizing.risk_based import risk_per_trade
from qlcore.sizing.kelly import kelly_fraction
from qlcore.sizing.volatility import atr_position_size
from qlcore.sizing.constraints import apply_position_limits


def test_sizing_functions():
    assert fixed_quantity(Decimal("2")) == Decimal("2")
    assert fixed_notional(Decimal("1000"), Decimal("100")) == Decimal("10")
    assert percent_of_equity(
        Decimal("1000"), Decimal("0.1"), Decimal("100")
    ) == Decimal("1")
    assert risk_per_trade(Decimal("1000"), Decimal("0.01"), Decimal("50")) == Decimal(
        "0.2"
    )
    assert atr_position_size(Decimal("1000"), Decimal("10")) == Decimal("100")
    frac = kelly_fraction(Decimal("0.6"), Decimal("2"))
    assert frac == Decimal("0.4")
    constrained = apply_position_limits(
        Decimal("5"),
        max_position=Decimal("3"),
        price=Decimal("100"),
        max_notional=Decimal("250"),
    )
    assert constrained == Decimal("2.5")
