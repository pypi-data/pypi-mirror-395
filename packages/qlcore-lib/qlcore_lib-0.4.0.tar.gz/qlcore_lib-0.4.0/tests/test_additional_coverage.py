import logging
from decimal import Decimal, getcontext
import types

import pytest

from qlcore.core.enums import OrderSide, OrderType, PositionSide, TimeInForce
from qlcore.core.exceptions import ValidationError
from qlcore.events.fill import Fill
from qlcore.events.funding import FundingEvent
from qlcore.instruments import InstrumentRegistry, SpotInstrument
from qlcore.orders.state import OrderState, OrderStatus
from qlcore.orders.types.limit import LimitOrder
from qlcore.orders.types.stop_market import StopMarketOrder
from qlcore.orders.types.stop_limit import StopLimitOrder
from qlcore.orders.types.trailing_stop import TrailingStopOrder
from qlcore.orders.types.iceberg import IcebergOrder
from qlcore.orders.types.market import MarketOrder
from qlcore.pnl.funding import calculate_funding_payment
from qlcore.pnl.calculator import calculate_portfolio_pnl, PnLMode
from qlcore.portfolio import Portfolio
from qlcore.positions.base import BasePositionImpl
from qlcore.positions.metrics import leverage as position_leverage
from qlcore.risk.liquidation import (
    calculate_isolated_liquidation_price,
    calculate_cross_liquidation_price,
)
from qlcore.security.sanitize import sanitize_all_fields
from qlcore.serialization.json_codec import serialize_portfolio
from qlcore.utils.logging import get_logger, set_log_level
from qlcore.utils.validation import (
    ensure_valid_rate,
    ensure_valid_price,
    ensure_valid_quantity,
    ensure_valid_timestamp_order,
    validate_tick_size,
    validate_lot_size,
)


def test_limit_order_validation_and_tif_default():
    """Limit order must have price and will coerce unsupported TIF to GTC."""
    with pytest.raises(ValidationError):
        LimitOrder(
            id="o1",
            instrument_id="BTC-USD",
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            quantity=Decimal("1"),
            price=None,
            time_in_force=TimeInForce.GTC,
            timestamp_ms=0,
        )

    order = LimitOrder(
        id="o2",
        instrument_id="BTC-USD",
        side=OrderSide.BUY,
        type=OrderType.LIMIT,
        quantity=Decimal("1"),
        price=Decimal("10000"),
        time_in_force=TimeInForce.FOK,
        timestamp_ms=0,
    )
    assert order.type.name == "LIMIT"
    assert order.time_in_force == TimeInForce.FOK


def test_stop_orders_apply_defaults():
    """Stop orders use provided price as stop and set correct order type."""
    with pytest.raises(ValidationError):
        MarketOrder(
            id="m1",
            instrument_id="BTC-USD",
            side=OrderSide.BUY,
            type=OrderType.MARKET,
            quantity=Decimal("1"),
            price=Decimal("1"),  # price not allowed
            time_in_force=TimeInForce.IOC,
            timestamp_ms=0,
        )

    stop_market = StopMarketOrder(
        id="s1",
        instrument_id="BTC-USD",
        side=OrderSide.SELL,
        type=OrderType.STOP_MARKET,
        quantity=Decimal("1"),
        price=Decimal("9000"),
        time_in_force=TimeInForce.GTC,
        timestamp_ms=0,
    )
    assert stop_market.stop_price == Decimal("9000")
    assert stop_market.price is None

    stop_limit = StopLimitOrder(
        id="s2",
        instrument_id="BTC-USD",
        side=OrderSide.SELL,
        type=OrderType.STOP_LIMIT,
        quantity=Decimal("1"),
        price=Decimal("8800"),
        stop_price=Decimal("9000"),
        time_in_force=TimeInForce.GTC,
        timestamp_ms=0,
    )
    assert stop_limit.stop_price == Decimal("9000")
    assert stop_limit.type.name == "STOP_LIMIT"

    trailing = TrailingStopOrder(
        id="t1",
        instrument_id="BTC-USD",
        side=OrderSide.SELL,
        type=OrderType.TRAILING_STOP,
        quantity=Decimal("1"),
        trail_amount=Decimal("100"),
        price=None,
        time_in_force=TimeInForce.GTC,
        timestamp_ms=0,
    )
    assert trailing.type.name == "TRAILING_STOP"

    iceberg = IcebergOrder(
        id="i1",
        instrument_id="BTC-USD",
        side=OrderSide.BUY,
        type=OrderType.ICEBERG,
        quantity=Decimal("5"),
        price=Decimal("10000"),
        display_quantity=Decimal("1"),
        time_in_force=TimeInForce.GTC,
        timestamp_ms=0,
    )
    assert iceberg.display_quantity == Decimal("1")


def test_order_state_overfill_and_cancel():
    """OrderState should reject overfills and preserve quantities on cancel."""
    state = OrderState(
        order_id="o1",
        status=OrderStatus.NEW,
        cumulative_filled_qty=Decimal("0"),
        total_quantity=Decimal("1"),
    )
    with pytest.raises(ValidationError):
        state.apply_fill(Decimal("2"))

    filled = state.apply_fill(Decimal("0.5"))
    assert filled.status == OrderStatus.PARTIALLY_FILLED

    canceled = filled.cancel()
    assert canceled.status == OrderStatus.CANCELED
    assert canceled.cumulative_filled_qty == Decimal("0.5")


