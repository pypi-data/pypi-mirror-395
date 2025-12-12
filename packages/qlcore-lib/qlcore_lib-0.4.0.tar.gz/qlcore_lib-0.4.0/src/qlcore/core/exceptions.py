"""Custom exceptions used throughout qlcore."""


class qlcoreError(Exception):
    """Base class for all qlcore-specific errors."""


class ValidationError(qlcoreError):
    """Raised when inputs are invalid or invariants are violated."""


class MathError(qlcoreError):
    """Raised when math operations fail or produce invalid results."""


class InsufficientMargin(qlcoreError):
    """Raised when a margin requirement cannot be satisfied."""


class MarginViolationError(InsufficientMargin):
    """Raised when a margin requirement is explicitly violated."""


class PositionNotFound(qlcoreError):
    """Raised when a requested position is missing."""


class InstrumentNotFound(qlcoreError):
    """Raised when a requested instrument is missing."""


class InvalidFillError(ValidationError):
    """Raised when a fill is malformed or fails validation."""


class InconsistentPortfolioError(ValidationError):
    """Raised when portfolio/account invariants are violated."""
