"""Core enums (order sides, position sides, etc.)."""

from enum import Enum, auto


class OrderSide(Enum):
    BUY = auto()
    SELL = auto()


class PositionSide(Enum):
    LONG = auto()
    SHORT = auto()


class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    STOP_MARKET = auto()
    STOP_LIMIT = auto()
    TRAILING_STOP = auto()
    ICEBERG = auto()


class TimeInForce(Enum):
    GTC = auto()
    IOC = auto()
    FOK = auto()
    POST_ONLY = auto()
