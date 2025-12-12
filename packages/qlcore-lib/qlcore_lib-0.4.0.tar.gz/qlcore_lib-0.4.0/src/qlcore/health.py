from __future__ import annotations

from dataclasses import dataclass, field
from decimal import getcontext, Decimal
from typing import List, Dict, Any
import sys
import time
import os

from .config import get_config
from .utils.logging import get_logger
from . import __version__
from .core.types import TimestampMs

logger = get_logger(__name__)


@dataclass
class ComponentHealth:
    """Health status of a single component."""

    name: str
    is_healthy: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    check_duration_ms: float = 0.0


@dataclass
class SystemHealth:
    """Overall system health status."""

    is_healthy: bool
    timestamp: float
    version: str
    components: List[ComponentHealth]
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "healthy": self.is_healthy,
            "timestamp": self.timestamp,
            "version": self.version,
            "components": [
                {
                    "name": c.name,
                    "healthy": c.is_healthy,
                    "message": c.message,
                    "details": c.details,
                    "check_duration_ms": c.check_duration_ms,
                }
                for c in self.components
            ],
            "errors": self.errors,
            "warnings": self.warnings,
        }


class HealthChecker:
    """System health checker."""

    def __init__(self) -> None:
        self.components: List[ComponentHealth] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def check_decimal_context(self) -> ComponentHealth:
        """Check decimal context configuration."""
        start = time.time()

        try:
            precision = getcontext().prec

            is_healthy = True
            message = f"Decimal precision: {precision}"
            details = {"precision": precision}

            if precision < 10:
                is_healthy = False
                message = f"Decimal precision too low: {precision} (minimum 10)"
                self.errors.append(message)
            elif precision < 20:
                self.warnings.append(
                    f"Decimal precision low: {precision} (recommended 28+)"
                )

            duration_ms = (time.time() - start) * 1000

            return ComponentHealth(
                name="decimal_context",
                is_healthy=is_healthy,
                message=message,
                details=details,
                check_duration_ms=duration_ms,
            )
        except Exception as e:  # defensive
            logger.error("Decimal context check failed", exc_info=True)
            return ComponentHealth(
                name="decimal_context",
                is_healthy=False,
                message=f"Check failed: {e}",
                details={},
                check_duration_ms=(time.time() - start) * 1000,
            )

    def check_imports(self) -> ComponentHealth:
        """Check that critical imports work."""
        start = time.time()

        try:
            # Try importing critical modules
            from .core import Money, Price, Quantity  # type: ignore  # noqa:F401
            from .positions.base import BasePositionImpl  # type: ignore  # noqa:F401
            from .portfolio import Portfolio  # type: ignore  # noqa:F401
            from .pnl import calculate_pnl  # type: ignore  # noqa:F401
            from .events.fill import Fill  # type: ignore  # noqa:F401

            is_healthy = True
            message = "All critical imports successful"
            details = {"modules_checked": 5}

            duration_ms = (time.time() - start) * 1000

            return ComponentHealth(
                name="imports",
                is_healthy=is_healthy,
                message=message,
                details=details,
                check_duration_ms=duration_ms,
            )
        except ImportError as e:
            logger.error("Import check failed", exc_info=True)
            error_msg = f"Import failed: {e}"
            self.errors.append(error_msg)
            return ComponentHealth(
                name="imports",
                is_healthy=False,
                message=error_msg,
                details={"error": str(e)},
                check_duration_ms=(time.time() - start) * 1000,
            )

    def check_configuration(self) -> ComponentHealth:
        """Check configuration validity."""
        start = time.time()

        try:
            config = get_config()
            errors = config.validate()

            is_healthy = len(errors) == 0
            message = (
                "Configuration valid"
                if is_healthy
                else f"Configuration errors: {len(errors)}"
            )
            details = {
                "decimal_precision": config.decimal_precision,
                "base_currency": config.base_currency,
                "log_level": config.log_level,
            }

            if errors:
                self.errors.extend(errors)
                details["validation_errors"] = errors

            duration_ms = (time.time() - start) * 1000

            return ComponentHealth(
                name="configuration",
                is_healthy=is_healthy,
                message=message,
                details=details,
                check_duration_ms=duration_ms,
            )
        except Exception as e:  # defensive
            logger.error("Configuration check failed", exc_info=True)
            error_msg = f"Check failed: {e}"
            self.errors.append(error_msg)
            return ComponentHealth(
                name="configuration",
                is_healthy=False,
                message=error_msg,
                details={"error": str(e)},
                check_duration_ms=(time.time() - start) * 1000,
            )

    def check_python_version(self) -> ComponentHealth:
        """Check Python version compatibility."""
        start = time.time()

        try:
            version = sys.version_info
            version_str = f"{version.major}.{version.minor}.{version.micro}"

            is_healthy = version.major == 3 and version.minor >= 11

            if is_healthy:
                message = f"Python version OK: {version_str}"
            else:
                message = f"Python version too old: {version_str} (require 3.11+)"
                self.errors.append(message)

            details = {
                "version": version_str,
                "major": version.major,
                "minor": version.minor,
                "micro": version.micro,
            }

            duration_ms = (time.time() - start) * 1000

            return ComponentHealth(
                name="python_version",
                is_healthy=is_healthy,
                message=message,
                details=details,
                check_duration_ms=duration_ms,
            )
        except Exception as e:  # defensive
            logger.error("Python version check failed", exc_info=True)
            return ComponentHealth(
                name="python_version",
                is_healthy=False,
                message=f"Check failed: {e}",
                details={},
                check_duration_ms=(time.time() - start) * 1000,
            )

    def check_basic_operations(self) -> ComponentHealth:
        """Test basic operations work correctly."""
        start = time.time()

        try:
            from .positions.base import BasePositionImpl
            from .events.fill import Fill
            from .core.enums import OrderSide
            from .core.types import Money, Price, Quantity

            # FIXED: Use valid instrument_id format
            pos = BasePositionImpl.flat("TEST-USD")
            fill = Fill(
                order_id="test",
                instrument_id="TEST-USD",  # FIXED: Changed from "TEST"
                side=OrderSide.BUY,
                quantity=Quantity(Decimal("1")),
                price=Price(Decimal("100")),
                fee=Money(Decimal("1")),
                timestamp_ms=TimestampMs(0),
            )
            pos = pos.apply_fill(fill)

            is_healthy = pos.size == Quantity(
                Decimal("1")
            ) and pos.avg_entry_price == Price(Decimal("100"))

            message = (
                "Basic operations work" if is_healthy else "Basic operations failed"
            )
            details = {
                "test_passed": is_healthy,
                "position_size": str(pos.size),
                "avg_entry": str(pos.avg_entry_price),
            }

            if not is_healthy:
                self.errors.append(message)

            duration_ms = (time.time() - start) * 1000

            return ComponentHealth(
                name="basic_operations",
                is_healthy=is_healthy,
                message=message,
                details=details,
                check_duration_ms=duration_ms,
            )
        except Exception as e:  # defensive
            logger.error("Basic operations check failed", exc_info=True)
            error_msg = f"Operations test failed: {e}"
            self.errors.append(error_msg)
            return ComponentHealth(
                name="basic_operations",
                is_healthy=False,
                message=error_msg,
                details={"error": str(e)},
                check_duration_ms=(time.time() - start) * 1000,
            )

    def run_all_checks(self, include_operations_test: bool = True) -> SystemHealth:
        """Run all health checks and return overall status.

        Args:
            include_operations_test: Whether to include basic operations test.

        Returns:
            SystemHealth with complete status.
        """
        logger.info("Running health checks")

        self.components = []
        self.errors = []
        self.warnings = []

        self.components.append(self.check_python_version())
        self.components.append(self.check_decimal_context())
        self.components.append(self.check_configuration())
        self.components.append(self.check_imports())

        if include_operations_test:
            self.components.append(self.check_basic_operations())

        is_healthy = all(c.is_healthy for c in self.components)

        health = SystemHealth(
            is_healthy=is_healthy,
            timestamp=time.time(),
            version=__version__,
            components=self.components,
            errors=self.errors,
            warnings=self.warnings,
        )

        if is_healthy:
            logger.info(
                "All health checks passed",
                components=len(self.components),
                warnings=len(self.warnings),
            )
        else:
            logger.error(
                "Health checks failed",
                failed_components=[c.name for c in self.components if not c.is_healthy],
                errors=len(self.errors),
            )

        return health


def check_health(include_operations_test: bool = True) -> SystemHealth:
    """Run health checks and return status."""
    checker = HealthChecker()
    return checker.run_all_checks(include_operations_test=include_operations_test)


def health_check_middleware(
    check_interval: float = 60.0,
    fail_on_unhealthy: bool = False,
) -> None:
    """Periodic health check for long-running processes.

    If fail_on_unhealthy is True, the process will be terminated (os._exit(1))
    when an unhealthy state is detected.
    """
    import threading

    def run_checks() -> None:
        while True:
            health = check_health()

            if not health.is_healthy:
                logger.warning(
                    "Periodic health check failed",
                    errors=health.errors,
                    warnings=health.warnings,
                )

                if fail_on_unhealthy:
                    logger.error(
                        "Health check marked unhealthy; terminating process",
                        errors=health.errors,
                    )
                    os._exit(1)

            time.sleep(check_interval)

    thread = threading.Thread(target=run_checks, daemon=True)
    thread.start()
    logger.info("Health check middleware started", interval=check_interval)
