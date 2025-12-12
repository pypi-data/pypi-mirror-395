import math


def simple_interest(P, R, T):
    """P = principal, R = rate% per year, T = time in years."""
    return P * R * T / 100.0


def compound_interest(P, R, T, n=1):
    """n = times compounded per year."""
    return P * (1 + R / (100.0 * n)) ** (n * T) - P


def loan_emi(P, annual_rate, months):
    """Standard EMI formula."""
    r = annual_rate / (12 * 100.0)
    if r == 0:
        return P / months
    return P * r * (1 + r) ** months / ((1 + r) ** months - 1)
