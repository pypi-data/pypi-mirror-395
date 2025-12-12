"""Spot instrument helpers."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from .base import InstrumentSpec


@dataclass(frozen=True)
class SpotInstrument(InstrumentSpec):
    """Spot instruments trade the base against the quote."""

    @staticmethod
    def create(
        symbol: str, base: str, quote: str, tick_size: Decimal, lot_size: Decimal
    ) -> "SpotInstrument":
        return SpotInstrument(
            instrument_id=symbol,
            base=base,
            quote=quote,
            tick_size=tick_size,
            lot_size=lot_size,
            max_leverage=None,
            contract_size=None,
        )
