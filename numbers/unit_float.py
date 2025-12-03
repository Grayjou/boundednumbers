
from __future__ import annotations
from typing import Union
from .types import RealNumber
from .functions import clamp01 as _clamp01

class UnitFloat(float):
    def __new__(cls, value: RealNumber):
        if not 0.0 <= value <= 1.0:
            value = _clamp01(value)
        return super().__new__(cls, value)
    def __repr__(self):
        return f"UnitFloat({float(self)})"
    

class EnforcedUnitFloat(UnitFloat):
    """
    A UnitFloat that auto-clamps all arithmetic results.
    """
    # Helper to wrap numeric results

    def __float__(self) -> float:
        return super().__float__()

    @staticmethod
    def _wrap(value: RealNumber) -> "EnforcedUnitFloat":
        return EnforcedUnitFloat(_clamp01(float(value)))

    def _coerce(self, other: RealNumber) -> float:
        if isinstance(other, (EnforcedUnitFloat, UnitFloat, float, int, RealNumber)):
            return float(other)
        return NotImplemented

    # ------------------------------------------------------------
    # Arithmetic (auto-clamping)
    # ------------------------------------------------------------

    def __add__(self, other):
        o = self._coerce(other)
        return self._wrap(float(self) + o)

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        return self._wrap(float(self) - o)

    def __rsub__(self, other):
        o = self._coerce(other)
        return self._wrap(o - float(self))

    def __mul__(self, other):
        o = self._coerce(other)
        return self._wrap(float(self) * o)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._coerce(other)
        return self._wrap(float(self) / o)

    def __rtruediv__(self, other):
        o = self._coerce(other)
        return self._wrap(o / float(self))

    def __pow__(self, other):
        o = self._coerce(other)
        return self._wrap(float(self) ** o)

    # ------------------------------------------------------------
    # Pretty representation
    # ------------------------------------------------------------
    def __repr__(self):
        return f"EnforcedUnitFloat({float(self)})"