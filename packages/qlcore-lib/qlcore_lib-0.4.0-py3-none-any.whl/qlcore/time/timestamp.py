"""Timestamp conversion helpers."""

from datetime import datetime, timezone
from ..core.types import TimestampMs


def to_unix_ms(dt: datetime) -> TimestampMs:
    """Convert a datetime into a Unix timestamp in milliseconds."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return TimestampMs(int(dt.timestamp() * 1000))


def from_unix_ms(ms: TimestampMs) -> datetime:
    """Create a UTC datetime from a Unix timestamp in milliseconds."""
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
