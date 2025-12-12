"""Asset allocation helpers."""

from __future__ import annotations

from decimal import Decimal
from typing import Mapping


def weights(values: Mapping[str, Decimal]) -> Mapping[str, Decimal]:
    total = sum(values.values(), Decimal(0))
    if total == 0:
        return {k: Decimal(0) for k in values}
    return {k: Decimal(v) / total for k, v in values.items()}
