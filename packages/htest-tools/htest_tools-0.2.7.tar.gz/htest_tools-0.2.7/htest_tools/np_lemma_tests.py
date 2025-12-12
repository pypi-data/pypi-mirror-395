# np_lemma_tests.py
import numpy as np
from dataclasses import dataclass
from typing import Literal, Dict, Any

from scipy.stats import binom, poisson, norm


Alternative = Literal["greater", "less", "two-sided"]


@dataclass
class TestResult:
    test_name: str
    distribution: str
    statistic_name: str
    statistic_value: float
    critical_region: str
    alpha: float
    p_value: float
    reject_h0: bool
    h0: str
    h1: str
    interpretation: str
    extra: Dict[str, Any]

    def __str__(self):
        """Pretty print summary with interpretation."""
        lines = [
            f"Test: {self.test_name}",
            f"Distribution: {self.distribution}",
            f"Statistic: {self.statistic_name} = {self.statistic_value}",
            f"Critical region: {self.critical_region}",
            f"alpha: {self.alpha}",
            f"p-value: {self.p_value}",
            f"Reject H0? {self.reject_h0}",
            f"H0: {self.h0}",
            f"H1: {self.h1}",
            "Interpretation:",
            self.interpretation,
        ]
        return "\n".join(lines)


# ---------- 3.1 & 3.2 Neyman–Pearson for Binomial ----------

