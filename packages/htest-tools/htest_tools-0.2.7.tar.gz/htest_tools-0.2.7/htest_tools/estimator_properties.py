# estimator_properties.py
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EstimatorSummary:
    estimator_name: str
    parameter_name: str
    estimate: float
    theoretical_bias: float
    theoretical_variance: float
    crlb: float
    efficient: bool
    interpretation: str
    extra: Dict[str, Any]

    def __str__(self):
        """Pretty print estimator summary with interpretation."""
        lines = [
            f"Estimator: {self.estimator_name}",
            f"Parameter: {self.parameter_name}",
            f"Estimate: {self.estimate}",
            f"Theoretical bias: {self.theoretical_bias}",
            f"Theoretical variance: {self.theoretical_variance}",
            f"Cramér–Rao lower bound: {self.crlb}",
            f"Efficient (Var == CRLB)? {self.efficient}",
            "Interpretation:",
            self.interpretation,
        ]
        return "\n".join(lines)


# ---------- Cramér–Rao lower bounds (robust) ----------

def crlb_norm(sigma2: float, n: int) -> float:
    """
    CRLB for unbiased estimators of μ in N(μ, σ²).

    For σ² > 0: CRLB = σ² / n
    For σ² = 0 (degenerate): return 0.0
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if sigma2 < 0:
        raise ValueError("sigma2 must be >= 0.")
    return sigma2 / n


def crlb_binom(p: float, n: int) -> float:
    """
    CRLB for unbiased estimators of p in Binomial(n, p).

    For 0 < p < 1: CRLB = p(1 - p) / n
    For p = 0 or p = 1: Fisher info degenerates -> return 0.0
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be in [0, 1].")

    if p == 0.0 or p == 1.0:
        return 0.0
    return p * (1 - p) / n


def crlb_pois(lam: float, n: int) -> float:
    """
    CRLB for unbiased estimators of λ in Poisson(λ).

    For λ > 0: CRLB = λ / n
    For λ = 0: degenerate at 0 -> return 0.0
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if lam < 0:
        raise ValueError("λ must be >= 0.")
    if lam == 0.0:
        return 0.0
    return lam / n


# ---------- Estimator summaries (short names, robust) ----------

def est_norm_mean(sample: np.ndarray, sigma2_known: float) -> EstimatorSummary:
    """
    Properties of the sample mean as estimator of μ for N(μ, σ²)
    with known σ² ≥ 0.
    """
    x = np.asarray(sample, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("Sample must be non-empty.")

    xbar = float(x.mean())
    crlb = crlb_norm(sigma2_known, n)
    var_est = sigma2_known / n

    interpretation = (
        "For Normal(μ, σ²) with known σ², the sample mean x̄ is unbiased for μ. "
        "Its variance is σ²/n, which equals the Cramér–Rao lower bound whenever σ² > 0, "
        "so x̄ is efficient and consistent in that case. If σ² = 0, the distribution is "
        "degenerate and the estimator has zero variance."
    )

    efficient_flag = np.isclose(var_est, crlb)

    return EstimatorSummary(
        estimator_name="sample mean",
        parameter_name="μ",
        estimate=xbar,
        theoretical_bias=0.0,
        theoretical_variance=var_est,
        crlb=crlb,
        efficient=efficient_flag,
        interpretation=interpretation,
        extra={"n": n, "sigma2": sigma2_known},
    )


def est_binom_p(k: int, n: int, p_true: float) -> EstimatorSummary:
    """
    Properties of the sample proportion p̂ = k/n for p in Binomial(n, p_true).

    Handles boundary cases p_true = 0 or 1 gracefully.
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if not (0 <= k <= n):
        raise ValueError("k must be between 0 and n.")
    if not (0.0 <= p_true <= 1.0):
        raise ValueError("p_true must be in [0, 1].")

    p_hat = k / n
    crlb = crlb_binom(p_true, n)
    var_est = p_true * (1 - p_true) / n

    interpretation = (
        "For Binomial(n, p), the estimator p̂ = k/n is unbiased for p. "
        "For 0 < p < 1, Var(p̂) = p(1 - p)/n, which equals the CRLB so p̂ is efficient "
        "and consistent. At the boundary p = 0 or 1, the distribution is degenerate and "
        "both the variance and CRLB are zero."
    )

    efficient_flag = np.isclose(var_est, crlb)

    return EstimatorSummary(
        estimator_name="sample proportion",
        parameter_name="p",
        estimate=p_hat,
        theoretical_bias=0.0,
        theoretical_variance=var_est,
        crlb=crlb,
        efficient=efficient_flag,
        interpretation=interpretation,
        extra={"n": n, "k": k, "p_true": p_true},
    )


def est_pois_lam(counts: np.ndarray, lambda_true: float) -> EstimatorSummary:
    """
    Properties of x̄ as estimator of λ for Poisson(λ_true).

    Handles λ_true = 0 gracefully.
    """
    x = np.asarray(counts, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("Sample must be non-empty.")
    if lambda_true < 0:
        raise ValueError("lambda_true must be >= 0.")

    xbar = float(x.mean())
    crlb = crlb_pois(lambda_true, n)
    var_est = lambda_true / n if lambda_true >= 0 else np.nan

    interpretation = (
        "For Poisson(λ), the sample mean x̄ is unbiased for λ. "
        "For λ > 0, Var(x̄) = λ/n, which equals the CRLB so x̄ is efficient and "
        "consistent. For λ = 0, the distribution is degenerate at 0 and the variance "
        "and CRLB are both zero."
    )

    efficient_flag = np.isclose(var_est, crlb)

    return EstimatorSummary(
        estimator_name="sample mean",
        parameter_name="λ",
        estimate=xbar,
        theoretical_bias=0.0,
        theoretical_variance=var_est,
        crlb=crlb,
        efficient=efficient_flag,
        interpretation=interpretation,
        extra={"n": n, "lambda_true": lambda_true},
    )
