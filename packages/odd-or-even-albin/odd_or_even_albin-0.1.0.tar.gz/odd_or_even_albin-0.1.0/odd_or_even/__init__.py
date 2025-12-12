def is_even(num: int) -> bool:
    """Return True if number is even."""
    return num % 2 == 0


def is_odd(num: int) -> bool:
    """Return True if number is odd."""
    return num % 2 != 0


def check(num: int) -> str:
    """Return 'even' or 'odd'."""
    return "even" if is_even(num) else "odd"
