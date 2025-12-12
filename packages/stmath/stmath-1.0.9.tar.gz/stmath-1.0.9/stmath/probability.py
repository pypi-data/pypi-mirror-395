import math
from typing import Iterable, Dict


def nCr(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    num = 1
    den = 1
    for k in range(1, r + 1):
        num *= n - (r - k)
        den *= k
    return num // den


def nPr(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    result = 1
    for k in range(r):
        result *= n - k
    return result


def bayes(p_a: float, p_b_given_a: float, p_b: float) -> float:
    if p_b == 0:
        raise ZeroDivisionError("P(B) cannot be zero in Bayes theorem.")
    return (p_b_given_a * p_a) / p_b


def expected_value(values: Iterable[float], probs: Iterable[float]) -> float:
    values = list(values)
    probs = list(probs)
    if len(values) != len(probs):
        raise ValueError("values and probs must have same length.")
    if not math.isclose(sum(probs), 1.0, rel_tol=1e-6):
        raise ValueError("Probabilities must sum to 1.")
    return sum(v * p for v, p in zip(values, probs))
