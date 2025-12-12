"""Implementation of integers with modular arithmetic semantics."""

from __future__ import annotations

from enum import Enum, auto
from math import gcd
from typing import Generator


class ModuloInt(int):
    """Integer modulo ``n`` supporting common arithmetic operators."""

    modulus: int

    def __new__(cls, value: int, modulus: int):
        if modulus <= 0:
            raise ValueError("Modulus must be a positive integer.")
        obj = super().__new__(cls, value % modulus)
        obj.modulus = modulus
        return obj

    def _coerce(self, other):
        """Convert operand to a compatible ``ModuloInt``."""

        if isinstance(other, ModuloInt):
            if other.modulus != self.modulus:
                raise ValueError(
                    f"Cannot operate on ModuloInt with different moduli ({self.modulus} vs {other.modulus})"
                )
            return int(other)

        if isinstance(other, int):
            return other

        return NotImplemented

    def opposite(self) -> ModuloInt:
        """Return the additive inverse modulo ``n``."""

        return ModuloInt(-int(self), self.modulus)

    def inverse(self) -> ModuloInt:
        """Return the multiplicative inverse modulo ``n`` (requires ``gcd(self, n) == 1``)."""

        a, n = int(self), self.modulus
        if gcd(a, n) != 1:
            raise ValueError(f"{a} has no multiplicative inverse modulo {n}.")

        t, new_t = 0, 1
        r, new_r = n, a
        while new_r != 0:
            q = r // new_r
            t, new_t = new_t, t - q * new_t
            r, new_r = new_r, r - q * new_r

        return ModuloInt(t, n)

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

    def __pow__(self, other, modulo=None):  # noqa: D401 - part of arithmetic API
        if modulo is not None:
            raise ValueError("Use built-in pow(a, b, n) instead of a**b with modulo.")
        o = self._coerce(other)
        return ModuloInt(pow(int(self), o, self.modulus), self.modulus)

    def __repr__(self):
        return f"ModuloInt({int(self)} mod {self.modulus})"


class Direction(Enum):
    """Direction to advance in :func:`modulo_range`."""

    INCREASING = 1
    DECREASING = -1
    INCREASE = 1
    DECREASE = -1


class ModuloRangeMode(Enum):
    """Modes that control :func:`modulo_range` iteration length."""

    DETECT = auto()
    INFINITE = auto()

def modulo_yield_many(
        start: int,
        step: int,
        modulus: int,
        amount: int,
        direction: Direction = Direction.INCREASING,
    ) -> Generator[ModuloInt, None, None]:
    """Yield a specified amount of ModuloInt values starting from 'start'."""
    if step <= 0:
        raise ValueError("Step must be positive.")
    start_mod = ModuloInt(start, modulus)
    current = start_mod
    step = abs(step)
    if direction == Direction.DECREASING:
        step = -step
    for _ in range(amount):
        yield current
        current = ModuloInt(int(current) + step, modulus)

def modulo_range(
    start: int,
    stop: int,
    step: int,
    modulus: int,
    direction: Direction = Direction.INCREASING,
    max_range_amount: ModuloRangeMode | int | float = ModuloRangeMode.DETECT,
    *,
    forced_amount: int | None = None,
) -> Generator[ModuloInt, None, None]:

    if step <= 0:
        raise ValueError("Step must be positive.")

    # --- Forced mode: just yield N steps -----------------------------
    if forced_amount is not None:
        yield from modulo_yield_many(start, step, modulus, forced_amount, direction)
        return

    start_mod = ModuloInt(start, modulus)
    stop_mod = ModuloInt(stop, modulus)
    current = start_mod

    # --- Determine iteration limit ----------------------------------
    if max_range_amount is ModuloRangeMode.INFINITE:
        max_iter = float("inf")

    elif max_range_amount is ModuloRangeMode.DETECT:
        # one full modular cycle WITHOUT allowing a repeat of start
        cycle_len = modulus // gcd(modulus, step)
        max_iter = cycle_len

    else:
        max_iter = int(max_range_amount)
        if max_iter <= 0:
            raise ValueError("max_range_amount must be positive.")

    step = abs(step)
    if direction == Direction.DECREASING:
        step = -step

    # --- Main loop ---------------------------------------------------
    # Always yield the start
    yield current
    count = 1  

    while count < max_iter:
        next_val = ModuloInt(int(current) + step, modulus)

        # stop before repeating stop
        if next_val == stop_mod:
            break

        yield next_val
        current = next_val
        count += 1

        
