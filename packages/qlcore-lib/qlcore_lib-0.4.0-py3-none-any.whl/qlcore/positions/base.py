from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Any, Mapping, Sequence, Tuple

from ..core.enums import OrderSide, PositionSide
from ..core.exceptions import ValidationError
from ..core.types import Money, Price, Quantity, TimestampMs
from ..core.protocols import BasePosition as BasePositionProtocol
from ..events.fill import Fill
from ..events.funding import FundingEvent
from .cost_basis import CostBasisMethod, Lot, add_lot, match_lots
from ..utils.validation import ensure_non_negative


@dataclass(frozen=True)
class BasePositionImpl(BasePositionProtocol):
    """Minimal concrete base implementation for reuse.

    Thread Safety:
        Immutable and fully thread-safe. All operations return new instances.

    Performance:
        - FIFO/LIFO matching: O(n) where n = number of lots
        - Average cost: O(1)
        - Consider using AVERAGE method if accumulating 100+ lots
    """

    instrument_id: str
    side: PositionSide
    size: Quantity
    entry_value: Money
    realized_pnl: Money
    fees: Money
    lots: Tuple[Lot, ...] = ()
    cost_basis_method: CostBasisMethod = CostBasisMethod.FIFO
    unrealized_pnl: Money = Decimal(0)
    last_update_ms: TimestampMs = TimestampMs(0)

    @staticmethod
    def flat(instrument_id: str) -> "BasePositionImpl":
        """Create an empty position."""
        zero = Decimal(0)
        return BasePositionImpl(
            instrument_id=instrument_id,
            side=PositionSide.LONG,
            size=zero,
            entry_value=zero,
            realized_pnl=zero,
            fees=zero,
            lots=(),
            cost_basis_method=CostBasisMethod.FIFO,
            unrealized_pnl=zero,
            last_update_ms=TimestampMs(0),
        )

    def apply_fill(self, fill: "Fill") -> "BasePositionImpl":
        """Apply a fill event and return updated position.

        Args:
            fill: Fill event to apply

        Returns:
            New position instance with fill applied

        Raises:
            ValidationError: If fill quantity is invalid or would create invalid state

        Examples:
            >>> pos = BasePositionImpl.flat("BTC-USD")
            >>> fill = Fill("o1", "BTC-USD", OrderSide.BUY, Decimal("1"), Decimal("100"), Decimal("1"), 0)
            >>> pos = pos.apply_fill(fill)
            >>> pos.size
            Decimal('1')
        """
        if fill.quantity <= 0:
            raise ValidationError(
                f"Fill quantity must be positive, got {fill.quantity} for order {fill.order_id}"
            )

        # Opening a new position from flat derives side from the fill.
        if self.size == 0:
            side = (
                PositionSide.LONG if fill.side == OrderSide.BUY else PositionSide.SHORT
            )
            lot = Lot(
                size=fill.quantity,
                price=fill.price,
                fee=fill.fee,
                timestamp_ms=fill.timestamp_ms,
            )
            entry_value = _calculate_entry_value((lot,), side)
            return replace(
                self,
                side=side,
                size=fill.quantity,
                entry_value=entry_value,
                realized_pnl=self.realized_pnl,
                fees=self.fees + fill.fee,
                lots=(lot,),
                cost_basis_method=self.cost_basis_method,
                unrealized_pnl=self.unrealized_pnl,
                last_update_ms=TimestampMs(fill.timestamp_ms),
            )

        same_direction = (
            self.side == PositionSide.LONG and fill.side == OrderSide.BUY
        ) or (self.side == PositionSide.SHORT and fill.side == OrderSide.SELL)

        if same_direction:
            lot = Lot(
                size=fill.quantity,
                price=fill.price,
                fee=fill.fee,
                timestamp_ms=fill.timestamp_ms,
            )
            new_lots = add_lot(self.lots, lot, self.cost_basis_method)
            new_size = self.size + fill.quantity
            entry_value = _calculate_entry_value(new_lots, self.side)
            return replace(
                self,
                size=new_size,
                entry_value=entry_value,
                realized_pnl=self.realized_pnl,
                fees=self.fees + fill.fee,
                lots=new_lots,
                cost_basis_method=self.cost_basis_method,
                unrealized_pnl=self.unrealized_pnl,
                last_update_ms=TimestampMs(fill.timestamp_ms),
            )

        # Closing or reducing position
        if fill.quantity > self.size:
            # Close entire position and open opposite side
            close_qty = self.size
            flip_qty = fill.quantity - self.size
            _close_fee, open_fee = _split_fill_fee(fill.fee, close_qty, flip_qty)

            # Close existing position
            updated_lots, realized_delta = match_lots(
                lots=self.lots,
                qty=close_qty,
                exit_price=Decimal(fill.price),
                side=self.side,
                method=self.cost_basis_method,
            )

            # Open new opposite position with remaining quantity
            new_side = (
                PositionSide.SHORT
                if self.side == PositionSide.LONG
                else PositionSide.LONG
            )
            new_lot = Lot(
                size=flip_qty,
                price=fill.price,
                fee=open_fee,
                timestamp_ms=fill.timestamp_ms,
            )
            new_entry_value = _calculate_entry_value((new_lot,), new_side)

            return replace(
                self,
                side=new_side,
                size=flip_qty,
                entry_value=new_entry_value,
                realized_pnl=self.realized_pnl + realized_delta,
                fees=self.fees + fill.fee,
                lots=(new_lot,),
                cost_basis_method=self.cost_basis_method,
                unrealized_pnl=self.unrealized_pnl,
                last_update_ms=TimestampMs(fill.timestamp_ms),
            )

        # Partial close
        updated_lots, realized_delta = match_lots(
            lots=self.lots,
            qty=fill.quantity,
            exit_price=Decimal(fill.price),
            side=self.side,
            method=self.cost_basis_method,
        )

        new_size = self.size - fill.quantity
        if new_size == 0:
            updated_lots = ()
            entry_value = Decimal(0)
        else:
            entry_value = _calculate_entry_value(tuple(updated_lots), self.side)

        return replace(
            self,
            size=new_size,
            entry_value=entry_value,
            realized_pnl=self.realized_pnl + realized_delta,
            fees=self.fees + fill.fee,
            lots=tuple(updated_lots),
            cost_basis_method=self.cost_basis_method,
            unrealized_pnl=self.unrealized_pnl,
            last_update_ms=TimestampMs(fill.timestamp_ms),
        )

    def apply_funding(
        self, event: "FundingEvent", fills: Sequence["Fill"] | None = None
    ) -> "BasePositionImpl":
        """Apply funding event and return updated position.

        Args:
            event: Funding event to apply
            fills: Optional fills during funding period for time segmentation

        Returns:
            New position with funding payment added to realized PnL

        Note:
            Negative payment = cost paid by position holder
            Positive payment = payment received by position holder
        """
        from ..pnl.funding import (
            calculate_funding_payment,
        )  # lazy import to avoid cycles

        funding_pnl = calculate_funding_payment(
            position=self,
            event=event,
            fills=fills or (),
            fills_applied=True,
        )
        return replace(
            self,
            realized_pnl=self.realized_pnl + funding_pnl,
            fees=self.fees,
            unrealized_pnl=self.unrealized_pnl,
            last_update_ms=TimestampMs(event.period_end_ms),
        )

    @property
    def avg_entry_price(self) -> Price | None:
        """Weighted average entry price across all lots."""
        if self.size == 0:
            return None
        price_component = sum(lot.price * lot.size for lot in self.lots)
        return price_component / self.size

    @property
    def notional(self) -> Money:
        """Position notional value (size * avg_entry_price)."""
        if self.size == 0:
            return Decimal(0)
        return self.size * (self.avg_entry_price or Decimal(0))

    def evolve(self, **kwargs: Any) -> "BasePositionImpl":
        """Return a copy with specified fields updated.

        This uses dataclasses.replace() internally, which preserves the
        actual class type. So PerpetualPosition.evolve() returns PerpetualPosition.

        Example:
            >>> pos = pos.evolve(unrealized_pnl=Decimal("100"))
            >>> pos = pos.evolve(size=Decimal("2"), fees=Decimal("5"))
        """
        return replace(self, **kwargs)

    def summary(self) -> str:
        """Return a human-readable summary for REPL use."""
        avg = self.avg_entry_price
        avg_str = f"{avg:.4f}" if avg is not None else "N/A"
        lines = [
            f"{self.__class__.__name__}({self.instrument_id})",
            f"  Side: {self.side.name:<5} | Size: {self.size}",
            f"  Avg Entry: {avg_str}",
            f"  Unrealized P&L: {self.unrealized_pnl}",
            f"  Realized P&L: {self.realized_pnl}",
            f"  Fees: {self.fees}",
        ]
        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BasePositionImpl":
        """Construct from a dictionary.

        Handles common serialization formats. For full round-trip with
        type preservation, use deserialize_position from serialization module.

        Example:
            >>> pos = BasePositionImpl.from_dict({
            ...     "instrument_id": "BTC-USD",
            ...     "side": "LONG",
            ...     "size": "1.5",
            ...     "entry_value": "15000",
            ... })
        """
        side = data.get("side", "LONG")
        if isinstance(side, str):
            side = PositionSide[side.upper()]
        elif isinstance(side, int):
            side = PositionSide(side)

        cost_basis = data.get("cost_basis_method", CostBasisMethod.FIFO.value)
        if isinstance(cost_basis, str):
            cost_basis = CostBasisMethod(cost_basis)
        elif isinstance(cost_basis, int):
            cost_basis = CostBasisMethod(cost_basis)

        return cls(
            instrument_id=str(data["instrument_id"]),
            side=side,
            size=Quantity(Decimal(str(data.get("size", 0)))),
            entry_value=Money(Decimal(str(data.get("entry_value", 0)))),
            realized_pnl=Money(Decimal(str(data.get("realized_pnl", 0)))),
            fees=Money(Decimal(str(data.get("fees", 0)))),
            lots=tuple(
                Lot(
                    size=Quantity(Decimal(str(lot.get("size", 0)))),
                    price=Price(Decimal(str(lot.get("price", 0)))),
                    fee=Money(Decimal(str(lot.get("fee", 0)))),
                    timestamp_ms=TimestampMs(int(lot.get("timestamp_ms", 0))),
                )
                for lot in data.get("lots", [])
            ),
            cost_basis_method=cost_basis,
            unrealized_pnl=Money(Decimal(str(data.get("unrealized_pnl", 0)))),
            last_update_ms=TimestampMs(int(data.get("last_update_ms", 0))),
        )


