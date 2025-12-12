import math
from scipy.stats import norm, t
import numpy as np


# ======================================================================
#   1. Z-TEST FOR ONE MEAN  (supports two-tailed, left, right)
# ======================================================================
def z_test_one_mean(xbar, mu0, sigma, n, alpha=0.05, tail="two"):
    """
    Perform a Z-test for one mean.

    Parameters:
    - xbar : sample mean
    - mu0 : population mean under H0
    - sigma : population standard deviation
    - n : sample size
    - alpha : significance level (default 0.05)
    - tail : 'two' (default), 'left', or 'right'

    Returns:
    - z : Z-statistic
    - p_value : p-value according to tail type
    """

    # Z statistic
    z = (xbar - mu0) / (sigma / math.sqrt(n))

    # ---- Two-tailed test ----
    if tail == "two":
        p_value = 2 * (1 - norm.cdf(abs(z)))
        z_crit = norm.ppf(1 - alpha / 2)
        reject = abs(z) > z_crit
        critical_region = f"|Z| > {z_crit:.3f}"

    # ---- Right-tailed test ----
    elif tail == "right":
        p_value = 1 - norm.cdf(z)
        z_crit = norm.ppf(1 - alpha)
        reject = z > z_crit
        critical_region = f"Z > {z_crit:.3f}"

    # ---- Left-tailed test ----
    elif tail == "left":
        p_value = norm.cdf(z)
        z_crit = norm.ppf(alpha)
        reject = z < z_crit
        critical_region = f"Z < {z_crit:.3f}"

    else:
        raise ValueError("tail must be 'two', 'left', or 'right'")

    # Output
    print("\n--- Z-Test for One Mean ---")
    print(f"Test Type: {tail}-tailed")
    print(f"Z-statistic = {z:.3f}")
    print(f"p-value     = {p_value:.5f}")
    print(f"Critical Region: {critical_region}")

    if reject:
        print("Decision: Reject H₀ → Significant difference.")
    else:
        print("Decision: Fail to reject H₀ → No significant difference.")

    return z, p_value



# ======================================================================
#   2. Z-TEST FOR TWO PROPORTIONS (also supports tail options)
# ======================================================================
def z_test_two_proportions(n1, x1, n2, x2, alpha=0.05, tail="two"):
    """
    Perform a Z-test for the difference of two proportions.

    Parameters:
    - n1, x1 : sample size and successes for group 1
    - n2, x2 : sample size and successes for group 2
    - alpha : significance level
    - tail : 'two' (default), 'left', 'right'

    Returns:
    - z : Z-statistic
    - p_value : p-value
    """

    # Validation
    if not (0 <= x1 <= n1):
        raise ValueError("x1 must be between 0 and n1.")
    if not (0 <= x2 <= n2):
        raise ValueError("x2 must be between 0 and n2.")

    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    if p_pool in [0, 1]:
        raise ValueError("Pooled proportion is 0 or 1 → Z-test undefined.")

    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se

    # ---- Two-tailed ----
    if tail == "two":
        p_value = 2 * (1 - norm.cdf(abs(z)))
        z_crit = norm.ppf(1 - alpha / 2)
        reject = abs(z) > z_crit
        critical_region = f"|Z| > {z_crit:.3f}"

    # ---- Right-tailed ----
    elif tail == "right":
        p_value = 1 - norm.cdf(z)
        z_crit = norm.ppf(1 - alpha)
        reject = z > z_crit
        critical_region = f"Z > {z_crit:.3f}"

    # ---- Left-tailed ----
    elif tail == "left":
        p_value = norm.cdf(z)
        z_crit = norm.ppf(alpha)
        reject = z < z_crit
        critical_region = f"Z < {z_crit:.3f}"

    else:
        raise ValueError("tail must be 'two', 'left', or 'right'")

    print("\n--- Z-Test for Two Proportions ---")
    print(f"p1 = {p1:.3f}, p2 = {p2:.3f}, pooled p = {p_pool:.3f}")
    print(f"Z-statistic = {z:.3f}")
    print(f"p-value     = {p_value:.5f}")
    print(f"Critical Region: {critical_region}")

    if reject:
        print("Decision: Reject H₀ → Proportions differ.")
    else:
        print("Decision: Fail to reject H₀ → No significant difference.")

    return z, p_value



