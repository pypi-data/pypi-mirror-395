"""Futures instrument definitions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from .base import InstrumentSpec
from ..core.types import TimestampMs


@dataclass(frozen=True)
class FuturesInstrument(InstrumentSpec):
    expiry_ms: TimestampMs | None = None

    @staticmethod
    def create(
        symbol: str,
        base: str,
        quote: str,
        tick_size: Decimal,
        lot_size: Decimal,
        max_leverage: Decimal,
        expiry_ms: TimestampMs | None = None,
        contract_size: Decimal | None = None,
    ) -> "FuturesInstrument":
        return FuturesInstrument(
            instrument_id=symbol,
            base=base,
            quote=quote,
            tick_size=tick_size,
            lot_size=lot_size,
            max_leverage=max_leverage,
            contract_size=contract_size,
            expiry_ms=expiry_ms,
        )
