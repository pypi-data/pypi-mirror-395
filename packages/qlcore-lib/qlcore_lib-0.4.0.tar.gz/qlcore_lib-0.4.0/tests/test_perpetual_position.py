"""Tests for PerpetualPosition."""

from decimal import Decimal
import pytest

from qlcore.positions import PerpetualPosition
from qlcore.positions.base import BasePositionImpl
from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.core.enums import OrderSide, PositionSide


class TestPerpetualPositionBasics:
    """Test basic PerpetualPosition functionality."""

    def test_flat_creates_empty_position(self):
        """Flat should create a position with zero size and zero funding."""
        pos = PerpetualPosition.flat("BTC-PERP")
        assert pos.size == Decimal(0)
        assert pos.accumulated_funding == Decimal(0)
        assert pos.last_funding_timestamp_ms == 0
        assert pos.funding_pnl == Decimal(0)

    def test_apply_fill_preserves_funding_fields(self):
        """Applying a fill should preserve funding accumulator."""
        pos = PerpetualPosition.flat("BTC-PERP")

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=1000,
        )

        pos = pos.apply_fill(fill)

        assert pos.size == Decimal("1")
        assert pos.accumulated_funding == Decimal(0)
        assert isinstance(pos, PerpetualPosition)

    def test_funding_pnl_property(self):
        """funding_pnl should return accumulated_funding."""
        pos = PerpetualPosition.flat("BTC-PERP")
        assert pos.funding_pnl == Decimal(0)


class TestPerpetualFundingAccumulation:
    """Test funding accumulation in PerpetualPosition."""

    def test_apply_funding_updates_accumulator(self):
        """apply_funding should update accumulated_funding."""
        pos = PerpetualPosition.flat("BTC-PERP")

        # Open a position first
        fill = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=0,
        )
        pos = pos.apply_fill(fill)

        # Apply funding
        funding = FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("0.0001"),  # 0.01% funding rate
            period_start_ms=0,
            period_end_ms=8 * 60 * 60 * 1000,  # 8 hours
            index_price=Decimal("10000"),
        )
        pos = pos.apply_funding(funding)

        # Long pays funding when rate is positive
        # Payment = -1 * 10000 * 0.0001 = -1
        assert pos.accumulated_funding == Decimal("-1")
        assert pos.funding_pnl == Decimal("-1")
        assert pos.last_funding_timestamp_ms == 8 * 60 * 60 * 1000

    def test_multiple_funding_periods_accumulate(self):
        """Multiple funding events should accumulate correctly."""
        pos = PerpetualPosition.flat("BTC-PERP")

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=0,
        )
        pos = pos.apply_fill(fill)

        # First funding period
        funding1 = FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("0.0001"),
            period_start_ms=0,
            period_end_ms=8 * 60 * 60 * 1000,
            index_price=Decimal("10000"),
        )
        pos = pos.apply_funding(funding1)
        first_funding = pos.accumulated_funding

        # Second funding period
        funding2 = FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("-0.0001"),  # Negative rate = longs receive
            period_start_ms=8 * 60 * 60 * 1000,
            period_end_ms=16 * 60 * 60 * 1000,
            index_price=Decimal("10000"),
        )
        pos = pos.apply_funding(funding2)

        # Funding should cancel out
        assert pos.accumulated_funding == first_funding + Decimal("1")
        assert pos.last_funding_timestamp_ms == 16 * 60 * 60 * 1000

    def test_short_position_funding(self):
        """Short positions should receive funding when rate is positive."""
        pos = PerpetualPosition.flat("BTC-PERP")

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.SELL,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=0,
        )
        pos = pos.apply_fill(fill)

        funding = FundingEvent(
            instrument_id="BTC-PERP",
            rate=Decimal("0.0001"),
            period_start_ms=0,
            period_end_ms=8 * 60 * 60 * 1000,
            index_price=Decimal("10000"),
        )
        pos = pos.apply_funding(funding)

        # Short receives funding when rate is positive
        # Payment = -(-1) * 10000 * 0.0001 = 1
        assert pos.accumulated_funding == Decimal("1")
        assert pos.side == PositionSide.SHORT


class TestPerpetualFromBase:
    """Test from_base factory method."""

    def test_from_base_converts_position(self):
        """from_base should convert BasePositionImpl to PerpetualPosition."""
        base = BasePositionImpl.flat("BTC-PERP")
        fill = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.BUY,
            quantity=Decimal("2"),
            price=Decimal("10000"),
            fee=Decimal("20"),
            timestamp_ms=1000,
        )
        base = base.apply_fill(fill)

        perp = PerpetualPosition.from_base(base)

        assert isinstance(perp, PerpetualPosition)
        assert perp.size == Decimal("2")
        assert perp.accumulated_funding == Decimal(0)

    def test_from_base_with_initial_funding(self):
        """from_base should accept initial funding value."""
        base = BasePositionImpl.flat("BTC-PERP")

        perp = PerpetualPosition.from_base(
            base,
            accumulated_funding=Decimal("-50"),
            last_funding_timestamp_ms=1000,
        )

        assert perp.accumulated_funding == Decimal("-50")
        assert perp.last_funding_timestamp_ms == 1000


class TestPerpetualTotalPnL:
    """Test total P&L calculations."""

    def test_total_realized_pnl_includes_funding(self):
        """total_realized_pnl should include both trading and funding P&L."""
        pos = PerpetualPosition.flat("BTC-PERP")

        # Open position
        buy = Fill(
            order_id="o1",
            instrument_id="BTC-PERP",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=0,
        )
        pos = pos.apply_fill(buy)

        # Close with profit
        sell = Fill(
            order_id="o2",
            instrument_id="BTC-PERP",
            side=OrderSide.SELL,
            quantity=Decimal("1"),
            price=Decimal("10100"),
            fee=Decimal("10"),
            timestamp_ms=1000,
        )
        pos = pos.apply_fill(sell)

        # Trading P&L = 100
        assert pos.realized_pnl == Decimal("100")

        # Simulate some funding was accumulated
        pos = PerpetualPosition.from_base(
            pos,
            accumulated_funding=Decimal("-25"),
        )

        # Total should be trading + funding
        assert pos.total_realized_pnl == Decimal("75")