def _calculate_entry_value(lots: Tuple[Lot, ...], side: PositionSide) -> Money:
    """Calculate signed entry value including fees.

    Args:
        lots: Position lots
        side: Position side (LONG or SHORT)

    Returns:
        Entry value with sign based on position side
    """
    sign = Decimal(1) if side == PositionSide.LONG else Decimal(-1)
    price_component = sum(lot.price * lot.size for lot in lots)
    fee_component = sum(lot.fee for lot in lots)
    return sign * price_component + fee_component


def _split_fill_fee(
    total_fee: Money, close_qty: Quantity, open_qty: Quantity
) -> tuple[Money, Money]:
    """Allocate a single fill fee between closing and opening legs when flipping.

    Args:
        total_fee: Total fee paid on the fill
        close_qty: Quantity used to close existing position
        open_qty: Quantity used to open new opposite position

    Returns:
        Tuple of (close_fee, open_fee)

    Raises:
        ValidationError: If quantities are negative
    """
    # Validate inputs
    ensure_non_negative(total_fee, "total_fee")
    ensure_non_negative(close_qty, "close_qty")
    ensure_non_negative(open_qty, "open_qty")

    total_qty = Decimal(close_qty) + Decimal(open_qty)
    if total_qty == 0:
        return Decimal(0), Decimal(0)

    close_fee = (
        Decimal(total_fee) * (Decimal(close_qty) / total_qty)
        if close_qty
        else Decimal(0)
    )
    open_fee = Decimal(total_fee) - close_fee
    return close_fee, open_fee
