import math

def is_prime(n: int) -> bool:
    """
    Check if a given number is prime.

    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is prime, False otherwise.

    Examples:
        >>> is_prime(5)
        True
        >>> is_prime(4)
        False
        >>> is_prime(1)
        False
        >>> is_prime(2)
        True
    """
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True