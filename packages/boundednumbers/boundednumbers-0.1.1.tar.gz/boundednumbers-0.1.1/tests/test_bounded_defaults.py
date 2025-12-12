

def test_clamped_int_basic(clamp_int):
    x = clamp_int(12)  # clamp to 10
    assert x == 10
    assert x + 5 == 10   # stays clamped
    assert x - 20 == 0

def test_cyclic_int_basic(cyclic_int):
    x = cyclic_int(12)  # wraps to 1 (0–10 range)
    assert x == 1
    assert x + 10 == 11 % 11  # (1 + 10) mod 11 = 0

def test_bounced_int_basic(bounced_int):
    x = bounced_int(12)  
    assert x == 8  
    assert x + 10 == 2  # 8+10=18 → reflected

def test_arithmetic_preserves_bounds(cyclic_int):
    x = cyclic_int(5)
    y = x + 100
    assert y == cyclic_int(5 + 100)

def test_modulo_int_basic(mod):
    x = mod(12)
    assert x == 2
    assert x + 15 == mod(17)

def test_clamped_float_basic(clamp_float):
    x = clamp_float(1.5)  # clamp to 1.0
    assert x == 1.0
    assert x + 0.5 == 1.0   # stays clamped
    assert x - 2.0 == 0.0

def test_cyclic_float_basic(cyclic_float):
    x = cyclic_float(0.20, 0.0, 1.0)  # wraps to 0.2 (0.0–1.0 range)
    assert x == 0.2
    assert x + 1.5 == 0.7  # (0.2 + 1.5) mod 1.0 = 0.7

def test_bounced_float_basic(bounced_float):
    x = bounced_float(1.5, 0.0, 1.0)  
    assert x == 0.5  
    assert x + 1.0 == 0.5  # 0.5+1.0=1.5 → reflected

def test_arithmetic_preserves_float_bounds(cyclic_float):
    x = cyclic_float(0.5, 0.0, 1.0)
    y = x + 3.0
    assert y == cyclic_float(0.5 + 3.0, 0.0, 1.0)