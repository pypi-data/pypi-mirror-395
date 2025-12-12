from primevalidation import is_prime

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(17) is True
    assert is_prime(1) is False
    assert is_prime(4) is False
    assert is_prime(9) is False
    assert is_prime(15) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False  # Negative numbers aren't prime