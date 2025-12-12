"""Decimal context configuration."""

from decimal import getcontext

# Export the global decimal context so callers can configure it explicitly.
# Precision should be set once at process startup (for example via qlcoreConfig),
# not implicitly on import.
ctx = getcontext()
