from dataclasses import dataclass
from decimal import Decimal

import pytest

from qlcore.utils.serialization import to_dict, from_dict
from qlcore.utils.validation import (
    sanitize_instrument_id,
    sanitize_currency,
    ensure_valid_money,
    validate_tick_size,
    validate_lot_size,
)
from qlcore.core.exceptions import ValidationError


@dataclass
class Dummy:
    a: int
    b: str


def test_to_dict_requires_dataclass():
    dummy = Dummy(1, "x")
    assert to_dict(dummy) == {"a": 1, "b": "x"}
    with pytest.raises(TypeError):
        to_dict({"a": 1})


def test_from_dict_roundtrip():
    dummy = Dummy(1, "x")
    restored = from_dict(Dummy, {"a": 1, "b": "x"})
    assert restored == dummy


def test_validation_money_and_sanitizers():
    with pytest.raises(ValidationError):
        ensure_valid_money(Decimal("-1"), "amount")
    assert ensure_valid_money(Decimal("0"), "amount", allow_negative=True) == Decimal(
        "0"
    )

    assert sanitize_currency(" usd ") == "USD"
    assert sanitize_instrument_id("  eth-usd ") == "eth-usd"

    with pytest.raises(ValidationError):
        validate_tick_size(Decimal("10.05"), Decimal("0.1"))
    with pytest.raises(ValidationError):
        validate_lot_size(Decimal("1.01"), Decimal("0.1"))
