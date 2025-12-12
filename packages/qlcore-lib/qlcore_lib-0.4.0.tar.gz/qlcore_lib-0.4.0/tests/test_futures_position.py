"""Tests for FuturesPosition."""

from decimal import Decimal
import pytest

from qlcore.positions import FuturesPosition
from qlcore.positions.base import BasePositionImpl
from qlcore.events.fill import Fill
from qlcore.events.settlement import SettlementEvent
from qlcore.core.enums import OrderSide, PositionSide


class TestFuturesPositionBasics:
    """Test basic FuturesPosition functionality."""

    def test_flat_creates_empty_position(self):
        """Flat should create a position with zero size."""
        pos = FuturesPosition.flat("BTC-DEC24")
        assert pos.size == Decimal(0)
        assert pos.expiry_ms is None
        assert pos.settlement_price is None
        assert pos.is_settled is False

    def test_flat_with_expiry(self):
        """Flat should accept expiry timestamp."""
        expiry = 1725289600000  # Dec 31, 2024
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)
        assert pos.expiry_ms == expiry

    def test_apply_fill_preserves_futures_fields(self):
        """Applying a fill should preserve futures-specific fields."""
        expiry = 1725289600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=1000,
        )

        pos = pos.apply_fill(fill)

        assert pos.size == Decimal("1")
        assert pos.expiry_ms == expiry
        assert isinstance(pos, FuturesPosition)


class TestFuturesExpiration:
    """Test expiration-related functionality."""

    def test_is_expired_returns_false_when_no_expiry(self):
        """is_expired should return False when expiry_ms is None."""
        pos = FuturesPosition.flat("BTC-DEC24")
        assert pos.is_expired(1735689600000) is False

    def test_is_expired_returns_false_before_expiry(self):
        """is_expired should return False before expiry time."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)
        assert pos.is_expired(expiry - 1) is False

    def test_is_expired_returns_true_at_expiry(self):
        """is_expired should return True at expiry time."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)
        assert pos.is_expired(expiry) is True

    def test_is_expired_returns_true_after_expiry(self):
        """is_expired should return True after expiry time."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)
        assert pos.is_expired(expiry + 1000) is True

    def test_time_to_expiry_returns_none_when_no_expiry(self):
        """time_to_expiry should return None when expiry_ms is None."""
        pos = FuturesPosition.flat("BTC-DEC24")
        assert pos.time_to_expiry(0) is None

    def test_time_to_expiry_calculates_correctly(self):
        """time_to_expiry should return correct milliseconds."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)

        current_time = expiry - 3600000  # 1 hour before
        assert pos.time_to_expiry(current_time) == 3600000

    def test_time_to_expiry_returns_zero_when_expired(self):
        """time_to_expiry should return 0 when already expired."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)
        assert pos.time_to_expiry(expiry + 1000) == 0

    def test_time_to_expiry_hours(self):
        """time_to_expiry_hours should return hours."""
        expiry = 1735689600000
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=expiry)

        current_time = expiry - (24 * 60 * 60 * 1000)  # 24 hours before
        assert pos.time_to_expiry_hours(current_time) == 24.0


class TestFuturesSettlement:
    """Test settlement functionality."""

    def test_settle_closes_long_position(self):
        """Settling should close position and realize P&L."""
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1735689600000)

        # Open long position at 10000
        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.BUY,
            quantity=Decimal("2"),
            price=Decimal("10000"),
            fee=Decimal("20"),
            timestamp_ms=1000,
        )
        pos = pos.apply_fill(fill)

        # Settle at 10500
        settlement = SettlementEvent(
            instrument_id="BTC-DEC24",
            price=Decimal("10500"),
            timestamp_ms=1735689600000,
        )
        settled = pos.settle(settlement)

        # Position should be closed
        assert settled.size == Decimal(0)
        assert settled.is_settled is True
        assert settled.settlement_price == Decimal("10500")

        # P&L: (10500 - 10000) * 2 = 1000
        assert settled.realized_pnl == Decimal("1000")

    def test_settle_closes_short_position(self):
        """Settling short position should calculate P&L correctly."""
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1735689600000)

        # Open short position at 10000
        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.SELL,
            quantity=Decimal("2"),
            price=Decimal("10000"),
            fee=Decimal("20"),
            timestamp_ms=1000,
        )
        pos = pos.apply_fill(fill)

        # Settle at 9500 (profit for short)
        settlement = SettlementEvent(
            instrument_id="BTC-DEC24",
            price=Decimal("9500"),
            timestamp_ms=1735689600000,
        )
        settled = pos.settle(settlement)

        # P&L: (10000 - 9500) * 2 = 1000
        assert settled.realized_pnl == Decimal("1000")
        assert settled.is_settled is True

    def test_settle_short_with_loss(self):
        """Short position should have loss when price goes up."""
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1735689600000)

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.SELL,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=1000,
        )
        pos = pos.apply_fill(fill)

        # Settle at 10500 (loss for short)
        settlement = SettlementEvent(
            instrument_id="BTC-DEC24",
            price=Decimal("10500"),
            timestamp_ms=1735689600000,
        )
        settled = pos.settle(settlement)

        # P&L: (10000 - 10500) * 1 = -500
        assert settled.realized_pnl == Decimal("-500")

    def test_settle_raises_if_already_settled(self):
        """Settling an already-settled position should raise."""
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1735689600000)

        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
            timestamp_ms=1000,
        )
        pos = pos.apply_fill(fill)

        settlement = SettlementEvent(
            instrument_id="BTC-DEC24",
            price=Decimal("10500"),
            timestamp_ms=1735689600000,
        )
        settled = pos.settle(settlement)

        with pytest.raises(ValueError, match="already settled"):
            settled.settle(settlement)

    def test_settle_raises_if_flat(self):
        """Settling a flat position should raise."""
        pos = FuturesPosition.flat("BTC-DEC24", expiry_ms=1735689600000)

        settlement = SettlementEvent(
            instrument_id="BTC-DEC24",
            price=Decimal("10500"),
            timestamp_ms=1735689600000,
        )

        with pytest.raises(ValueError, match="flat position"):
            pos.settle(settlement)


class TestFuturesFromBase:
    """Test from_base factory method."""

    def test_from_base_converts_position(self):
        """from_base should convert BasePositionImpl to FuturesPosition."""
        base = BasePositionImpl.flat("BTC-DEC24")
        fill = Fill(
            order_id="o1",
            instrument_id="BTC-DEC24",
            side=OrderSide.BUY,
            quantity=Decimal("2"),
            price=Decimal("10000"),
            fee=Decimal("20"),
            timestamp_ms=1000,
        )
        base = base.apply_fill(fill)

        futures = FuturesPosition.from_base(base, expiry_ms=1735689600000)

        assert isinstance(futures, FuturesPosition)
        assert futures.size == Decimal("2")
        assert futures.expiry_ms == 1735689600000
        assert futures.is_settled is False

    def test_from_base_without_expiry(self):
        """from_base should work without expiry."""
        base = BasePositionImpl.flat("BTC-DEC24")

        futures = FuturesPosition.from_base(base)

        assert futures.expiry_ms is None
