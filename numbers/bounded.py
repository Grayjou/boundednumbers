"""Factory helpers for bounded integer types.

This module provides the :class:`BoundType` enum to describe the
bounding strategy and :func:`make_bounded_int` to generate subclasses of
``int`` that automatically enforce the selected behavior.
"""

from __future__ import annotations

from enum import Enum, auto

from .functions import bounce, clamp, cyclic_wrap
from .modulo_int import ModuloInt
from .types import RealNumber


class BoundType(Enum):
    """Available strategies for constraining integer values."""

    CLAMP = auto()
    CYCLIC = auto()
    BOUNCE = auto()
    MODULO = auto()  # pure 0..n-1 modular arithmetic


def _apply_bound(bound_type: BoundType, value: RealNumber, min_value: RealNumber, max_value: RealNumber):
    """Apply a bounding strategy to the provided value."""

    if bound_type == BoundType.CLAMP:
        return clamp(value, min_value, max_value)

    if bound_type == BoundType.CYCLIC:
        return cyclic_wrap(value, min_value, max_value)

    if bound_type == BoundType.BOUNCE:
        return bounce(value, min_value, max_value)

    raise ValueError("Invalid BoundType")


def make_bounded_int(bound_type: BoundType):
    """Return an ``int`` subclass that applies ``bound_type`` on every operation."""

    if bound_type == BoundType.MODULO:
        return ModuloInt

    def apply_bound(value, min_value, max_value):
        return _apply_bound(bound_type, value, min_value, max_value)

    class BoundedInt(int):
        """Auto-bounded integer for the chosen :class:`BoundType`."""

        min_value: RealNumber
        max_value: RealNumber

        def __new__(cls, value: RealNumber, min_value: RealNumber, max_value: RealNumber):
            bounded = apply_bound(value, min_value, max_value)

            # ``apply_bound`` returns a Python ``int`` OR a ``ModuloInt``
            obj = int.__new__(cls, int(bounded))
            obj.min_value = min_value
            obj.max_value = max_value
            return obj

        def _bounded(self, value):
            """Helper to apply bounds consistently."""

            return type(self)(value, self.min_value, self.max_value)

        def __add__(self, other):
            return self._bounded(int(self) + other)

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            return self._bounded(int(self) - other)

        def __mul__(self, other):
            return self._bounded(int(self) * other)

    BoundedInt.__name__ = f"{bound_type.name.capitalize()}Int"

    return BoundedInt


ClampedInt = make_bounded_int(BoundType.CLAMP)
CyclicInt = make_bounded_int(BoundType.CYCLIC)
BouncedInt = make_bounded_int(BoundType.BOUNCE)
ModuloBoundedInt = make_bounded_int(BoundType.MODULO)
