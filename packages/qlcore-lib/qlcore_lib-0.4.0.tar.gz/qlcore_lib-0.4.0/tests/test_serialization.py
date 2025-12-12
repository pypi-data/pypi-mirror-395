from decimal import Decimal
import json
import tempfile
import os

from qlcore.serialization.json_codec import (
    to_dict,
    from_dict,
    to_json,
    from_json,
    save_to_file,
    load_from_file,
)
from qlcore.positions.base import BasePositionImpl
from qlcore.portfolio import Portfolio
from qlcore.events.fill import Fill
from qlcore.core.enums import OrderSide


def test_serialize_deserialize_position():
    """Test position serialization round-trip."""
    pos = BasePositionImpl.flat("BTC-USD")
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
    )

    # Serialize
    data = to_dict(pos)
    assert data["instrument_id"] == "BTC-USD"
    assert data["side"] == "LONG"
    assert data["size"] == "1"

    # Deserialize
    restored = from_dict(data, BasePositionImpl)
    assert restored.instrument_id == pos.instrument_id
    assert restored.side == pos.side
    assert restored.size == pos.size
    assert restored.realized_pnl == pos.realized_pnl


def test_serialize_deserialize_portfolio():
    """Test portfolio serialization round-trip."""
    portfolio = Portfolio()
    portfolio.apply_fill(
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
    )
    portfolio.account.deposit("USD", Decimal("5000"))

    # Serialize
    data = to_dict(portfolio)
    assert "account" in data
    assert "positions" in data
    assert len(data["positions"]) == 1

    # Deserialize
    restored = from_dict(data, Portfolio)
    assert len(restored.positions) == 1

    # BUY 1 @ 10000 with fee 10 => -10010 cash
    # deposit 5000 => net -5010
    assert restored.account.balances["USD"] == Decimal("-5010")
    assert len(restored.ledger.entries) >= 2


def test_to_json_from_json():
    """Test JSON string conversion."""
    pos = BasePositionImpl.flat("BTC-USD")
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
    )

    # To JSON
    json_str = to_json(pos, indent=2)
    assert "BTC-USD" in json_str
    assert "LONG" in json_str

    # Parse JSON
    data = json.loads(json_str)
    assert data["instrument_id"] == "BTC-USD"

    # From JSON
    restored = from_json(json_str, BasePositionImpl)
    assert restored.instrument_id == pos.instrument_id
    assert restored.size == pos.size


def test_save_load_file():
    """Test file save/load."""
    pos = BasePositionImpl.flat("BTC-USD")
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "position.json")

        # Save
        save_to_file(pos, filepath)
        assert os.path.exists(filepath)

        # Load
        restored = load_from_file(filepath, BasePositionImpl)
        assert restored.instrument_id == pos.instrument_id
        assert restored.size == pos.size