def np_binom(
    x: int,
    n: int,
    p0: float,
    p1: float,
    alpha: float = 0.05,
    alternative: Alternative = "greater",
) -> TestResult:
    """
    Neyman–Pearson MP/UMP test for Binomial(n, p):

    H0: p = p0  vs  H1: p = p1

    For 'greater'/'less' this is UMP over one-sided composite alternatives.
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if not (0 <= x <= n):
        raise ValueError("x must be between 0 and n (inclusive).")
    if not (0.0 <= p0 <= 1.0 and 0.0 <= p1 <= 1.0):
        raise ValueError("p0 and p1 must be in [0, 1].")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1).")

    if alternative == "greater":
        if p1 <= p0:
            raise ValueError("For 'greater', require p1 > p0.")

        # Critical region {X >= c}, smallest c with P(X >= c | p0) <= alpha
        c = None
        for k in range(n + 1):
            if binom.sf(k - 1, n, p0) <= alpha:
                c = k
                break
        if c is None:
            c = n + 1  # essentially no rejection region

        critical_region_str = f"{{x: x >= {c}}}"
        p_value = binom.sf(x - 1, n, p0)
        reject_h0 = x >= c

    elif alternative == "less":
        if p1 >= p0:
            raise ValueError("For 'less', require p1 < p0.")

        # Critical region {X <= c}, largest c with P(X <= c | p0) <= alpha
        c = None
        for k in range(n + 1):
            if binom.cdf(k, n, p0) <= alpha:
                c = k
            else:
                break
        if c is None:
            c = -1  # no rejection region

        critical_region_str = f"{{x: x <= {c}}}"
        p_value = binom.cdf(x, n, p0)
        reject_h0 = x <= c

    else:  # two-sided LRT-style (not UMP in general)
        xs = np.arange(n + 1)
        probs = binom.pmf(xs, n, p0)
        order = np.argsort(probs)   # smallest prob = most extreme
        cum = 0.0
        reject_set = []

        for idx in order:
            if cum + probs[idx] <= alpha + 1e-12:
                reject_set.append(xs[idx])
                cum += probs[idx]
            else:
                break

        reject_h0 = x in reject_set
        # "two-sided" p-value as sum of probabilities <= prob at x
        p_value = float(np.sum(probs[probs <= probs[x] + 1e-15]))
        critical_region_str = f"{{x in {sorted(reject_set)}}}"

    h0 = f"p = {p0}"
    h1 = f"p = {p1} ({alternative})"

    interpretation = (
        f"At α = {alpha}, we {'reject' if reject_h0 else 'do not reject'} H0: {h0}. "
        + (
            "This is the most powerful test for the specified simple hypotheses "
            "and is UMP for the corresponding one-sided composite alternative."
            if alternative in ("greater", "less")
            else "This two-sided test is based on the likelihood-ratio principle."
        )
    )

    return TestResult(
        test_name="Neyman–Pearson Binomial test",
        distribution="Binomial",
        statistic_name="X (number of successes)",
        statistic_value=float(x),
        critical_region=critical_region_str,
        alpha=alpha,
        p_value=float(p_value),
        reject_h0=reject_h0,
        h0=h0,
        h1=h1,
        interpretation=interpretation,
        extra={"n": n, "p0": p0, "p1": p1, "alternative": alternative},
    )


# ---------- Neyman–Pearson for Poisson ----------

def np_pois(
    x: int,
    lambda0: float,
    lambda1: float,
    alpha: float = 0.05,
    alternative: Alternative = "greater",
) -> TestResult:
    """
    Neyman–Pearson MP/UMP test for Poisson(λ):

    H0: λ = lambda0  vs  H1: λ = lambda1
    """
    if x < 0:
        raise ValueError("x must be non-negative.")
    if lambda0 < 0 or lambda1 < 0:
        raise ValueError("lambda0 and lambda1 must be >= 0.")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1).")

    if alternative == "greater":
        if lambda1 <= lambda0:
            raise ValueError("For 'greater', require lambda1 > lambda0.")

        # {X >= c} – search c such that P(X >= c | λ0) <= alpha
        c = None
        max_k = int(lambda0 + 10 * np.sqrt(lambda0 + 1)) + 20
        for k in range(max_k + 1):
            if poisson.sf(k - 1, lambda0) <= alpha:
                c = k
                break
        if c is None:
            c = max_k + 1

        critical_region_str = f"{{x: x >= {c}}}"
        p_value = poisson.sf(x - 1, lambda0)
        reject_h0 = x >= c

    elif alternative == "less":
        if lambda1 >= lambda0:
            raise ValueError("For 'less', require lambda1 < lambda0.")

        # {X <= c} – largest c with P(X <= c | λ0) <= alpha
        c = None
        max_k = int(lambda0 + 10 * np.sqrt(lambda0 + 1)) + 20
        for k in range(max_k + 1):
            if poisson.cdf(k, lambda0) <= alpha:
                c = k
            else:
                break
        if c is None:
            c = -1

        critical_region_str = f"{{x: x <= {c}}}"
        p_value = poisson.cdf(x, lambda0)
        reject_h0 = x <= c

    else:  # two-sided LRT-style
        upper = max(20, int(lambda0 + 10 * np.sqrt(lambda0 + 1)) + 20)
        xs = np.arange(0, upper + 1)
        pmf = poisson.pmf(xs, lambda0)
        order = np.argsort(pmf)
        cum = 0.0
        reject_set = []

        for idx in order:
            if cum + pmf[idx] <= alpha + 1e-12:
                reject_set.append(xs[idx])
                cum += pmf[idx]
            else:
                break

        reject_h0 = x in reject_set
        p_value = float(np.sum(pmf[pmf <= poisson.pmf(x, lambda0) + 1e-15]))
        critical_region_str = f"{{x in {sorted(reject_set)}}}"

    h0 = f"λ = {lambda0}"
    h1 = f"λ = {lambda1} ({alternative})"

    interpretation = (
        f"At α = {alpha}, we {'reject' if reject_h0 else 'do not reject'} H0: {h0}. "
        + (
            "This Neyman–Pearson test is most powerful for the given simple hypotheses "
            "and UMP for the corresponding one-sided composite alternative."
            if alternative in ("greater", "less")
            else "This two-sided test is based on the likelihood-ratio principle."
        )
    )

    return TestResult(
        test_name="Neyman–Pearson Poisson test",
        distribution="Poisson",
        statistic_name="X (count)",
        statistic_value=float(x),
        critical_region=critical_region_str,
        alpha=alpha,
        p_value=float(p_value),
        reject_h0=reject_h0,
        h0=h0,
        h1=h1,
        interpretation=interpretation,
        extra={"lambda0": lambda0, "lambda1": lambda1, "alternative": alternative},
    )


# ---------- Neyman–Pearson for Normal (known σ²) ----------

def np_norm(
    xbar: float,
    n: int,
    mu0: float,
    mu1: float,
    sigma: float,
    alpha: float = 0.05,
    alternative: Alternative = "greater",
) -> TestResult:
    """
    Neyman–Pearson MP/UMP z-test for Normal(mean, known variance):

    H0: μ = mu0  vs  H1: μ = mu1
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if sigma <= 0:
        raise ValueError("sigma must be positive.")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1).")

    se = sigma / np.sqrt(n)

    if alternative == "greater":
        if mu1 <= mu0:
            raise ValueError("For 'greater', require mu1 > mu0.")

        z_crit = norm.ppf(1 - alpha)
        c = mu0 + z_crit * se
        z_obs = (xbar - mu0) / se
        p_value = 1 - norm.cdf(z_obs)
        reject_h0 = xbar >= c
        crit_region_str = f"{{x̄: x̄ >= {c:.4f}}}"

    elif alternative == "less":
        if mu1 >= mu0:
            raise ValueError("For 'less', require mu1 < mu0.")

        z_crit = norm.ppf(alpha)
        c = mu0 + z_crit * se
        z_obs = (xbar - mu0) / se
        p_value = norm.cdf(z_obs)
        reject_h0 = xbar <= c
        crit_region_str = f"{{x̄: x̄ <= {c:.4f}}}"

    else:  # two-sided
        z_crit = norm.ppf(1 - alpha / 2)
        lower = mu0 - z_crit * se
        upper = mu0 + z_crit * se
        z_obs = (xbar - mu0) / se
        p_value = 2 * (1 - norm.cdf(abs(z_obs)))
        reject_h0 = (xbar <= lower) or (xbar >= upper)
        crit_region_str = f"{{x̄: x̄ <= {lower:.4f} or x̄ >= {upper:.4f}}}"

    h0 = f"μ = {mu0}"
    h1 = f"μ = {mu1} ({alternative})"

    interpretation = (
        f"At α = {alpha}, we {'reject' if reject_h0 else 'do not reject'} H0: {h0}. "
        + (
            "For one-sided alternatives, this z-test coincides with the Neyman–Pearson "
            "most powerful test and is UMP over μ > μ₀ or μ < μ₀."
            if alternative in ("greater", "less")
            else "This is the usual two-sided z-test based on the likelihood ratio."
        )
    )

    return TestResult(
        test_name="Neyman–Pearson Normal test (known σ²)",
        distribution="Normal",
        statistic_name="x̄ (sample mean)",
        statistic_value=float(xbar),
        critical_region=crit_region_str,
        alpha=alpha,
        p_value=float(p_value),
        reject_h0=reject_h0,
        h0=h0,
        h1=h1,
        interpretation=interpretation,
        extra={
            "n": n,
            "mu0": mu0,
            "mu1": mu1,
            "sigma": sigma,
            "alternative": alternative,
        },
    )
