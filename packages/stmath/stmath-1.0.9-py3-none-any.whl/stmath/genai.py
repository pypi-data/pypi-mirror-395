# \"\"\"GenAI math helpers: logits->prob, softmax temperature, simple attention scores\"\"\"
import math
from typing import List


def logits_to_prob(logits: List[float]) -> List[float]:
    ex = [math.exp(x) for x in logits]
    s = sum(ex) or 1.0
    return [x / s for x in ex]


def softmax_temperature(logits: List[float], T: float = 1.0):
    if T <= 0:
        raise ValueError("Temperature must be > 0")
    ex = [math.exp(x / T) for x in logits]
    s = sum(ex) or 1.0
    return [x / s for x in ex]


def attention_scores(queries, keys, softmax=True):
    # queries, keys: list-of-lists (vector per token). returns attention matrix normalized row-wise.
    import math

    # compute scaled dot product
    scores = []
    for q in queries:
        row = []
        for k in keys:
            # dot product (ensure numeric)
            dot = sum(a * b for a, b in zip(q, k))
            row.append(dot)
        scores.append(row)
    if softmax:

        def softmax_row(r):
            ex = [math.exp(x) for x in r]
            s = sum(ex) or 1.0
            return [x / s for x in ex]

        return [softmax_row(r) for r in scores]
    return scores
