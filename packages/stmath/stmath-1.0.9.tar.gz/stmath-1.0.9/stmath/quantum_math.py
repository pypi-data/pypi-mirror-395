import math
from typing import Sequence, List


def hadamard(qubit: Sequence[complex]) -> List[complex]:
    """
    Apply Hadamard gate to single qubit [a, b].
    """
    if len(qubit) != 2:
        raise ValueError("hadamard expects a 2-element state vector.")
    a, b = qubit
    factor = 1 / math.sqrt(2)
    return [
        factor * (a + b),
        factor * (a - b),
    ]


def pauli_x(qubit: Sequence[complex]) -> List[complex]:
    if len(qubit) != 2:
        raise ValueError("pauli_x expects 2-element state.")
    a, b = qubit
    return [b, a]
