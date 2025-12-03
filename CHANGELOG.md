# Changelog

All notable changes to **boundednumbers** will be documented in this file.

## 0.1.0 – 2024-06-07

### Added
- First official release of the bounded numeric helpers.
- `ClampedInt`, `CyclicInt`, `BouncedInt`, and `ModuloBoundedInt` factories for creating bounded integer subclasses.
- `ClampedFloat`, `CyclicFloat`, and `BouncedFloat` for float values that respect bounds after arithmetic.
- `ModuloInt` and `ModuloFloat` types for modular arithmetic with operator support and inverses.
- `UnitFloat` and `EnforcedUnitFloat` for values constrained to the `[0, 1]` interval.
- Range helper functions: `clamp`, `clamp01`, `bounce`, `cyclic_wrap`, `cyclic_wrap_float`, and modular iteration via `modulo_range`.

### Documentation
- Expanded README with installation, usage walkthroughs, and API overview.
- Added in-depth module documentation under `numbers/README.md`.
