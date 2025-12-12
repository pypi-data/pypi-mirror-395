def check(num: int) -> str:
    """
    Returns whether a number is Odd or Even.
    """
    if not isinstance(num, int):
        raise ValueError("Input must be an integer")

    return "Even" if num % 2 == 0 else "Odd"
