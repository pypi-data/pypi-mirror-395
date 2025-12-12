"""PnL engine."""

from __future__ import annotations

from decimal import Decimal
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence

from ..core.types import Money, Price
from ..core.protocols import BasePosition
from ..events.fill import Fill
from ..events.funding import FundingEvent
from ..events.fee import FeeEvent
from ..portfolio.portfolio import Portfolio
from .funding import calculate_funding_payment
from ..positions.metrics import unrealized_pnl as calc_unrealized


class PnLMode(Enum):
    REALIZED = "realized"
    UNREALIZED = "unrealized"
    BOTH = "both"


@dataclass(frozen=True)
class PnLBreakdown:
    realized: Money
    unrealized: Money
    fees: Money
    funding: Money
    trading: Money
    slippage: Money
    total: Money


@dataclass(frozen=True)
class PortfolioPnL:
    per_position: Mapping[str, PnLBreakdown]
    total: PnLBreakdown

    @property
    def fees(self) -> Money:
        """Convenience access to aggregate fees."""
        return self.total.fees

    @property
    def unrealized(self) -> Money:
        """Convenience access to aggregate unrealized PnL."""
        return self.total.unrealized


def pnl(
    *,
    position: BasePosition,
    mark_price: Price,
    fills: Sequence[Fill] = (),
    funding_events: Sequence[FundingEvent] = (),
    fee_events: Sequence[FeeEvent | Money] = (),
    slippage_events: Sequence[Money] = (),
    mode: PnLMode = PnLMode.BOTH,
    fills_applied: bool = False,
) -> PnLBreakdown:
    realized = Decimal(position.realized_pnl)
    unrealized = Decimal(0)
    if mode in (PnLMode.UNREALIZED, PnLMode.BOTH):
        unrealized = calc_unrealized(position, mark_price)
    if mode == PnLMode.REALIZED:
        unrealized = Decimal(0)

    funding = sum(
        (
            calculate_funding_payment(
                position=position,
                event=event,
                fills=fills,
                fills_applied=fills_applied,
            )
            for event in funding_events
        ),
        Decimal(0),
    )
    fees_total = Decimal(position.fees) + sum(
        Decimal(f.amount if isinstance(f, FeeEvent) else f) for f in fee_events
    )
    trading_component = realized + unrealized
    slippage = sum((Decimal(s) for s in slippage_events), Decimal(0))
    total = trading_component + funding - fees_total - slippage

    return PnLBreakdown(
        realized=realized,
        unrealized=unrealized,
        fees=fees_total,
        funding=funding,
        trading=trading_component,
        slippage=slippage,
        total=total,
    )


def portfolio_pnl(
    *,
    portfolio: Portfolio,
    marks: Mapping[str, Price],
    fills: Sequence[Fill] = (),
    funding_events: Sequence[FundingEvent] = (),
    fee_events: Sequence[Money] = (),
    slippage_events: Sequence[Money] = (),
    mode: PnLMode = PnLMode.BOTH,
) -> PortfolioPnL:
    per_position: dict[str, PnLBreakdown] = {}
    aggregate = PnLBreakdown(
        realized=Decimal(0),
        unrealized=Decimal(0),
        fees=Decimal(0),
        funding=Decimal(0),
        trading=Decimal(0),
        slippage=Decimal(0),
        total=Decimal(0),
    )

    for (instrument_id, _side), position in portfolio.positions.items():
        mark = marks.get(instrument_id)
        if mark is None:
            continue
        breakdown = pnl(
            position=position,
            mark_price=mark,
            fills=fills,
            funding_events=[
                e for e in funding_events if e.instrument_id == instrument_id
            ],
            fee_events=fee_events,
            slippage_events=slippage_events,
            mode=mode,
            fills_applied=True,
        )
        per_position[f"{instrument_id}:{position.side.name}"] = breakdown
        aggregate = _combine_breakdowns(aggregate, breakdown)

    # If no open positions, still account for explicit fees provided via fills
    if not per_position and fills:
        fee_total = sum((Decimal(f.fee) for f in fills), Decimal(0))
        fee_breakdown = PnLBreakdown(
            realized=Decimal(0),
            unrealized=Decimal(0),
            fees=fee_total,
            funding=Decimal(0),
            trading=Decimal(0),
            slippage=Decimal(0),
            total=Decimal(0) - fee_total,
        )
        aggregate = _combine_breakdowns(aggregate, fee_breakdown)

    return PortfolioPnL(per_position=per_position, total=aggregate)


def _combine_breakdowns(left: PnLBreakdown, right: PnLBreakdown) -> PnLBreakdown:
    return PnLBreakdown(
        realized=left.realized + right.realized,
        unrealized=left.unrealized + right.unrealized,
        fees=left.fees + right.fees,
        funding=left.funding + right.funding,
        trading=left.trading + right.trading,
        slippage=left.slippage + right.slippage,
        total=left.total + right.total,
    )


def calculate_pnl(**kwargs) -> PnLBreakdown:
    """Backward-compatible alias for pnl()."""
    return pnl(**kwargs)


def calculate_portfolio_pnl(**kwargs) -> PortfolioPnL:
    """Backward-compatible alias for portfolio_pnl()."""
    return portfolio_pnl(**kwargs)
