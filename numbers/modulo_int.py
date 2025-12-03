from __future__ import annotations
from math import gcd
from enum import Enum, auto
from typing import Generator, Tuple
class ModuloInt(int):
    """
    Integer modulo n.
    
    Supports +, -, *, //, %, **, unary -, comparisons, etc.
    """

    modulus: int

    def __new__(cls, value: int, modulus: int):
        if modulus <= 0:
            raise ValueError("Modulus must be a positive integer.")
        obj = super().__new__(cls, value % modulus)
        obj.modulus = modulus
        return obj

    # ------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------

    def _coerce(self, other):
        """Convert operand to a compatible ModuloInt."""
        if isinstance(other, ModuloInt):
            if other.modulus != self.modulus:
                raise ValueError(
                    f"Cannot operate on ModuloInt with different moduli "
                    f"({self.modulus} vs {other.modulus})"
                )
            return int(other)
        elif isinstance(other, int):
            return other
        return NotImplemented

    def opposite(self) -> ModuloInt:
        """Additive inverse modulo n."""
        return ModuloInt(-int(self), self.modulus)

    def inverse(self) -> ModuloInt:
        """Multiplicative inverse modulo n (requires gcd(self, n) == 1)."""
        a, n = int(self), self.modulus
        if gcd(a, n) != 1:
            raise ValueError(f"{a} has no multiplicative inverse modulo {n}.")
        # Using extended Euclidean algorithm
        t, new_t = 0, 1
        r, new_r = n, a
        while new_r != 0:
            q = r // new_r
            t, new_t = new_t, t - q * new_t
            r, new_r = new_r, r - q * new_r
        return ModuloInt(t, n)

    # ------------------------------------------------------------
    # Arithmetic operators
    # ------------------------------------------------------------

    def __add__(self, other):
        o = self._coerce(other)
        return ModuloInt(int(self) + o, self.modulus)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        o = self._coerce(other)
        return ModuloInt(int(self) - o, self.modulus)

    def __rsub__(self, other):
        o = self._coerce(other)
        return ModuloInt(o - int(self), self.modulus)

    def __mul__(self, other):
        o = self._coerce(other)
        return ModuloInt(int(self) * o, self.modulus)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        o = self._coerce(other)
        return ModuloInt(int(self) // o, self.modulus)

    def __mod__(self, other):
        o = self._coerce(other)
        return ModuloInt(int(self) % o, self.modulus)

    def __pow__(self, other, modulo=None):
        if modulo is not None:
            raise ValueError("Use built-in pow(a, b, n) instead of a**b with modulo.")
        o = self._coerce(other)
        return ModuloInt(pow(int(self), o, self.modulus), self.modulus)

    # ------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------
    def __repr__(self):
        return f"ModuloInt({int(self)} mod {self.modulus})"

class Direction(Enum):
    INCREASING = 1
    DECREASING = -1
    INCREASE = 1
    DECREASE = -1

class ModuloRangeMode(Enum):
    DETECT = auto()
    INFINITE = auto()

def modulo_range(
    start: int,
    stop: int,
    step: int,
    modulus: int,
    direction: Direction = Direction.INCREASING,
    max_range_amount: ModuloRangeMode | int | float = ModuloRangeMode.DETECT
) -> Generator[ModuloInt, None, None]:

    if step <= 0:
        raise ValueError("Step must be positive.")

    start_mod = ModuloInt(start, modulus)
    stop_mod = ModuloInt(stop, modulus)
    current = start_mod

    # --- Determine max iterations -----------------------------------

    if max_range_amount is ModuloRangeMode.INFINITE:
        max_iter = float("inf")

    elif max_range_amount is ModuloRangeMode.DETECT:
        # Length of cycle: modulus / gcd(modulus, step)
        cycle_len = modulus // gcd(modulus, step)
        max_iter = cycle_len + 1  # +1 to give stop chance to appear

    elif isinstance(max_range_amount, (int, float)):
        max_iter = int(max_range_amount)
        if max_iter <= 0:
            raise ValueError("max_range_amount must be positive.")
    else:
        raise TypeError("Invalid max_range_amount")

    # --- Determine step direction -----------------------------------

    step = abs(step)
    if direction == Direction.DECREASING:
        step = -step

    # --- Iteration loop ----------------------------------------------

    count = 0
    while current != stop_mod and count < max_iter:
        yield current
        current = ModuloInt(int(current) + step, modulus)
        count += 1