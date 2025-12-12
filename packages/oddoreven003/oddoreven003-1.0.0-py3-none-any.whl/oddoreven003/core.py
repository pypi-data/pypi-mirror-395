def _to_int(n):
    """Convert input to int if possible."""
    try:
        return int(n)
    except (TypeError, ValueError):
        raise ValueError(f"Cannot convert '{n}' to an integer.")


def is_even(n):
    """Return True if the number is even."""
    n = _to_int(n)
    return n % 2 == 0


def is_odd(n):
    """Return True if the number is odd."""
    n = _to_int(n)
    return n % 2 != 0


def parity(n):
    """Return 'even' or 'odd'."""
    return "even" if is_even(n) else "odd"
