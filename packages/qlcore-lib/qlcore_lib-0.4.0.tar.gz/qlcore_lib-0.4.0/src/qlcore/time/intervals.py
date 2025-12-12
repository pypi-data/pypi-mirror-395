"""Common trading interval helpers."""

from __future__ import annotations

INTERVAL_MS = {
    "1m": 60_000,
    "5m": 300_000,
    "15m": 900_000,
    "1h": 3_600_000,
    "4h": 14_400_000,
    "1d": 86_400_000,
}


def to_milliseconds(interval: str) -> int:
    """Return the interval length in milliseconds."""
    try:
        return INTERVAL_MS[interval]
    except KeyError as exc:
        raise ValueError(f"unknown interval: {interval}") from exc


def floor_timestamp_ms(timestamp_ms: int, interval: str) -> int:
    """Floor a timestamp to the start of the given interval."""
    step = to_milliseconds(interval)
    return (timestamp_ms // step) * step
