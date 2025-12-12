from __future__ import annotations

import re
from typing import Iterable, Tuple

from ..core.exceptions import ValidationError
from .validation import sanitize_instrument_id

_KNOWN_QUOTES: Tuple[str, ...] = (
    "USDT",
    "USDC",
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "BTC",
    "ETH",
    "AUD",
    "CAD",
    "CHF",
    "HKD",
    "SGD",
    "TRY",
    "BRL",
    "MXN",
    "ZAR",
    "NGN",
    "IDR",
    "KRW",
)

_MONTHS = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12",
}


def normalize_symbol(raw_symbol: str, *, market: str = "spot") -> str:
    """Convert an exchange/raw symbol into the canonical instrument_id.

    Canonical shapes:
    - Spot: BASE-QUOTE
    - Perp: BASE-QUOTE-PERP
    - Future: BASE-QUOTE-YYYYMMDD
    - Option: BASE-QUOTE-YYYYMMDD-STRIKE-C|P
    """
    if not isinstance(raw_symbol, str):
        raise ValidationError("symbol must be a string")

    symbol = raw_symbol.strip().upper()
    if not symbol:
        raise ValidationError("symbol cannot be empty")

    if market == "spot":
        canonical = _normalize_spot(symbol)
    elif market == "perp":
        canonical = _normalize_perp(symbol)
    elif market == "future":
        canonical = _normalize_future(symbol)
    elif market == "option":
        canonical = _normalize_option(symbol)
    else:
        raise ValidationError(f"unsupported market '{market}'")

    return sanitize_instrument_id(canonical)


def _normalize_spot(symbol: str) -> str:
    pair = _normalize_pair(symbol)
    return pair


def _normalize_perp(symbol: str) -> str:
    core = _strip_perp_markers(symbol)
    try:
        pair = _normalize_pair(core)
    except ValidationError:
        # Allow bare BASE-PERP symbols by preserving the base when no quote can be inferred
        return f"{core}-PERP"
    return f"{pair}-PERP"


def _normalize_future(symbol: str) -> str:
    pair_part, date_part = _split_date_suffix(symbol)
    pair = _normalize_pair(pair_part)
    expiry = _normalize_date(date_part)
    return f"{pair}-{expiry}"


def _normalize_option(symbol: str) -> str:
    try:
        core, opt_type = symbol.rsplit("-", 1)
    except ValueError as exc:
        raise ValidationError("option symbol must end with -C or -P") from exc

    if opt_type not in {"C", "P"}:
        raise ValidationError("option type must be C or P")

    try:
        core, strike_raw = core.rsplit("-", 1)
    except ValueError as exc:
        raise ValidationError("option symbol missing strike") from exc

    if not re.fullmatch(r"\d+(\.\d+)?", strike_raw):
        raise ValidationError("option strike must be numeric")

    underlying_raw, expiry_raw = _extract_expiry(core)
    pair = _normalize_pair(underlying_raw, default_quote="USD")
    expiry = _normalize_date(expiry_raw)
    return f"{pair}-{expiry}-{strike_raw}-{opt_type}"


def _normalize_pair(symbol: str, *, default_quote: str | None = None) -> str:
    """Normalize a base/quote pair into BASE-QUOTE."""
    candidate = symbol.split(":", 1)[0]
    candidate = candidate.strip("-_/")

    for sep in ("/", "-", "_"):
        if sep in candidate:
            parts = candidate.split(sep)
            if len(parts) >= 2:
                base, quote = parts[0], parts[1]
                return _format_pair(base, quote)

    return _split_compact_pair(candidate, default_quote=default_quote)


def _split_compact_pair(symbol: str, *, default_quote: str | None) -> str:
    for quote in _sorted_quotes():
        if symbol.endswith(quote):
            base = symbol[: -len(quote)]
            if not base:
                break
            return _format_pair(base, quote)

    if default_quote:
        if not symbol:
            raise ValidationError("base currency cannot be empty")
        return _format_pair(symbol, default_quote)

    raise ValidationError("could not infer quote currency from symbol")


def _format_pair(base: str, quote: str) -> str:
    base_clean = base.strip()
    quote_clean = quote.strip()
    if not base_clean or not quote_clean:
        raise ValidationError("base or quote currency missing")
    return f"{base_clean}-{quote_clean}"


def _strip_perp_markers(symbol: str) -> str:
    core = symbol
    for marker in (":USDT", ":USD", ":USDC"):
        if core.endswith(marker):
            core = core[: -len(marker)]
            break
    for marker in ("_SWAP", "_PERP", "-SWAP", "-PERP"):
        if core.endswith(marker):
            core = core[: -len(marker)]
            break
    if core.endswith("PERP") and len(core) > 4:
        core = core[:-4]
    return core


def _split_date_suffix(symbol: str) -> tuple[str, str]:
    for sep in ("-", "_"):
        if sep in symbol:
            left, right = symbol.rsplit(sep, 1)
            if _looks_like_date(right):
                return left.rstrip("-_/"), right

    match = re.search(r"(.+?)(\d{6}|\d{8})$", symbol)
    if match:
        return match.group(1).rstrip("-_/"), match.group(2)

    raise ValidationError("future symbol missing expiry date")


def _looks_like_date(value: str) -> bool:
    compact = re.sub(r"[/_-]", "", value)
    return bool(
        re.fullmatch(r"\d{6}", compact)
        or re.fullmatch(r"\d{8}", compact)
        or re.fullmatch(r"\d{1,2}[A-Z]{3}\d{2}", compact)
    )


def _normalize_date(raw: str) -> str:
    compact = re.sub(r"[\s/_-]", "", raw.upper())

    if re.fullmatch(r"\d{8}", compact):
        return compact
    if re.fullmatch(r"\d{6}", compact):
        return f"20{compact}"

    match = re.fullmatch(r"(\d{1,2})([A-Z]{3})(\d{2})", compact)
    if match:
        day, mon, year = match.groups()
        month_num = _MONTHS.get(mon)
        if not month_num:
            raise ValidationError(f"unknown month code '{mon}'")
        return f"20{year}{month_num}{day.zfill(2)}"

    raise ValidationError(f"unrecognized expiry date '{raw}'")


def _extract_expiry(core: str) -> tuple[str, str]:
    patterns = [
        r"(\d{4}[/_-]?\d{2}[/_-]?\d{2})$",
        r"(\d{6})$",
        r"(\d{1,2}[A-Z]{3}\d{2})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, core)
        if match:
            expiry = match.group(1)
            underlying = core[: match.start()].rstrip("-_/")
            if not underlying:
                raise ValidationError("option symbol missing underlying")
            return underlying, expiry

    raise ValidationError("option symbol missing expiry")


def _sorted_quotes() -> Iterable[str]:
    return sorted(_KNOWN_QUOTES, key=len, reverse=True)


def infer_market_from_symbol(symbol: str) -> str | None:
    """Best-effort market inference from a raw symbol."""
    upper = symbol.strip().upper()
    if not upper:
        return None

    if re.search(r"\d+(?:\.\d+)?-[CP]$", upper):
        return "option"

    if any(
        marker in upper
        for marker in (
            "-PERP",
            "_PERP",
            "_SWAP",
            "-SWAP",
            ":USDT",
            ":USD",
            ":USDC",
            "SWAP",
        )
    ):
        return "perp"

    # Futures often end with dates but no option suffix
    if re.search(r"(\d{6}|\d{8}|[0-9]{1,2}[A-Z]{3}\d{2})$", upper):
        return "future"

    return None
