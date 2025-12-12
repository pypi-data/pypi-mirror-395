"""Presets and factory functions for common setups.

Quick-start functions for common trading configurations.

Usage:
    from qlcore.presets import crypto_portfolio, binance_btc_perp
    
    portfolio = crypto_portfolio()
    instrument = binance_btc_perp()
"""

from __future__ import annotations

from decimal import Decimal

from .portfolio.portfolio import Portfolio
from .portfolio.account import Account
from .core.types import TimestampMs
from .instruments.perpetual import PerpetualInstrument
from .instruments.futures import FuturesInstrument
from .instruments.spot import SpotInstrument
from .fees import FeeSchedule, VipTier


def crypto_portfolio(
    base_currency: str = "USDT",
    initial_balance: Decimal | str | float = 10000,
) -> Portfolio:
    """Create a portfolio configured for crypto trading.

    Args:
        base_currency: Quote currency (default: USDT)
        initial_balance: Starting balance

    Example:
        >>> portfolio = crypto_portfolio(base_currency="USDT", initial_balance=10000)
        >>> portfolio.apply_fill(fill)
    """
    balance = Decimal(str(initial_balance))
    account = Account(
        base_currency=base_currency,
        balances={base_currency: balance},
    )
    return Portfolio(account=account)


def spot_portfolio(
    base_currency: str = "USD",
    initial_balance: Decimal | str | float = 100000,
) -> Portfolio:
    """Create a portfolio configured for spot/equity trading.

    Args:
        base_currency: Account currency (default: USD)
        initial_balance: Starting balance
    """
    balance = Decimal(str(initial_balance))
    account = Account(
        base_currency=base_currency,
        balances={base_currency: balance},
    )
    return Portfolio(account=account)


def binance_btc_perp() -> PerpetualInstrument:
    """Create Binance BTCUSDT perpetual instrument spec.

    Returns instrument with Binance-like parameters:
    - 8-hour funding interval
    - 0.001 tick size
    - 0.001 lot size
    """
    return PerpetualInstrument.create(
        symbol="BTCUSDT",
        base="BTC",
        quote="USDT",
        tick_size=Decimal("0.01"),
        lot_size=Decimal("0.001"),
        max_leverage=Decimal("125"),
        funding_interval_ms=8 * 60 * 60 * 1000,  # 8 hours
    )


def binance_eth_perp() -> PerpetualInstrument:
    """Create Binance ETHUSDT perpetual instrument spec."""
    return PerpetualInstrument.create(
        symbol="ETHUSDT",
        base="ETH",
        quote="USDT",
        tick_size=Decimal("0.01"),
        lot_size=Decimal("0.001"),
        max_leverage=Decimal("125"),
        funding_interval_ms=8 * 60 * 60 * 1000,
    )


def cme_btc_futures(expiry_ms: int) -> FuturesInstrument:
    """Create CME Bitcoin futures instrument spec.

    Args:
        expiry_ms: Expiration timestamp in milliseconds
    """
    return FuturesInstrument.create(
        symbol="BTC",
        base="BTC",
        quote="USD",
        tick_size=Decimal("5"),
        lot_size=Decimal("5"),  # 5 BTC per contract
        max_leverage=Decimal("50"),
        expiry_ms=TimestampMs(expiry_ms),
    )


def btc_spot() -> SpotInstrument:
    """Create BTC/USD spot instrument spec."""
    return SpotInstrument.create(
        symbol="BTC/USD",
        base="BTC",
        quote="USD",
        tick_size=Decimal("0.01"),
        lot_size=Decimal("0.00001"),
    )


def eth_spot() -> SpotInstrument:
    """Create ETH/USD spot instrument spec."""
    return SpotInstrument.create(
        symbol="ETH/USD",
        base="ETH",
        quote="USD",
        tick_size=Decimal("0.01"),
        lot_size=Decimal("0.0001"),
    )


def default_fee_schedule() -> FeeSchedule:
    """Create a typical crypto exchange fee schedule.

    Returns schedule with:
    - 0.1% maker fee
    - 0.1% taker fee
    """
    return FeeSchedule(
        maker_rate=Decimal("0.001"),
        taker_rate=Decimal("0.001"),
    )


def vip_fee_schedule(tier: int = 1) -> FeeSchedule:
    """Create VIP-tier fee schedule.

    Args:
        tier: VIP tier (1-9, higher = lower fees)
    """
    # Approximate Binance VIP tiers
    tiers = {
        1: (Decimal("0.0008"), Decimal("0.0009")),
        2: (Decimal("0.0006"), Decimal("0.0008")),
        3: (Decimal("0.0004"), Decimal("0.0007")),
        4: (Decimal("0.0002"), Decimal("0.0006")),
        5: (Decimal("0.0000"), Decimal("0.0005")),
    }
    maker, taker = tiers.get(tier, tiers[1])
    return FeeSchedule(maker_rate=maker, taker_rate=taker)


def backtest_config() -> dict:
    """Get recommended configuration for backtesting.

    Returns dict of settings optimized for backtesting speed.
    """
    return {
        "cost_basis_method": "AVERAGE",  # Faster than FIFO for many trades
        "track_lots": False,  # Skip lot tracking if not needed
        "validate_fills": True,
        "audit_logging": False,  # Disable for speed
    }


def live_config() -> dict:
    """Get recommended configuration for live trading.

    Returns dict of settings optimized for safety and auditability.
    """
    return {
        "cost_basis_method": "FIFO",
        "track_lots": True,
        "validate_fills": True,
        "audit_logging": True,
        "health_checks": True,
    }
