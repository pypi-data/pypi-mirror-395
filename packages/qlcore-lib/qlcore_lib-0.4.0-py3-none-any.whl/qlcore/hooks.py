"""Event hooks system for qlcore.

Provides a simple pub/sub mechanism for hooking into library events.

Usage:
    from qlcore.hooks import on, emit, EventBus
    
    # Global hooks
    @on("fill_applied")
    def log_fill(fill, portfolio):
        print(f"Applied: {fill}")
    
    # Or use instance-based bus
    bus = EventBus()
    bus.on("fill", handler)
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Dict, List


# Type alias for event handlers
EventHandler = Callable[..., Any]


class EventBus:
    """Simple event bus for pub/sub pattern.

    Example:
        >>> bus = EventBus()
        >>> @bus.on("fill")
        ... def handle_fill(fill):
        ...     print(f"Received fill: {fill}")
        >>> bus.emit("fill", fill=my_fill)
    """

    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)

    def on(self, event: str, handler: EventHandler | None = None) -> EventHandler:
        """Register a handler for an event.

        Can be used as decorator or direct call:
            @bus.on("fill")
            def handler(fill): ...

            # or
            bus.on("fill", handler)
        """

        def decorator(fn: EventHandler) -> EventHandler:
            self._handlers[event].append(fn)
            return fn

        if handler is not None:
            return decorator(handler)
        return decorator

    def off(self, event: str, handler: EventHandler | None = None) -> None:
        """Remove handler(s) for an event.

        If handler is None, removes all handlers for the event.
        """
        if handler is None:
            self._handlers[event] = []
        else:
            self._handlers[event] = [h for h in self._handlers[event] if h != handler]

    def emit(self, event: str, **kwargs: Any) -> None:
        """Emit an event to all registered handlers."""
        for handler in self._handlers[event]:
            try:
                handler(**kwargs)
            except Exception:
                # Don't let handler errors break the chain
                pass

    def clear(self) -> None:
        """Remove all handlers."""
        self._handlers.clear()


# Global event bus instance
_global_bus = EventBus()


def on(event: str, handler: EventHandler | None = None) -> EventHandler:
    """Register a global event handler.

    Example:
        @on("fill_applied")
        def log_fill(fill, portfolio):
            print(f"Applied {fill}")
    """
    return _global_bus.on(event, handler)


def off(event: str, handler: EventHandler | None = None) -> None:
    """Remove global event handler(s)."""
    _global_bus.off(event, handler)


def emit(event: str, **kwargs: Any) -> None:
    """Emit a global event."""
    _global_bus.emit(event, **kwargs)


def clear() -> None:
    """Clear all global handlers."""
    _global_bus.clear()


# Common event names
EVENTS = {
    "fill_applied": "Emitted after a fill is applied to portfolio",
    "funding_applied": "Emitted after funding is applied",
    "position_opened": "Emitted when a new position is opened",
    "position_closed": "Emitted when a position is fully closed",
    "position_flipped": "Emitted when position flips from long to short or vice versa",
    "pnl_realized": "Emitted when P&L is realized",
    "margin_warning": "Emitted when margin utilization exceeds threshold",
}
