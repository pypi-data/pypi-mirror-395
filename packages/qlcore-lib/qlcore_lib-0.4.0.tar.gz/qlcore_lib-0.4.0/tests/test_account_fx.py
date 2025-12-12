from decimal import Decimal

from qlcore.portfolio.account import Account


def test_account_equity_with_rates():
    account = Account()
    account.deposit("USD", Decimal("100"))
    account.deposit("EUR", Decimal("50"))

    equity_native = account.equity()
    assert equity_native == Decimal("150")

    equity_usd = account.equity(base_currency="USD", rates={"EUR": Decimal("1.2")})
    assert equity_usd == Decimal("160")
