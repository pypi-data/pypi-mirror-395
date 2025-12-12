from typing import Sequence, List
import math


def sma(series: Sequence[float], window: int) -> List[float]:
    """Simple Moving Average. Returns list with None for positions < window-1."""
    series = list(series)
    n = len(series)
    if window <= 0:
        raise ValueError("window must be positive.")
    result: List[float] = []
    for i in range(n):
        if i + 1 < window:
            result.append(None)
        else:
            window_vals = series[i + 1 - window : i + 1]
            result.append(sum(window_vals) / window)
    return result


def ema(series: Sequence[float], alpha: float) -> List[float]:
    """Exponential Moving Average, simple recursive version."""
    series = list(series)
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0,1].")
    if not series:
        return []
    ema_vals = [series[0]]
    for x in series[1:]:
        ema_vals.append(alpha * x + (1 - alpha) * ema_vals[-1])
    return ema_vals
