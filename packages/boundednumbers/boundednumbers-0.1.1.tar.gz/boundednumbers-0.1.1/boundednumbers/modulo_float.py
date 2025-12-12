"""Implementation of floats with modular arithmetic semantics."""

from __future__ import annotations

class ModuloFloat(float):
    """Float modulo ``n`` supporting common arithmetic operators."""

    modulus: float

    def __new__(cls, value: float, modulus: float):
        if modulus <= 0.0:
            raise ValueError("Modulus must be a positive float.")
        obj = super().__new__(cls, value % modulus)
        obj.modulus = modulus
        return obj
    
    def _coerce(self, other):
        """Convert operand to a compatible ``ModuloFloat``."""

        if isinstance(other, ModuloFloat):
            if other.modulus != self.modulus:
                raise ValueError(
                    f"Cannot operate on ModuloFloat with different moduli ({self.modulus} vs {other.modulus})"
                )
            return float(other)

        if isinstance(other, (float, int)):
            return float(other)

        return NotImplemented
    
    def __add__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) + o, self.modulus)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) - o, self.modulus)
    def __rsub__(self, other):
        o = self._coerce(other)
        return ModuloFloat(o - float(self), self.modulus)
    def __mul__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) * o, self.modulus)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) / o, self.modulus)
    def __rtruediv__(self, other):
        o = self._coerce(other)
        return ModuloFloat(o / float(self), self.modulus)
    def __floordiv__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) // o, self.modulus)
    def __rfloordiv__(self, other):
        o = self._coerce(other)
        return ModuloFloat(o // float(self), self.modulus)
    def __mod__(self, other):
        o = self._coerce(other)
        return ModuloFloat(float(self) % o, self.modulus)
    def __rmod__(self, other):
        o = self._coerce(other)
        return ModuloFloat(o % float(self), self.modulus)