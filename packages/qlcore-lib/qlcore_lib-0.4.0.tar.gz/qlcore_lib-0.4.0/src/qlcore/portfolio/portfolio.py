from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Tuple, Sequence
import threading

from ..core.constants import DEFAULT_BASE_CURRENCY
from ..core.enums import OrderSide, PositionSide
from ..core.exceptions import ValidationError
from ..core.protocols import BasePosition
from ..core.types import Money, TimestampMs
from ..events.fill import Fill
from ..events.funding import FundingEvent
from ..events.fee import FeeEvent
from ..positions.base import BasePositionImpl
from ..positions.cost_basis import CostBasisMethod
from ..utils.logging import get_logger, get_audit_logger
from ..utils.symbols import normalize_symbol, infer_market_from_symbol
from ..utils.validation import sanitize_instrument_id
from .account import Account, _EquityView
from .ledger import Ledger, LedgerEntry

PositionKey = Tuple[str, PositionSide]

logger = get_logger(__name__)
audit_logger = get_audit_logger()


def _instrument_currency(instrument_id: str) -> str:
    """Extract the quote currency portion of an instrument identifier."""
    cleaned = sanitize_instrument_id(instrument_id)
    market = infer_market_from_symbol(cleaned) or "spot"
    try:
        normalized = normalize_symbol(cleaned, market=market)
    except ValidationError:
        normalized = cleaned

    parts = normalized.split("-")
    if len(parts) < 2:
        raise ValidationError(
            f"Invalid instrument_id format: {instrument_id}. Expected at least BASE-QUOTE"
        )

    # Spot, futures, options and explicit perp symbols encode the quote as the
    # second component (BASE-QUOTE-...?).
    if len(parts) >= 3:
        # Handle canonical forms like BTC-USDT-PERP or BTC-USD-20241227.
        return parts[1]

    quote_candidate = parts[1]
    if quote_candidate.upper() in {"PERP", "SWAP"}:
        # Legacy shorthand without explicit quote - fall back to account base.
        return DEFAULT_BASE_CURRENCY

    return quote_candidate


def _cash_flow_from_fill(fill: Fill) -> tuple[Money, str]:
    """Cash flow from the perspective of the cash account.

    Positive value = cash received, negative = cash spent.
    Includes trading fee.

    For a BUY:
        cash_flow = -(price * qty + fee)
    For a SELL:
        cash_flow = +(price * qty - fee)
    """
    notional = Decimal(fill.price) * Decimal(fill.quantity)
    currency = _instrument_currency(fill.instrument_id)
    if fill.side == OrderSide.BUY:
        return Money(-(notional + Decimal(fill.fee))), currency
    return Money(notional - Decimal(fill.fee)), currency


