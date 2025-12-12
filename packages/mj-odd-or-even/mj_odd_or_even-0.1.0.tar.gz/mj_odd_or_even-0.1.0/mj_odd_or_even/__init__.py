# mj_odd_or_even/mj_odd_or_even/__init__.py

def is_odd(n: int) -> bool:
    """Return True if n is odd (integers only)."""
    if not isinstance(n, int):
        raise TypeError("is_odd expects an int")
    return n % 2 == 1


def is_even(n: int) -> bool:
    """Return True if n is even (integers only)."""
    if not isinstance(n, int):
        raise TypeError("is_even expects an int")
    return n % 2 == 0


__all__ = ["is_odd", "is_even"]
