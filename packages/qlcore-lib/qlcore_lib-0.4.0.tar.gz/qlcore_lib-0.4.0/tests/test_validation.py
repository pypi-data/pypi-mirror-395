from decimal import Decimal
import pytest

from qlcore.utils.validation import (
    ensure_valid_decimal,
    ensure_valid_rate,
    ensure_valid_price,
    ensure_valid_quantity,
    ensure_valid_timestamp_order,
    sanitize_instrument_id,
    sanitize_currency,
    ensure_valid_leverage,
)
from qlcore.core.exceptions import ValidationError


def test_ensure_valid_decimal_nan():
    """Test rejection of NaN values."""
    with pytest.raises(ValidationError, match="NaN"):
        ensure_valid_decimal(Decimal("NaN"), "test_value")


def test_ensure_valid_decimal_infinity():
    """Test rejection of infinite values."""
    with pytest.raises(ValidationError, match="infinite"):
        ensure_valid_decimal(Decimal("Infinity"), "test_value")


def test_ensure_valid_decimal_bounds():
    """Test min/max bounds checking."""
    ensure_valid_decimal(
        Decimal("5"), "test", min_val=Decimal("0"), max_val=Decimal("10")
    )

    with pytest.raises(ValidationError, match="must be >= 0"):
        ensure_valid_decimal(Decimal("-1"), "test", min_val=Decimal("0"))

    with pytest.raises(ValidationError, match="must be <= 10"):
        ensure_valid_decimal(Decimal("11"), "test", max_val=Decimal("10"))


def test_ensure_valid_rate():
    """Test rate validation."""
    ensure_valid_rate(Decimal("0.001"), "fee_rate")
    ensure_valid_rate(Decimal("-0.001"), "funding_rate", allow_negative=True)

    with pytest.raises(ValidationError):
        ensure_valid_rate(Decimal("15"), "invalid_rate")


def test_ensure_valid_price():
    """Test price validation."""
    ensure_valid_price(Decimal("100"), "price")

    with pytest.raises(ValidationError, match="must be positive"):
        ensure_valid_price(Decimal("0"), "price")

    with pytest.raises(ValidationError):
        ensure_valid_price(Decimal("-10"), "price")


def test_ensure_valid_quantity():
    """Test quantity validation."""
    ensure_valid_quantity(Decimal("1"), "qty")
    ensure_valid_quantity(Decimal("0"), "qty", allow_zero=True)

    with pytest.raises(ValidationError, match="must be positive"):
        ensure_valid_quantity(Decimal("0"), "qty", allow_zero=False)


def test_ensure_valid_timestamp_order():
    """Test timestamp ordering."""
    ensure_valid_timestamp_order(0, 1000)

    with pytest.raises(ValidationError, match="must be >="):
        ensure_valid_timestamp_order(1000, 500)


def test_sanitize_instrument_id():
    """Test instrument ID sanitization."""
    assert sanitize_instrument_id("BTC-USD") == "BTC-USD"
    assert sanitize_instrument_id("  BTC-USD  ") == "BTC-USD"

    with pytest.raises(ValidationError, match="empty"):
        sanitize_instrument_id("")

    with pytest.raises(ValidationError, match="forbidden"):
        sanitize_instrument_id("BTC;DROP TABLE")

    with pytest.raises(ValidationError, match="too long"):
        sanitize_instrument_id("X" * 101)


def test_sanitize_currency():
    """Test currency sanitization."""
    assert sanitize_currency("usd") == "USD"
    assert sanitize_currency("  eur  ") == "EUR"

    with pytest.raises(ValidationError, match="empty"):
        sanitize_currency("")

    with pytest.raises(ValidationError, match="2-10 characters"):
        sanitize_currency("X")


def test_ensure_valid_leverage():
    """Test leverage validation."""
    ensure_valid_leverage(Decimal("10"), "leverage")

    with pytest.raises(ValidationError):
        ensure_valid_leverage(Decimal("0.5"), "leverage")

    with pytest.raises(ValidationError):
        ensure_valid_leverage(Decimal("5000"), "leverage")
