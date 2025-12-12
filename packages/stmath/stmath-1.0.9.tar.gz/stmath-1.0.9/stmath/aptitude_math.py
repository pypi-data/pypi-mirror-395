from .core import percent


def profit_percent(cp, sp):
    if cp == 0:
        raise ZeroDivisionError("cp cannot be zero.")
    return (sp - cp) * 100.0 / cp


def loss_percent(cp, sp):
    if cp == 0:
        raise ZeroDivisionError("cp cannot be zero.")
    return (cp - sp) * 100.0 / cp


def avg_speed(distance1, speed1, distance2, speed2):
    """Average speed over two equal distances with different speeds."""
    time = distance1 / speed1 + distance2 / speed2
    total_dist = distance1 + distance2
    return total_dist / time
