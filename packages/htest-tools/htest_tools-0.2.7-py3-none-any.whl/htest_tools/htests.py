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
