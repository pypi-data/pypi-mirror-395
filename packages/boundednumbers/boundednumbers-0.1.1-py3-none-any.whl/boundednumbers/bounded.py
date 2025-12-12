"""Factory helpers for bounded integer types.

This module provides the :class:`BoundType` enum to describe the
bounding strategy and :func:`make_bounded_int` to generate subclasses of
``int`` that automatically enforce the selected behavior.
"""

from __future__ import annotations

from enum import Enum, auto

from .functions import bounce, clamp, cyclic_wrap, cyclic_wrap_float
from .modulo_int import ModuloInt
from .modulo_float import ModuloFloat
from .types import RealNumber

from typing import Callable, Optional, Type, cast

class BoundType(Enum):
    """Available strategies for constraining integer values."""

    CLAMP = auto()
    CYCLIC = auto()
    BOUNCE = auto()
    MODULO = auto()  # pure 0..n-1 modular arithmetic


def _apply_bounding_function(value: RealNumber, min_value: RealNumber, max_value: RealNumber, bounding_function: Callable[[RealNumber, RealNumber, RealNumber], RealNumber]) -> RealNumber:
    """Apply a bounding function to the provided value."""

    return bounding_function(value, min_value, max_value)

def make_bounded_number(bounding_function: Callable[[RealNumber, RealNumber, RealNumber], RealNumber], number_type: Type, class_name: Optional[str] = None) -> type[RealNumber]:
    """Return a numeric subclass that applies ``bound_type`` on every operation."""

    class BoundedNumber(number_type):
        """Auto-bounded number for the chosen :class:`BoundType`."""

        min_value: RealNumber
        max_value: RealNumber

        def __new__(cls, value: RealNumber, min_value: RealNumber, max_value: RealNumber):
            bounded = _apply_bounding_function(value, min_value, max_value, bounding_function)

            obj = number_type.__new__(cls, bounded)
            obj.min_value = min_value
            obj.max_value = max_value
            return obj

        def _bounded(self, value):
            """Helper to apply bounds consistently."""

            return type(self)(value, self.min_value, self.max_value)

        def __add__(self, other):
            return self._bounded(number_type(self) + other)

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            return self._bounded(number_type(self) - other)

        def __mul__(self, other):
            return self._bounded(number_type(self) * other)
        
        def __truediv__(self, other):
            return self._bounded(number_type(self) / other)
        
        def __floordiv__(self, other):
            return self._bounded(number_type(self) // other)
        

    if class_name is not None:
        BoundedNumber.__name__ = class_name
    return BoundedNumber

def make_bounded_int(bounding_function: Callable[[RealNumber, RealNumber, RealNumber], RealNumber], class_name: Optional[str] = None) -> type[int]:
    """Return an ``int`` subclass that applies ``bound_type`` on every operation."""
    class_made = make_bounded_number(bounding_function, int, class_name)
    class_made = cast(type[int], class_made)
    return class_made

def make_bounded_float(bounding_function: Callable[[RealNumber, RealNumber, RealNumber], RealNumber], class_name: Optional[str] = None) -> type[float]:
    """Return a ``float`` subclass that applies ``bound_type`` on every operation."""
    class_made = make_bounded_number(bounding_function, float, class_name)
    class_made = cast(type[float], class_made)
    return class_made

def make_default_bounded_number(bound_type: BoundType, number_type: Type, class_name: Optional[str] = None) -> type[RealNumber]:
    """Return a numeric subclass that applies ``bound_type`` on every operation."""

    if bound_type == BoundType.MODULO:
        if number_type is int:
            return ModuloInt
        elif number_type is float:
            return ModuloFloat
        else:
            raise ValueError("Modulo bounding is only supported for int and float types.")

    if bound_type not in BoundType:
        raise ValueError("Invalid BoundType")
    
    if bound_type == BoundType.CLAMP:
        bounding_function = clamp
    elif bound_type == BoundType.CYCLIC:
        if number_type is float:
            bounding_function = cyclic_wrap_float
        else:
            bounding_function = cyclic_wrap
    elif bound_type == BoundType.BOUNCE:
        bounding_function = bounce

    BoundedNumber = make_bounded_number(bounding_function, number_type, class_name)

    return BoundedNumber

def make_default_bounded_int(bound_type: BoundType) -> type[int]:
    """Return an ``int`` subclass that applies ``bound_type`` on every operation."""

    BoundedInt = make_default_bounded_number(bound_type, int)
    BoundedInt = cast(type[int], BoundedInt)
    return BoundedInt
def make_default_bounded_float(bound_type: BoundType) -> type[float]:
    """Return a ``float`` subclass that applies ``bound_type`` on every operation."""

    BoundedFloat = make_default_bounded_number(bound_type, float)
    BoundedFloat = cast(type[float], BoundedFloat)
    return BoundedFloat

ClampedInt = make_default_bounded_int(BoundType.CLAMP)
CyclicInt = make_default_bounded_int(BoundType.CYCLIC)
BouncedInt = make_default_bounded_int(BoundType.BOUNCE)
ModuloBoundedInt = make_default_bounded_int(BoundType.MODULO)

ClampedFloat = make_default_bounded_float(BoundType.CLAMP)
CyclicFloat = make_default_bounded_float(BoundType.CYCLIC)
BouncedFloat = make_default_bounded_float(BoundType.BOUNCE)
ModuloBoundedFloat = make_default_bounded_float(BoundType.MODULO)