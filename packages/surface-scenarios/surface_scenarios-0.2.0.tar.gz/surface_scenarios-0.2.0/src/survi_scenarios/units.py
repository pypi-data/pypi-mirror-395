"""Tiny unit shim to keep SurfaceParams API stable."""
from __future__ import annotations
from enum import Enum

class Unit(str, Enum):
    METERS = "m"


def convert_unit(value: float, src: Unit, dst: Unit) -> float:
    if src == dst:
        return value
    raise ValueError(f"Unsupported unit conversion {src} -> {dst}")

__all__ = ["Unit", "convert_unit"]
