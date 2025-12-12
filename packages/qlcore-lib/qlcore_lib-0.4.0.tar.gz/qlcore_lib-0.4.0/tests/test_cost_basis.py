from decimal import Decimal

from qlcore.core.enums import PositionSide
from qlcore.positions.cost_basis import (
    CostBasisMethod,
    Lot,
    add_lot,
    match_lots,
)


def test_fifo_realized_pnl():
    lots = (
        Lot(size=Decimal("1"), price=Decimal("100"), fee=Decimal("1"), timestamp_ms=0),
        Lot(size=Decimal("1"), price=Decimal("110"), fee=Decimal("1"), timestamp_ms=1),
    )
    remaining, realized = match_lots(
        lots=lots,
        qty=Decimal("1.5"),
        exit_price=Decimal("120"),
        side=PositionSide.LONG,
        method=CostBasisMethod.FIFO,
    )
    assert realized.quantize(Decimal("0.0001")) == Decimal("25.0000")
    assert remaining[0].size == Decimal("0.5")
    assert remaining[0].price == Decimal("110")


def test_average_cost_basis():
    lots: tuple[Lot, ...] = ()
    lots = add_lot(
        lots,
        Lot(size=Decimal("1"), price=Decimal("100"), fee=Decimal("1"), timestamp_ms=0),
        CostBasisMethod.AVERAGE,
    )
    lots = add_lot(
        lots,
        Lot(size=Decimal("1"), price=Decimal("110"), fee=Decimal("1"), timestamp_ms=1),
        CostBasisMethod.AVERAGE,
    )
    # Average price = 105, average fee per unit = 1
    remaining, realized = match_lots(
        lots=lots,
        qty=Decimal("1"),
        exit_price=Decimal("120"),
        side=PositionSide.LONG,
        method=CostBasisMethod.AVERAGE,
    )
    assert realized == Decimal("15")
    assert remaining[0].size == Decimal("1")
    assert remaining[0].price == Decimal("105")


def test_lifo_matches_latest_lot_first():
    lots = (
        Lot(size=Decimal("1"), price=Decimal("100"), fee=Decimal("1"), timestamp_ms=0),
        Lot(size=Decimal("1"), price=Decimal("110"), fee=Decimal("1"), timestamp_ms=1),
    )
    remaining, realized = match_lots(
        lots=lots,
        qty=Decimal("1.5"),
        exit_price=Decimal("120"),
        side=PositionSide.LONG,
        method=CostBasisMethod.LIFO,
    )
    # LIFO uses the newest lot (110) first, then half of the older lot (100)
    assert realized == Decimal("20")
    assert remaining[0].size == Decimal("0.5")
    assert remaining[0].price == Decimal("100")


def test_short_fifo_realized_no_fee():
    lots = (
        Lot(size=Decimal("2"), price=Decimal("100"), fee=Decimal("0"), timestamp_ms=0),
    )
    remaining, realized = match_lots(
        lots=lots,
        qty=Decimal("1"),
        exit_price=Decimal("90"),
        side=PositionSide.SHORT,
        method=CostBasisMethod.FIFO,
    )
    assert realized == Decimal("10")
    assert remaining[0].size == Decimal("1")
    assert remaining[0].price == Decimal("100")


def test_lifo_short_consumes_latest():
    lots = (
        Lot(size=Decimal("1"), price=Decimal("100"), fee=Decimal("0"), timestamp_ms=0),
        Lot(size=Decimal("1"), price=Decimal("110"), fee=Decimal("0"), timestamp_ms=1),
    )
    remaining, realized = match_lots(
        lots=lots,
        qty=Decimal("1.5"),
        exit_price=Decimal("95"),
        side=PositionSide.SHORT,
        method=CostBasisMethod.LIFO,
    )
    assert realized == Decimal("17.5")
    assert remaining[0].size == Decimal("0.5")
    assert remaining[0].price == Decimal("100")
