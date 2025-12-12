from decimal import Decimal

from qlcore.pricing.index import index_price
from qlcore.pricing.funding_rate import annualize_rate


def test_index_price_passthrough_and_annualize():
    assert index_price(Decimal("100")) == Decimal("100")
    # simple annualization check
    ar = annualize_rate(Decimal("0.01"), periods_per_year=2)
    assert ar == (Decimal("1.01") ** 2) - 1
