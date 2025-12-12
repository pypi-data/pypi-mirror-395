"""Cross margin helpers."""

from __future__ import annotations

from decimal import Decimal
from ..core.types import Money


def free_margin(equity: Money, maintenance_margin: Money) -> Money:
    """Return free margin available under cross margin."""
    return Decimal(equity) - Decimal(maintenance_margin)
