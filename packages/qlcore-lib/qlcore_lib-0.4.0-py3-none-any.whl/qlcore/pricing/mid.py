"""Mid price helpers."""

from __future__ import annotations

from ..core.types import Price
from ..data.orderbook import OrderBook


def mid_price(orderbook: OrderBook) -> Price | None:
    """Return mid price from an orderbook snapshot."""
    return orderbook.mid
