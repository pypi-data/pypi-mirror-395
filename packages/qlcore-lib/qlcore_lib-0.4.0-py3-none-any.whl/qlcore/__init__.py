"""qlcore - Pure trading math and domain models."""

__version__ = "0.4.0"

# Core types
from .core.types import Money, Price, Quantity, Rate, TimestampMs
from .core.constants import DEFAULT_DECIMAL_PRECISION, DEFAULT_BASE_CURRENCY
from .core.enums import OrderSide, PositionSide, OrderType, TimeInForce
from .core.protocols import BasePosition
from .core.exceptions import (
    qlcoreError,
    ValidationError,
    MathError,
    InsufficientMargin,
    PositionNotFound,
    InstrumentNotFound,
)

# Events
from .events import Fill, FundingEvent, FeeEvent, LiquidationEvent, SettlementEvent

# Positions
from .positions import (
    BasePositionImpl,
    SpotPosition,
    PerpetualPosition,
    FuturesPosition,
    mark_to_market,
    unrealized_pnl,
    leverage,
    Lot,
)

# Portfolio
from .portfolio import Account, Portfolio, Ledger, LedgerEntry, weights

# Orders
from .orders import (
    BaseOrder,
    OrderStatus,
    OrderState,
    MarketOrder,
    LimitOrder,
    StopMarketOrder,
    StopLimitOrder,
    TrailingStopOrder,
    IcebergOrder,
)

# Instruments
from .instruments import (
    InstrumentSpec,
    SpotInstrument,
    PerpetualInstrument,
    FuturesInstrument,
    OptionInstrument,
    OptionType,
    InstrumentRegistry,
)

# PnL
from .pnl import (
    PnLMode,
    PnLBreakdown,
    PortfolioPnL,
    pnl,
    portfolio_pnl,
    funding_payment,
    realized_pnl,
)

# Margin
from .margin import (
    MarginRequirements,
    MarginLevel,
    MarginSchedule,
    IsolatedMargin,
    initial_margin,
    maintenance_margin,
    free_margin,
    margin_utilization,
)

# Risk
from .risk import (
    sharpe_ratio,
    sortino_ratio,
    calmar_ratio,
    information_ratio,
    DAILY_PERIODS,
    WEEKLY_PERIODS,
    HOURLY_PERIODS,
    EIGHT_HOURLY_PERIODS,
    isolated_liquidation_price,
    cross_liquidation_price,
    net_exposure,
    gross_exposure,
    max_drawdown,
    historical_var,
)

# Sizing
from .sizing import (
    fixed_quantity,
    fixed_notional,
    percent_of_equity,
    risk_per_trade,
    atr_position_size,
    kelly_fraction,
    apply_position_limits,
)

# Fees
from .fees import (
    FeeSchedule,
    VipTier,
    calculate_fee,
    trade_fee,
    select_vip_tier,
    funding_fee,
)

# Pricing
from .pricing import mark_price, mid_price, vwap, estimate_slippage, annualize_rate

# Serialization (one way: to_json / from_json)
from .serialization import (
    to_dict,
    from_dict,
    to_json,
    from_json,
    save_to_file,
    load_from_file,
    encode_domain_object,
    decode_domain_object,
)

# Time
from .time import to_unix_ms, from_unix_ms, floor_timestamp_ms, TimePeriod

# Math
from .math import (
    round_price_to_tick,
    round_qty_to_lot,
    quantize_fee,
    simple_return,
    log_return,
    cumulative_return,
    annualized_return,
    returns_from_prices,
    mean,
    stddev,
    variance,
    realized_volatility,
    annualize_volatility,
)

# Builders
from .builders import PositionBuilder, FillBuilder

# Hooks
from .hooks import EventBus, on, off, emit

# Presets
from .presets import (
    crypto_portfolio,
    spot_portfolio,
    binance_btc_perp,
    binance_eth_perp,
    default_fee_schedule,
    backtest_config,
    live_config,
)

# Config & Health
from .config import get_config, set_config, qlcoreConfig
from .health import check_health, HealthChecker
from .bootstrap import init_qlcore, ConfigError, HealthCheckError

# Helpers
from .helpers import apply_fills

# Validators
from .validators import validate_fill_sequence, validate_portfolio_state

# Logging
from .utils.logging import (
    get_logger,
    get_audit_logger,
    set_log_level,
    disable_logging,
    enable_logging,
)

# Monitoring
from .monitoring.metrics import get_metrics, timed_operation, metric

# Security
from .security import (
    AuditTrail,
    AuditEvent,
    AuditEventType,
    RateLimiter,
    RateLimitExceeded,
    rate_limit,
)


