"""Mark price helpers."""

from __future__ import annotations

from ..core.types import Price
from ..data.orderbook import OrderBook


def mark_price(
    orderbook: OrderBook | None = None, index_price: Price | None = None
) -> Price:
    """Return a mark price using mid from the orderbook or fallback to index price."""
    if orderbook and orderbook.mid is not None:
        return orderbook.mid
    if index_price is not None:
        return index_price
    raise ValueError("mark price requires orderbook or index price")
