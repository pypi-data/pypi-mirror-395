from decimal import Decimal

from qlcore.instruments import (
    SpotInstrument,
    PerpetualInstrument,
    FuturesInstrument,
    OptionInstrument,
    OptionType,
    InstrumentRegistry,
)


def test_instrument_construction_and_registry():
    spot = SpotInstrument.create(
        "BTC-USD", "BTC", "USD", Decimal("0.01"), Decimal("0.0001")
    )
    perp = PerpetualInstrument.create(
        "BTC-PERP", "BTC", "USD", Decimal("0.1"), Decimal("0.001"), Decimal("20")
    )
    fut = FuturesInstrument.create(
        "BTC-FUT",
        "BTC",
        "USD",
        Decimal("0.5"),
        Decimal("0.01"),
        Decimal("10"),
        expiry_ms=123,
    )
    opt = OptionInstrument.create(
        "BTC-OPT",
        "BTC",
        "USD",
        strike=Decimal("20000"),
        expiry_ms=456,
        option_type=OptionType.CALL,
        tick_size=Decimal("0.1"),
        lot_size=Decimal("0.01"),
    )

    reg = InstrumentRegistry()
    for inst in (spot, perp, fut, opt):
        reg.add(inst)
        assert reg.get(inst.instrument_id) == inst
        # test rounding helpers
        reg.get(inst.instrument_id).round_price(Decimal("1.234"))
