"""Isolated margin bookkeeping helpers."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from ..core.types import Money


@dataclass
class IsolatedMargin:
    wallet: Money
    requirement: Money

    @property
    def free(self) -> Money:
        return Decimal(self.wallet) - Decimal(self.requirement)