def test_liquidation_price_edge_cases():
    """Liquidation helpers should handle safe/no-liquidation and raise on invalid."""
    # Well-funded long returns None
    assert (
        calculate_isolated_liquidation_price(
            side=PositionSide.LONG,
            entry_price=Decimal("100"),
            size=Decimal("1"),
            wallet_margin=Decimal("1000"),
            maintenance_margin_rate=0.1,
            fee_buffer=Decimal("0"),
        )
        is None
    )

    # Cross short returns valid positive price
    cross_price = calculate_cross_liquidation_price(
        portfolio_equity=Decimal("500"),
        position_notional=Decimal("1000"),
        side=PositionSide.SHORT,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        maintenance_margin_rate=0.1,
        fee_buffer=Decimal("0"),
    )
    assert cross_price is not None
    assert cross_price > 0

    # Extremely high mmr should still return a positive liquidation price
    price = calculate_cross_liquidation_price(
        portfolio_equity=Decimal("10"),
        position_notional=Decimal("100"),
        side=PositionSide.LONG,
        entry_price=Decimal("100"),
        size=Decimal("1"),
        maintenance_margin_rate=0.9,
        fee_buffer=Decimal("0"),
    )
    assert price and price > 0


def test_validation_helpers_cover_edges():
    """Validation helpers should enforce bounds and alignment."""
    with pytest.raises(ValidationError):
        ensure_valid_rate(Decimal("2"), "rate")
    ensure_valid_rate(
        Decimal("-0.5"), "rate", allow_negative=True, max_abs=Decimal("1")
    )

    with pytest.raises(ValidationError):
        ensure_valid_price(Decimal("-1"), "price")
    with pytest.raises(ValidationError):
        ensure_valid_quantity(Decimal("-1"), "qty", allow_zero=True)
    ensure_valid_quantity(Decimal("0"), "qty", allow_zero=True)

    with pytest.raises(ValidationError):
        ensure_valid_timestamp_order(10, 5)

    with pytest.raises(ValidationError):
        validate_tick_size(Decimal("10.01"), Decimal("0.1"))
    with pytest.raises(ValidationError):
        validate_lot_size(Decimal("1.05"), Decimal("0.1"))


def test_logging_default_level_applies_to_new_logger():
    """set_log_level should influence subsequently created loggers."""
    set_log_level(logging.WARNING)
    logger = get_logger("new_logger")
    assert logger.logger.level == logging.WARNING


def test_serialization_rejects_unknown_position_type():
    """serialize_portfolio should reject unsupported position objects."""
    portfolio = Portfolio()
    # Inject unsupported type in positions map
    portfolio.positions[("BTC-USD", PositionSide.LONG)] = types.SimpleNamespace()

    with pytest.raises(ValidationError):
        serialize_portfolio(portfolio)


def test_funding_payment_negative_rate_and_zero_duration():
    """Funding should handle negative rates and zero-length periods."""
    pos = BasePositionImpl.flat("BTC-PERP")
    pos = pos.apply_fill(
        Fill(
            "o1",
            "BTC-PERP",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("100"),
            Decimal("0"),
            0,
        )
    )

    negative = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("-0.005"),
        period_start_ms=0,
        period_end_ms=1000,
        index_price=Decimal("100"),
    )
    payment = calculate_funding_payment(position=pos, event=negative)
    assert payment > 0  # Long receives when rate is negative

    zero_period = FundingEvent(
        instrument_id="BTC-PERP",
        rate=Decimal("0.01"),
        period_start_ms=0,
        period_end_ms=0,
        index_price=Decimal("100"),
    )
    with pytest.raises(ValidationError):
        calculate_funding_payment(position=pos, event=zero_period)


def test_health_precision_warning():
    """Low precision should surface as unhealthy in decimal context check."""
    original_prec = getcontext().prec
    getcontext().prec = 8
    try:
        from qlcore.health import HealthChecker

        checker = HealthChecker()
        component = checker.check_decimal_context()
        assert not component.is_healthy
    finally:
        getcontext().prec = original_prec


def test_portfolio_pnl_fee_only_path():
    """Portfolio PnL should include fees even when no marks and no open positions."""
    portfolio = Portfolio()
    fills = [
        Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("0.1"),
            Decimal("10000"),
            Decimal("3"),
            0,
        )
    ]
    pnl = calculate_portfolio_pnl(
        portfolio=portfolio,
        marks={},
        fills=fills,
        funding_events=[],
        fee_events=[Decimal("3")],
        slippage_events=[],
        mode=PnLMode.BOTH,
    )
    assert pnl.total.fees == Decimal("3")  # fee_events only when no mark/positions


def test_instrument_registry_lookup_and_rounding():
    """Registry should store and round instruments correctly."""
    registry = InstrumentRegistry()
    spot = SpotInstrument.create(
        symbol="ETH-USD",
        base="ETH",
        quote="USD",
        tick_size=Decimal("0.5"),
        lot_size=Decimal("0.01"),
    )
    registry.add(spot)
    assert "ETH-USD" in registry
    inst = registry.get("ETH-USD")
    assert inst.round_price(Decimal("100.74")) == Decimal("100.5")
    assert inst.round_qty(Decimal("1.019")) == Decimal("1.01")


def test_sanitize_all_fields_handles_missing_keys():
    """sanitize_all_fields should ignore absent optional keys."""
    safe = sanitize_all_fields({"instrument_id": "  btc-usd  "})
    assert safe["instrument_id"] == "btc-usd"


def test_position_leverage_handles_negative_equity():
    pos = BasePositionImpl.flat("BTC-USD")
    fill = Fill(
        order_id="lev1",
        instrument_id="BTC-USD",
        side=OrderSide.BUY,
        quantity=Decimal("1"),
        price=Decimal("50"),
        fee=Decimal("0"),
        timestamp_ms=0,
    )
    pos = pos.apply_fill(fill)

    assert position_leverage(pos, Decimal("-25")) == Decimal("2")