@dataclass
class Portfolio:
    """Single-currency portfolio with positions and a cash account.

    Thread Safety:
        Uses internal lock for thread-safe operations.
        Methods that modify state are protected.
        The _assert_locked helper can be enabled in development to
        catch missing lock usage.
    """

    account: Account = field(
        default_factory=lambda: Account(base_currency=DEFAULT_BASE_CURRENCY)
    )
    positions: Dict[PositionKey, BasePosition] = field(default_factory=dict)
    ledger: Ledger = field(default_factory=Ledger)
    _lock: threading.RLock = field(
        default_factory=threading.RLock, init=False, repr=False
    )

    @property
    def base_currency(self) -> str:
        return self.account.base_currency

    @property
    def equity(self) -> "_EquityView":
        # Note: this is a read without the portfolio lock. For strict
        # consistency in multi-threaded environments, prefer taking a
        # snapshot under self._lock.
        return self.account.equity

    def summary(self) -> str:
        """Return a human-readable portfolio summary for REPL use."""
        lines = [
            f"Portfolio ({self.base_currency})",
            f"  Equity: {self.account.equity}",
            f"  Cash: {self.account.balances}",
            f"  Unrealized P&L: {self.account.unrealized_pnl}",
            f"  Positions: {len(self.positions)}",
        ]
        for (instrument_id, side), pos in self.positions.items():
            size_str = str(pos.size)
            lines.append(f"    {instrument_id} {side.name}: {size_str}")
        return "\n".join(lines)

    def _assert_locked(self) -> None:
        """Assert that the current thread holds the portfolio lock.

        This is intended for debugging and should only be called from
        code paths that are documented as "must hold _lock".

        It relies on the private RLock._is_owned() when available and
        falls back to a no-op if not supported by the runtime.
        """
        lock = self._lock
        owned = False

        # CPython's RLock exposes _is_owned() from 3.13 onwards; older
        # versions may also have it but it's not part of the public API.
        is_owned = getattr(lock, "_is_owned", None)
        if callable(is_owned):
            try:
                owned = bool(is_owned())
            except Exception:
                owned = False

        if not owned:
            raise RuntimeError(
                "Internal error: method that requires portfolio lock was called "
                "without the lock being held. This is a bug in the caller."
            )

    def _find_position_key(self, instrument_id: str) -> PositionKey | None:
        """Return the key for the active position in an instrument, if any.

        Must be called with lock held when used from mutating methods.
        """
        for (inst, side), position in self.positions.items():
            if inst == instrument_id and position.size != 0:
                return (inst, side)
        return None

    def _get_position(self, instrument_id: str) -> BasePositionImpl:
        """Get current position for instrument, creating a flat one if needed.

        Must be called with lock held when used from mutating methods.
        """
        key = self._find_position_key(instrument_id)
        if key is not None:
            position = self.positions[key]
            if isinstance(position, BasePositionImpl):
                return position
            # Adapt any BasePosition implementation into BasePositionImpl via snapshot
            return BasePositionImpl(
                instrument_id=position.instrument_id,
                side=position.side,
                size=position.size,
                entry_value=position.entry_value,
                realized_pnl=position.realized_pnl,
                fees=position.fees,
                lots=getattr(position, "lots", ()),
                cost_basis_method=getattr(
                    position, "cost_basis_method", CostBasisMethod.FIFO
                ),
                unrealized_pnl=getattr(position, "unrealized_pnl", Decimal(0)),
                last_update_ms=TimestampMs(
                    getattr(position, "last_update_ms", TimestampMs(0))
                ),
            )

        return BasePositionImpl.flat(instrument_id)

    def apply_fill(self, fill: Fill, *, user_id: str | None = None) -> None:
        """Apply a trade fill to positions, account, and ledger.

        Thread-safe operation.
        """
        with self._lock:
            logger.info(
                "Applying fill",
                instrument_id=fill.instrument_id,
                side=fill.side.name,
                quantity=str(fill.quantity),
                price=str(fill.price),
                fee=str(fill.fee),
            )

            # Update position
            current = self._get_position(fill.instrument_id)
            updated = current.apply_fill(fill)

            # Remove old key (if any) and store updated under its new side
            old_key = self._find_position_key(fill.instrument_id)
            if old_key is not None and old_key in self.positions:
                del self.positions[old_key]

            if updated.size != 0:
                new_key: PositionKey = (fill.instrument_id, updated.side)
                self.positions[new_key] = updated

            # Cash movement - FIXED: Better error handling for invalid instruments
            try:
                cash_flow, currency = _cash_flow_from_fill(fill)
            except ValidationError as e:
                logger.error(f"Invalid instrument format in fill: {e}")
                raise

            self.account.apply_cash_flow(cash_flow, currency=currency)

            # Ledger entry
            self.ledger.record(
                LedgerEntry(
                    description="FILL",
                    amount=cash_flow,
                    currency=currency,
                    timestamp_ms=fill.timestamp_ms,
                    instrument_id=fill.instrument_id,
                    meta={
                        "order_id": fill.order_id,
                        "side": fill.side.name,
                        "price": str(fill.price),
                        "quantity": str(fill.quantity),
                        "fee": str(fill.fee),
                    },
                )
            )

            audit_logger.info(
                "FILL",
                instrument_id=fill.instrument_id,
                side=fill.side.name,
                quantity=str(fill.quantity),
                price=str(fill.price),
                fee=str(fill.fee),
                order_id=fill.order_id,
                timestamp_ms=int(fill.timestamp_ms),
                user_id=user_id or "system",
            )

    def apply_fill_batch(
        self, fills: Sequence[Fill], *, timed_metric: str | None = None
    ) -> None:
        """Apply a sequence of fills. Optionally time the batch via metrics."""
        if timed_metric:
            from ..monitoring.metrics import timed_operation

            with timed_operation(timed_metric):
                for fill in fills:
                    self.apply_fill(fill)
            return

        for fill in fills:
            self.apply_fill(fill)

    def apply_funding(
        self, event: FundingEvent, fills: Sequence[Fill] | None = None
    ) -> None:
        """Apply a funding payment to the account and ledger.

        Calculates funding payment based on position and event, then applies it.

        Thread-safe operation.
        """
        with self._lock:
            from ..pnl.funding import (
                calculate_funding_payment,
            )

            position = self._get_position(event.instrument_id)
            if position.size == 0:
                return  # No funding for flat position

            amount = calculate_funding_payment(
                position=position,
                event=event,
                fills=fills,
                fills_applied=True,
            )

            updated_position = position.apply_funding(event, fills=fills or ())
            key = self._find_position_key(event.instrument_id)
            if key is not None:
                self.positions[key] = updated_position
            else:
                self.positions[(event.instrument_id, updated_position.side)] = (
                    updated_position
                )

            logger.info(
                "Applying funding",
                instrument_id=event.instrument_id,
                rate=str(event.rate),
                index_price=str(event.index_price),
                amount=str(amount),
            )

            # FIXED: Better error handling for invalid instruments
            try:
                currency = _instrument_currency(event.instrument_id)
            except ValidationError as e:
                logger.error(f"Invalid instrument format in funding event: {e}")
                raise

            self.account.apply_cash_flow(amount, currency=currency)

            self.ledger.record(
                LedgerEntry(
                    description="FUNDING",
                    amount=amount,
                    currency=currency,
                    timestamp_ms=event.period_end_ms,
                    instrument_id=event.instrument_id,
                    meta={
                        "rate": str(event.rate),
                        "index_price": str(event.index_price),
                        "period_start_ms": int(event.period_start_ms),
                        "period_end_ms": int(event.period_end_ms),
                    },
                )
            )

            audit_logger.info(
                "FUNDING",
                instrument_id=event.instrument_id,
                rate=str(event.rate),
                index_price=str(event.index_price),
                amount=str(amount),
                timestamp_ms=int(event.period_end_ms),
            )

    def apply_fee(self, event: FeeEvent) -> None:
        """Apply an explicit fee event to the account and ledger.

        event.amount:
            Positive fee size (e.g. 1.5 USDT means a 1.5-unit fee).
        Account cash-flow:
            Uses event.signed_amount (negative) so fees reduce balance.

        Thread-safe operation.
        """
        with self._lock:
            logger.info(
                "Applying fee",
                instrument_id=event.instrument_id,
                amount=str(event.amount),
                currency=event.currency,
            )

            # Cash movement: fees reduce the account balance.
            cash_flow = event.signed_amount
            self.account.apply_cash_flow(cash_flow, currency=event.currency)

            self.ledger.record(
                LedgerEntry(
                    description="FEE",
                    amount=cash_flow,
                    currency=event.currency,
                    timestamp_ms=event.timestamp_ms,
                    instrument_id=event.instrument_id,
                    meta={
                        "is_maker": event.is_maker,
                        "note": event.note,
                    },
                )
            )

            audit_logger.info(
                "FEE",
                instrument_id=event.instrument_id,
                amount=str(event.amount),
                currency=event.currency,
                timestamp_ms=int(event.timestamp_ms),
            )
