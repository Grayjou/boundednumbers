# Bounded numeric helpers

This package provides a small set of numeric utilities that keep values within
explicit bounds. It is intended for simulations, games, and mathematical
experiments where out-of-range values can lead to bugs or unclear behavior.

## Contents

- **`bounded.py`** – Factory utilities that generate bounded integer subclasses
  using clamp, cyclic, bounce, or modulo semantics.
- **`modulo_int.py`** – A rich `ModuloInt` type with arithmetic, inversion, and
  modular range iteration helpers.
- **`unit_float.py`** – `UnitFloat` and `EnforcedUnitFloat` variants that stay in
  the `[0, 1]` interval.
- **`functions.py`** – Shared helpers such as `clamp`, `clamp01`, `bounce`, and
  `cyclic_wrap` for range management.
- **`types.py`** – Shared type aliases for readability.

## Usage

```python
from numbers import ClampedInt, ModuloInt, UnitFloat

score = ClampedInt(105, 0, 100)  # -> 100
angle = ModuloInt(370, 360)      # -> 10 (mod 360)
opacity = UnitFloat(1.5)         # -> 1.0
```

`EnforcedUnitFloat` and the bounded integer factories apply their constraints to
new values produced by arithmetic operations as well, making it easy to keep
intermediate results safe by construction.
