"""Basic statistics helpers using Decimal."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable


def mean(values: Iterable[Decimal]) -> Decimal:
    vals = [Decimal(v) for v in values]
    if not vals:
        raise ValueError("mean requires at least one value")
    return sum(vals) / Decimal(len(vals))


def variance(values: Iterable[Decimal], sample: bool = False) -> Decimal:
    vals = [Decimal(v) for v in values]
    n = len(vals)
    if n < 2 and sample:
        raise ValueError("sample variance requires at least two values")
    if n == 0:
        raise ValueError("variance requires data")
    avg = mean(vals)
    denom = Decimal(n - 1 if sample else n)
    return sum((v - avg) ** 2 for v in vals) / denom


def stddev(values: Iterable[Decimal], sample: bool = False) -> Decimal:
    return variance(values, sample=sample).sqrt()
