from decimal import Decimal

import pytest

from qlcore.math.stats import mean, variance
from qlcore.math.volatility import realized_volatility, annualize_volatility


def test_stats_require_values():
    with pytest.raises(ValueError):
        mean([])
    with pytest.raises(ValueError):
        variance([], sample=False)
    with pytest.raises(ValueError):
        variance([Decimal("1")], sample=True)


def test_realized_volatility_and_annualization():
    returns = [Decimal("0.01"), Decimal("-0.01"), Decimal("0.02")]
    vol = realized_volatility(returns, periods_per_year=356)
    assert vol > 0

    annual = annualize_volatility(Decimal("0.1"), periods_per_year=356)
    assert annual > Decimal("0.1")

    with pytest.raises(ValueError):
        annualize_volatility(Decimal("0.1"), periods_per_year=0)
