from oddoreven003 import is_even, is_odd, parity

def test_even():
    assert is_even(10) is True

def test_odd():
    assert is_odd(7) is True

def test_parity():
    assert parity(8) == "even"
