"""Utility functions for constraining numeric values."""

from __future__ import annotations

from .types import RealNumber


def clamp(value: RealNumber, min_value: RealNumber, max_value: RealNumber) -> RealNumber:
    """Clamp a value between ``min_value`` and ``max_value``."""

    return max(min(value, max_value), min_value)


def clamp01(value: RealNumber) -> RealNumber:
    """Clamp a value to the inclusive range ``[0, 1]``."""

    return clamp(value, 0.0, 1.0)


def bounce(value: RealNumber, min_value: RealNumber, max_value: RealNumber) -> RealNumber:
    """Bounce a value within a specified range."""

    range_size = max_value - min_value
    if range_size <= 0:
        raise ValueError("max_value must be greater than min_value")

    mod_value = (value - min_value) % (2 * range_size)
    if mod_value > range_size:
        return max_value - (mod_value - range_size)

    return min_value + mod_value


def cyclic_wrap(value: RealNumber, min_value: RealNumber, max_value: RealNumber) -> RealNumber:
    """Wrap inside ``[min_value, max_value]`` like a cyclic range."""

    size = max_value - min_value + 1
    return (value - min_value) % size + min_value
