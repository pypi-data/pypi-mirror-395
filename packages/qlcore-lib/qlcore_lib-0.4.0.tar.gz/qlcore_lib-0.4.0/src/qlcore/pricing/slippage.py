"""Simple slippage estimation."""

from __future__ import annotations

from decimal import Decimal
from ..core.enums import OrderSide
from ..core.types import Price, Quantity
from ..data.orderbook import OrderBook


def estimate_slippage(
    orderbook: OrderBook,
    side: OrderSide,
    quantity: Quantity,
    impact_bps: Decimal | None = None,
) -> Price:
    """
    Estimate volume-weighted execution price for a market order.
    Optionally add a linear market impact in basis points on the notional.
    """
    levels = orderbook.asks if side == OrderSide.BUY else orderbook.bids
    remaining = Decimal(quantity)
    if remaining <= 0:
        raise ValueError("quantity must be positive")
    total_value = Decimal(0)
    total_filled = Decimal(0)
    for price, qty in levels:
        take = min(remaining, Decimal(qty))
        total_value += Decimal(price) * take
        total_filled += take
        remaining -= take
        if remaining <= 0:
            break
    if remaining > 0:
        raise ValueError("insufficient liquidity to satisfy quantity")
    vwap = total_value / total_filled
    if impact_bps:
        impact = vwap * (Decimal(impact_bps) / Decimal("10000"))
        vwap = vwap + impact if side == OrderSide.BUY else vwap - impact
    return vwap
