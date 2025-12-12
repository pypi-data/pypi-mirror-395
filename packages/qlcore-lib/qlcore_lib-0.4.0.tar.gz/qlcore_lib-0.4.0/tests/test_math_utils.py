from decimal import Decimal

import pytest

from qlcore.math.rounding import round_price_to_tick, round_qty_to_lot, quantize_fee
from qlcore.math.returns import simple_return, log_return, cumulative_return
from qlcore.math.stats import mean, stddev


def test_rounding():
    assert round_price_to_tick(Decimal("100.123"), Decimal("0.01")) == Decimal("100.12")
    assert round_qty_to_lot(Decimal("1.234"), Decimal("0.1")) == Decimal("1.2")
    assert quantize_fee(Decimal("1.2345"), precision=2) == Decimal("1.23")


def test_returns_and_stats():
    assert simple_return(Decimal("110"), Decimal("100")) == Decimal("0.1")
    assert cumulative_return([Decimal("0.1"), Decimal("0.1")]) == Decimal("0.21")
    assert mean([Decimal("1"), Decimal("3")]) == Decimal("2")
    assert stddev([Decimal("1"), Decimal("3")]) == Decimal("1")
    with pytest.raises(ValueError):
        log_return(Decimal("-1"), Decimal("1"))
