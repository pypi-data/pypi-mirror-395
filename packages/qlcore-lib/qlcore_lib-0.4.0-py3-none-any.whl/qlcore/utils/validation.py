from __future__ import annotations

import re
from decimal import Decimal
from typing import Optional

from ..core.exceptions import ValidationError


def ensure_positive(value, name: str) -> None:
    """Raise ValidationError if value is not positive."""
    try:
        if value <= 0:
            raise ValidationError(f"{name} must be positive")
    except TypeError as exc:
        raise ValidationError(f"{name} must be comparable to zero") from exc


def ensure_non_negative(value, name: str) -> None:
    """Raise ValidationError if value is negative."""
    try:
        if value < 0:
            raise ValidationError(f"{name} must be non-negative")
    except TypeError as exc:
        raise ValidationError(f"{name} must be comparable to zero") from exc


def ensure_valid_decimal(
    value: Decimal,
    name: str,
    *,
    min_val: Optional[Decimal] = None,
    max_val: Optional[Decimal] = None,
) -> Decimal:
    """Validate a Decimal for NaN/inf and optional bounds."""
    if not isinstance(value, Decimal):
        raise ValidationError(f"{name} must be a Decimal")

    if value.is_nan():
        raise ValidationError(f"{name} cannot be NaN")
    if value.is_infinite():
        raise ValidationError(f"{name} cannot be infinite")

    if min_val is not None and value < min_val:
        raise ValidationError(f"{name} must be >= {min_val}")
    if max_val is not None and value > max_val:
        raise ValidationError(f"{name} must be <= {max_val}")

    return value


def ensure_valid_rate(
    rate: Decimal,
    name: str,
    *,
    allow_negative: bool = False,
    max_abs: Decimal = Decimal("1"),
) -> Decimal:
    """Validate a rate/percentage value."""
    rate = ensure_valid_decimal(rate, name)

    if not allow_negative and rate < 0:
        raise ValidationError(f"{name} must be non-negative")
    if rate.copy_abs() > max_abs:
        raise ValidationError(f"{name} magnitude too large: {rate} (max {max_abs})")

    return rate


def ensure_valid_price(price: Decimal, name: str) -> Decimal:
    """Validate a price (must be strictly positive)."""
    price = ensure_valid_decimal(price, name)
    if price <= 0:
        raise ValidationError(f"{name} must be positive")
    return price


def ensure_valid_quantity(
    quantity: Decimal, name: str, *, allow_zero: bool = False
) -> Decimal:
    """Validate a quantity value."""
    quantity = ensure_valid_decimal(quantity, name)
    if allow_zero:
        if quantity < 0:
            raise ValidationError(f"{name} must be non-negative")
    else:
        if quantity <= 0:
            raise ValidationError(f"{name} must be positive")
    return quantity


def ensure_valid_money(
    amount: Decimal,
    name: str,
    *,
    allow_negative: bool = False,
) -> Decimal:
    """Validate a money amount."""
    amount = ensure_valid_decimal(amount, name)
    if not allow_negative and amount < 0:
        raise ValidationError(f"{name} must be non-negative")
    return amount


def ensure_valid_timestamp(timestamp_ms: int, name: str = "timestamp") -> int:
    """Validate a millisecond timestamp."""
    if not isinstance(timestamp_ms, int):
        raise ValidationError(f"{name} must be an integer milliseconds value")
    if timestamp_ms < 0:
        raise ValidationError(f"{name} must be >= 0")
    return timestamp_ms


def ensure_valid_timestamp_order(
    start_ms: int, end_ms: int, *, start_name: str = "start", end_name: str = "end"
) -> None:
    """Ensure timestamps are non-negative and ordered."""
    ensure_valid_timestamp(start_ms, start_name)
    ensure_valid_timestamp(end_ms, end_name)
    if end_ms < start_ms:
        raise ValidationError(f"{end_name} must be >= {start_name}")


def sanitize_instrument_id(instrument_id: str) -> str:
    """Normalize and validate an instrument identifier.

    FIXED: Enhanced validation to reject malformed IDs.
    """
    cleaned = instrument_id.strip()
    if not cleaned:
        raise ValidationError("instrument_id cannot be empty")
    if len(cleaned) > 100:
        raise ValidationError("instrument_id too long")

    if cleaned.startswith(".") or cleaned.endswith("."):
        raise ValidationError("instrument_id cannot start or end with '.'")
    if cleaned.startswith("-") or cleaned.endswith("-"):
        raise ValidationError("instrument_id cannot start or end with '-'")

    if not re.fullmatch(r"[A-Za-z0-9_.:/\\-]+", cleaned):
        raise ValidationError("instrument_id contains forbidden characters")

    if "-" not in cleaned:
        raise ValidationError(
            "instrument_id should contain '-' separator (expected format: BASE-QUOTE)"
        )

    return cleaned


def sanitize_currency(currency: str) -> str:
    """Normalize and validate a currency code."""
    cleaned = currency.strip().upper()
    if not cleaned:
        raise ValidationError("currency cannot be empty")
    if len(cleaned) < 2 or len(cleaned) > 10:
        raise ValidationError("currency must be 2-10 characters")
    if not re.fullmatch(r"[A-Z0-9]+", cleaned):
        raise ValidationError("currency contains forbidden characters")
    return cleaned


def ensure_valid_percentage(value: Decimal, name: str) -> Decimal:
    """Validate a percentage in the range [0, 100]."""
    return ensure_valid_decimal(
        value, name, min_val=Decimal("0"), max_val=Decimal("100")
    )


def ensure_valid_leverage(
    leverage: Decimal,
    name: str,
    *,
    min_leverage: Decimal = Decimal("1"),
    max_leverage: Decimal = Decimal("1000"),
) -> Decimal:
    """Validate a leverage value."""
    leverage = ensure_valid_decimal(leverage, name)
    if leverage < min_leverage:
        raise ValidationError(f"{name} must be >= {min_leverage}")
    if leverage > max_leverage:
        raise ValidationError(f"{name} must be <= {max_leverage}")
    return leverage


def validate_tick_size(price: Decimal, tick_size: Decimal) -> None:
    """Ensure a price aligns with the provided tick size."""
    price = ensure_valid_price(price, "price")
    tick_size = ensure_valid_price(tick_size, "tick_size")
    if tick_size == 0:
        raise ValidationError("tick_size must be positive")
    if (price % tick_size) != 0:
        raise ValidationError("price not aligned to tick_size")


def validate_lot_size(quantity: Decimal, lot_size: Decimal) -> None:
    """Ensure a quantity aligns with a lot size increment."""
    quantity = ensure_valid_quantity(quantity, "quantity", allow_zero=True)
    lot_size = ensure_valid_price(lot_size, "lot_size")
    if lot_size == 0:
        raise ValidationError("lot_size must be positive")
    if quantity % lot_size != 0:
        raise ValidationError("quantity not aligned to lot_size")
