"""Cost basis models (FIFO, LIFO, average)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Sequence, Tuple

from ..core.enums import PositionSide
from ..core.exceptions import ValidationError
from ..core.types import Money, Price, Quantity, TimestampMs


@dataclass(frozen=True)
class Lot:
    size: Quantity
    price: Price
    fee: Money
    timestamp_ms: TimestampMs


class CostBasisMethod(str, Enum):
    FIFO = "fifo"
    LIFO = "lifo"
    AVERAGE = "average"


def _validate_available(lots: Sequence[Lot], qty: Decimal) -> None:
    available = sum(Decimal(lot.size) for lot in lots)
    if qty > available:
        raise ValidationError("fill would reduce position below zero size")


def add_lot(
    lots: Tuple[Lot, ...], new_lot: Lot, method: CostBasisMethod
) -> Tuple[Lot, ...]:
    """Add a lot according to the cost basis method."""
    if method == CostBasisMethod.AVERAGE:
        total_size = sum(Decimal(lot.size) for lot in lots) + Decimal(new_lot.size)
        if total_size == 0:
            return ()
        total_price = sum(
            Decimal(lot.price) * Decimal(lot.size) for lot in lots
        ) + Decimal(new_lot.price) * Decimal(new_lot.size)
        total_fee = sum(Decimal(lot.fee) for lot in lots) + Decimal(new_lot.fee)
        avg_price = total_price / total_size
        fee_per_unit = total_fee / total_size
        return (
            Lot(
                size=total_size,
                price=avg_price,
                fee=fee_per_unit * total_size,
                timestamp_ms=new_lot.timestamp_ms,
            ),
        )
    if method == CostBasisMethod.FIFO:
        return lots + (new_lot,)
    if method == CostBasisMethod.LIFO:
        return lots + (new_lot,)
    raise ValidationError(f"unknown cost basis method {method}")


def match_lots(
    lots: Tuple[Lot, ...],
    qty: Decimal,
    exit_price: Decimal,
    side: PositionSide,
    method: CostBasisMethod,
) -> Tuple[Tuple[Lot, ...], Decimal]:
    """Match lots for an exit trade and return (remaining_lots, realized_pnl_delta).

    Realized PnL excludes fees; fees are tracked separately on the position.
    """
    qty = Decimal(qty)
    _validate_available(lots, qty)

    if method == CostBasisMethod.AVERAGE:
        if not lots:
            raise ValidationError("no lots to match")
        total_size = sum((Decimal(lot.size) for lot in lots), Decimal(0))
        if total_size == 0:
            raise ValidationError("no position size to match")
        total_price = sum(
            (Decimal(lot.price) * Decimal(lot.size) for lot in lots), Decimal(0)
        )
        total_fee = sum((Decimal(lot.fee) for lot in lots), Decimal(0))
        avg_price = total_price / total_size
        fee_per_unit = total_fee / total_size
        realized = _realized_piece(
            qty=qty,
            entry_price=avg_price,
            exit_price=Decimal(exit_price),
            side=side,
        )
        remaining_size = total_size - qty
        remaining_fee = fee_per_unit * remaining_size
        if remaining_size <= 0:
            return (), realized
        return (
            (
                Lot(
                    size=remaining_size,
                    price=avg_price,
                    fee=remaining_fee,
                    timestamp_ms=lots[0].timestamp_ms,
                ),
            ),
            realized,
        )

    work = list(lots)
    realized_total = Decimal(0)
    remaining_qty = qty
    remaining_lots: list[Lot] = []

    def pop_next() -> Lot:
        if method == CostBasisMethod.LIFO:
            return work.pop()
        return work.pop(0)

    while remaining_qty > 0:
        lot = pop_next()
        lot_size = Decimal(lot.size)
        use_qty = min(lot_size, remaining_qty)
        entry_fee_per_unit = (
            Decimal(0) if lot_size == 0 else Decimal(lot.fee) / lot_size
        )

        realized_total += _realized_piece(
            qty=use_qty,
            entry_price=Decimal(lot.price),
            exit_price=Decimal(exit_price),
            side=side,
        )

        remaining_in_lot = lot_size - use_qty
        if remaining_in_lot > 0:
            fee_remaining = entry_fee_per_unit * remaining_in_lot
            remaining_lots.append(
                Lot(
                    size=remaining_in_lot,
                    price=lot.price,
                    fee=fee_remaining,
                    timestamp_ms=lot.timestamp_ms,
                )
            )
        remaining_qty -= use_qty

    remaining_lots.extend(work)
    if method == CostBasisMethod.FIFO:
        remaining_lots.sort(key=lambda lot: lot.timestamp_ms)
    return tuple(remaining_lots), realized_total


def _realized_piece(
    *,
    qty: Decimal,
    entry_price: Decimal,
    exit_price: Decimal,
    side: PositionSide,
) -> Decimal:
    if side == PositionSide.LONG:
        return qty * (exit_price - entry_price)
    return qty * (entry_price - exit_price)
