def is_even(num: int) -> bool:
    return num % 2 == 0

def is_odd(num: int) -> bool:
    return num % 2 != 0

def check(num: int) -> str:
    return "Even" if is_even(num) else "Odd"
