"""Input sanitization helpers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Dict

from ..utils.validation import sanitize_instrument_id, sanitize_currency
from ..utils.symbols import normalize_symbol, infer_market_from_symbol


def sanitize_string_field(value: str, name: str, *, max_length: int = 255) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{name} cannot be empty")
    if "\x00" in cleaned:
        raise ValueError(f"{name} contains null byte")
    if len(cleaned) > max_length:
        raise ValueError(f"{name} too long")
    return cleaned


def sanitize_numeric_field(value: Any, name: str) -> Decimal:
    try:
        num = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc

    if num.is_nan():
        raise ValueError(f"{name} is NaN")
    if num.is_infinite():
        raise ValueError(f"{name} is infinite")
    return num


def sanitize_all_fields(
    data: Dict[str, Any], *, market: str | None = None
) -> Dict[str, Any]:
    """Sanitize a dict of user-provided fields."""
    cleaned: Dict[str, Any] = {}

    market_hint = market or data.get("market") or data.get("type")

    if "symbol" in data and data["symbol"] is not None:
        symbol_raw = str(data["symbol"])
        inferred_market = infer_market_from_symbol(symbol_raw)
        market_used = (market_hint or inferred_market or "spot").lower()
        cleaned["instrument_id"] = normalize_symbol(symbol_raw, market=market_used)
    elif "instrument_id" in data:
        cleaned["instrument_id"] = sanitize_instrument_id(str(data["instrument_id"]))
    if "currency" in data:
        cleaned["currency"] = sanitize_currency(str(data["currency"]))
    if "price" in data:
        cleaned["price"] = sanitize_numeric_field(data["price"], "price")
    if "note" in data and data["note"] is not None:
        cleaned["note"] = sanitize_string_field(
            str(data["note"]), "note", max_length=500
        )

    return cleaned
