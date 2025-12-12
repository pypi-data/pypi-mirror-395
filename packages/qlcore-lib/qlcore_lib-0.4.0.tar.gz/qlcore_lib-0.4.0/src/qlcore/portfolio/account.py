"""Account balances and equity calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict

from ..core.constants import DEFAULT_BASE_CURRENCY
from ..core.types import Money
from ..core.exceptions import ValidationError


class _EquityView:
    """Callable/operable wrapper around Account equity.

    Allows both attribute-style arithmetic (account.equity + x) and
    callable conversion (account.equity(base_currency="USD", rates=...)).
    """

    def __init__(self, account: "Account") -> None:
        self._account = account

    def _value(self) -> Money:
        return self._account._compute_equity()

    def __call__(
        self,
        *,
        base_currency: str | None = None,
        rates: Dict[str, Decimal] | None = None,
    ) -> Money:
        return self._account._compute_equity(base_currency=base_currency, rates=rates)

    def __add__(self, other):
        return self._value() + other

    def __radd__(self, other):
        return other + self._value()

    def __sub__(self, other):
        return self._value() - other

    def __rsub__(self, other):
        return other - self._value()

    def __lt__(self, other):
        return self._value() < other

    def __le__(self, other):
        return self._value() <= other

    def __gt__(self, other):
        return self._value() > other

    def __ge__(self, other):
        return self._value() >= other

    def __eq__(self, other):
        return self._value() == other

    def __float__(self) -> float:  # pragma: no cover - convenience
        return float(self._value())

    def __repr__(self) -> str:
        return f"{self._value()!r}"

    def __str__(self) -> str:
        return str(self._value())


@dataclass
class Account:
    """Multi-currency trading account with basic FX conversion support.

    Tracks balances per currency and provides an equity view that can be
    summed natively or converted using provided FX rates.

    Conventions:
        - Positive cash flow = money into the account
        - Negative cash flow = money out of the account
    """

    base_currency: str = DEFAULT_BASE_CURRENCY
    balances: Dict[str, Money] = field(default_factory=dict)
    unrealized_pnl: Money = Decimal(0)
    _equity_view: _EquityView = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Ensure base currency bucket exists
        if self.base_currency not in self.balances:
            self.balances[self.base_currency] = Money(Decimal(0))
        self._equity_view = _EquityView(self)

    def _ensure_currency(self, currency: str) -> str:
        code = currency.upper()
        if code not in self.balances:
            self.balances[code] = Money(Decimal(0))
        return code

    @property
    def balance(self) -> Money:
        """Aggregate balance across all currencies (native sum)."""
        return Money(sum(Decimal(v) for v in self.balances.values()))

    @property
    def equity(self) -> _EquityView:
        """Return equity view (callable for FX conversion)."""
        return self._equity_view

    def _compute_equity(
        self,
        *,
        base_currency: str | None = None,
        rates: Dict[str, Decimal] | None = None,
    ) -> Money:
        """Compute equity optionally converting to a base currency."""
        rates = rates or {}
        if base_currency is None:
            return Money(self.balance + Decimal(self.unrealized_pnl))

        total = Decimal(0)
        target = base_currency.upper()
        for currency, amount in self.balances.items():
            if currency == target:
                total += Decimal(amount)
            else:
                if currency not in rates:
                    raise ValidationError(f"missing rate for {currency}->{target}")
                total += Decimal(amount) * Decimal(rates[currency])

        total += Decimal(self.unrealized_pnl)
        return Money(total)

    def update_unrealized_pnl(self, value: Money) -> None:
        """Set unrealized PnL (used when marking positions to market)."""
        self.unrealized_pnl = Money(Decimal(value))

    def apply_cash_flow(self, amount: Money, currency: str | None = None) -> None:
        """Apply a signed cash flow in the specified currency.

        Positive = cash into the account
        Negative = cash out of the account
        """
        code = self._ensure_currency(currency or self.base_currency)
        self.balances[code] = Money(
            Decimal(self.balances.get(code, 0)) + Decimal(amount)
        )

    def deposit(
        self, currency_or_amount: Money | str, amount: Money | None = None
    ) -> None:
        """Increase balance by a non-negative deposit amount.

        Accepts either:
            deposit(Decimal("100"))          # uses base currency, adds 100
            deposit("EUR", Decimal("50"))    # adds 50 EUR to existing EUR balance

        In both forms, the deposit is additive. Use set_balance(...) if you need
        to hard-set a balance for tests or admin operations.
        """
        if amount is None:
            currency = self.base_currency
            value = currency_or_amount
        else:
            currency = str(currency_or_amount)
            value = amount

        if Decimal(value) < 0:
            raise ValidationError("deposit amount must be non-negative")

        # Always additive, regardless of whether a currency is provided.
        code = self._ensure_currency(currency)
        self.balances[code] = Money(
            Decimal(self.balances.get(code, 0)) + Decimal(value)
        )

    def set_balance(self, currency: str, amount: Money) -> None:
        """Hard-set a currency balance (primarily for tests/admin tooling)."""
        code = self._ensure_currency(currency)
        self.balances[code] = Money(Decimal(amount))

    def withdraw(
        self, currency_or_amount: Money | str, amount: Money | None = None
    ) -> None:
        """Withdraw funds, ensuring sufficient balance."""
        if amount is None:
            currency = self.base_currency
            value = currency_or_amount
        else:
            currency = str(currency_or_amount)
            value = amount

        code = self._ensure_currency(currency)
        if Decimal(value) < 0:
            raise ValidationError("withdraw amount must be non-negative")
        current = Decimal(self.balances.get(code, 0))
        if Decimal(value) > current:
            raise ValidationError("insufficient funds")
        self.balances[code] = Money(current - Decimal(value))
