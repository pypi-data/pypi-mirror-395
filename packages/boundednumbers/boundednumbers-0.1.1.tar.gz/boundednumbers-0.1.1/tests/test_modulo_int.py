from boundednumbers.numbers.modulo_int import ModuloInt, ModuloRangeMode, modulo_range, Direction

def test_modulo_basic():
    x = ModuloInt(12, 10)
    assert x == 2
    assert x.modulus == 10

def test_modulo_addition():
    x = ModuloInt(9, 10)
    assert x + 5 == ModuloInt(4, 10)

def test_modulo_subtraction():
    assert ModuloInt(1, 10) - 5 == ModuloInt(6, 10)

def test_modulo_multiplication():
    assert ModuloInt(3, 10) * 4 == ModuloInt(2, 10)

def test_modulo_inverse():
    assert ModuloInt(3, 7).inverse() == ModuloInt(5, 7)

def test_modulo_inverse_invalid():
    import pytest
    with pytest.raises(ValueError):
        ModuloInt(2, 4).inverse()

def test_modulo_range_detect():
    values = list(modulo_range(0, 3, 1, 5))
    assert values[0] == ModuloInt(0, 5)
    assert values[-1] != ModuloInt(3, 5)  # stops before stop
    assert len(values) == 3

def test_modulo_range_step():
    values = list(modulo_range(1, 1, 2, 6, Direction.INCREASING, 4))
    assert len(values) == 3
    assert values == [
        ModuloInt(1, 6),
        ModuloInt(3, 6),
        ModuloInt(5, 6),
    ]

def test_modulo_range_decreasing():
    values = list(modulo_range(4, 1, 1, 7, Direction.DECREASING, 5))
    assert len(values) == 3
    assert values == [
        ModuloInt(4, 7),
        ModuloInt(3, 7),
        ModuloInt(2, 7),
    ]

def test_modulo_range_forced_amount():
    values = list(modulo_range(0, 0, 3, 10, forced_amount=5))
    assert len(values) == 5
    assert values == [
        ModuloInt(0, 10),
        ModuloInt(3, 10),
        ModuloInt(6, 10),
        ModuloInt(9, 10),
        ModuloInt(2, 10),
    ]

def test_detect_modulo_range_infinite():
    start = 1
    stop = 0
    modulo = 2
    step = 2
    values = list(modulo_range(start, stop, step, modulo, Direction.INCREASING, ModuloRangeMode.DETECT))
    assert len(values) == 1