"""Pandas integration for qlcore.

Optional module that provides DataFrame conversion utilities.
Requires pandas to be installed.

Usage:
    from qlcore.pandas_ext import positions_to_dataframe, fills_to_dataframe
    
    df = positions_to_dataframe(portfolio.positions)
    fills_df = fills_to_dataframe(fills)
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, TypeVar

if TYPE_CHECKING:
    import pandas as pd

from .core.protocols import BasePosition
from .core.enums import PositionSide
from .core.types import Money, Quantity
from .events.fill import Fill
from .portfolio.portfolio import Portfolio


def _ensure_pandas() -> "pd":
    """Import pandas or raise helpful error."""
    try:
        import pandas as pd

        return pd
    except ImportError:
        raise ImportError(
            "pandas is required for DataFrame operations. "
            "Install with: pip install pandas"
        )


def positions_to_dataframe(positions: Dict[tuple, BasePosition]) -> "pd.DataFrame":
    """Convert portfolio positions dict to DataFrame.

    Args:
        positions: Dict mapping (instrument_id, side) to position

    Returns:
        DataFrame with position data

    Example:
        >>> df = positions_to_dataframe(portfolio.positions)
        >>> df[['instrument_id', 'side', 'size', 'unrealized_pnl']]
    """
    pd = _ensure_pandas()

    rows = []
    for (instrument_id, side), pos in positions.items():
        rows.append(
            {
                "instrument_id": instrument_id,
                "side": side.name,
                "size": float(pos.size),
                "entry_value": float(pos.entry_value),
                "avg_entry_price": (
                    float(pos.avg_entry_price)
                    if hasattr(pos, "avg_entry_price") and pos.avg_entry_price
                    else None
                ),
                "realized_pnl": float(pos.realized_pnl),
                "unrealized_pnl": float(getattr(pos, "unrealized_pnl", 0)),
                "fees": float(pos.fees),
                "last_update_ms": int(getattr(pos, "last_update_ms", 0)),
            }
        )

    return pd.DataFrame(rows)


def fills_to_dataframe(fills: Sequence[Fill]) -> "pd.DataFrame":
    """Convert sequence of fills to DataFrame.

    Args:
        fills: List of Fill events

    Returns:
        DataFrame with fill data

    Example:
        >>> df = fills_to_dataframe(fills)
        >>> df.groupby('instrument_id')['quantity'].sum()
    """
    pd = _ensure_pandas()

    rows = []
    for fill in fills:
        rows.append(
            {
                "order_id": fill.order_id,
                "instrument_id": fill.instrument_id,
                "side": fill.side.name,
                "quantity": float(fill.quantity),
                "price": float(fill.price),
                "fee": float(fill.fee),
                "timestamp_ms": int(fill.timestamp_ms),
                "notional": float(fill.quantity * fill.price),
            }
        )

    return pd.DataFrame(rows)


def portfolio_to_dataframe(portfolio: Portfolio) -> "pd.DataFrame":
    """Convert portfolio to DataFrame.

    Args:
        portfolio: Portfolio instance

    Returns:
        DataFrame with position data plus account info
    """
    df = positions_to_dataframe(portfolio.positions)
    df["base_currency"] = portfolio.base_currency
    return df


def equity_series(
    portfolio: Portfolio,
    fills: Sequence[Fill],
    mark_prices: Dict[str, Decimal],
) -> "pd.Series":
    """Calculate equity curve from fills.

    Args:
        portfolio: Starting portfolio
        fills: Chronological sequence of fills
        mark_prices: Current mark prices per instrument

    Returns:
        pd.Series with equity at each timestamp
    """
    pd = _ensure_pandas()
    from .pnl import calculate_portfolio_pnl

    # Clone portfolio for simulation
    sim_portfolio = Portfolio(
        account=portfolio.account,
        positions=dict(portfolio.positions),
    )

    timestamps = []
    equities = []

    for fill in fills:
        sim_portfolio.apply_fill(fill)

        # Calculate current equity
        pnl_result = calculate_portfolio_pnl(
            portfolio=sim_portfolio,
            marks=mark_prices,
            fills=[],
        )
        equity = float(sim_portfolio.account.equity + pnl_result.total.unrealized)

        timestamps.append(fill.timestamp_ms)
        equities.append(equity)

    return pd.Series(equities, index=pd.to_datetime(timestamps, unit="ms"))


# Mixin for adding to_dataframe to positions
class DataFrameMixin:
    """Mixin adding DataFrame conversion to position classes."""

    instrument_id: str
    side: PositionSide
    size: Quantity
    entry_value: Money
    realized_pnl: Money
    fees: Money
    avg_entry_price: Decimal | None
    unrealized_pnl: Money
    accumulated_funding: Money
    expiry_ms: int | None

    def to_dataframe(self) -> "pd.DataFrame":
        """Convert this position to a single-row DataFrame."""
        pd = _ensure_pandas()

        data = {
            "instrument_id": [self.instrument_id],
            "side": [self.side.name],
            "size": [float(self.size)],
            "entry_value": [float(self.entry_value)],
            "realized_pnl": [float(self.realized_pnl)],
            "fees": [float(self.fees)],
        }

        if hasattr(self, "avg_entry_price") and self.avg_entry_price:
            data["avg_entry_price"] = [float(self.avg_entry_price)]
        if hasattr(self, "unrealized_pnl"):
            data["unrealized_pnl"] = [float(self.unrealized_pnl)]
        if hasattr(self, "accumulated_funding"):
            data["accumulated_funding"] = [float(self.accumulated_funding)]
        if hasattr(self, "expiry_ms"):
            data["expiry_ms"] = [self.expiry_ms]

        return pd.DataFrame(data)
