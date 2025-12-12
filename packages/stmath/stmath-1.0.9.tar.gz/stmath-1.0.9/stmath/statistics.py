import math
from typing import Iterable, List
from collections import Counter


def mean(data: Iterable[float]) -> float:
    data = list(data)
    if not data:
        raise ValueError("mean() of empty data.")
    return sum(data) / len(data)


def median(data: Iterable[float]) -> float:
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise ValueError("median() of empty data.")
    mid = n // 2
    if n % 2 == 1:
        return data[mid]
    return (data[mid - 1] + data[mid]) / 2.0


def mode(data: Iterable[float]):
    data = list(data)
    if not data:
        raise ValueError("mode() of empty data.")
    counts = Counter(data)
    max_count = max(counts.values())
    modes = [x for x, c in counts.items() if c == max_count]
    # If all counts are 1, treat as no clear mode
    if max_count == 1:
        return None
    return modes if len(modes) > 1 else modes[0]


def variance(data: Iterable[float], sample: bool = True) -> float:
    data = list(data)
    n = len(data)
    if n < 2:
        raise ValueError("variance() needs at least two data points.")
    m = mean(data)
    sse = sum((x - m) ** 2 for x in data)
    return sse / (n - 1 if sample else n)


def std(data: Iterable[float], sample: bool = True) -> float:
    return math.sqrt(variance(data, sample=sample))


def data_range(data: Iterable[float]) -> float:
    data = list(data)
    if not data:
        raise ValueError("range() of empty data.")
    return max(data) - min(data)


def iqr(data: Iterable[float]) -> float:
    """Interquartile range: Q3 - Q1."""
    data = sorted(data)
    n = len(data)
    if n < 4:
        raise ValueError("iqr() needs at least 4 data points.")

    mid = n // 2
    if n % 2 == 0:
        lower = data[:mid]
        upper = data[mid:]
    else:
        lower = data[:mid]
        upper = data[mid + 1 :]

    q1 = median(lower)
    q3 = median(upper)
    return q3 - q1


def z_score(x, data):
    m = mean(data)
    s = std(data, sample=True)
    return (x - m) / s

def z_score(x, mean, std):
  return (x - mean) / std

