"""Orderbook snapshot structure."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple
from ..core.types import Price, Quantity, TimestampMs

BookSide = Sequence[Tuple[Price, Quantity]]


@dataclass(frozen=True)
class OrderBook:
    instrument_id: str
    bids: BookSide
    asks: BookSide
    timestamp_ms: TimestampMs

    @property
    def best_bid(self) -> Tuple[Price, Quantity] | None:
        return max(self.bids, key=lambda x: x[0]) if self.bids else None

    @property
    def best_ask(self) -> Tuple[Price, Quantity] | None:
        return min(self.asks, key=lambda x: x[0]) if self.asks else None

    @property
    def mid(self) -> Price | None:
        bid = self.best_bid
        ask = self.best_ask
        if bid is None or ask is None:
            return None
        return (bid[0] + ask[0]) / 2
