"""
AIMATHX — One-line import math + ML + AI + Crypto + Quantum library.

Example:
    import aimath as am
    print(am.sqrt(144))
    print(am.mean([10, 20, 30]))
"""

# =====================================================
# CORE
# =====================================================
from .core import add, sub, mul, div, square, cube, sqrt, power, percent, percent_change

# =====================================================
# SCIENTIFIC
# =====================================================
from .scientific import sin, cos, tan, log10, ln, exp, factorial, deg2rad, rad2deg

# =====================================================
# STATISTICS
# =====================================================
from .statistics import mean, median, mode, variance, std, data_range, iqr, z_score

# =====================================================
# PROBABILITY
# =====================================================
from .probability import nCr, nPr, bayes, expected_value
from .distributions import (
    normal_pdf,
    normal_cdf,
    bernoulli_pmf,
    binomial_pmf,
    poisson_pmf,
    exponential_pdf,
    uniform_pdf,
    t_pdf,
    chi_square_pdf,
)

# =====================================================
# MACHINE LEARNING
# =====================================================
from .ml import mse, rmse, mae, accuracy, precision, recall, f1_score, r2_score

# =====================================================
# DEEP LEARNING
# =====================================================
from .dl import (
    sigmoid,
    relu,
    tanh,
    softmax,
    entropy,
    kl_divergence,
    binary_cross_entropy,
)

# =====================================================
# NLP
# =====================================================
from .nlp import (
    term_frequency,
    inverse_document_frequency,
    tfidf,
    cosine_similarity,
    perplexity,
)

# =====================================================
# TIME SERIES
# =====================================================
from .timeseries import sma, ema

# =====================================================
# FINANCE
# =====================================================
from .finance_math import simple_interest, compound_interest, loan_emi

# =====================================================
# CRYPTO / BLOCKCHAIN
# =====================================================
from .crypto_math import sha256, gas_fee

# =====================================================
# QUANTUM
# =====================================================
from .quantum_math import hadamard, pauli_x

# =====================================================
# APTITUDE
# =====================================================
from .aptitude_math import profit_percent, loss_percent, avg_speed

# =====================================================
# ALGEBRA
# =====================================================
from .algebra import solve_linear, quadratic_roots

# =====================================================
# GEN-AI (Phase 2)
# =====================================================
from .genai import logits_to_prob, softmax_temperature, attention_scores

# =====================================================
# OPTIMIZATION (Phase 2)
# =====================================================
from .optimization import (
    sgd_update,
    momentum_update,
    adam_update,
    rmsprop_update,
    lr_step_decay,
    lr_cosine_anneal,
)


# =====================================================
# GRAPH (Phase 2)
# =====================================================
from .graph import (
    bfs_distance,
    dijkstra_shortest_path,
)

# =====================================================
# VISION (Phase 2)
# =====================================================
from .vision import conv2d_output_shape, maxpool_output_shape, iou, nms

# =====================================================
# FULL MATH EXTENSION (Python math module exposed)
# =====================================================
from .math_ext import *

# =====================================================
# BENCHMARK + DOCS
# =====================================================
from .benchmark import timeit, mem_profile

# =====================================================
# NUMBER_THEORY 
# =====================================================
from .number_theory import gcd, lcm, is_prime, prime_factors, totient, mod_inverse, modular_pow, fibonacci, pell_number, catalan_number, divisor_count, divisor_sum



# =====================================================
# EXPORTED API LIST
# =====================================================
__all__ = [
    # core
    "add",
    "sub",
    "mul",
    "div",
    "square",
    "cube",
    "sqrt",
    "power",
    "percent",
    "percent_change",
    # scientific
    "sin",
    "cos",
    "tan",
    "log10",
    "ln",
    "exp",
    "factorial",
    "deg2rad",
    "rad2deg",
    # statistics
    "mean",
    "median",
    "mode",
    "variance",
    "std",
    "data_range",
    "iqr",
    "z_score",
    # probability
    "nCr",
    "nPr",
    "bayes",
    "expected_value",
    # distributions
    "normal_pdf",
    "normal_cdf",
    "bernoulli_pmf",
    "binomial_pmf",
    "poisson_pmf",
    "exponential_pdf",
    "uniform_pdf",
    "t_pdf",
    "chi_square_pdf",
    # ML
    "mse",
    "rmse",
    "mae",
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "r2_score",
    # DL
    "sigmoid",
    "relu",
    "tanh",
    "softmax",
    "entropy",
    "kl_divergence",
    "binary_cross_entropy",
    # NLP
    "term_frequency",
    "inverse_document_frequency",
    "tfidf",
    "cosine_similarity",
    "perplexity",
    # time series
    "sma",
    "ema",
    # finance
    "simple_interest",
    "compound_interest",
    "loan_emi",
    # crypto
    "sha256",
    "gas_fee",
    # quantum
    "hadamard",
    "pauli_x",
    # aptitude
    "profit_percent",
    "loss_percent",
    "avg_speed",
    # algebra
    "solve_linear",
    "quadratic_roots",
    # GEN-AI
    "logits_to_prob",
    "softmax_temperature",
    "attention_scores",
    # optimization
    "sgd_update",
    "adam_update",
    "rmsprop_update",
    "lr_step_decay",
    "lr_cosine_anneal",
    "momentum_update",
    # graph
    "bfs_distance",
    "dijkstra_shortest_path",
    # vision
    "conv2d_output_shape",
    "maxpool_output_shape",
    "iou",
    "nms",
    # math_ext (all math.* names are included automatically)
    # benchmark
    "timeit",
    "mem_profile",
    # number_theory
    "gcd", "lcm", "is_prime", "prime_factors", "totient",
    "mod_inverse", "modular_pow", "fibonacci",
    "pell_number", "catalan_number", "divisor_count", "divisor_sum",

]
