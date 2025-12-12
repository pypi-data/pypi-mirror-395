from datetime import datetime, timezone

from qlcore.time.timestamp import to_unix_ms, from_unix_ms
from qlcore.time.intervals import to_milliseconds, floor_timestamp_ms


def test_timestamp_roundtrip():
    now = datetime(2020, 1, 1, tzinfo=timezone.utc)
    ms = to_unix_ms(now)
    assert from_unix_ms(ms) == now


def test_intervals():
    assert to_milliseconds("1m") == 60000
    assert floor_timestamp_ms(123456, "1m") == 120000
