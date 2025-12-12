import math
from typing import Iterable, List


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b


def square(x):
    return x * x


def cube(x):
    return x * x * x


def sqrt(x):
    if x < 0:
        raise ValueError("sqrt() only defined for non-negative numbers.")
    return math.sqrt(x)


def power(x, n):
    return x**n


def percent(part, whole):
    if whole == 0:
        raise ZeroDivisionError("whole cannot be zero in percent().")
    return (part / whole) * 100.0


def percent_change(old, new):
    if old == 0:
        raise ZeroDivisionError("old value cannot be zero in percent_change().")
    return ((new - old) / old) * 100.0
