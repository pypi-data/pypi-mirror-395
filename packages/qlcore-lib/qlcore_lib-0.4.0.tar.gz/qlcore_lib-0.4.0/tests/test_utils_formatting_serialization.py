from dataclasses import dataclass
from decimal import Decimal

from qlcore.utils.formatting import format_decimal, format_percent
from qlcore.utils.serialization import to_dict, from_dict


@dataclass
class Sample:
    value: int
    text: str


def test_formatting_and_serialization():
    assert format_decimal(Decimal("1.2345"), precision=2) == "1.23"
    assert format_percent(Decimal("0.1234"), precision=1) == "12.3%"

    obj = Sample(1, "x")
    d = to_dict(obj)
    assert d["value"] == 1
    rebuilt = from_dict(Sample, d)
    assert isinstance(rebuilt, Sample)
