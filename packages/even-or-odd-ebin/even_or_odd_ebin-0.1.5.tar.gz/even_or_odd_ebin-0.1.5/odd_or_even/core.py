def is_even_or_odd(n: int) -> str:
    """
    Return the string "even" if n is even, otherwise "odd".

    Raises TypeError when input is not an int.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    return "even" if n % 2 == 0 else "odd"
