"""Margin requirement calculations."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple

from ..core.types import Money, Rate, Price, Quantity
from ..utils.validation import ensure_non_negative


@dataclass(frozen=True)
class MarginRequirements:
    initial: Rate
    maintenance: Rate


@dataclass(frozen=True)
class MarginLevel:
    notional_threshold: Money
    initial: Rate
    maintenance: Rate


@dataclass(frozen=True)
class MarginSchedule:
    levels: Tuple[MarginLevel, ...]

    def for_notional(self, notional: Money) -> MarginRequirements:
        """Pick margin requirements for a given notional (highest threshold <= notional)."""
        if not self.levels:
            raise ValueError("MarginSchedule.levels must not be empty")

        notional_dec = abs(Decimal(notional))
        sorted_levels = sorted(
            self.levels, key=lambda level: Decimal(level.notional_threshold)
        )
        selected = sorted_levels[0]
        for level in sorted_levels:
            if notional_dec >= Decimal(level.notional_threshold):
                selected = level
        return MarginRequirements(
            initial=selected.initial,
            maintenance=selected.maintenance,
        )

    def for_size(self, size: Quantity, price: Price) -> MarginRequirements:
        """Pick margin requirements given position size and price."""
        notional = Money(abs(Decimal(size) * Decimal(price)))
        return self.for_notional(notional)

    def get_initial_margin_rate(
        self,
        *,
        notional: Money | None = None,
        size: Quantity | None = None,
        price: Price | None = None,
    ) -> Rate:
        """Convenience wrapper returning initial margin rate.

        Provide either:
          - notional, or
          - size and price (notional = |size * price|)
        """
        if notional is None:
            if size is None or price is None:
                raise ValueError("Provide either notional or (size and price)")
            notional = Money(abs(Decimal(size) * Decimal(price)))
        req = self.for_notional(notional)
        return Rate(req.initial)

    def get_maintenance_margin_rate(
        self,
        *,
        notional: Money | None = None,
        size: Quantity | None = None,
        price: Price | None = None,
    ) -> Rate:
        """Convenience wrapper returning maintenance margin rate.

        Provide either:
          - notional, or
          - size and price (notional = |size * price|)
        """
        if notional is None:
            if size is None or price is None:
                raise ValueError("Provide either notional or (size and price)")
            notional = Money(abs(Decimal(size) * Decimal(price)))
        req = self.for_notional(notional)
        return Rate(req.maintenance)


def initial_margin(notional: Money, req: MarginRequirements) -> Money:
    """Calculate initial margin required to open a position.

    Initial margin is the collateral required to open a leveraged position.
    For example, 10% initial margin means 10x leverage.

    Args:
        notional: Position notional value (size * price)
        req: Margin requirements with initial rate

    Returns:
        Required initial margin

    Example:
        >>> from decimal import Decimal
        >>> req = MarginRequirements(initial=Decimal("0.1"), maintenance=Decimal("0.05"))
        >>> margin = calculate_initial_margin(Decimal("10000"), req)
        >>> float(margin)  # 10% of $10,000
        1000.0
    """
    ensure_non_negative(notional, "notional")
    ensure_non_negative(req.initial, "initial margin rate")
    return abs(notional) * req.initial


def maintenance_margin(notional: Money, req: MarginRequirements) -> Money:
    """Calculate maintenance margin required to keep a position open.

    Maintenance margin is the minimum collateral to avoid liquidation.
    It's typically lower than initial margin.

    Args:
        notional: Position notional value (size * price)
        req: Margin requirements with maintenance rate

    Returns:
        Required maintenance margin

    Example:
        >>> from decimal import Decimal
        >>> req = MarginRequirements(initial=Decimal("0.1"), maintenance=Decimal("0.05"))
        >>> margin = calculate_maintenance_margin(Decimal("10000"), req)
        >>> float(margin)  # 5% of $10,000
        500.0
    """
    ensure_non_negative(notional, "notional")
    ensure_non_negative(req.maintenance, "maintenance margin rate")
    return abs(notional) * req.maintenance


def calculate_initial_margin(notional: Money, req: MarginRequirements) -> Money:
    """Backward-compatible alias for initial_margin()."""
    return initial_margin(notional, req)


def calculate_maintenance_margin(notional: Money, req: MarginRequirements) -> Money:
    """Backward-compatible alias for maintenance_margin()."""
    return maintenance_margin(notional, req)
