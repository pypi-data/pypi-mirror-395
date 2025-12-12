from boundednumbers.numbers.bounded import make_bounded_int
from boundednumbers.numbers.functions import extract_excess
from boundednumbers.numbers.types import RealNumber

def substract_excess_squared_mod(value: RealNumber, min_value: RealNumber, max_value: RealNumber) -> RealNumber:
    """
    Bounding function that subtracts the square of the excess amount
    beyond the bounds from the nearest bound.
    """
    bounded_value, excess = extract_excess(value, min_value, max_value)
    return (bounded_value - (excess ** 2)) % (max_value - min_value) + min_value

SquaredExcessModInt = make_bounded_int(substract_excess_squared_mod, "SquaredExcessModInt")

def test_squared_excess_mod_int():
    x = SquaredExcessModInt(12, 0, 10)
    assert x == 6  # 10 - (2^2) = 6

    y = SquaredExcessModInt(-3, 0, 10)
    assert y == 1  # 0 + (3^2) = 9 % 10 = 9

    z = SquaredExcessModInt(25, 0, 10)
    assert z == 5  # 10 - (5^2) = -15 % 10 = 5

class ExcessGatherer:
    def __init__(self):
        self.total_excess = 0

excess_gatherer = ExcessGatherer()

def gather_excess(value: RealNumber, min_value: RealNumber, max_value: RealNumber) -> RealNumber:
    bounded_value, excess = extract_excess(value, min_value, max_value)
    excess_gatherer.total_excess += excess
    return bounded_value

GatheringBoundedInt = make_bounded_int(gather_excess, "GatheringBoundedInt")

def test_gathering_bounded_int():
    excess_gatherer.total_excess = 0  # Reset before test

    x = GatheringBoundedInt(15, 0, 10)
    assert x == 10
    assert excess_gatherer.total_excess == 5

    y = GatheringBoundedInt(-4, 0, 10)
    assert y == 0
    assert excess_gatherer.total_excess == 1  # 5 - 4

    z = GatheringBoundedInt(22, 0, 10)
    assert z == 10
    assert excess_gatherer.total_excess == 13  # 1 + 12