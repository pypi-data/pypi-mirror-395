"""Builder pattern for complex qlcore objects.

Usage:
    from qlcore.builders import PositionBuilder, FillBuilder
    
    position = (
        PositionBuilder("BTC-PERP")
        .long()
        .with_size("1.5")
        .with_entry_price("10000")
        .build()
    )
    
    fill = (
        FillBuilder()
        .order("o1")
        .instrument("BTC-USD")
        .buy("1")
        .at_price("10000")
        .build()
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .core.enums import OrderSide, PositionSide
from .core.types import Money, Price, Quantity, TimestampMs
from .positions.base import BasePositionImpl
from .positions.perpetual import PerpetualPosition
from .positions.futures import FuturesPosition
from .positions.cost_basis import CostBasisMethod, Lot
from .events.fill import Fill


class PositionBuilder:
    """Fluent builder for creating positions.

    Example:
        >>> pos = (
        ...     PositionBuilder("BTC-PERP")
        ...     .long()
        ...     .with_size("2.5")
        ...     .with_entry_price("10000")
        ...     .as_perpetual()
        ...     .build()
        ... )
    """

    def __init__(self, instrument_id: str):
        self._instrument_id = instrument_id
        self._side: PositionSide = PositionSide.LONG
        self._size: Decimal = Decimal(0)
        self._entry_price: Decimal = Decimal(0)
        self._realized_pnl: Decimal = Decimal(0)
        self._unrealized_pnl: Decimal = Decimal(0)
        self._fees: Decimal = Decimal(0)
        self._cost_basis: CostBasisMethod = CostBasisMethod.FIFO
        self._position_type: str = "base"
        self._expiry_ms: Optional[int] = None
        self._accumulated_funding: Decimal = Decimal(0)

    def long(self) -> "PositionBuilder":
        """Set position side to LONG."""
        self._side = PositionSide.LONG
        return self

    def short(self) -> "PositionBuilder":
        """Set position side to SHORT."""
        self._side = PositionSide.SHORT
        return self

    def with_side(self, side: PositionSide | str) -> "PositionBuilder":
        """Set position side."""
        if isinstance(side, str):
            side = PositionSide[side.upper()]
        self._side = side
        return self

    def with_size(self, size: Decimal | str | float) -> "PositionBuilder":
        """Set position size."""
        self._size = Decimal(str(size))
        return self

    def with_entry_price(self, price: Decimal | str | float) -> "PositionBuilder":
        """Set average entry price."""
        self._entry_price = Decimal(str(price))
        return self

    def with_realized_pnl(self, pnl: Decimal | str | float) -> "PositionBuilder":
        """Set realized P&L."""
        self._realized_pnl = Decimal(str(pnl))
        return self

    def with_unrealized_pnl(self, pnl: Decimal | str | float) -> "PositionBuilder":
        """Set unrealized P&L."""
        self._unrealized_pnl = Decimal(str(pnl))
        return self

    def with_fees(self, fees: Decimal | str | float) -> "PositionBuilder":
        """Set accumulated fees."""
        self._fees = Decimal(str(fees))
        return self

    def with_cost_basis(self, method: CostBasisMethod | str) -> "PositionBuilder":
        """Set cost basis method."""
        if isinstance(method, str):
            method = CostBasisMethod(method)
        self._cost_basis = method
        return self

    def as_perpetual(self) -> "PositionBuilder":
        """Build as PerpetualPosition."""
        self._position_type = "perpetual"
        return self

    def as_futures(self, expiry_ms: int | None = None) -> "PositionBuilder":
        """Build as FuturesPosition."""
        self._position_type = "futures"
        self._expiry_ms = expiry_ms
        return self

    def with_accumulated_funding(
        self, funding: Decimal | str | float
    ) -> "PositionBuilder":
        """Set accumulated funding (for perpetuals)."""
        self._accumulated_funding = Decimal(str(funding))
        return self

    def build(self) -> BasePositionImpl:
        """Build the position."""
        # Calculate entry value
        sign = Decimal(1) if self._side == PositionSide.LONG else Decimal(-1)
        entry_value = sign * self._entry_price * self._size + self._fees

        # Create a single lot if we have size
        lots: tuple[Lot, ...] = tuple()
        if self._size > 0:
            lot = Lot(
                size=self._size,
                price=Price(self._entry_price),
                fee=Money(self._fees),
                timestamp_ms=TimestampMs(0),
            )
            lots = (lot,)

        base_position = BasePositionImpl(
            instrument_id=self._instrument_id,
            side=self._side,
            size=Quantity(self._size),
            entry_value=Money(entry_value),
            realized_pnl=Money(self._realized_pnl),
            fees=Money(self._fees),
            lots=lots,
            cost_basis_method=self._cost_basis,
            unrealized_pnl=Money(self._unrealized_pnl),
            last_update_ms=TimestampMs(0),
        )

        if self._position_type == "perpetual":
            return PerpetualPosition.from_base(
                base_position,
                accumulated_funding=Money(self._accumulated_funding),
                last_funding_timestamp_ms=TimestampMs(0),
            )
        if self._position_type == "futures":
            expiry = TimestampMs(self._expiry_ms) if self._expiry_ms else None
            return FuturesPosition.from_base(base_position, expiry_ms=expiry)
        return base_position


class FillBuilder:
    """Fluent builder for creating fills.

    Example:
        >>> fill = (
        ...     FillBuilder()
        ...     .order("order-123")
        ...     .instrument("BTC-PERP")
        ...     .buy("1.5")
        ...     .at_price("10000")
        ...     .with_fee("10")
        ...     .at_time(1234567890000)
        ...     .build()
        ... )
    """

    def __init__(self):
        self._order_id: str = ""
        self._instrument_id: str = ""
        self._side: OrderSide = OrderSide.BUY
        self._quantity: Decimal = Decimal(0)
        self._price: Decimal = Decimal(0)
        self._fee: Decimal = Decimal(0)
        self._timestamp_ms: int = 0

    def order(self, order_id: str) -> "FillBuilder":
        """Set order ID."""
        self._order_id = order_id
        return self

    def instrument(self, instrument_id: str) -> "FillBuilder":
        """Set instrument ID."""
        self._instrument_id = instrument_id
        return self

    def buy(self, quantity: Decimal | str | float) -> "FillBuilder":
        """Set as buy with quantity."""
        self._side = OrderSide.BUY
        self._quantity = Decimal(str(quantity))
        return self

    def sell(self, quantity: Decimal | str | float) -> "FillBuilder":
        """Set as sell with quantity."""
        self._side = OrderSide.SELL
        self._quantity = Decimal(str(quantity))
        return self

    def with_side(self, side: OrderSide | str) -> "FillBuilder":
        """Set side."""
        if isinstance(side, str):
            side = OrderSide[side.upper()]
        self._side = side
        return self

    def with_quantity(self, quantity: Decimal | str | float) -> "FillBuilder":
        """Set quantity."""
        self._quantity = Decimal(str(quantity))
        return self

    def at_price(self, price: Decimal | str | float) -> "FillBuilder":
        """Set fill price."""
        self._price = Decimal(str(price))
        return self

    def with_fee(self, fee: Decimal | str | float) -> "FillBuilder":
        """Set fee."""
        self._fee = Decimal(str(fee))
        return self

    def at_time(self, timestamp_ms: int) -> "FillBuilder":
        """Set timestamp."""
        self._timestamp_ms = timestamp_ms
        return self

    def build(self) -> Fill:
        """Build the fill."""
        return Fill(
            order_id=self._order_id,
            instrument_id=self._instrument_id,
            side=self._side,
            quantity=Quantity(self._quantity),
            price=Price(self._price),
            fee=Money(self._fee),
            timestamp_ms=TimestampMs(self._timestamp_ms),
        )
