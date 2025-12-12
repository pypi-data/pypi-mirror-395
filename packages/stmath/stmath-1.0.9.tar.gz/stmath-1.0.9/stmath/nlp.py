import math
from typing import List, Sequence


def term_frequency(term: str, document: Sequence[str]) -> float:
    """document is list of tokens."""
    if not document:
        return 0.0
    count = sum(1 for t in document if t == term)
    return count / len(document)


def inverse_document_frequency(term: str, corpus: List[Sequence[str]]) -> float:
    n_docs = len(corpus)
    if n_docs == 0:
        return 0.0
    docs_with_term = sum(1 for doc in corpus if term in doc)
    if docs_with_term == 0:
        return 0.0
    return math.log(n_docs / docs_with_term)


def tfidf(term: str, document: Sequence[str], corpus: List[Sequence[str]]) -> float:
    return term_frequency(term, document) * inverse_document_frequency(term, corpus)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("cosine_similarity: length mismatch.")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def perplexity(log_probs: Sequence[float]) -> float:
    """
    log_probs: list of log probabilities (natural log).
    Perplexity = exp(- average log prob).
    """
    log_probs = list(log_probs)
    if not log_probs:
        return float("inf")
    return math.exp(-sum(log_probs) / len(log_probs))
