# qlcore

[![PyPI](https://img.shields.io/pypi/v/qlcore-lib)](https://pypi.org/project/qlcore-lib/)
[![Python](https://img.shields.io/pypi/pyversions/qlcore-lib)](https://pypi.org/project/qlcore-lib/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

**Pure trading math and domain models** — orders, positions, portfolio, PnL, sizing, risk, margin, and fees.

## Why qlcore?

- **Pure computation** — No I/O, no network, no database. Just math.
- **Decimal-safe** — All calculations use Python's `Decimal` for financial precision.
- **Immutable positions** — Positions are frozen dataclasses; audit-friendly and thread-safe.
- **Type-safe** — PEP 561 compliant with full type annotations.
- **Zero dependencies** — Core functionality requires only Python 3.11+ standard library.

## Installation

```bash
pip install qlcore-lib
```

With optional monitoring support:

```bash
pip install qlcore-lib[monitoring]
```

## Quick Start

```python
import qlcore as qc

# Create a portfolio with USDT balance
portfolio = qc.crypto_portfolio(initial_balance=10_000)

# Record a fill (trade execution)
fill = qc.Fill.create(
    order_id="order-001",
    instrument_id="BTC-USDT-PERP",
    side=qc.OrderSide.BUY,
    quantity="0.1",
    price="45000",
    fee="4.5",
    timestamp_ms=1701849600000,
)

# Apply fill to portfolio
portfolio = portfolio.apply_fill(fill)

# Check position
position = portfolio.positions["BTC-USDT-PERP"]
print(position.summary())

# Calculate unrealized PnL at current price
upnl = qc.unrealized_pnl(position, current_price="46000")
print(f"Unrealized PnL: {upnl}")
```

## Key Features

### Positions
```python
# Three position types
qc.SpotPosition        # Spot/equity holdings
qc.PerpetualPosition   # Perpetual futures with funding
qc.FuturesPosition     # Expiring futures contracts

# Fluent builder pattern
position = (
    qc.PositionBuilder("BTC-PERP")
    .long()
    .with_size("1.5")
    .with_entry_price("45000")
    .as_perpetual()
    .build()
)
```

### Risk Metrics
```python
returns = [0.02, -0.01, 0.03, -0.02, 0.01]
qc.sharpe_ratio(returns, risk_free_rate=0.0)
qc.sortino_ratio(returns, risk_free_rate=0.0)
qc.max_drawdown(returns)
qc.historical_var(returns, confidence=0.95)
```

### Position Sizing
```python
# Risk-based sizing
size = qc.risk_per_trade(
    equity=10000,
    risk_percent="0.02",
    entry_price="45000",
    stop_price="44000",
)

# Kelly fraction
kelly = qc.kelly_fraction(win_rate=0.55, avg_win=100, avg_loss=80)
```

### Margin Calculations
```python
initial = qc.calculate_initial_margin(
    notional="45000",
    leverage=10,
)

maintenance = qc.calculate_maintenance_margin(
    notional="45000",
    rate="0.005",
)
```

## Organized Imports

```python
import qlcore as qc

# Namespaced access
qc.positions.PerpetualPosition
qc.risk.sharpe_ratio()
qc.sizing.kelly_fraction()
qc.margin.calculate_initial_margin()
qc.fees.calculate_fee()
qc.pnl.calculate_portfolio_pnl()
qc.math.round_price_to_tick()
qc.time.to_unix_ms()
qc.serialization.to_json()
```

## Documentation

- [Getting Started](docs/quickstart.md)
- [Core Concepts](docs/concepts.md)
- [API Reference](docs/api/index.md)
- [Cookbook](docs/cookbook.md)

## Development

```bash
# Install with dev dependencies
pip install -e .[dev]

# Run tests
PYTHONPATH=src pytest --cov=qlcore

# Type checking
PYTHONPATH=src mypy --config-file mypy.ini src
```

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
