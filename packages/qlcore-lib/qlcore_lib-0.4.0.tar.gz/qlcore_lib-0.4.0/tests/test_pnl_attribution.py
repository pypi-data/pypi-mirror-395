from decimal import Decimal

from qlcore.pnl.attribution import total_by_instrument, component_by_instrument
from qlcore.pnl.calculator import PnLBreakdown


def test_pnl_attribution_totals_and_components():
    breakdowns = {
        "BTC-USD:LONG": PnLBreakdown(
            realized=Decimal("10"),
            unrealized=Decimal("5"),
            fees=Decimal("1"),
            funding=Decimal("-1"),
            trading=Decimal("15"),
            slippage=Decimal("0"),
            total=Decimal("13"),
        ),
        "ETH-USD:SHORT": PnLBreakdown(
            realized=Decimal("0"),
            unrealized=Decimal("2"),
            fees=Decimal("0.5"),
            funding=Decimal("0"),
            trading=Decimal("2"),
            slippage=Decimal("0"),
            total=Decimal("1.5"),
        ),
    }
    totals = total_by_instrument(breakdowns)
    assert totals["BTC-USD:LONG"] == Decimal("13")
    comps = component_by_instrument(breakdowns, "unrealized")
    assert comps["ETH-USD:SHORT"] == Decimal("2")
