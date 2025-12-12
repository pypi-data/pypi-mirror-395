"""Validation helpers for fills and portfolio state."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from .core.exceptions import InvalidFillError, InconsistentPortfolioError
from .events.fill import Fill
from .portfolio.portfolio import Portfolio


def validate_fill_sequence(fills: Iterable[Fill]) -> None:
    """Validate a sequence of fills for basic sanity (ids, quantities, duplicates)."""
    seen_ids: set[str] = set()
    for fill in fills:
        if not fill.order_id:
            raise InvalidFillError("fill.order_id cannot be empty")
        if fill.order_id in seen_ids:
            raise InvalidFillError(f"duplicate fill order_id detected: {fill.order_id}")
        seen_ids.add(fill.order_id)

        if not fill.instrument_id:
            raise InvalidFillError("fill.instrument_id cannot be empty")
        if Decimal(fill.quantity) <= 0:
            raise InvalidFillError(f"fill.quantity must be > 0 for {fill.order_id}")
        if Decimal(fill.price) <= 0:
            raise InvalidFillError(f"fill.price must be > 0 for {fill.order_id}")


def validate_portfolio_state(
    portfolio: Portfolio, *, allow_negative_cash: bool = False
) -> None:
    """Validate basic portfolio/account invariants."""
    for currency, balance in portfolio.account.balances.items():
        if not allow_negative_cash and Decimal(balance) < 0:
            raise InconsistentPortfolioError(
                f"negative balance detected for {currency}: {balance}"
            )

    for (inst, side), position in portfolio.positions.items():
        if position.instrument_id != inst:
            raise InconsistentPortfolioError(
                f"position key mismatch: key {inst}, position {position.instrument_id}"
            )
        if position.side != side:
            raise InconsistentPortfolioError(
                f"position side mismatch: key {side}, position {position.side}"
            )
        if Decimal(position.size) < 0:
            raise InconsistentPortfolioError(
                f"position size must be non-negative for {inst}"
            )
