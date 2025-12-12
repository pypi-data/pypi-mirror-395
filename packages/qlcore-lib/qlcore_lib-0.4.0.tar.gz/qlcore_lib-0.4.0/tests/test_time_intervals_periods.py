import pytest

from qlcore.time.intervals import to_milliseconds, floor_timestamp_ms
from qlcore.time.periods import TimePeriod


def test_intervals_known_and_unknown():
    assert to_milliseconds("1m") == 60_000
    assert floor_timestamp_ms(123456, "1m") == 120000

    with pytest.raises(ValueError):
        to_milliseconds("7m")


def test_time_period_validation_and_contains():
    with pytest.raises(ValueError):
        TimePeriod(start_ms=10, end_ms=5)

    period = TimePeriod(start_ms=0, end_ms=100)
    assert period.duration_ms == 100
    assert period.contains(50)
    assert not period.contains(101)
