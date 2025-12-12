import cmath
from typing import Tuple


def solve_linear(a: float, b: float) -> float:
    """Solve ax + b = 0"""
    if a == 0:
        raise ZeroDivisionError("a cannot be zero in solve_linear.")
    return -b / a


def quadratic_roots(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """Solve ax^2 + bx + c = 0 (supports real + complex roots)."""
    if a == 0:
        raise ZeroDivisionError("a cannot be zero in quadratic_roots.")

    D = b**2 - 4 * a * c
    sqrtD = cmath.sqrt(D)

    x1 = (-b + sqrtD) / (2 * a)
    x2 = (-b - sqrtD) / (2 * a)

    return x1, x2
