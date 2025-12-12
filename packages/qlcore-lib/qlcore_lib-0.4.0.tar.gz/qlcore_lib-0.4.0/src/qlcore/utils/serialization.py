"""Serialization helpers."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass


def to_dict(obj):
    if is_dataclass(obj):
        return asdict(obj)
    raise TypeError("to_dict expects a dataclass instance")


def from_dict(cls, data: dict):
    return cls(**data)
