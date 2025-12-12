# boundednumbers

Boundednumbers provides lightweight numeric types that automatically respect the limits you set.
Use them to keep values in range across math operations without littering your code with manual
clamping or wraparound logic.

## Installation

```bash
pip install boundednumbers
```

## Quick start

```python
from numbers import ClampedInt, CyclicInt, BouncedInt, ModuloInt, UnitFloat, modulo_range

health = ClampedInt(120, 0, 100)   # -> 100, and stays within [0, 100]
angle = CyclicInt(-15, 0, 360)     # -> 345, wraps on every operation
paddle = BouncedInt(130, 0, 100)   # -> 70, reflects back into range
counter = ModuloInt(7, 5)          # -> 2, supports modular arithmetic
opacity = UnitFloat(1.25)          # -> 1.0, always between 0 and 1

# Iterate around a circle without repeating the stop value
points = list(modulo_range(start=350, stop=170, step=40, modulus=360))
```

## Features

- **Bounded integers**: `ClampedInt`, `CyclicInt`, `BouncedInt`, and `ModuloBoundedInt`
  automatically enforce their strategy after arithmetic (addition, subtraction, multiplication,
  division, and floor division).
- **Bounded floats**: `ClampedFloat`, `CyclicFloat`, and `BouncedFloat` mirror the integer
  behavior for floating-point values.
- **Unit interval helpers**: `UnitFloat` corrects values into `[0, 1]` on construction; `EnforcedUnitFloat`
  reapplies the bounds after arithmetic.
- **Modular arithmetic**: `ModuloInt` exposes additive and multiplicative inverses along with safe
  modular iteration via `modulo_range`.
- **Utility functions**: Reusable helpers like `clamp`, `clamp01`, `bounce`, `cyclic_wrap`, and
  `cyclic_wrap_float` are available when you prefer to keep native numeric types.

## API overview

### Bounded factories

Use the factory helpers when you need custom class names or number types:

```python
from numbers import BoundType, bounce, make_default_bounded_int, make_default_bounded_float, make_bounded_int

# Create a custom bounded integer that bounces inside [-5, 5]
BouncyFive = make_bounded_int(lambda v, mn, mx: bounce(v, mn, mx), class_name="BouncyFive")
value = BouncyFive(17, -5, 5)  # -> -3

# Or rely on the built-in enum to pick a strategy
WrappedFloat = make_default_bounded_float(BoundType.CYCLIC)
angle = WrappedFloat(725.0, 0.0, 360.0)  # -> 5.0
```

### Modular utilities

`ModuloInt` and `modulo_range` simplify common modular workflows:

```python
from numbers import Direction, ModuloRangeMode, modulo_range, ModuloInt

# Compute a multiplicative inverse
inverse = ModuloInt(7, 26).inverse()  # -> ModuloInt(15 mod 26)

# Visit points around a circle without repeating stop (one full modular cycle)
for value in modulo_range(start=0, stop=0, step=3, modulus=10, direction=Direction.DECREASING, max_range_amount=ModuloRangeMode.DETECT):
    ...
```

### Unit floats

`UnitFloat` corrects values into the unit interval on construction, while `EnforcedUnitFloat` applies
bounds after every operation:

```python
from numbers import EnforcedUnitFloat

u = EnforcedUnitFloat(1.4)
print(u - 3.0)  # -> 0.0
```

## Further reading

See [`numbers/README.md`](numbers/README.md) for a deeper, module-by-module breakdown and usage tips.
