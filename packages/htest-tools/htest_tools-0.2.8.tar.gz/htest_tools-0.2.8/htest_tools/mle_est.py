# mle_estimators.py
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MLEOutput:
    model: str
    parameters_hat: Dict[str, float]
    log_likelihood: float
    interpretation: str
    extra: Dict[str, Any]

    def __str__(self):
        """Pretty print MLE result with interpretation."""
        param_str = ", ".join(
            f"{k} = {v}" for k, v in self.parameters_hat.items()
        )
        lines = [
            f"Model: {self.model}",
            f"MLE parameters: {param_str}",
            f"Log-likelihood at MLE: {self.log_likelihood}",
            "Interpretation:",
            self.interpretation,
        ]
        return "\n".join(lines)


# ---------- Normal distribution MLE (μ, σ² both unknown) ----------

def mle_norm(sample: np.ndarray) -> MLEOutput:
    """
    MLE for Normal(μ, σ²) with both μ and σ² unknown.

    μ̂ = x̄
    σ̂² = (1/n) Σ (x_i - x̄)²

    If all x_i are equal, σ̂² = 0 and the likelihood is unbounded above
    as σ² → 0. We treat this as a degenerate case and set log-likelihood = +∞.
    """
    x = np.asarray(sample, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("Sample must be non-empty.")

    mu_hat = float(x.mean())
    sigma2_hat = float(((x - mu_hat) ** 2).mean())

    if sigma2_hat <= 0.0:
        loglik = float("inf")
    else:
        loglik = -0.5 * n * (np.log(2 * np.pi * sigma2_hat) + 1)

    interpretation = (
        "For Normal(μ, σ²), the MLEs are μ̂ = x̄ and σ̂² = (1/n) Σ (x_i - x̄)². "
        "For non-degenerate data (σ̂² > 0), μ̂ is unbiased and σ̂² is biased but "
        "asymptotically unbiased and efficient. If all observations are equal so that "
        "σ̂² = 0, the likelihood becomes unbounded as σ² → 0 and the model is effectively "
        "degenerate at μ̂."
    )

    return MLEOutput(
        model="Normal(μ, σ²)",
        parameters_hat={"mu_hat": mu_hat, "sigma2_hat": sigma2_hat},
        log_likelihood=float(loglik),
        interpretation=interpretation,
        extra={"n": n},
    )


# ---------- Binomial distribution MLE ----------

def mle_binom(k: int, n: int) -> MLEOutput:
    """
    MLE for p in Binomial(n, p): p̂ = k/n.

    For k = 0 → p̂ = 0, likelihood L = (1 - 0)^n = 1 → log L = 0.
    For k = n → p̂ = 1, likelihood L = 1^n = 1 → log L = 0.
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if not (0 <= k <= n):
        raise ValueError("k must be between 0 and n.")

    p_hat = k / n

    if p_hat == 0.0:
        loglik = 0.0
    elif p_hat == 1.0:
        loglik = 0.0
    else:
        loglik = k * np.log(p_hat) + (n - k) * np.log(1 - p_hat)

    interpretation = (
        "For Binomial(n, p), the MLE is p̂ = k/n (the sample proportion). "
        "For 0 < p̂ < 1, this maximises the binomial likelihood in the interior. "
        "For k = 0 or k = n, the MLE lies at the boundary p̂ = 0 or p̂ = 1, with "
        "log-likelihood 0 (up to the combinatorial constant). The estimator is "
        "unbiased, consistent, and asymptotically efficient."
    )

    return MLEOutput(
        model="Binomial(n, p)",
        parameters_hat={"p_hat": float(p_hat)},
        log_likelihood=float(loglik),
        interpretation=interpretation,
        extra={"n": n, "k": k},
    )


# ---------- Exponential distribution MLE ----------

def mle_exp(sample: np.ndarray) -> MLEOutput:
    """
    MLE for λ in Exponential(λ): λ̂ = 1/x̄, with x_i ≥ 0.

    If all x_i = 0 ⇒ x̄ = 0, the likelihood L(λ) = λ^n is unbounded as λ → ∞.
    We treat this as λ̂ = +∞ and log-likelihood = +∞.
    """
    x = np.asarray(sample, dtype=float)
    if np.any(x < 0):
        raise ValueError("Exponential sample must be non-negative.")

    n = x.size
    if n == 0:
        raise ValueError("Sample must be non-empty.")

    xbar = float(x.mean())

    if xbar <= 0.0:
        lambda_hat = float("inf")
        loglik = float("inf")
    else:
        lambda_hat = 1.0 / xbar
        loglik = n * np.log(lambda_hat) - lambda_hat * x.sum()

    interpretation = (
        "For Exponential(λ), the MLE is λ̂ = 1/x̄ when x̄ > 0. "
        "This estimator is biased but consistent and asymptotically efficient. "
        "If all observations are 0 (x̄ = 0), the likelihood L(λ) = λ^n is unbounded "
        "as λ → ∞, so the MLE formally occurs at λ̂ = +∞ and the model is effectively "
        "degenerate at 0."
    )

    return MLEOutput(
        model="Exponential(λ)",
        parameters_hat={"lambda_hat": float(lambda_hat)},
        log_likelihood=float(loglik),
        interpretation=interpretation,
        extra={"n": n},
    )
