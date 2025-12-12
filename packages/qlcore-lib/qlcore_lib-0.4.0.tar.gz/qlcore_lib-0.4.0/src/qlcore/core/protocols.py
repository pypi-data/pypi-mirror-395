"""Protocol definitions for key domain objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence, TYPE_CHECKING
from .types import Money, Price, Quantity
from .enums import PositionSide

if TYPE_CHECKING:
    from ..events.fill import Fill
    from ..events.funding import FundingEvent


class Instrument(Protocol):
    instrument_id: str


@dataclass(frozen=True)
class BasePosition(Protocol):
    """Base position protocol used by pnl and portfolio."""

    instrument_id: str
    side: PositionSide
    size: Quantity
    entry_value: Money
    realized_pnl: Money
    fees: Money

    def apply_fill(self, fill: "Fill") -> "BasePosition": ...

    def apply_funding(
        self, event: "FundingEvent", fills: Sequence["Fill"] | None = None
    ) -> "BasePosition": ...

    @property
    def avg_entry_price(self) -> Price | None: ...

    @property
    def notional(self) -> Money: ...
