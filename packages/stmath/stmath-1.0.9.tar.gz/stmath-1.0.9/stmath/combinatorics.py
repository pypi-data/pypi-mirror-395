# combinatorics.py

import math
from typing import Iterable


def comb(n: int, r: int) -> int:
    """n choose r"""
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)


def perm(n: int, r: int) -> int:
    """n permute r"""
    if r < 0 or r > n:
        return 0
    return math.perm(n, r)


def bayes(p_a: float, p_b: float, p_b_given_a: float) -> float:
    """P(A|B) = P(B|A)P(A) / P(B)"""
    if p_b == 0:
        raise ZeroDivisionError("P(B) cannot be zero")
    return (p_b_given_a * p_a) / p_b


def entropy(p: Iterable[float], base: float = 2.0) -> float:
    """Shannon entropy of probability list p"""
    import math

    H = 0.0
    for pi in p:
        if pi > 0:
            H -= pi * math.log(pi, base)
    return H


def kl_divergence(p: Iterable[float], q: Iterable[float], base: float = 2.0) -> float:
    """KL divergence D(P||Q)"""
    import math

    p = list(p)
    q = list(q)
    if len(p) != len(q):
        raise ValueError("p and q must have same length")
    total = 0.0
    for pi, qi in zip(p, q):
        if pi == 0:
            continue
        if qi == 0:
            return float("inf")
        total += pi * math.log(pi / qi, base)
    return total
