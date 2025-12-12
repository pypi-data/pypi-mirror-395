from decimal import Decimal

import pytest

from qlcore.core.enums import OrderSide
from qlcore.data.orderbook import OrderBook
from qlcore.pricing.mark import mark_price
from qlcore.pricing.mid import mid_price
from qlcore.pricing.vwap import vwap
from qlcore.pricing.slippage import estimate_slippage


def test_mark_price_prefers_orderbook_mid():
    ob = OrderBook(
        instrument_id="BTC-USD",
        bids=[(Decimal("99"), Decimal("1"))],
        asks=[(Decimal("101"), Decimal("1"))],
        timestamp_ms=0,
    )
    assert mark_price(orderbook=ob, index_price=Decimal("100")) == Decimal("100")


def test_mid_price_none_when_empty():
    ob = OrderBook(instrument_id="BTC-USD", bids=[], asks=[], timestamp_ms=0)
    assert mid_price(ob) is None


def test_vwap():
    data = [(Decimal("10"), Decimal("2")), (Decimal("12"), Decimal("1"))]
    assert vwap(data) == Decimal("10.66666666666666666666666667")


def test_slippage_estimate_and_insufficient_liquidity():
    ob = OrderBook(
        instrument_id="BTC-USD",
        bids=[(Decimal("99"), Decimal("1"))],
        asks=[(Decimal("101"), Decimal("0.5")), (Decimal("102"), Decimal("1"))],
        timestamp_ms=0,
    )
    px = estimate_slippage(ob, OrderSide.BUY, Decimal("1"))
    # Expected avg: 0.5@101 + 0.5@102 = 101.5
    assert px == Decimal("101.5")
    impacted = estimate_slippage(
        ob, OrderSide.BUY, Decimal("1"), impact_bps=Decimal("10")
    )
    assert impacted > px
    with pytest.raises(ValueError):
        estimate_slippage(ob, OrderSide.BUY, Decimal("5"))
