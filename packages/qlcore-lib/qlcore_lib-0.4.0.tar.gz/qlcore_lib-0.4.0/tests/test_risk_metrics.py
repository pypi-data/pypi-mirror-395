from decimal import Decimal

import pytest

from qlcore.risk.metrics import sharpe_ratio, sortino_ratio
from qlcore.risk.drawdown import max_drawdown
from qlcore.risk.var import historical_var
from qlcore.risk.exposure import net_exposure, gross_exposure


def test_risk_metrics_basic_and_empty():
    rets = [Decimal("0.01"), Decimal("0.02"), Decimal("-0.01")]
    assert sharpe_ratio(rets) is not None
    assert sortino_ratio(rets) is not None
    assert historical_var(rets, confidence=0.95) >= 0

    dd, peak = max_drawdown(
        [Decimal("100"), Decimal("105"), Decimal("95"), Decimal("120")]
    )
    assert dd < 0
    assert peak == Decimal("120")

    assert net_exposure(Decimal("100"), Decimal("50")) == Decimal("50")
    assert gross_exposure(Decimal("100"), Decimal("50")) == Decimal("150")

    # Empty returns should yield None ratios
    assert sharpe_ratio([]) is None
    assert sortino_ratio([]) is None
    assert historical_var([], confidence=0.95) == Decimal(0)


def test_sortino_uses_downside_deviation():
    returns = [
        Decimal("0.03"),
        Decimal("-0.02"),
        Decimal("0.01"),
        Decimal("-0.01"),
    ]

    ratio = sortino_ratio(returns)
    assert ratio is not None
    assert float(ratio) == pytest.approx(0.2236067977, rel=1e-9)