# ======================================================================
#   3. CI FOR ONE MEAN  (t and z)
# ======================================================================
def ci_one_mean_t(n, xbar, sd, confidence=0.95):
    alpha = 1 - confidence
    t_crit = t.ppf(1 - alpha / 2, df=n - 1)
    margin = t_crit * (sd / math.sqrt(n))
    return xbar - margin, xbar + margin


def ci_one_mean_z(n, xbar, sigma, confidence=0.95):
    alpha = 1 - confidence
    z_crit = norm.ppf(1 - alpha / 2)
    margin = z_crit * (sigma / math.sqrt(n))
    return xbar - margin, xbar + margin



# ======================================================================
#   4. CI FOR DIFFERENCE OF TWO MEANS (t and z)
# ======================================================================
def ci_two_means_independent_t(n1, mean1, sd1, n2, mean2, sd2, confidence=0.95):
    alpha = 1 - confidence

    se = math.sqrt(sd1**2 / n1 + sd2**2 / n2)

    df = (se**4) / (
        (sd1**4 / (n1**2 * (n1 - 1))) +
        (sd2**4 / (n2**2 * (n2 - 1)))
    )

    t_crit = t.ppf(1 - alpha / 2, df=df)

    diff = mean1 - mean2
    margin = t_crit * se
    return diff - margin, diff + margin


def ci_two_means_independent_z(n1, mean1, sigma1, n2, mean2, sigma2, confidence=0.95):
    alpha = 1 - confidence
    z_crit = norm.ppf(1 - alpha / 2)

    se = math.sqrt(sigma1**2 / n1 + sigma2**2 / n2)
    diff = mean1 - mean2
    margin = z_crit * se

    return diff - margin, diff + margin

import math

def sprt_normal(data, mu0, mu1, sigma, alpha=0.05, beta=0.10):
    """
    SPRT for Normal distribution with known variance.
    
    data: iterable of samples X1, X2, ...
    mu0, mu1: means under H0 and H1
    sigma: known standard deviation
    """
    A = math.log((1-beta)/alpha)
    B = math.log(beta/(1-alpha))

    llr = 0
    sum_x = 0
    
    for i, x in enumerate(data, start=1):
        sum_x += x
        
        # LLR formula
        llr = ((mu1 - mu0) / (sigma**2)) * (sum_x - i * (mu0 + mu1) / 2)

        print(f"n={i}, x={x}, LLR={llr:.4f}")

        # Decisions
        if llr >= A:
            print(f"Accept H1 at n={i}")
            return "H1"
        elif llr <= B:
            print(f"Accept H0 at n={i}")
            return "H0"

    print("Continue sampling...")
    return "Continue"

import math

def sprt_binomial(data, p0, p1, alpha=0.05, beta=0.10):
    """
    Wald SPRT for Binomial data (Bernoulli stream of 0/1 values)
    
    data: iterable of observations (0 or 1)
    p0, p1 : probabilities under H0 and H1
    alpha : Type I error
    beta : Type II error
    """
    # Decision thresholds
    A = math.log((1 - beta) / alpha)
    B = math.log(beta / (1 - alpha))

    log_likelihood_ratio = 0

    for i, x in enumerate(data, start=1):
        # Log likelihood increment
        ll = math.log(p1 / p0) if x == 1 else math.log((1 - p1) / (1 - p0))
        log_likelihood_ratio += ll

        print(f"n={i}, x={x}, LLR={log_likelihood_ratio:.4f}")

        # Decision rules
        if log_likelihood_ratio >= A:
            print(f"Accept H1 at n={i}")
            return "H1"
        elif log_likelihood_ratio <= B:
            print(f"Accept H0 at n={i}")
            return "H0"

    print("Continue sampling...")
    return "Continue"

