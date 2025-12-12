"""Perpetual swap instrument definitions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from .base import InstrumentSpec


@dataclass(frozen=True)
class PerpetualInstrument(InstrumentSpec):
    funding_interval_ms: int = 8 * 60 * 60 * 1000  # default 8h

    @staticmethod
    def create(
        symbol: str,
        base: str,
        quote: str,
        tick_size: Decimal,
        lot_size: Decimal,
        max_leverage: Decimal,
        contract_size: Decimal | None = None,
        funding_interval_ms: int = 8 * 60 * 60 * 1000,
    ) -> "PerpetualInstrument":
        return PerpetualInstrument(
            instrument_id=symbol,
            base=base,
            quote=quote,
            tick_size=tick_size,
            lot_size=lot_size,
            max_leverage=max_leverage,
            contract_size=contract_size,
            funding_interval_ms=funding_interval_ms,
        )
