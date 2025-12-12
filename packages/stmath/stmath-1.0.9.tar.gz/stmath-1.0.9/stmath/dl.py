import math
from typing import Sequence, Iterable


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def relu(x: float) -> float:
    return x if x > 0 else 0.0


def tanh(x: float) -> float:
    e_pos = math.exp(x)
    e_neg = math.exp(-x)
    return (e_pos - e_neg) / (e_pos + e_neg)


def softmax(xs: Sequence[float]) -> list[float]:
    xs = list(xs)
    if not xs:
        return []
    max_x = max(xs)  # for numerical stability
    exps = [math.exp(x - max_x) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


def entropy(probs: Sequence[float]) -> float:
    e = 0.0
    for p in probs:
        if p > 0:
            e -= p * math.log(p, 2)
    return e


def kl_divergence(p: Sequence[float], q: Sequence[float]) -> float:
    if len(p) != len(q):
        raise ValueError("p and q must have same length for KL divergence.")
    total = 0.0
    for pi, qi in zip(p, q):
        if pi == 0:
            continue
        if qi == 0:
            raise ValueError("KL divergence undefined when q has zero where p>0.")
        total += pi * math.log(pi / qi, 2)
    return total


def binary_cross_entropy(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("binary_cross_entropy: length mismatch.")
    eps = 1e-15
    loss = 0.0
    for t, p in zip(y_true, y_pred):
        p = min(max(p, eps), 1 - eps)
        loss += -(t * math.log(p) + (1 - t) * math.log(1 - p))
    return loss / len(y_true)
