from decimal import getcontext
import threading
import logging
import time

import pytest


from qlcore.config import (
    qlcoreConfig,
    get_config,
    set_config,
    reset_config,
)
from qlcore.bootstrap import init_qlcore, ConfigError, HealthCheckError
from qlcore.health import SystemHealth


def test_config_from_env(monkeypatch):
    """Test loading config from environment without implicit global side effects."""
    monkeypatch.setenv("qlcore_DECIMAL_PRECISION", "34")
    monkeypatch.setenv("qlcore_BASE_CURRENCY", "EUR")
    monkeypatch.setenv("qlcore_LOG_LEVEL", "DEBUG")

    # Reset to force reload from env
    reset_config()

    original_prec = getcontext().prec

    cfg = qlcoreConfig.from_env()
    assert cfg.decimal_precision == 34
    assert cfg.base_currency == "EUR"
    assert cfg.log_level == "DEBUG"

    # from_env should NOT mutate global decimal context by itself
    assert getcontext().prec == original_prec

    # Applying decimal context should update global precision
    cfg.apply_decimal_context()
    assert getcontext().prec == 34

    # Cleanup
    getcontext().prec = original_prec
    reset_config()


def test_config_presets():
    """Test preset configurations."""
    dev = qlcoreConfig.development()
    assert dev.log_level == "DEBUG"
    assert dev.enable_performance_logging is True

    prod = qlcoreConfig.production()
    assert prod.decimal_precision == 34
    assert prod.log_level == "INFO"

    test = qlcoreConfig.testing()
    assert test.log_level == "ERROR"
    assert test.enable_audit_logging is False


def test_config_override():
    """Test overriding config values (pure config object)."""
    cfg = qlcoreConfig()
    original_prec = getcontext().prec

    # Override should only change the config object
    cfg.override(decimal_precision=50, log_level="WARNING")
    assert cfg.decimal_precision == 50
    assert cfg.log_level == "WARNING"

    # Global decimal context should remain unchanged until explicitly applied
    assert getcontext().prec == original_prec

    # When we apply the context, precision should update
    cfg.apply_decimal_context()
    assert getcontext().prec == 50

    # Reset global state
    getcontext().prec = original_prec
    reset_config()


def test_config_validation():
    """Test config validation."""
    cfg = qlcoreConfig(decimal_precision=5)
    errors = cfg.validate()
    assert any("decimal_precision too low" in e for e in errors)

    cfg = qlcoreConfig(log_level="INVALID")
    errors = cfg.validate()
    assert any("Invalid log_level" in e for e in errors)


def test_config_singleton():
    """Test global config singleton."""
    reset_config()

    # Seed global config explicitly (no more lazy creation)
    base_cfg = qlcoreConfig.development()
    set_config(base_cfg)

    cfg1 = get_config()
    cfg2 = get_config()

    assert cfg1 is cfg2
    assert cfg1 is base_cfg

    reset_config()


def test_init_qlcore_helper():
    """Test bootstrap helper for one-shot initialization."""

    original_prec = getcontext().prec
    reset_config()
    logger = logging.getLogger("qlcore")
    original_level = logger.level

    # Use named environment, not a qlcoreConfig instance
    cfg = init_qlcore("testing", run_health_checks=False)

    # init_qlcore should:
    # - return a qlcoreConfig
    # - install it as the global config
    assert isinstance(cfg, qlcoreConfig)
    assert get_config() is cfg

    # It should match the testing preset
    preset = qlcoreConfig.testing()
    assert cfg.decimal_precision == preset.decimal_precision
    assert cfg.log_level == preset.log_level
    assert cfg.base_currency == preset.base_currency

    # Decimal precision should be applied
    assert getcontext().prec == preset.decimal_precision

    # Cleanup
    logger.setLevel(original_level)
    getcontext().prec = original_prec
    reset_config()


def test_init_qlcore_accepts_explicit_config():
    """init_qlcore should accept a provided qlcoreConfig and apply logging."""
    original_prec = getcontext().prec
    reset_config()

    cfg = qlcoreConfig(decimal_precision=45, base_currency="EUR", log_level="WARNING")
    logger = logging.getLogger("qlcore")
    original_level = logger.level

    result = init_qlcore(env="development", run_health_checks=False, config=cfg)

    assert result is cfg
    assert get_config() is cfg
    assert getcontext().prec == 45
    assert logger.level == logging.WARNING

    logger.setLevel(original_level)
    getcontext().prec = original_prec
    reset_config()


def test_init_qlcore_raises_on_invalid_config():
    """init_qlcore should raise ConfigError instead of exiting on bad config."""
    reset_config()

    bad_cfg = qlcoreConfig(log_level="INVALID")

    with pytest.raises(ConfigError):
        init_qlcore(env="testing", run_health_checks=False, config=bad_cfg)

    reset_config()


def test_init_qlcore_raises_on_failed_health_check(monkeypatch):
    """init_qlcore should raise HealthCheckError when health checks fail."""
    original_prec = getcontext().prec
    reset_config()

    cfg = qlcoreConfig.testing()
    logger = logging.getLogger("qlcore")
    original_level = logger.level

    def fake_health(
        include_operations_test: bool = True,
    ) -> SystemHealth:  # noqa: ARG001
        return SystemHealth(
            is_healthy=False,
            timestamp=time.time(),
            version="test",
            components=[],
            errors=["boom"],
            warnings=["warn"],
        )

    monkeypatch.setattr("qlcore.bootstrap.check_health", fake_health)

    with pytest.raises(HealthCheckError) as exc_info:
        init_qlcore(env="testing", run_health_checks=True, config=cfg)

    assert exc_info.value.health.errors == ["boom"]

    logger.setLevel(original_level)
    getcontext().prec = original_prec
    reset_config()


def test_config_thread_safety():
    """Test config is thread-safe (singleton per process)."""
    reset_config()

    # Ensure config is initialised before threads start calling get_config()
    seed = qlcoreConfig.testing()
    set_config(seed)

    results = []

    def get_config_thread():
        cfg = get_config()
        results.append(cfg)

    threads = [threading.Thread(target=get_config_thread) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All threads should get the same config instance
    assert len({id(r) for r in results}) == 1
    assert results and results[0] is seed

    reset_config()
