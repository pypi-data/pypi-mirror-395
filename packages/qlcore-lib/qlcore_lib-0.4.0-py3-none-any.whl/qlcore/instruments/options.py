"""Options instrument definitions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from .base import InstrumentSpec
from ..core.types import TimestampMs


class OptionType:
    CALL = "CALL"
    PUT = "PUT"


@dataclass(frozen=True, kw_only=True)
class OptionInstrument(InstrumentSpec):
    strike: Decimal
    expiry_ms: TimestampMs
    option_type: str

    @staticmethod
    def create(
        symbol: str,
        base: str,
        quote: str,
        strike: Decimal,
        expiry_ms: TimestampMs,
        option_type: str,
        tick_size: Decimal,
        lot_size: Decimal,
    ) -> "OptionInstrument":
        if option_type not in (OptionType.CALL, OptionType.PUT):
            raise ValueError("option_type must be CALL or PUT")
        return OptionInstrument(
            instrument_id=symbol,
            base=base,
            quote=quote,
            tick_size=tick_size,
            lot_size=lot_size,
            strike=strike,
            expiry_ms=expiry_ms,
            option_type=option_type,
            max_leverage=None,
            contract_size=None,
        )