__all__ = [
    # Version
    "__version__",
    # Core types
    "Money",
    "Price",
    "Quantity",
    "Rate",
    "TimestampMs",
    "DEFAULT_DECIMAL_PRECISION",
    "DEFAULT_BASE_CURRENCY",
    # Enums
    "OrderSide",
    "PositionSide",
    "OrderType",
    "TimeInForce",
    # Errors
    "qlcoreError",
    "ValidationError",
    "MathError",
    "InsufficientMargin",
    "PositionNotFound",
    "InstrumentNotFound",
    # Events
    "Fill",
    "FundingEvent",
    "FeeEvent",
    "LiquidationEvent",
    "SettlementEvent",
    # Positions
    "BasePosition",
    "BasePositionImpl",
    "SpotPosition",
    "PerpetualPosition",
    "FuturesPosition",
    "mark_to_market",
    "unrealized_pnl",
    "leverage",
    "Lot",
    # Portfolio
    "Account",
    "Portfolio",
    "Ledger",
    "LedgerEntry",
    "weights",
    # Orders
    "BaseOrder",
    "OrderStatus",
    "OrderState",
    "MarketOrder",
    "LimitOrder",
    "StopMarketOrder",
    "StopLimitOrder",
    "TrailingStopOrder",
    "IcebergOrder",
    # Instruments
    "InstrumentSpec",
    "SpotInstrument",
    "PerpetualInstrument",
    "FuturesInstrument",
    "OptionInstrument",
    "OptionType",
    "InstrumentRegistry",
    # PnL
    "PnLMode",
    "PnLBreakdown",
    "PortfolioPnL",
    "pnl",
    "portfolio_pnl",
    "funding_payment",
    "realized_pnl",
    # Margin
    "MarginRequirements",
    "MarginLevel",
    "MarginSchedule",
    "IsolatedMargin",
    "initial_margin",
    "maintenance_margin",
    "free_margin",
    "margin_utilization",
    # Risk
    "sharpe_ratio",
    "sortino_ratio",
    "calmar_ratio",
    "information_ratio",
    "DAILY_PERIODS",
    "WEEKLY_PERIODS",
    "HOURLY_PERIODS",
    "EIGHT_HOURLY_PERIODS",
    "isolated_liquidation_price",
    "cross_liquidation_price",
    "net_exposure",
    "gross_exposure",
    "max_drawdown",
    "historical_var",
    # Sizing
    "fixed_quantity",
    "fixed_notional",
    "percent_of_equity",
    "risk_per_trade",
    "atr_position_size",
    "kelly_fraction",
    "apply_position_limits",
    # Fees
    "FeeSchedule",
    "VipTier",
    "calculate_fee",
    "trade_fee",
    "select_vip_tier",
    "funding_fee",
    # Pricing
    "mark_price",
    "mid_price",
    "vwap",
    "estimate_slippage",
    "annualize_rate",
    # Serialization
    "to_dict",
    "from_dict",
    "to_json",
    "from_json",
    "save_to_file",
    "load_from_file",
    "encode_domain_object",
    "decode_domain_object",
    # Time
    "to_unix_ms",
    "from_unix_ms",
    "floor_timestamp_ms",
    "TimePeriod",
    # Math
    "round_price_to_tick",
    "round_qty_to_lot",
    "quantize_fee",
    "simple_return",
    "log_return",
    "cumulative_return",
    "annualized_return",
    "returns_from_prices",
    "mean",
    "stddev",
    "variance",
    "realized_volatility",
    "annualize_volatility",
    # Builders
    "PositionBuilder",
    "FillBuilder",
    # Hooks
    "EventBus",
    "on",
    "off",
    "emit",
    # Presets
    "crypto_portfolio",
    "spot_portfolio",
    "binance_btc_perp",
    "binance_eth_perp",
    "default_fee_schedule",
    "backtest_config",
    "live_config",
    # Config & Health
    "get_config",
    "set_config",
    "qlcoreConfig",
    "check_health",
    "HealthChecker",
    "init_qlcore",
    "ConfigError",
    "HealthCheckError",
    # Helpers
    "apply_fills",
    # Validators
    "validate_fill_sequence",
    "validate_portfolio_state",
    # Logging
    "get_logger",
    "get_audit_logger",
    "set_log_level",
    "disable_logging",
    "enable_logging",
    # Monitoring
    "get_metrics",
    "timed_operation",
    "metric",
    # Security
    "AuditTrail",
    "AuditEvent",
    "AuditEventType",
    "RateLimiter",
    "RateLimitExceeded",
    "rate_limit",
]
