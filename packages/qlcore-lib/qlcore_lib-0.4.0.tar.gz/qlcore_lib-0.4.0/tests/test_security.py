import time
from decimal import Decimal
import pytest

from qlcore.security.audit import AuditTrail, AuditEventType
from qlcore.security.rate_limit import (
    RateLimiter,
    RateLimitExceeded,
    rate_limit,
    clear_rate_limiters,
)
from qlcore.security.sanitize import (
    sanitize_string_field,
    sanitize_numeric_field,
    sanitize_all_fields,
)


def test_audit_trail():
    """Test audit trail recording."""
    audit = AuditTrail()

    audit.record_fill(
        user_id="user1",
        order_id="o1",
        instrument_id="BTC-USD",
        side="BUY",
        quantity=Decimal("1"),
        price=Decimal("10000"),
        fee=Decimal("10"),
    )

    assert len(audit.events) == 1
    event = audit.events[0]
    assert event.event_type == AuditEventType.FILL
    assert event.user_id == "user1"

    # Get by user
    user_events = audit.get_events_by_user("user1")
    assert len(user_events) == 1

    # Get by instrument
    inst_events = audit.get_events_by_instrument("BTC-USD")
    assert len(inst_events) == 1


def test_rate_limiter():
    """Test rate limiting."""
    limiter = RateLimiter(max_calls=3, time_window=1.0, identifier="test")

    # First 3 calls should succeed
    limiter.acquire()
    limiter.acquire()
    limiter.acquire()

    # 4th call should fail
    with pytest.raises(RateLimitExceeded):
        limiter.acquire()

    # Wait for window to expire
    time.sleep(1.1)

    # Should work again
    limiter.acquire()


def test_rate_limit_decorator():
    """Test rate limit decorator."""
    clear_rate_limiters()
    call_count = [0]

    @rate_limit(max_calls=2, time_window=1.0, identifier="test_func")
    def test_func():
        call_count[0] += 1
        return call_count[0]

    # First 2 calls succeed
    assert test_func() == 1
    assert test_func() == 2

    # 3rd call fails
    with pytest.raises(RateLimitExceeded):
        test_func()


def test_sanitize_string_field():
    """Test string sanitization."""
    # Normal case
    assert sanitize_string_field("  test  ", "field") == "test"

    # Too long
    with pytest.raises(ValueError, match="too long"):
        sanitize_string_field("x" * 501, "field", max_length=500)

    # Null byte
    with pytest.raises(ValueError, match="null byte"):
        sanitize_string_field("test\x00", "field")


def test_sanitize_numeric_field():
    """Test numeric sanitization."""
    from decimal import Decimal

    # Normal cases
    assert sanitize_numeric_field(Decimal("100"), "field") == Decimal("100")
    assert sanitize_numeric_field(100, "field") == Decimal("100")
    assert sanitize_numeric_field("100.5", "field") == Decimal("100.5")

    # NaN
    with pytest.raises(ValueError, match="NaN"):
        sanitize_numeric_field(Decimal("NaN"), "field")

    # Infinity
    with pytest.raises(ValueError, match="infinite"):
        sanitize_numeric_field(Decimal("Infinity"), "field")


def test_sanitize_all_fields():
    """Test full dictionary sanitization."""
    unsafe = {
        "instrument_id": "  BTC-USD  ",
        "currency": "usd",
        "price": "10000",
        "note": "  Test note  ",
    }

    safe = sanitize_all_fields(unsafe)
    assert safe["instrument_id"] == "BTC-USD"
    assert safe["currency"] == "USD"
    assert safe["price"] == Decimal("10000")
    assert safe["note"] == "Test note"


def test_sanitize_all_fields_accepts_symbol_and_market():
    """Sanitization should normalize raw symbols into canonical instrument_id."""
    unsafe = {
        "symbol": "ethusdt_swap",
        "market": "perp",
        "price": "2000",
    }

    safe = sanitize_all_fields(unsafe)
    assert safe["instrument_id"] == "ETH-USDT-PERP"
    assert safe["price"] == Decimal("2000")
