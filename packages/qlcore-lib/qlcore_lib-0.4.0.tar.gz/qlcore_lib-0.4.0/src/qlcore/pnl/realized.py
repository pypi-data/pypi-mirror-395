"""Realized PnL helpers."""

from __future__ import annotations

from ..core.protocols import BasePosition
from ..core.types import Money


def realized_pnl(position: BasePosition) -> Money:
    return position.realized_pnl
