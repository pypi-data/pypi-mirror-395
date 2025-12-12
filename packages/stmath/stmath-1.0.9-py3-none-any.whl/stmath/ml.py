from typing import Iterable, Sequence
import math


def mse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("mse: y_true and y_pred length mismatch.")
    n = len(y_true)
    return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / n


def rmse(y_true, y_pred) -> float:
    return math.sqrt(mse(y_true, y_pred))


def mae(y_true, y_pred) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("mae: y_true and y_pred length mismatch.")
    n = len(y_true)
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / n


def accuracy(y_true, y_pred) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("accuracy: length mismatch.")
    if not y_true:
        raise ValueError("accuracy: empty input.")
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / len(y_true)


def _binary_confusion(y_true, y_pred, positive=1):
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        if p == positive and t == positive:
            tp += 1
        elif p == positive and t != positive:
            fp += 1
        elif p != positive and t != positive:
            tn += 1
        elif p != positive and t == positive:
            fn += 1
    return tp, fp, tn, fn


def precision(y_true, y_pred, positive=1) -> float:
    tp, fp, tn, fn = _binary_confusion(y_true, y_pred, positive)
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)


def recall(y_true, y_pred, positive=1) -> float:
    tp, fp, tn, fn = _binary_confusion(y_true, y_pred, positive)
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)


def f1_score(y_true, y_pred, positive=1) -> float:
    p = precision(y_true, y_pred, positive)
    r = recall(y_true, y_pred, positive)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def r2_score(y_true, y_pred) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("r2_score: length mismatch.")
    mean_y = sum(y_true) / len(y_true)
    ss_res = sum((a - b) ** 2 for a, b in zip(y_true, y_pred))
    ss_tot = sum((a - mean_y) ** 2 for a in y_true)
    if ss_tot == 0:
        return 0.0
    return 1 - ss_res / ss_tot
