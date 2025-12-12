"""Base instrument and specifications."""

from dataclasses import dataclass
from decimal import Decimal
from ..math.rounding import round_price_to_tick, round_qty_to_lot


@dataclass(frozen=True)
class InstrumentSpec:
    instrument_id: str
    base: str
    quote: str
    tick_size: Decimal
    lot_size: Decimal
    max_leverage: Decimal | None = None
    contract_size: Decimal | None = None

    def round_price(self, price: Decimal) -> Decimal:
        return round_price_to_tick(price, self.tick_size)

    def round_qty(self, qty: Decimal) -> Decimal:
        return round_qty_to_lot(qty, self.lot_size)
