"""Convenience helpers for common workflows."""

from __future__ import annotations

from typing import Sequence

from .core.protocols import BasePosition
from .events.fill import Fill
from .portfolio.portfolio import Portfolio
from .validators import validate_fill_sequence, validate_portfolio_state


def apply_fills(position: BasePosition, fills: Sequence[Fill]) -> BasePosition:
    """Apply a sequence of fills to a position."""
    validate_fill_sequence(fills)
    updated = position
    for fill in fills:
        updated = updated.apply_fill(fill)
    return updated
