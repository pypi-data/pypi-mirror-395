from decimal import Decimal

import pytest

from qlcore.data.orderbook import OrderBook
from qlcore.pricing import mark_price, mid_price


def test_mark_price_prefers_orderbook_mid():
    ob = OrderBook(
        instrument_id="BTC-USD",
        bids=[(Decimal("99"), Decimal("1"))],
        asks=[(Decimal("101"), Decimal("1"))],
        timestamp_ms=0,
    )
    assert mid_price(ob) == Decimal("100")
    assert mark_price(orderbook=ob, index_price=Decimal("99.5")) == Decimal("100")


def test_mark_price_fallback_to_index():
    assert mark_price(orderbook=None, index_price=Decimal("99.5")) == Decimal("99.5")
    with pytest.raises(ValueError):
        mark_price()
