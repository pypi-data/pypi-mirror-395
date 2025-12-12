import logging
from decimal import Decimal

from qlcore.utils.logging import (
    get_logger,
    get_audit_logger,
    set_log_level,
    disable_logging,
    enable_logging,
)


def test_get_logger():
    """Test logger creation."""
    logger = get_logger("test_module")
    assert logger.logger.name == "test_module"

    # Same logger instance
    logger2 = get_logger("test_module")
    assert logger is logger2


def test_logger_methods(caplog):
    """Test logger methods."""
    logger = get_logger("test_logger", level=logging.DEBUG)

    with caplog.at_level(logging.DEBUG):
        logger.debug("Debug message", value=Decimal("100"))
        logger.info("Info message", key="value")
        logger.warning("Warning message")

    assert "Debug message" in caplog.text
    assert "value=100" in caplog.text
    assert "Info message" in caplog.text


def test_audit_logger():
    """Test audit logger."""
    audit = get_audit_logger()

    audit.log_fill(
        order_id="o1",
        instrument_id="BTC-USD",
        side="BUY",
        quantity=Decimal("1"),
        price=Decimal("10000"),
        fee=Decimal("10"),
        user_id="user123",
    )

    audit.log_funding(
        instrument_id="BTC-PERP",
        rate=Decimal("0.0001"),
        payment=Decimal("-1"),
        period_start=0,
        period_end=1000,
    )


def test_log_level_control():
    """Test log level changes."""
    set_log_level(logging.ERROR)
    logger = get_logger("test_level")
    assert logger.logger.level == logging.ERROR


def test_disable_enable_logging():
    """Test disabling and enabling logging."""
    disable_logging()
    assert logging.getLogger("qlcore").disabled

    enable_logging()
    assert not logging.getLogger("qlcore").disabled
