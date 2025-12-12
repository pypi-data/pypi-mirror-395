import math
import pytest
import stmath as am


# =========================
# CORE
# =========================
def test_core_ops():
    assert am.add(10, 5) == 15
    assert am.sub(10, 5) == 5
    assert am.mul(10, 5) == 50
    assert am.div(10, 5) == 2.0
    assert am.square(4) == 16
    assert am.cube(3) == 27
    assert am.sqrt(16) == 4.0
    assert am.power(2, 3) == 8
    assert am.percent(50, 200) == 25.0
    assert am.percent_change(100, 120) == 20.0


# =========================
# SCIENTIFIC
# =========================
def test_scientific():
    assert am.sin(am.pi / 2) == pytest.approx(1.0)
    assert am.cos(0) == pytest.approx(1.0)
    assert am.tan(am.pi / 4) == pytest.approx(1.0)
    assert am.log10(100) == pytest.approx(2.0)
    assert am.ln(am.e) == pytest.approx(1.0)
    assert am.exp(1) == pytest.approx(math.e)
    assert am.factorial(5) == 120
    assert am.deg2rad(180) == pytest.approx(math.pi)
    assert am.rad2deg(math.pi) == pytest.approx(180.0)


# =========================
# STATISTICS
# =========================
def test_statistics():
    data = [10, 20, 30]
    assert am.mean(data) == 20.0
    assert am.median(data) == 20
    assert am.mode([10, 20, 20, 30]) == 20
    assert am.variance(data) == pytest.approx(100.0)
    assert am.std(data) == pytest.approx(10.0)
    assert am.data_range(data) == 20
    assert am.iqr([1, 2, 3, 4, 5, 6, 7, 8]) == pytest.approx(4.0)
    assert am.z_score(70, 60, 5) == pytest.approx(2.0)


# =========================
# PROBABILITY & DISTRIBUTIONS
# =========================
def test_probability_and_distributions():
    assert am.nCr(5, 2) == 10
    assert am.nPr(5, 2) == 20
    assert am.bayes(0.5, 0.4, 0.7) == pytest.approx(0.2857142857)
    assert am.expected_value([1, 2, 3], [0.2, 0.3, 0.5]) == pytest.approx(2.3)

    assert am.normal_pdf(0, 0, 1) == pytest.approx(0.3989422804)
    assert am.normal_cdf(0, 0, 1) == pytest.approx(0.5)
    assert am.bernoulli_pmf(1, 0.6) == pytest.approx(0.6)
    assert am.binomial_pmf(2, 5, 0.5) == pytest.approx(0.3125)
    assert am.poisson_pmf(3, 2) == pytest.approx(0.1804470443)
    assert am.exponential_pdf(2, 1) == pytest.approx(0.1353352832)
    assert am.uniform_pdf(2, 0, 5) == pytest.approx(0.2)
    assert am.t_pdf(0, 10) == pytest.approx(0.3891083839)
    assert am.chi_square_pdf(2, 4) == pytest.approx(0.1839397205)


# =========================
# MACHINE LEARNING METRICS
# =========================
def test_ml_metrics():
    assert am.mse([1, 2, 3], [1, 2, 4]) == pytest.approx(0.3333333333)
    assert am.rmse([1, 2, 3], [1, 2, 4]) == pytest.approx(0.5773502691)
    assert am.mae([1, 2, 3], [1, 2, 4]) == pytest.approx(0.3333333333)
    assert am.accuracy([1, 0, 1], [1, 0, 0]) == pytest.approx(2/3)
    assert am.precision([1, 0, 1, 0], [1, 1, 1, 0]) == pytest.approx(2/3)
    assert am.recall([1, 0, 1, 0], [1, 1, 1, 0]) == pytest.approx(1.0)
    assert am.f1_score([1, 0, 1, 0], [1, 1, 1, 0]) == pytest.approx(0.8)
    assert am.r2_score([1, 2, 3], [1, 2, 4]) == pytest.approx(0.5)


# =========================
# DEEP LEARNING
# =========================
def test_deep_learning():
    assert am.sigmoid(0) == pytest.approx(0.5)
    assert am.relu(-3) == 0.0
    assert am.tanh(1) == pytest.approx(0.7615941559)

    sm = am.softmax([1, 2, 3])
    assert sm[0] == pytest.approx(0.0900305732)
    assert sm[1] == pytest.approx(0.2447284711)
    assert sm[2] == pytest.approx(0.6652409558)

    assert am.entropy([0.5, 0.5]) == pytest.approx(1.0)
    assert am.binary_cross_entropy([1, 0], [0.9, 0.2]) == pytest.approx(
        0.1642520334, rel=1e-6
    )


# =========================
# NLP
# =========================
def test_nlp():
    assert am.term_frequency("machine", ["machine", "learning", "machine"]) == pytest.approx(2/3)
    assert am.inverse_document_frequency(
        "machine",
        [["machine", "learning"], ["deep", "learning"]]
    ) == pytest.approx(0.6931471806)

    tfidf_val = am.tfidf(
        "machine",
        ["machine", "learning"],
        [["machine", "learning"], ["deep", "learning"]]
    )
    assert tfidf_val > 0  # basic sanity check

    assert am.cosine_similarity([1, 0, 1], [0, 1, 1]) == pytest.approx(0.5)
    assert am.perplexity([0.25, 0.25, 0.25, 0.25]) == pytest.approx(0.7788007831)


