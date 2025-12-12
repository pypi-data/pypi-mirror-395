"""Core type aliases for qlcore."""

from decimal import Decimal
from typing import NewType

Money = Decimal
Price = Decimal
Quantity = Decimal
Rate = Decimal
TimestampMs = NewType("TimestampMs", int)
