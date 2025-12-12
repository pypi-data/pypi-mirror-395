import pytest

from qlcore.core.exceptions import ValidationError
from qlcore.utils import normalize_symbol
from qlcore.events.fill import Fill


def test_normalize_symbol_spot():
    assert normalize_symbol("BTC/USDT", market="spot") == "BTC-USDT"
    assert normalize_symbol("ethusdt", market="spot") == "ETH-USDT"
    assert normalize_symbol("BTC-USDT", market="spot") == "BTC-USDT"


def test_normalize_symbol_perp():
    assert normalize_symbol("BTCUSDT", market="perp") == "BTC-USDT-PERP"
    assert normalize_symbol("BTC/USDT:USDT", market="perp") == "BTC-USDT-PERP"
    assert normalize_symbol("ethusdt_swap", market="perp") == "ETH-USDT-PERP"


def test_normalize_symbol_future():
    assert normalize_symbol("BTCUSDT_250328", market="future") == "BTC-USDT-20250328"
    assert normalize_symbol("BTC-USD-250628", market="future") == "BTC-USD-20250628"
    assert normalize_symbol("BTCUSDT-20250328", market="future") == "BTC-USDT-20250328"
    assert (
        normalize_symbol("BTC/USDT:USDT-250328", market="future") == "BTC-USDT-20250328"
    )


def test_normalize_symbol_option():
    assert (
        normalize_symbol("BTC-30JUN23-30000-C", market="option")
        == "BTC-USD-20230630-30000-C"
    )
    assert (
        normalize_symbol("BTCUSDT-230630-30000-P", market="option")
        == "BTC-USDT-20230630-30000-P"
    )
    assert (
        normalize_symbol("BTC/USDT-2025-03-28-50000-C", market="option")
        == "BTC-USDT-20250328-50000-C"
    )


def test_normalize_symbol_errors():
    with pytest.raises(ValidationError):
        normalize_symbol("BTCUSDT", market="future")

    with pytest.raises(ValidationError):
        normalize_symbol("BTC-20250328-30000-X", market="option")


def test_fill_from_exchange_auto_normalizes_with_market_hint():
    fill = Fill.from_exchange_fill(
        "binance",
        {
            "id": "f1",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "qty": "1",
            "price": "100",
            "fee": "0",
            "ts": 0,
        },
        market="perp",
    )
    assert fill.instrument_id == "BTC-USDT-PERP"


def test_fill_from_exchange_infers_future_market():
    fill = Fill.from_exchange_fill(
        "okx",
        {
            "id": "f2",
            "symbol": "BTCUSDT_250328",
            "side": "BUY",
            "qty": "1",
            "price": "100",
            "fee": "0",
            "ts": 0,
        },
    )
    assert fill.instrument_id == "BTC-USDT-20250328"


def test_fill_from_dict_normalizes_non_canonical_instrument():
    fill = Fill.from_dict(
        {
            "order_id": "trade-1",
            "instrument_id": "BTC/USD",
            "side": "BUY",
            "quantity": "0.1",
            "price": "10000",
            "fee": "1",
            "timestamp_ms": 0,
        }
    )
    assert fill.instrument_id == "BTC-USD"
