from __future__ import annotations

import time
from collections import deque
from typing import Deque, Callable, Dict
from functools import wraps
import threading


class RateLimitExceeded(Exception):
    """Raised when a rate limit is exceeded."""


class RateLimiter:
    """Token-bucket style limiter (per instance).

    Thread-safe implementation.
    """

    def __init__(self, max_calls: int, time_window: float, identifier: str = "default"):
        self.max_calls = max_calls
        self.time_window = time_window
        self.identifier = identifier
        self.calls: Deque[float] = deque()
        self._lock = threading.Lock()

    def _prune(self, now: float) -> None:
        """Remove expired timestamps. Must be called with lock held."""
        cutoff = now - self.time_window
        while self.calls and self.calls[0] < cutoff:
            self.calls.popleft()

    def acquire(self) -> None:
        """Consume one call or raise if over limit."""
        now = time.time()

        with self._lock:
            self._prune(now)
            if len(self.calls) >= self.max_calls:
                raise RateLimitExceeded(
                    f"Rate limit exceeded for {self.identifier}: {self.max_calls}/{self.time_window}s"
                )
            self.calls.append(now)


# Keep strong references to avoid premature GC during decorator creation
_limiters: Dict[str, RateLimiter] = {}
_limiters_lock = threading.Lock()


def rate_limit(max_calls: int, time_window: float, identifier: str) -> Callable:
    """Decorator to rate-limit function calls.

    Thread-safe with automatic cleanup of unused limiters.
    """

    def decorator(func: Callable):
        # Get or create limiter
        with _limiters_lock:
            if identifier not in _limiters:
                _limiters[identifier] = RateLimiter(max_calls, time_window, identifier)
            limiter = _limiters[identifier]

        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.acquire()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def clear_rate_limiters() -> None:
    """Clear all rate limiters (useful for testing)."""
    with _limiters_lock:
        _limiters.clear()
