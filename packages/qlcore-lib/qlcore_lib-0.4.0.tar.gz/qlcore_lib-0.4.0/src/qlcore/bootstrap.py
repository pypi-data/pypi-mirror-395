from __future__ import annotations

import logging
import os
import sys
from typing import Literal

from .config import qlcoreConfig, set_config, get_config
from .health import SystemHealth, check_health
from .core.exceptions import qlcoreError
from .utils.logging import get_logger

logger = get_logger(__name__)

EnvName = Literal["development", "production", "testing"]
EnvInput = Literal["dev", "development", "prod", "production", "test", "testing"]

ENV_ALIASES: dict[str, EnvName] = {
    "dev": "development",
    "development": "development",
    "test": "testing",
    "testing": "testing",
    "prod": "production",
    "production": "production",
}


class ConfigError(qlcoreError):
    """Raised when qlcore configuration is invalid."""


class HealthCheckError(qlcoreError):
    """Raised when initial health checks fail."""

    def __init__(self, health: SystemHealth):
        self.health = health
        super().__init__("Initial health check failed")


def _normalise_env(env: str | None) -> EnvName:
    """Map user-friendly env names to canonical ones."""
    if env is None:
        return "production"
    env_lower = env.lower()
    mapped = ENV_ALIASES.get(env_lower)
    if mapped is None:
        logger.warning("Unknown qlcore_ENV, defaulting to production", env=env)
        return "production"
    return mapped


def _build_config(env: EnvName) -> qlcoreConfig:
    """Create a qlcoreConfig for the given environment, with env overrides."""
    if env == "development":
        config = qlcoreConfig.development()
    elif env == "testing":
        config = qlcoreConfig.testing()
    else:
        # default to production
        config = qlcoreConfig.production()

    # Overlay environment-specific overrides only when explicitly provided
    overrides: dict[str, object] = {}
    env_decimal_precision = os.getenv("qlcore_DECIMAL_PRECISION")
    if env_decimal_precision is not None:
        overrides["decimal_precision"] = int(env_decimal_precision)

    env_base_currency = os.getenv("qlcore_BASE_CURRENCY")
    if env_base_currency is not None:
        overrides["base_currency"] = env_base_currency

    env_log_level = os.getenv("qlcore_LOG_LEVEL")
    if env_log_level is not None:
        overrides["log_level"] = env_log_level

    env_strict_validation = os.getenv("qlcore_STRICT_VALIDATION")
    if env_strict_validation is not None:
        overrides["strict_validation"] = env_strict_validation.lower() == "true"

    if overrides:
        config.override(**overrides)
    return config


def _validate_or_raise(config: qlcoreConfig) -> None:
    """Validate config or raise a ConfigError."""
    errors = config.validate()
    if errors:
        for err in errors:
            logger.error("Configuration error", error=err)
        raise ConfigError(", ".join(errors))


def _apply_decimal_context(config: qlcoreConfig) -> None:
    """Apply global decimal precision once at process startup."""
    config.apply_decimal_context()
    logger.info("Decimal precision set", precision=config.decimal_precision)


def _log_effective_config(config: qlcoreConfig) -> None:
    """Log the effective configuration at startup."""
    cfg_dict = config.to_dict()
    logger.info("qlcore configuration initialised", **cfg_dict)


def init_qlcore(
    env: EnvInput | None = None,
    *,
    run_health_checks: bool = True,
    config: qlcoreConfig | None = None,
) -> qlcoreConfig:
    """Application entry point to initialise qlcore.

    Typical usage at process startup:

        from qlcore.bootstrap import init_qlcore

        config = init_qlcore()
        # continue with app startup...

    Steps:
        1. Determine environment (env argument overrides qlcore_ENV). Accepts "dev"/"development", "test"/"testing", "prod"/"production".
        2. Build config for env + environment overrides, unless a config is provided explicitly.
        3. Validate config and raise ConfigError on error.
        4. Apply global decimal context ONCE and configure logging.
        5. Install as global config via set_config().
        6. Optionally run health checks and raise HealthCheckError on failure.
    """
    raw_env = env if env is not None else os.getenv("qlcore_ENV", "production")
    env_name = _normalise_env(raw_env)

    if config is None:
        logger.info("Initialising qlcore", env=env_name)
        config = _build_config(env_name)
    else:
        logger.info("Initialising qlcore with provided config", env=env_name)

    _validate_or_raise(config)
    _apply_decimal_context(config)
    config.apply_logging()

    # Install as global config
    set_config(config)
    _log_effective_config(get_config())

    if run_health_checks:
        health = check_health(include_operations_test=(env_name != "testing"))
        if not health.is_healthy:
            logger.error(
                "Initial health check failed",
                errors=health.errors,
                warnings=health.warnings,
                failed_components=[
                    c.name for c in health.components if not c.is_healthy
                ],
            )
            raise HealthCheckError(health)

    logger.info("qlcore initialised successfully")
    return config


if __name__ == "__main__":
    # CLI bootstrap entry for:
    #   python -m qlcore.bootstrap
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    try:
        init_qlcore()
    except (ConfigError, HealthCheckError):
        logger.error("qlcore failed to initialise", exc_info=True)
        sys.exit(1)
