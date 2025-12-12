from boundednumbers.numbers.unit_float import UnitFloat, EnforcedUnitFloat

def test_unit_float_basic():
    assert UnitFloat(0.5) == 0.5
    assert UnitFloat(-1) == 0.0
    assert UnitFloat(2) == 1.0

def test_enforced_unit_add():
    x = EnforcedUnitFloat(0.8)
    y = x + 0.5
    assert y == 1.0

def test_enforced_unit_sub():
    x = EnforcedUnitFloat(0.2)
    assert (x - 1.0) == 0.0

def test_enforced_unit_mul():
    x = EnforcedUnitFloat(0.5)
    assert (x * 3) == 1.0

def test_enforced_unit_div():
    x = EnforcedUnitFloat(1.0)
    assert (x / 10) == 0.1

def test_pow():
    x = EnforcedUnitFloat(0.5)
    y = x ** 3
    assert y == 0.125
    y = y ** -1
    assert y == 1.0