# =========================
# TIME SERIES
# =========================
def test_time_series():
    sma_res = am.sma([10, 20, 30, 40, 50], 3)
    assert sma_res == [None, None, 20.0, 30.0, 40.0]

    ema_res = am.ema([10, 20, 30, 40, 50], 0.5)
    assert ema_res == pytest.approx([10, 15.0, 22.5, 31.25, 40.625])


# =========================
# FINANCE
# =========================
def test_finance():
    assert am.simple_interest(1000, 10, 2) == pytest.approx(200.0)
    assert am.compound_interest(1000, 10, 2) == pytest.approx(210.0, rel=1e-6)
    assert am.loan_emi(500000, 7.5, 240) == pytest.approx(4027.9659677, rel=1e-6)


# =========================
# CRYPTO
# =========================
def test_crypto():
    assert am.sha256("hello") == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )
    assert am.gas_fee(21000, 50, 2000) == pytest.approx(2.1)


# =========================
# QUANTUM
# =========================
def test_quantum():
    h = am.hadamard([1, 0])
    assert h[0] == pytest.approx(0.7071067812)
    assert h[1] == pytest.approx(0.7071067812)

    px = am.pauli_x([1, 0])
    assert px == [0, 1]


# =========================
# APTITUDE
# =========================
def test_aptitude():
    assert am.profit_percent(100, 120) == pytest.approx(20.0)
    assert am.loss_percent(100, 80) == pytest.approx(20.0)
    assert am.avg_speed(60, 1, 40, 1) == pytest.approx(1.0)


# =========================
# ALGEBRA
# =========================
def test_algebra():
    assert am.solve_linear(2, 4) == pytest.approx(-2.0)
    roots = am.quadratic_roots(1, -3, 2)
    assert roots[0].real == pytest.approx(2.0)
    assert roots[1].real == pytest.approx(1.0)


# =========================
# GEN-AI HELPERS
# =========================
def test_genai_helpers():
    probs = am.logits_to_prob([2.0, 1.0, 0.1])
    assert sum(probs) == pytest.approx(1.0)

    temp_probs = am.softmax_temperature([2.0, 1.0, 0.1], 0.7)
    assert sum(temp_probs) == pytest.approx(1.0)

    attn = am.attention_scores([[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1], [2]])
    assert len(attn) == 2


# =========================
# OPTIMIZATION
# =========================
def test_optimization():
    w_new = am.sgd_update([0.5, -0.3], [0.1, -0.2], 0.01)
    assert w_new == pytest.approx([0.499, -0.298])

    w_adam, m_adam, v_adam = am.adam_update(
        [0.5, -0.3], [0.1, -0.2], [0, 0], [0, 0],
        0.001, 0.9, 0.999, 1e-8
    )
    assert len(w_adam) == 2

    w_rmsprop, v_rmsprop = am.rmsprop_update(
        [0.5, -0.3], [0.1, -0.2], [0, 0], 0.001, 0.9, 1e-8
    )
    assert len(w_rmsprop) == 2

    assert am.lr_step_decay(0.1, 10, 0.5) == pytest.approx(1e-21, rel=1e-2)
    assert am.lr_cosine_anneal(0.1, 0.001, 50) == pytest.approx(0.1, rel=1e-3)

    w_mom, v_mom = am.momentum_update(
        [0.5, -0.3], [0.1, -0.2], [0, 0], 0.01, 0.9
    )
    assert len(w_mom) == 2


# =========================
# GRAPH
# =========================
def test_graph():
    dist = am.bfs_distance({0: [1, 2], 1: [2], 2: [3], 3: []}, 0)
    assert dist == {0: 0, 1: 1, 2: 1, 3: 2}

    dists, parents = am.dijkstra_shortest_path(
        {0: {1: 4, 2: 1}, 1: {3: 1}, 2: {1: 2, 3: 5}, 3: {}},
        0
    )
    assert dists[3] == 2  # shortest distance to node 3
    assert parents[3] in {1, 2}


# =========================
# VISION
# =========================
def test_vision():
    assert am.conv2d_output_shape((64, 64), (3, 3), 1, 0, 1) == (62, 62)
    assert am.maxpool_output_shape((64, 64), 2, 2, 0) == (32, 32)
    assert am.iou((0, 0, 10, 10), (5, 5, 15, 15)) == pytest.approx(0.1428571429)
    keep = am.nms([(0, 0, 10, 10, 0.9),
                   (1, 1, 9, 9, 0.8),
                   (20, 20, 30, 30, 0.7)])
    assert keep == [0, 2]


# =========================
# NUMBER THEORY
# =========================
def test_number_theory():
    assert am.is_prime(29) is True
    assert am.prime_factors(84) == [2, 2, 3, 7]
    assert am.totient(9) == 6
    assert am.mod_inverse(3, 11) == 4
    assert am.modular_pow(2, 10, 1000) == 24
    assert am.fibonacci(7) == 13
    assert am.pell_number(5) == 29
    assert am.catalan_number(4) == 14
    assert am.divisor_count(28) == 6
    assert am.divisor_sum(28) == 56
