from __future__ import annotations

import os
import logging
import threading
from decimal import Decimal, getcontext
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class qlcoreConfig:
    """Global configuration for qlcore.

    This object is now *side-effect free* on creation:
    - It does NOT change the global decimal context.
    - It does NOT touch logging.

    Callers must explicitly:
        - config.apply_decimal_context()  at process startup
        - config.apply_logging()          if they want log level wired in

    Note on Decimal Context:
        Decimal context is GLOBAL to the Python interpreter, not thread-local.
        Changing decimal_precision affects ALL threads. Set it once at startup.
    """

    # Decimal precision for calculations
    decimal_precision: int = 28

    # Default base currency
    base_currency: str = "USD"

    # Logging configuration
    log_level: str = "INFO"
    enable_audit_logging: bool = True

    # Validation strictness
    strict_validation: bool = True
    warn_on_extreme_values: bool = True

    # Performance settings
    enable_performance_logging: bool = False

    # Safety limits
    max_position_size: Optional[Decimal] = None
    max_notional: Optional[Decimal] = None
    max_leverage: Optional[Decimal] = field(default_factory=lambda: Decimal("1000"))

    # __post_init__ intentionally does NOT apply any global side effects.
    def __post_init__(self) -> None:
        pass

    # ---- Side-effect methods (call explicitly from bootstrap or app) ----

    def apply_decimal_context(self) -> None:
        """Set global decimal context precision.

        WARNING: This affects the entire Python interpreter, not just this thread.
        Call once at application startup.
        """
        getcontext().prec = self.decimal_precision

    def apply_logging(self) -> None:
        """Configure qlcore logger levels.

        This only adjusts logger levels; it does not add handlers.
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        level = level_map.get(self.log_level.upper(), logging.INFO)

        # Only set level, don't add handlers
        logger = logging.getLogger("qlcore")
        logger.setLevel(level)

        if self.enable_audit_logging:
            audit_logger = logging.getLogger("qlcore.audit")
            audit_logger.setLevel(logging.INFO)

    # ---- Construction helpers ----

    @classmethod
    def from_env(cls) -> "qlcoreConfig":
        """Load configuration from environment variables.

        Environment variables:
            qlcore_DECIMAL_PRECISION: Decimal precision (default: 28)
            qlcore_BASE_CURRENCY: Default currency (default: USD)
            qlcore_LOG_LEVEL: Logging level (default: INFO)
            qlcore_STRICT_VALIDATION: Enable strict validation (default: true)
            qlcore_WARN_EXTREME: Warn on extreme values (default: true)
            qlcore_ENABLE_AUDIT: Enable audit logging (default: true)
            qlcore_MAX_LEVERAGE: Maximum allowed leverage (default: 1000)

        Returns:
            qlcoreConfig instance
        """
        return cls(
            decimal_precision=int(os.getenv("qlcore_DECIMAL_PRECISION", "28")),
            base_currency=os.getenv("qlcore_BASE_CURRENCY", "USD"),
            log_level=os.getenv("qlcore_LOG_LEVEL", "INFO"),
            strict_validation=os.getenv("qlcore_STRICT_VALIDATION", "true").lower()
            == "true",
            warn_on_extreme_values=os.getenv("qlcore_WARN_EXTREME", "true").lower()
            == "true",
            enable_audit_logging=os.getenv("qlcore_ENABLE_AUDIT", "true").lower()
            == "true",
            max_leverage=Decimal(os.getenv("qlcore_MAX_LEVERAGE", "1000")),
        )

    @classmethod
    def development(cls) -> "qlcoreConfig":
        """Create development configuration with verbose logging."""
        return cls(
            decimal_precision=28,
            base_currency="USD",
            log_level="DEBUG",
            strict_validation=True,
            warn_on_extreme_values=True,
            enable_audit_logging=True,
            enable_performance_logging=True,
        )

    @classmethod
    def production(cls) -> "qlcoreConfig":
        """Create production configuration with stricter / safer defaults."""
        return cls(
            decimal_precision=34,  # Higher precision for production
            base_currency="USD",
            log_level="INFO",
            strict_validation=True,
            warn_on_extreme_values=True,
            enable_audit_logging=True,
            enable_performance_logging=False,
        )

    @classmethod
    def testing(cls) -> "qlcoreConfig":
        """Create testing configuration with minimal logging noise."""
        return cls(
            decimal_precision=28,
            base_currency="USD",
            log_level="ERROR",
            strict_validation=True,
            warn_on_extreme_values=False,
            enable_audit_logging=False,
            enable_performance_logging=False,
        )

    # ---- Mutation (no implicit global side effects) ----

    def override(self, **kwargs) -> None:
        """Override configuration values in place.

        NOTE:
            This now ONLY mutates the instance fields.
            It does NOT change decimal context or logging globally.
            Call apply_decimal_context()/apply_logging() yourself if needed.
        """
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Unknown configuration key: {key}")
            setattr(self, key, value)

    # ---- Validation / export ----

    def validate(self) -> list[str]:
        """Validate configuration values.

        Returns:
            List of validation errors (empty if valid)
        """
        errors: list[str] = []

        if self.decimal_precision < 10:
            errors.append(
                f"decimal_precision too low: {self.decimal_precision} (min 10)"
            )
        if self.decimal_precision > 100:
            errors.append(
                f"decimal_precision too high: {self.decimal_precision} (max 100)"
            )

        if not self.base_currency or len(self.base_currency) < 2:
            errors.append(f"Invalid base_currency: {self.base_currency}")

        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid log_level: {self.log_level}")

        if self.max_leverage and self.max_leverage < Decimal("1"):
            errors.append(f"max_leverage must be >= 1, got {self.max_leverage}")

        return errors

    def to_dict(self) -> dict:
        """Export configuration as dictionary."""
        return {
            "decimal_precision": self.decimal_precision,
            "base_currency": self.base_currency,
            "log_level": self.log_level,
            "enable_audit_logging": self.enable_audit_logging,
            "strict_validation": self.strict_validation,
            "warn_on_extreme_values": self.warn_on_extreme_values,
            "enable_performance_logging": self.enable_performance_logging,
            "max_position_size": (
                str(self.max_position_size) if self.max_position_size else None
            ),
            "max_notional": str(self.max_notional) if self.max_notional else None,
            "max_leverage": str(self.max_leverage),
        }


# ---- Thread-safe global configuration ----

_config: Optional[qlcoreConfig] = None
_config_lock = threading.RLock()


def get_config() -> qlcoreConfig:
    """Return the global configuration instance.

    This no longer auto-creates a config.
    You must call set_config() or qlcore.bootstrap.init_qlcore() at startup.
    """
    global _config
    with _config_lock:
        if _config is None:
            raise RuntimeError(
                "qlcore configuration has not been initialised. "
                "Call qlcore.bootstrap.init_qlcore() or set_config() "
                "at process startup."
            )
        return _config


def set_config(config: qlcoreConfig) -> None:
    """Install the global configuration instance.

    Intended to be called exactly once at process startup
    (typically from qlcore.bootstrap.init_qlcore()).
    """
    global _config
    errors = config.validate()
    if errors:
        raise ValueError(f"Invalid configuration: {', '.join(errors)}")

    with _config_lock:
        if _config is not None:
            raise RuntimeError(
                "Global qlcoreConfig is already set. "
                "Use reset_config() in tests before re-initialising."
            )
        _config = config


def reset_config() -> None:
    """Testing helper: clear global config.

    This allows tests to install a fresh config. Do not use in production flows.
    """
    global _config
    with _config_lock:
        _config = None
