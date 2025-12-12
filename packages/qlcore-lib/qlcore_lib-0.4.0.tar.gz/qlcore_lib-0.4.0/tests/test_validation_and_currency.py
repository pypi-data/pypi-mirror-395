from decimal import Decimal

import pytest

from qlcore.utils.validation import ensure_positive, ensure_non_negative
from qlcore.utils.currency import convert


def test_validation_helpers():
    with pytest.raises(Exception):
        ensure_positive(Decimal("0"), "value")
    with pytest.raises(Exception):
        ensure_non_negative(Decimal("-1"), "value")
    ensure_positive(Decimal("1"), "value")
    ensure_non_negative(Decimal("0"), "value")


def test_currency_convert():
    assert convert(Decimal("10"), Decimal("1.5")) == Decimal("15")
