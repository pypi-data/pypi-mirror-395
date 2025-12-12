from decimal import Decimal

import pytest

from qlcore.core.types import TimestampMs
from qlcore.utils.validation import ensure_positive, ensure_non_negative


def test_validation_types():
    ensure_positive(Decimal("1"), "value")
    ensure_non_negative(Decimal("0"), "value")
    with pytest.raises(Exception):
        ensure_positive(Decimal("0"), "value")
    with pytest.raises(Exception):
        ensure_non_negative(Decimal("-1"), "value")

    ts = TimestampMs(123)
    assert int(ts) == 123
