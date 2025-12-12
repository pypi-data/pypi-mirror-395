from __future__ import annotations

import logging
import threading
from typing import Any, Optional
from decimal import Decimal
from datetime import datetime


class qlcoreLogger:
    """Structured logger for qlcore operations."""

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        # Never auto-add handlers - let the application configure logging
        self.logger.propagate = True

    def _format_value(self, value: Any) -> str:
        """Format value for logging (handles Decimal, etc.)."""
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    def debug(self, message: str, **context: Any) -> None:
        """Log debug message with context."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.debug(message)

    def info(self, message: str, **context: Any) -> None:
        """Log info message with context."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.info(message)

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message with context."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False, **context: Any) -> None:
        """Log error message with context."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False, **context: Any) -> None:
        """Log critical message with context."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.critical(message, exc_info=exc_info)


class AuditLogger:
    """Specialized logger for audit trail of financial operations."""

    def __init__(self):
        self.logger = logging.getLogger("qlcore.audit")
        self.logger.setLevel(logging.INFO)
        # Never auto-add handlers
        self.logger.propagate = True

    def _format_value(self, value: Any) -> str:
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    def info(self, message: str, **context: Any) -> None:
        """Generic structured info logging for audit events."""
        if context:
            ctx_str = " | ".join(
                f"{k}={self._format_value(v)}" for k, v in context.items()
            )
            message = f"{message} | {ctx_str}"
        self.logger.info(message)

    def log_fill(
        self,
        order_id: str,
        instrument_id: str,
        side: str,
        quantity: Decimal,
        price: Decimal,
        fee: Decimal,
        user_id: Optional[str] = None,
    ) -> None:
        """Log fill execution."""
        self.logger.info(
            f"FILL | order={order_id} | instrument={instrument_id} | "
            f"side={side} | qty={quantity} | price={price} | fee={fee} | "
            f"user={user_id or 'system'}"
        )

    def log_funding(
        self,
        instrument_id: str,
        rate: Decimal,
        payment: Decimal,
        period_start: int,
        period_end: int,
    ) -> None:
        """Log funding payment."""
        self.logger.info(
            f"FUNDING | instrument={instrument_id} | rate={rate} | "
            f"payment={payment} | period={period_start}-{period_end}"
        )

    def log_withdrawal(
        self,
        currency: str,
        amount: Decimal,
        user_id: Optional[str] = None,
    ) -> None:
        """Log withdrawal."""
        self.logger.info(
            f"WITHDRAWAL | currency={currency} | amount={amount} | "
            f"user={user_id or 'system'}"
        )

    def log_deposit(
        self,
        currency: str,
        amount: Decimal,
        user_id: Optional[str] = None,
    ) -> None:
        """Log deposit."""
        self.logger.info(
            f"DEPOSIT | currency={currency} | amount={amount} | "
            f"user={user_id or 'system'}"
        )


_local = threading.local()
_audit_logger: Optional[AuditLogger] = None
_default_log_level: int = logging.INFO
_logger_lock = threading.Lock()


def get_logger(name: str, level: Optional[int] = None) -> qlcoreLogger:
    """Get or create a logger for a module.

    Thread-safe logger creation.
    """
    if not hasattr(_local, "loggers"):
        _local.loggers = {}

    effective_level = level if level is not None else _default_log_level

    if name not in _local.loggers:
        _local.loggers[name] = qlcoreLogger(name, effective_level)
    elif level is not None:
        _local.loggers[name].logger.setLevel(effective_level)

    return _local.loggers[name]


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger."""
    global _audit_logger
    if _audit_logger is None:
        with _logger_lock:
            if _audit_logger is None:
                _audit_logger = AuditLogger()
    return _audit_logger


def set_log_level(level: int) -> None:
    """Set log level for all qlcore loggers."""
    global _default_log_level
    _default_log_level = level

    # Update existing loggers in current thread
    if hasattr(_local, "loggers"):
        for logger in _local.loggers.values():
            logger.logger.setLevel(level)

    if _audit_logger is not None:
        _audit_logger.logger.setLevel(level)

    logging.getLogger("qlcore").setLevel(level)


def disable_logging() -> None:
    """Disable all qlcore logging (useful for tests)."""
    logging.getLogger("qlcore").disabled = True


def enable_logging() -> None:
    """Re-enable qlcore logging."""
    logging.getLogger("qlcore").disabled = False
