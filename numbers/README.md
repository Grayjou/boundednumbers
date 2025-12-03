# Bounded numeric helpers

This package provides a small set of numeric utilities that keep values within
explicit bounds. It is intended for simulations, games, and mathematical
experiments where out-of-range values can lead to bugs or unclear behavior.

## Contents

- **`bounded.py`** – Factory utilities that generate bounded integer and float
  subclasses using clamp, cyclic, bounce, or modulo semantics.
- **`modulo_int.py`** – A rich `ModuloInt` type with arithmetic, inversion, and
  modular range iteration helpers.
- **`modulo_float.py`** – `ModuloFloat` for modular floating-point math.
- **`unit_float.py`** – `UnitFloat` and `EnforcedUnitFloat` variants that stay in
  the `[0, 1]` interval.
- **`functions.py`** – Shared helpers such as `clamp`, `clamp01`, `bounce`,
  `cyclic_wrap`, and `cyclic_wrap_float` for range management.
- **`types.py`** – Shared type aliases for readability.

## Bounding strategies

### Clamp
Coerces values to the nearest boundary.
```python
from numbers import ClampedInt
score = ClampedInt(105, 0, 100)  # -> 100
score -= 250                     # -> 0
```

### Cyclic wrap
Wraps around when crossing a boundary (useful for angles and counters).
```python
from numbers import CyclicInt
angle = CyclicInt(-30, 0, 360)  # -> 330
angle += 45                     # -> 15
```

### Bounce
Reflects back into the interval when leaving it.
```python
from numbers import BouncedInt
position = BouncedInt(120, 0, 100)  # -> 80
position += 50                      # -> 50 (bounces at each edge)
```

### Modulo
Uses pure modular arithmetic over `[0, n)`.
```python
from numbers import ModuloBoundedInt
counter = ModuloBoundedInt(14, 10)  # -> 4
```

## Modular arithmetic helpers

`ModuloInt` exposes rich operations for modular math while validating moduli to
avoid subtle errors:

```python
from numbers import ModuloInt

x = ModuloInt(7, 26)
add_inverse = x.opposite()  # -> ModuloInt(19 mod 26)
mul_inverse = x.inverse()   # -> ModuloInt(15 mod 26)
```

Use `modulo_range` to iterate around a ring without repeating the stop value:

```python
from numbers import Direction, ModuloRangeMode, modulo_range

values = list(
    modulo_range(
        start=350,
        stop=170,
        step=40,
        modulus=360,
        direction=Direction.DECREASING,
        max_range_amount=ModuloRangeMode.DETECT,
    )
)
# -> [ModuloInt(350 mod 360), ModuloInt(310 mod 360), ModuloInt(270 mod 360)]
```

When you know how many steps you need, use `forced_amount` to avoid detection
logic:

```python
list(modulo_range(start=0, stop=0, step=3, modulus=10, forced_amount=5))
# -> [ModuloInt(0 mod 10), ModuloInt(3 mod 10), ...]
```

## Unit interval floats

`UnitFloat` coerces the input into `[0, 1]` once, while `EnforcedUnitFloat`
reapplies the bounds after every arithmetic operation to keep results safe.

```python
from numbers import EnforcedUnitFloat

opacity = EnforcedUnitFloat(1.4)  # -> 1.0
opacity -= 3.2                    # -> 0.0
```

## Factory helpers

For custom class names or number types, use the factories in `bounded.py`:

```python
from numbers import BoundType, make_bounded_int, make_default_bounded_float

Wrapped = make_bounded_int(lambda v, mn, mx: max(mn, min(v, mx)), class_name="Wrapped")
value = Wrapped(5, 0, 3)  # -> 3

CyclicFloat = make_default_bounded_float(BoundType.CYCLIC)
angle = CyclicFloat(725.0, 0.0, 360.0)  # -> 5.0
```

## Utility functions

All bounding behaviors are also available as standalone helpers for native
numbers:

```python
from numbers import bounce, clamp, clamp01, cyclic_wrap, cyclic_wrap_float

clamp(12, 0, 10)             # -> 10
bounce(-7, -5, 5)            # -> 3
cyclic_wrap(370, 0, 360)     # -> 10
cyclic_wrap_float(8.5, 0, 2) # -> 0.5
```
