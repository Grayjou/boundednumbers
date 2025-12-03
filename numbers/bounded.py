
from enum import Enum, auto
from .modulo_int import ModuloInt
from .functions import clamp, bounce, cyclic_wrap
from .types import RealNumber

class BoundType(Enum):
    CLAMP = auto()
    CYCLIC = auto()
    BOUNCE = auto()
    MODULO = auto()   # pure 0..n-1 modular arithmetic

def make_bounded_int(bound_type: BoundType):
    """
    Factory that generates int subclasses with a specific bounding behavior.
    """

    if bound_type == BoundType.MODULO:
        return ModuloInt

    def apply_bound(value, min_value, max_value):
        if bound_type == BoundType.CLAMP:
            return clamp(value, min_value, max_value)

        elif bound_type == BoundType.CYCLIC:
            return cyclic_wrap(value, min_value, max_value)

        elif bound_type == BoundType.BOUNCE:
            return bounce(value, min_value, max_value)

        else:
            raise ValueError("Invalid BoundType")

    class BoundedInt(int):

        """
        Auto-bounded integer for the chosen BoundType.
        """
        min_value: RealNumber
        max_value: RealNumber

        def __new__(cls, value: RealNumber, min_value: RealNumber, max_value: RealNumber):
            bounded = apply_bound(value, min_value, max_value)

            # apply_bound returns a Python int OR a ModuloInt
            obj = int.__new__(cls, int(bounded))
            obj.min_value = min_value
            obj.max_value = max_value
            return obj

        # Helper to apply bounds consistently
        def _bounded(self, value):
            return type(self)(value, self.min_value, self.max_value)

        # Basic operator example—expand as needed
        def __add__(self, other):
            return self._bounded(int(self) + other)

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            return self._bounded(int(self) - other)

        def __mul__(self, other):
            return self._bounded(int(self) * other)

    # Give each class a nice name
    BoundedInt.__name__ = f"{bound_type.name.capitalize()}Int"

    return BoundedInt

# Predefined bounded int types
ClampedInt = make_bounded_int(BoundType.CLAMP)
CyclicInt = make_bounded_int(BoundType.CYCLIC)
BouncedInt = make_bounded_int(BoundType.BOUNCE)
ModuloBoundedInt = make_bounded_int(BoundType.MODULO)