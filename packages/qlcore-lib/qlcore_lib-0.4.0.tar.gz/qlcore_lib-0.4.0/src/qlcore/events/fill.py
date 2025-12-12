"""Fill event structure."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Any
from ..core.enums import OrderSide
from ..core.types import Money, Price, Quantity, TimestampMs
from ..core.exceptions import ValidationError, InvalidFillError
from ..utils.validation import (
    ensure_valid_money,
    ensure_valid_price,
    ensure_valid_quantity,
    ensure_valid_timestamp,
)
from ..utils.symbols import normalize_symbol, infer_market_from_symbol


@dataclass(frozen=True)
class Fill:
    order_id: str
    instrument_id: str
    side: OrderSide
    quantity: Quantity
    price: Price
    fee: Money
    timestamp_ms: TimestampMs

    def __post_init__(self) -> None:
        if not self.order_id or not self.order_id.strip():
            raise InvalidFillError("order_id cannot be empty")

        instrument_id = self._normalize_instrument(self.instrument_id, None)
        object.__setattr__(self, "instrument_id", instrument_id)

        try:
            ensure_valid_quantity(self.quantity, "quantity")
            ensure_valid_price(self.price, "price")
            ensure_valid_money(self.fee, "fee")
            ensure_valid_timestamp(self.timestamp_ms, "timestamp_ms")
        except ValidationError as exc:
            raise InvalidFillError(str(exc)) from exc

    def to_dict(self) -> dict[str, Any]:
        """Return a log/serialization-friendly dict."""
        return {
            "order_id": self.order_id,
            "instrument_id": self.instrument_id,
            "side": self.side.name,
            "quantity": str(self.quantity),
            "price": str(self.price),
            "fee": str(self.fee),
            "timestamp_ms": int(self.timestamp_ms),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Fill":
        """Construct a Fill from a mapping (e.g., exchange fill JSON)."""
        side = data.get("side")
        try:
            if isinstance(side, OrderSide):
                side_enum = side
            elif isinstance(side, str):
                side_enum = OrderSide[side.upper()]
            else:
                side_enum = OrderSide(int(side))
        except Exception as exc:
            raise InvalidFillError(f"invalid side: {side}") from exc
        return cls(
            order_id=str(data["order_id"]),
            instrument_id=str(data["instrument_id"]),
            side=side_enum,
            quantity=Quantity(Decimal(str(data["quantity"]))),
            price=Price(Decimal(str(data["price"]))),
            fee=Money(Decimal(str(data.get("fee", 0)))),
            timestamp_ms=TimestampMs(int(data["timestamp_ms"])),
        )

    @classmethod
    def create(
        cls,
        *,
        order_id: str,
        instrument_id: str,
        side: OrderSide | str,
        quantity: Quantity | Decimal | str,
        price: Price | Decimal | str,
        timestamp_ms: TimestampMs | int,
        fee: Money | Decimal | str = Decimal(0),
    ) -> "Fill":
        """Create Fill with keyword-only arguments for safety.

        All parameters must be passed by name, preventing positional
        argument order mistakes that are common with the regular constructor.

        Example:
            >>> fill = Fill.create(
            ...     order_id="o1",
            ...     instrument_id="BTC-USD",
            ...     side=OrderSide.BUY,
            ...     quantity=Decimal("1"),
            ...     price=Decimal("10000"),
            ...     timestamp_ms=1234567890,
            ... )
        """
        if isinstance(side, str):
            side = OrderSide[side.upper()]
        return cls(
            order_id=order_id,
            instrument_id=instrument_id,
            side=side,
            quantity=Quantity(Decimal(str(quantity))),
            price=Price(Decimal(str(price))),
            fee=Money(Decimal(str(fee))),
            timestamp_ms=TimestampMs(int(timestamp_ms)),
        )

    @classmethod
    def from_exchange_fill(
        cls, exchange: str, raw: Mapping[str, Any], *, market: str | None = None
    ) -> "Fill":
        """Construct a Fill from a raw exchange payload.

        Known keys (fallbacks are used if a key is missing):
        - id | fill_id | trade_id | order_id -> order_id
        - symbol | instrument | instrument_id -> instrument_id
        - side (BUY/SELL) -> side
        - qty | size | quantity -> quantity
        - price -> price
        - fee | commission -> fee (defaults to 0)
        - ts | timestamp | time | timestamp_ms -> timestamp_ms
        """
        exchange_lower = exchange.lower()
        order_id = cls._pick(raw, "id", "fill_id", "trade_id", "order_id")
        instrument_raw = cls._pick(raw, "symbol", "instrument", "instrument_id")
        side_val = cls._pick(raw, "side")
        qty = cls._pick(raw, "qty", "size", "quantity")
        price = cls._pick(raw, "price")
        fee = cls._pick(raw, "fee", "commission")
        ts = cls._pick(raw, "ts", "timestamp", "time", "timestamp_ms")

        if (
            order_id is None
            or instrument_raw is None
            or side_val is None
            or qty is None
            or price is None
            or ts is None
        ):
            raise InvalidFillError(
                f"missing required fields in {exchange_lower} fill payload"
            )

        market_hint = market or raw.get("market") or raw.get("type")
        instrument_id = cls._normalize_instrument(str(instrument_raw), market_hint)

        return cls.from_dict(
            {
                "order_id": str(order_id),
                "instrument_id": instrument_id,
                "side": str(side_val),
                "quantity": str(qty),
                "price": str(price),
                "fee": str(fee if fee is not None else 0),
                "timestamp_ms": int(ts),
                "exchange": exchange_lower,
            }
        )

    @staticmethod
    def _normalize_instrument(symbol: str, market_hint: str | None) -> str:
        hinted = market_hint.lower() if isinstance(market_hint, str) else None
        inferred = infer_market_from_symbol(symbol)
        market = hinted or inferred or "spot"
        try:
            return normalize_symbol(symbol, market=market)
        except ValidationError as exc:
            raise InvalidFillError(f"invalid instrument_id: {symbol}") from exc

    @staticmethod
    def _pick(raw: Mapping[str, Any], *keys: str) -> Any:
        for key in keys:
            if key in raw and raw[key] is not None:
                return raw[key]
        return None
