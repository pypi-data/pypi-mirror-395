"""Fee event structure."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..core.types import Money, TimestampMs
from ..core.exceptions import ValidationError
from ..utils.validation import (
    ensure_valid_money,
    ensure_valid_timestamp,
    sanitize_currency,
    sanitize_instrument_id,
)


@dataclass(frozen=True)
class FeeEvent:
    """Explicit fee charged to an account.

    amount:
        Positive fee size (e.g. Decimal("1.5") for a 1.5 USDT fee).
        From the account's point of view this is a cash outflow.

    signed_amount:
        Signed representation from the account's perspective
        (negative = cash paid out).
    """

    instrument_id: str | None
    amount: Money
    currency: str
    timestamp_ms: TimestampMs
    is_maker: bool | None = None
    note: str | None = None

    @property
    def signed_amount(self) -> Money:
        """Return fee as a signed cash-flow (negative = outflow)."""
        # FIXED: Fees are always cash outflows, so negate the amount
        return Money(-Decimal(self.amount))

    def __post_init__(self) -> None:
        if self.instrument_id is not None:
            instrument_id = sanitize_instrument_id(self.instrument_id)
            object.__setattr__(self, "instrument_id", instrument_id)

        # FIXED: Allow negative amounts for rebates, but validate as money
        amount = ensure_valid_money(self.amount, "amount", allow_negative=True)
        object.__setattr__(self, "amount", amount)

        currency = sanitize_currency(self.currency)
        object.__setattr__(self, "currency", currency)

        ensure_valid_timestamp(self.timestamp_ms, "timestamp_ms")

        if self.note is not None and len(self.note) > 500:
            raise ValidationError("note too long")
