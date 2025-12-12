"""Namespace shortcuts for organized imports.

Usage:
    import qlcore as qc
    
    # Access everything through organized namespaces
    qc.Portfolio()
    qc.Fill.create(...)
    qc.positions.PerpetualPosition
    qc.risk.sharpe_ratio()
    qc.math.round_price_to_tick()
"""

from importlib import import_module
from types import SimpleNamespace

# Re-export top-level items for direct access
from . import (
    Portfolio,
    Account,
    Fill,
    FundingEvent,
    FeeEvent,
    SettlementEvent,
    LiquidationEvent,
)

# Organized namespaces
from . import positions as _positions_module
from . import instruments as _instruments_module
from . import risk as _risk_module
from . import sizing as _sizing_module
from . import fees as _fees_module
_pnl_module = import_module("qlcore.pnl")
from . import margin as _margin_module
from . import math as _math_module
from . import time as _time_module
_json_codec = import_module("qlcore.serialization.json_codec")

# Create namespace objects for organized access
positions = SimpleNamespace(
    BasePositionImpl=_positions_module.BasePositionImpl,
    SpotPosition=_positions_module.SpotPosition,
    PerpetualPosition=_positions_module.PerpetualPosition,
    FuturesPosition=_positions_module.FuturesPosition,
    Lot=_positions_module.Lot,
    mark_to_market=_positions_module.mark_to_market,
    unrealized_pnl=_positions_module.unrealized_pnl,
    leverage=_positions_module.leverage,
)

instruments = SimpleNamespace(
    InstrumentSpec=_instruments_module.InstrumentSpec,
    SpotInstrument=_instruments_module.SpotInstrument,
    PerpetualInstrument=_instruments_module.PerpetualInstrument,
    FuturesInstrument=_instruments_module.FuturesInstrument,
    OptionInstrument=_instruments_module.OptionInstrument,
    OptionType=_instruments_module.OptionType,
    InstrumentRegistry=_instruments_module.InstrumentRegistry,
)

risk = SimpleNamespace(
    sharpe_ratio=_risk_module.sharpe_ratio,
    sortino_ratio=_risk_module.sortino_ratio,
    max_drawdown=_risk_module.max_drawdown,
    historical_var=_risk_module.historical_var,
    net_exposure=_risk_module.net_exposure,
    gross_exposure=_risk_module.gross_exposure,
    calculate_isolated_liquidation_price=_risk_module.calculate_isolated_liquidation_price,
    calculate_cross_liquidation_price=_risk_module.calculate_cross_liquidation_price,
)

sizing = SimpleNamespace(
    fixed_quantity=_sizing_module.fixed_quantity,
    fixed_notional=_sizing_module.fixed_notional,
    percent_of_equity=_sizing_module.percent_of_equity,
    risk_per_trade=_sizing_module.risk_per_trade,
    atr_position_size=_sizing_module.atr_position_size,
    kelly_fraction=_sizing_module.kelly_fraction,
    apply_position_limits=_sizing_module.apply_position_limits,
)

fees = SimpleNamespace(
    calculate_fee=_fees_module.calculate_fee,
    FeeSchedule=_fees_module.FeeSchedule,
    fee_for_trade=_fees_module.fee_for_trade,
    funding_fee=_fees_module.funding_fee,
    VipTier=_fees_module.VipTier,
    select_vip_tier=_fees_module.select_vip_tier,
)

pnl = SimpleNamespace(
    calculate_pnl=_pnl_module.calculate_pnl,
    calculate_portfolio_pnl=_pnl_module.calculate_portfolio_pnl,
    calculate_funding_payment=_pnl_module.calculate_funding_payment,
    realized_pnl=_pnl_module.realized_pnl,
    unrealized_pnl=_pnl_module.unrealized_pnl,
    PnLMode=_pnl_module.PnLMode,
    PnLBreakdown=_pnl_module.PnLBreakdown,
    PortfolioPnL=_pnl_module.PortfolioPnL,
)

margin = SimpleNamespace(
    calculate_initial_margin=_margin_module.calculate_initial_margin,
    calculate_maintenance_margin=_margin_module.calculate_maintenance_margin,
    free_margin=_margin_module.free_margin,
    margin_utilization=_margin_module.margin_utilization,
    MarginRequirements=_margin_module.MarginRequirements,
    MarginLevel=_margin_module.MarginLevel,
    MarginSchedule=_margin_module.MarginSchedule,
    IsolatedMargin=_margin_module.IsolatedMargin,
)

math = SimpleNamespace(
    round_price_to_tick=_math_module.round_price_to_tick,
    round_qty_to_lot=_math_module.round_qty_to_lot,
    quantize_fee=_math_module.quantize_fee,
    simple_return=_math_module.simple_return,
    log_return=_math_module.log_return,
    cumulative_return=_math_module.cumulative_return,
    mean=_math_module.mean,
    stddev=_math_module.stddev,
    variance=_math_module.variance,
    realized_volatility=_math_module.realized_volatility,
    annualize_volatility=_math_module.annualize_volatility,
)

time = SimpleNamespace(
    to_unix_ms=_time_module.to_unix_ms,
    from_unix_ms=_time_module.from_unix_ms,
    to_milliseconds=_time_module.to_milliseconds,
    floor_timestamp_ms=_time_module.floor_timestamp_ms,
    TimePeriod=_time_module.TimePeriod,
)

serialization = SimpleNamespace(
    serialize_position=_json_codec.serialize_position,
    deserialize_position=_json_codec.deserialize_position,
    serialize_portfolio=_json_codec.serialize_portfolio,
    deserialize_portfolio=_json_codec.deserialize_portfolio,
    serialize_fill=_json_codec.serialize_fill,
    deserialize_fill=_json_codec.deserialize_fill,
    to_json=_json_codec.to_json,
    from_json=_json_codec.from_json,
    save_to_file=_json_codec.save_to_file,
    load_from_file=_json_codec.load_from_file,
)
