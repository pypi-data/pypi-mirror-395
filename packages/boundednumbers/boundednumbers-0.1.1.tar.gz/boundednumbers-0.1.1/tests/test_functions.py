from ..numbers.functions import clamp, clamp01, bounce, cyclic_wrap

def test_clamp_basic():
    assert clamp(5, 0, 10) == 5
    assert clamp(-2, 0, 10) == 0
    assert clamp(50, 0, 10) == 10

def test_clamp01():
    assert clamp01(0.5) == 0.5
    assert clamp01(-1) == 0.0
    assert clamp01(2) == 1.0

def test_cyclic_wrap():
    assert cyclic_wrap(0, 0, 10) == 0
    assert cyclic_wrap(11, 0, 10) == 0
    assert cyclic_wrap(12, 0, 10) == 1
    assert cyclic_wrap(-1, 0, 10) == 10

def test_bounce_inside():
    assert bounce(5, 0, 10) == 5

def test_bounce_outside():
    assert bounce(12, 0, 10) == 8   # moving backward
    assert bounce(-2, 0, 10) == 2  # bouncing forward

def test_bounce_multi_reflections():
    assert bounce(25, 0, 10) == 5   # 25 → bounce back and forth
    assert bounce(-15, 0, 10) == 5  # -15 → bounce back and forth