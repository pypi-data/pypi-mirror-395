"""Floating-point helpers that constrain values to the unit interval."""

from __future__ import annotations

from .functions import clamp01 as _clamp01
from .types import RealNumber


class UnitFloat(float):
    """A floating-point number clamped to the inclusive range ``[0, 1]``."""

    def __new__(cls, value: RealNumber):
        if not 0.0 <= value <= 1.0:
            value = _clamp01(value)
        return super().__new__(cls, value)

    def __repr__(self):
        return f"UnitFloat({float(self)})"


class EnforcedUnitFloat(UnitFloat):
    """A :class:`UnitFloat` that auto-clamps all arithmetic results."""

    def __float__(self) -> float:
        return super().__float__()

    @staticmethod
    def _wrap(value: RealNumber) -> "EnforcedUnitFloat":
        return EnforcedUnitFloat(_clamp01(float(value)))

    def _coerce(self, other: RealNumber) -> float:
        if isinstance(other, (EnforcedUnitFloat, UnitFloat, float, int)):
            return float(other)
        return NotImplemented

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

    def __repr__(self):
        return f"EnforcedUnitFloat({float(self)})"
