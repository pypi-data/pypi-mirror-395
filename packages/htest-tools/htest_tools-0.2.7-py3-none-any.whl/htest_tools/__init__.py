# __init__.py

# -------------------------------
# Z-tests (your existing functions)
# -------------------------------
from .htests import (
    z_test_one_mean,
    z_test_two_proportions,
    ci_one_mean_t,
    ci_one_mean_z,
    ci_two_means_independent_t,
    ci_two_means_independent_z,
)

# -------------------------------
# Neyman–Pearson / UMP Tests
# -------------------------------
from .np_lemma_tests import (
    np_binom,
    np_pois,
    np_norm,
)

# -------------------------------
# Estimator Properties + CRLB
# -------------------------------
from .estimator_properties import (
    est_norm_mean,
    est_binom_p,
    est_pois_lam,
    crlb_norm,
    crlb_binom,
    crlb_pois,
)

# -------------------------------
# Maximum Likelihood Estimators
# (now from mle_est.py)
# -------------------------------
from .mle_est import (
    mle_norm,
    mle_binom,
    mle_exp,
)

# -------------------------------
# What this package exports
# -------------------------------
__all__ = [

    # Z-tests
    "z_test_one_mean",
    "z_test_two_proportions",
    "ci_one_mean_t",
    "ci_one_mean_z",
    "ci_two_means_independent_t",
    "ci_two_means_independent_z",

    # NP / UMP
    "np_binom",
    "np_pois",
    "np_norm",

    # Estimators
    "est_norm_mean",
    "est_binom_p",
    "est_pois_lam",

    # CRLB
    "crlb_norm",
    "crlb_binom",
    "crlb_pois",

    # MLE
    "mle_norm",
    "mle_binom",
    "mle_exp",
]
