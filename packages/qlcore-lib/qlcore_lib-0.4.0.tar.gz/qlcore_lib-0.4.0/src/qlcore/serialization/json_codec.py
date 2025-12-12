from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict, is_dataclass, replace
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from ..core.enums import OrderSide, PositionSide
from ..core.exceptions import ValidationError
from ..core.types import Money, Price, Quantity, TimestampMs
from ..events.fill import Fill
from ..events.funding import FundingEvent
from ..events.fee import FeeEvent
from ..core.protocols import BasePosition
from ..portfolio.account import Account
from ..portfolio.ledger import Ledger, LedgerEntry
from ..portfolio.portfolio import Portfolio
from ..positions.base import BasePositionImpl
from ..positions.perpetual import PerpetualPosition
from ..positions.futures import FuturesPosition
from ..positions.cost_basis import CostBasisMethod, Lot
from ..utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimals and Money-like types."""

    def default(self, obj: Any) -> Any:  # type: ignore[override]
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, (Money, Price, Quantity)):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, int):  # covers TimestampMs
            return obj
        if isinstance(obj, (OrderSide, PositionSide)):
            return obj.value
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        return super().default(obj)


def _decode_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        return Decimal(value)
    raise TypeError(f"Cannot decode {value!r} as Decimal")


def _decode_money(value: Any) -> Money:
    return Money(_decode_decimal(value))


def _decode_price(value: Any) -> Price:
    return Price(_decode_decimal(value))


def _decode_quantity(value: Any) -> Quantity:
    return Quantity(_decode_decimal(value))


def _decode_timestamp_ms(value: Any) -> TimestampMs:
    if isinstance(value, (int, float, str)):
        return TimestampMs(int(value))
    raise TypeError(f"Cannot decode {value!r} as TimestampMs")


def encode_to_json(data: Any, *, pretty: bool = False) -> str:
    """Encode data to JSON using DecimalEncoder."""
    if pretty:
        return json.dumps(data, cls=DecimalEncoder, indent=2, sort_keys=True)
    return json.dumps(data, cls=DecimalEncoder)


def decode_from_json(data: Union[str, bytes]) -> Any:
    """Decode JSON string to Python object."""
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    return json.loads(data)


def _serialize_fill(fill: Fill) -> Dict[str, Any]:
    """Serialize Fill event to JSON-compatible dict."""
    return {
        "type": "fill",
        "order_id": fill.order_id,
        "instrument_id": fill.instrument_id,
        "side": fill.side.value,
        "quantity": str(fill.quantity),
        "price": str(fill.price),
        "fee": str(fill.fee),
        "timestamp_ms": int(fill.timestamp_ms),
    }


def _deserialize_fill(data: Dict[str, Any]) -> Fill:
    """Deserialize Fill event from dict."""
    return Fill(
        order_id=str(data["order_id"]),
        instrument_id=str(data["instrument_id"]),
        side=OrderSide(data["side"]),
        quantity=_decode_quantity(data["quantity"]),
        price=_decode_price(data["price"]),
        fee=_decode_money(data["fee"]),
        timestamp_ms=_decode_timestamp_ms(data["timestamp_ms"]),
    )


def _serialize_funding(event: FundingEvent) -> Dict[str, Any]:
    """Serialize FundingEvent to dict."""
    return {
        "type": "funding",
        "instrument_id": event.instrument_id,
        "rate": str(event.rate),
        "period_start_ms": int(event.period_start_ms),
        "period_end_ms": int(event.period_end_ms),
        "index_price": str(event.index_price),
    }


def _deserialize_funding(data: Dict[str, Any]) -> FundingEvent:
    """Deserialize FundingEvent from dict."""
    return FundingEvent(
        instrument_id=str(data["instrument_id"]),
        rate=_decode_decimal(data["rate"]),
        period_start_ms=_decode_timestamp_ms(data["period_start_ms"]),
        period_end_ms=_decode_timestamp_ms(data["period_end_ms"]),
        index_price=_decode_price(data["index_price"]),
    )


def _serialize_fee(event: FeeEvent) -> Dict[str, Any]:
    """Serialize FeeEvent to dict."""
    return {
        "type": "fee",
        "instrument_id": event.instrument_id,
        "amount": str(event.amount),
        "currency": event.currency,
        "timestamp_ms": int(event.timestamp_ms),
        "is_maker": event.is_maker,
        "note": event.note,
    }


def _deserialize_fee(data: Dict[str, Any]) -> FeeEvent:
    """Deserialize FeeEvent from dict."""
    return FeeEvent(
        instrument_id=data.get("instrument_id"),
        amount=_decode_money(data["amount"]),
        currency=str(data["currency"]),
        timestamp_ms=_decode_timestamp_ms(data["timestamp_ms"]),
        is_maker=data.get("is_maker"),
        note=data.get("note"),
    )


def _serialize_position(position: BasePositionImpl) -> Dict[str, Any]:
    """Serialize BasePositionImpl to dict with type information."""
    if not isinstance(position, BasePositionImpl):
        raise ValidationError("serialize_position expects BasePositionImpl")

    avg_price = position.avg_entry_price

    # Determine position type for deserialization
    pos_type = "base"
    if isinstance(position, PerpetualPosition):
        pos_type = "perpetual"
    elif isinstance(position, FuturesPosition):
        pos_type = "futures"

    result: Dict[str, Any] = {
        "type": pos_type,
        "instrument_id": position.instrument_id,
        "side": position.side.name,
        "size": str(position.size),
        "entry_value": str(position.entry_value),
        "avg_entry_price": str(avg_price) if avg_price is not None else None,
        "realized_pnl": str(position.realized_pnl),
        "unrealized_pnl": str(position.unrealized_pnl),
        "fees": str(position.fees),
        "last_update_ms": int(position.last_update_ms),
        "cost_basis_method": position.cost_basis_method.value,
        "lots": [
            {
                "size": str(lot.size),
                "price": str(lot.price),
                "fee": str(lot.fee),
                "timestamp_ms": int(lot.timestamp_ms),
            }
            for lot in position.lots
        ],
    }

    # Add subclass-specific fields
    if isinstance(position, PerpetualPosition):
        result["accumulated_funding"] = str(position.accumulated_funding)
        result["last_funding_timestamp_ms"] = int(position.last_funding_timestamp_ms)
    elif isinstance(position, FuturesPosition):
        result["expiry_ms"] = int(position.expiry_ms) if position.expiry_ms else None
        result["settlement_price"] = (
            str(position.settlement_price) if position.settlement_price else None
        )
        result["is_settled"] = position.is_settled

    return result


def _deserialize_position(data: Dict[str, Any]) -> BasePositionImpl:
    """Deserialize position from dict, returning the correct subclass.

    Ensures that reconstructed positions have consistent lots so closing
    trades and cost-basis operations keep working after a persistence
    round-trip. Supports PerpetualPosition and FuturesPosition subclasses.
    """
    side = PositionSide[data["side"]]
    size = _decode_quantity(data["size"])
    fees = _decode_money(data.get("fees", "0"))

    entry_value_raw = data.get("entry_value")
    entry_value = (
        _decode_money(entry_value_raw) if entry_value_raw is not None else Money(0)
    )

    avg_entry_price_raw = data.get("avg_entry_price")

    # If entry_value was not stored or is zero but we have an average price,
    # reconstruct entry_value from avg price, side, size and fees to keep
    # it consistent with _calculate_entry_value.
    if entry_value == 0 and avg_entry_price_raw is not None and size != 0:
        sign = Decimal(1) if side == PositionSide.LONG else Decimal(-1)
        entry_value = Money(
            sign * _decode_decimal(avg_entry_price_raw) * Decimal(size) + Decimal(fees)
        )

    cost_basis_method = CostBasisMethod(
        data.get("cost_basis_method", CostBasisMethod.FIFO.value)
    )
    last_update_ms = _decode_timestamp_ms(data.get("last_update_ms", 0))

    # Reconstruct lots.
    lots_field = data.get("lots")
    lots: List[Lot] = []

    if lots_field:
        # Newer payloads can include exact lot detail.
        for lot_data in lots_field:
            lots.append(
                Lot(
                    size=_decode_quantity(lot_data["size"]),
                    price=_decode_price(lot_data["price"]),
                    fee=_decode_money(lot_data["fee"]),
                    timestamp_ms=_decode_timestamp_ms(lot_data["timestamp_ms"]),
                )
            )
    elif size != 0:
        # Older payloads: reconstruct a single synthetic lot consistent with
        # the current position economics.
        if avg_entry_price_raw is not None:
            avg_price = _decode_decimal(avg_entry_price_raw)
        else:
            # Derive average price from entry_value and fees:
            # entry_value = sign * price * size + fees
            sign = Decimal(1) if side == PositionSide.LONG else Decimal(-1)
            qty_dec = Decimal(size)
            if qty_dec == 0:
                avg_price = Decimal(0)
            else:
                avg_price = (Decimal(entry_value) - Decimal(fees)) / (sign * qty_dec)

        lots.append(
            Lot(
                size=size,
                price=Price(avg_price),
                fee=fees,
                timestamp_ms=last_update_ms,
            )
        )

    # Create base position fields
    base_position = BasePositionImpl(
        instrument_id=str(data["instrument_id"]),
        side=side,
        size=size,
        entry_value=entry_value,
        realized_pnl=_decode_money(data.get("realized_pnl", "0")),
        fees=fees,
        lots=tuple(lots),
        cost_basis_method=cost_basis_method,
        unrealized_pnl=_decode_money(data.get("unrealized_pnl", "0")),
        last_update_ms=last_update_ms,
    )

    # Determine position type and create appropriate subclass
    pos_type = data.get("type", "base")

    if pos_type == "perpetual":
        return PerpetualPosition.from_base(
            base_position,
            accumulated_funding=_decode_money(data.get("accumulated_funding", "0")),
            last_funding_timestamp_ms=_decode_timestamp_ms(
                data.get("last_funding_timestamp_ms", 0)
            ),
        )
    elif pos_type == "futures":
        expiry_raw = data.get("expiry_ms")
        settlement_raw = data.get("settlement_price")
        fut = FuturesPosition.from_base(
            base_position,
            expiry_ms=TimestampMs(int(expiry_raw)) if expiry_raw else None,
        )
        return replace(
            fut,
            settlement_price=_decode_price(settlement_raw) if settlement_raw else None,
            is_settled=data.get("is_settled", False),
        )
    else:
        return base_position


def serialize_position(position: BasePositionImpl) -> Dict[str, Any]:
    """Public wrapper for serializing a position."""
    return _serialize_position(position)


def deserialize_position(data: Dict[str, Any]) -> BasePositionImpl:
    """Public wrapper for deserializing a position."""
    return _deserialize_position(data)


def _serialize_portfolio(portfolio: Portfolio) -> Dict[str, Any]:
    """Serialize Portfolio to dict including account, positions and ledger."""
    positions_by_instrument: Dict[str, List[Dict[str, Any]]] = {}
    for (instrument_id, _side), position in portfolio.positions.items():
        if not isinstance(position, BasePositionImpl):
            raise ValidationError("Unsupported position type for serialization")
        bucket = positions_by_instrument.setdefault(instrument_id, [])
        bucket.append(_serialize_position(position))

    account_data = {
        "base_currency": portfolio.account.base_currency,
        "balances": {k: str(v) for k, v in portfolio.account.balances.items()},
        "unrealized_pnl": str(portfolio.account.unrealized_pnl),
    }

    ledger_data = [
        {
            "description": entry.description,
            "amount": str(entry.amount),
            "currency": entry.currency,
            "timestamp_ms": int(entry.timestamp_ms),
            "instrument_id": entry.instrument_id,
            "meta": entry.meta,
        }
        for entry in portfolio.ledger.entries
    ]

    # If account balances don't reconcile with ledger cash flows (e.g. missing
    # deposit/withdrawal events), append synthetic adjustments so persisted
    # data remains self-consistent on reload.
    ledger_totals: Dict[str, Decimal] = {}
    for entry in portfolio.ledger.entries:
        ledger_totals[entry.currency] = ledger_totals.get(
            entry.currency, Decimal(0)
        ) + Decimal(entry.amount)

    for currency, balance in portfolio.account.balances.items():
        diff = Decimal(balance) - ledger_totals.get(currency, Decimal(0))
        if diff != 0:
            ledger_data.append(
                {
                    "description": "BALANCE_ADJUSTMENT",
                    "amount": str(diff),
                    "currency": currency,
                    "timestamp_ms": 0,
                    "instrument_id": None,
                    "meta": {"reason": "reconcile_account_balance"},
                }
            )

    return {
        "account": account_data,
        "positions": positions_by_instrument,
        "ledger": ledger_data,
    }


def _deserialize_portfolio(data: Dict[str, Any]) -> Portfolio:
    """Deserialize Portfolio from dict."""
    account_data = data["account"]
    balances = {
        code: _decode_money(val)
        for code, val in account_data.get("balances", {}).items()
    }
    account = Account(
        base_currency=str(account_data.get("base_currency", "USD")),
        balances=balances,
        unrealized_pnl=_decode_money(account_data.get("unrealized_pnl", "0")),
    )

    positions_dict: Dict[tuple[str, PositionSide], BasePosition] = {}
    for instrument_id, positions in data["positions"].items():
        for pos_data in positions:
            pos = _deserialize_position(pos_data)
            key = (instrument_id, pos.side)
            positions_dict[key] = pos

    ledger_entries = [
        LedgerEntry(
            description=str(entry["description"]),
            amount=_decode_money(entry["amount"]),
            currency=str(entry["currency"]),
            timestamp_ms=_decode_timestamp_ms(entry["timestamp_ms"]),
            instrument_id=entry.get("instrument_id"),
            meta=entry.get("meta", {}),
        )
        for entry in data.get("ledger", [])
    ]

    # Ensure ledger cash flows reconcile with account balances even if older
    # payloads omitted deposit/withdrawal entries.
    ledger_totals: Dict[str, Decimal] = {}
    for entry in ledger_entries:
        ledger_totals[entry.currency] = ledger_totals.get(
            entry.currency, Decimal(0)
        ) + Decimal(entry.amount)

    for currency, balance in account.balances.items():
        diff = Decimal(balance) - ledger_totals.get(currency, Decimal(0))
        if diff != 0:
            ledger_entries.append(
                LedgerEntry(
                    description="BALANCE_ADJUSTMENT",
                    amount=Money(diff),
                    currency=currency,
                    timestamp_ms=TimestampMs(0),
                    instrument_id=None,
                    meta={"reason": "reconcile_account_balance"},
                )
            )

    ledger = Ledger()
    ledger.entries.extend(ledger_entries)

    return Portfolio(account=account, positions=positions_dict, ledger=ledger)


def serialize_portfolio(portfolio: Portfolio) -> Dict[str, Any]:
    """Public wrapper for portfolio serialization."""
    return _serialize_portfolio(portfolio)


def deserialize_portfolio(data: Dict[str, Any]) -> Portfolio:
    """Public wrapper for portfolio deserialization."""
    return _deserialize_portfolio(data)


def _default_encoder(obj: Any) -> Any:
    """Fallback encoder for JSON; encodes Decimal as strings."""
    if isinstance(obj, Decimal):
        return str(obj)
    # Last resort: string representation to avoid TypeError in json.dumps
    return str(obj)


def to_dict(obj: Any) -> Dict[str, Any]:
    """Serialize object to a dictionary."""
    if isinstance(obj, BasePositionImpl):
        return _serialize_position(obj)
    if isinstance(obj, Portfolio):
        return _serialize_portfolio(obj)
    if isinstance(obj, Fill):
        return _serialize_fill(obj)
    if isinstance(obj, FundingEvent):
        return _serialize_funding(obj)
    if isinstance(obj, FeeEvent):
        return _serialize_fee(obj)

    if hasattr(obj, "as_dict"):
        return obj.as_dict()  # type: ignore

    # Check if dataclass
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)

    raise TypeError(f"Cannot serialize object of type {type(obj).__name__} to dict")


def from_dict(data: Dict[str, Any], cls: Type[T]) -> T:
    """Deserialize object from dictionary."""
    if cls is BasePositionImpl:
        return _deserialize_position(data)  # type: ignore
    if cls is Portfolio:
        return _deserialize_portfolio(data)  # type: ignore
    if cls is Fill:
        return _deserialize_fill(data)  # type: ignore
    if cls is FundingEvent:
        return _deserialize_funding(data)  # type: ignore
    if cls is FeeEvent:
        return _deserialize_fee(data)  # type: ignore

    # Generic dataclass or constructor
    return cls(**data)  # type: ignore


def to_json(obj: Any, indent: int | None = None) -> str:
    """
    Serialize a supported qlcore object (position/portfolio) to a JSON string.
    """
    try:
        payload = to_dict(obj)
    except TypeError:
        # Fallback for simple types or types handled directly by encoder
        payload = obj

    return json.dumps(payload, indent=indent, default=_default_encoder)


def from_json(raw: str, cls: Type[T]) -> T:
    """
    Deserialize a JSON string produced by to_json back into the requested type.
    """
    data = json.loads(raw)
    return from_dict(data, cls)


def save_to_file(obj: Any, path: str | Path, indent: int | None = 2) -> None:
    """
    Serialize object to JSON and write it to disk.
    """
    text = to_json(obj, indent=indent)
    Path(path).write_text(text, encoding="utf-8")


def load_from_file(path: str | Path, cls: Type[T]) -> T:
    """
    Load JSON from disk and deserialize into the requested type.
    """
    text = Path(path).read_text(encoding="utf-8")
    return from_json(text, cls)


def encode_domain_object(obj: Any) -> Dict[str, Any]:
    """Encode domain object to JSON-serializable dict."""
    if isinstance(obj, Fill):
        return {"event": "fill", "data": _serialize_fill(obj)}
    if isinstance(obj, FundingEvent):
        return {"event": "funding", "data": _serialize_funding(obj)}
    if isinstance(obj, FeeEvent):
        return {"event": "fee", "data": _serialize_fee(obj)}
    if isinstance(obj, Portfolio):
        return {"event": "portfolio", "data": _serialize_portfolio(obj)}
    if isinstance(obj, BasePositionImpl):
        return {"event": "position", "data": _serialize_position(obj)}

    raise TypeError(f"Unsupported object type for encoding: {type(obj)!r}")


def decode_domain_object(data: Dict[str, Any]) -> Any:
    """Decode domain object from JSON-serializable dict."""
    event_type = data.get("event")
    payload = data.get("data", {})

    if event_type == "fill":
        return _deserialize_fill(cast(Dict[str, Any], payload))
    if event_type == "funding":
        return _deserialize_funding(cast(Dict[str, Any], payload))
    if event_type == "fee":
        return _deserialize_fee(cast(Dict[str, Any], payload))
    if event_type == "portfolio":
        return _deserialize_portfolio(cast(Dict[str, Any], payload))
    if event_type == "position":
        return _deserialize_position(cast(Dict[str, Any], payload))

    raise TypeError(f"Unsupported event type for decoding: {event_type!r}")
def serialize_fill(fill: Fill) -> Dict[str, Any]:
    return _serialize_fill(fill)


def deserialize_fill(data: Dict[str, Any]) -> Fill:
    return _deserialize_fill(data)


def serialize_funding(event: FundingEvent) -> Dict[str, Any]:
    return _serialize_funding(event)


def deserialize_funding(data: Dict[str, Any]) -> FundingEvent:
    return _deserialize_funding(data)


def serialize_fee(event: FeeEvent) -> Dict[str, Any]:
    return _serialize_fee(event)


def deserialize_fee(data: Dict[str, Any]) -> FeeEvent:
    return _deserialize_fee(data)

