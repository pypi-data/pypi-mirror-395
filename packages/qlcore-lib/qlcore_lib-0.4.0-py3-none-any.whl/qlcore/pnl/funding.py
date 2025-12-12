from __future__ import annotations

from decimal import Decimal
from typing import Sequence

from ..core.enums import OrderSide, PositionSide
from ..core.exceptions import ValidationError
from ..core.types import Money
from ..core.protocols import BasePosition
from ..events.fill import Fill
from ..events.funding import FundingEvent


def calculate_funding_payment(
    *,
    position: BasePosition,
    event: FundingEvent,
    fills: Sequence[Fill] | None = None,
    fills_applied: bool = False,
) -> Money:
    """Calculate funding P&L for a position over a funding period.

    Perpetual swaps have funding payments every 8 hours (typically).
    Long positions pay shorts when funding rate is positive, and vice versa.

    This function handles time-weighted calculation when fills occur
    during the funding period.

    Args:
        position: Current position state
        event: Funding event with rate and period info
        fills: Optional fills that occurred during the period
        fills_applied: Whether fills were already applied to position

    Returns:
        Funding P&L (positive = received, negative = paid)

    Raises:
        ValidationError: If period_end_ms <= period_start_ms

    Example:
        >>> from decimal import Decimal
        >>> # Long 1 BTC at $10,000, 0.01% funding rate
        >>> # Long pays: -1 * 10000 * 0.0001 = -$1
        >>> funding_pnl = funding_payment(
        ...     position=pos,
        ...     event=FundingEvent(
        ...         instrument_id="BTC-PERP",
        ...         rate=Decimal("0.0001"),
        ...         period_start_ms=0,
        ...         period_end_ms=8*60*60*1000,
        ...         index_price=Decimal("10000"),
        ...     ),
        ... )
    """
    if event.period_end_ms <= event.period_start_ms:
        raise ValidationError(
            "funding period_end_ms must be greater than period_start_ms"
        )

    relevant_fills = [
        f
        for f in (fills or [])
        if f.instrument_id == position.instrument_id
        and event.period_start_ms <= f.timestamp_ms <= event.period_end_ms
    ]
    relevant_fills.sort(key=lambda f: f.timestamp_ms)

    total_period = Decimal(event.period_end_ms - event.period_start_ms)
    base_signed_size = (
        Decimal(position.size)
        if position.side == PositionSide.LONG
        else -Decimal(position.size)
    )

    # Calculate net delta from fills
    net_delta = Decimal(0)
    for fill in relevant_fills:
        # FIXED: Calculate delta correctly based on position side
        if position.side == PositionSide.LONG:
            # For long: BUY adds, SELL reduces
            delta = (
                Decimal(fill.quantity)
                if fill.side == OrderSide.BUY
                else -Decimal(fill.quantity)
            )
        else:
            # For short: SELL adds (more negative), BUY reduces (less negative)
            delta = (
                -Decimal(fill.quantity)
                if fill.side == OrderSide.SELL
                else Decimal(fill.quantity)
            )
        net_delta += delta

    # If fills already applied to the position, rewind to period start size
    signed_size = base_signed_size - net_delta if fills_applied else base_signed_size

    payment = Decimal(0)
    timestamps = (
        [event.period_start_ms]
        + [f.timestamp_ms for f in relevant_fills]
        + [event.period_end_ms]
    )

    for idx in range(len(timestamps) - 1):
        # Apply fill that occurs at the current timestamp before accruing funding
        if idx > 0:
            fill = relevant_fills[idx - 1]
            # FIXED: Calculate delta correctly based on position side
            if position.side == PositionSide.LONG:
                delta = (
                    Decimal(fill.quantity)
                    if fill.side == OrderSide.BUY
                    else -Decimal(fill.quantity)
                )
            else:
                delta = (
                    -Decimal(fill.quantity)
                    if fill.side == OrderSide.SELL
                    else Decimal(fill.quantity)
                )
            signed_size += delta

        start, end = timestamps[idx], timestamps[idx + 1]
        duration = Decimal(end - start)
        if duration <= 0:
            continue

        payment += (
            -signed_size
            * Decimal(event.index_price)
            * Decimal(event.rate)
            * (duration / total_period)
        )

    return payment


# Backwards compatibility alias
funding_payment = calculate_funding_payment
