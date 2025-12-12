"""Instrument specification registry."""

from __future__ import annotations

from typing import Dict
from .base import InstrumentSpec


class InstrumentRegistry:
    """In-memory registry for instrument specs."""

    def __init__(self) -> None:
        self._registry: Dict[str, InstrumentSpec] = {}

    def add(self, spec: InstrumentSpec) -> None:
        self._registry[spec.instrument_id] = spec

    def get(self, instrument_id: str) -> InstrumentSpec:
        return self._registry[instrument_id]

    def __contains__(
        self, instrument_id: str
    ) -> bool:  # pragma: no cover - simple passthrough
        return instrument_id in self._registry
