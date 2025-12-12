import math
from .probability import nCr


# ---------- Normal ----------


def normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive.")
    coef = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
    expo = -((x - mu) ** 2) / (2.0 * sigma**2)
    return coef * math.exp(expo)


def normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive.")
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


# ---------- Discrete ----------


def bernoulli_pmf(k: int, p: float) -> float:
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0,1].")
    if k == 1:
        return p
    if k == 0:
        return 1 - p
    return 0.0


def binomial_pmf(k: int, n: int, p: float) -> float:
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0,1].")
    return nCr(n, k) * (p**k) * ((1 - p) ** (n - k))


def poisson_pmf(k: int, lam: float) -> float:
    if k < 0:
        return 0.0
    return (lam**k) * math.exp(-lam) / math.factorial(k)


# ---------- Continuous ----------


def exponential_pdf(x: float, lam: float) -> float:
    if lam <= 0:
        raise ValueError("lambda must be positive.")
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def uniform_pdf(x: float, a: float, b: float) -> float:
    if b <= a:
        raise ValueError("require b > a in uniform_pdf.")
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0


def t_pdf(x: float, df: int) -> float:
    """Student t-distribution pdf."""
    if df <= 0:
        raise ValueError("df must be positive.")
    num = math.gamma((df + 1) / 2)
    den = math.sqrt(df * math.pi) * math.gamma(df / 2)
    return num / den * (1 + (x**2) / df) ** (-(df + 1) / 2)


def chi_square_pdf(x: float, k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive.")
    if x < 0:
        return 0.0
    num = x ** (k / 2 - 1) * math.exp(-x / 2)
    den = (2 ** (k / 2)) * math.gamma(k / 2)
    return num / den
