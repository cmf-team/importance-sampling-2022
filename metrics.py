import math
from scipy.stats import chi2
import numpy as np


def pof_test(var, target, alpha=0.99):
    """Computes p-value for Kupiec’s Proportion of Failures Test.
    https://www.mathworks.com/help/risk/overview-of-var-backtesting.html#bu_mbvb-1
    """
    if len(var) != len(target):
        raise ValueError('`var` and `target` must have equal lengths')
    x = (target < var).astype(int).sum()  # number of failures
    p = 1 - alpha
    N = len(var)
    test_statistic = -2 * math.log(
        ((1 - p)**(N - x) * p**x) /
        ((1 - x/N)**(N - x) * (x/N)**x)
    )
    p_value = 1 - chi2.cdf(test_statistic, df=1)  # df is degrees of freedom
    return p_value


def if_test(var, target):
    """Computes p-value for ChristofferSen’s Interval Forecast Test.
    https://www.mathworks.com/help/risk/overview-of-var-backtesting.html#bu_mbwo-1
    """
    if len(var) != len(target):
        raise ValueError('`var` and `target` must have equal lengths')
    hits = (target < var).astype(int)
    changes = hits[1:] - hits[:-1]
    n01 = (changes == 1).sum()
    n10 = (changes == -1).sum()
    n00 = (changes == 0)[hits[1:] == 0].sum()
    n11 = (changes == 0)[hits[1:] == 1].sum()
    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    test_statistic = -2 * math.log(
        ((1 - pi)**(n00 + n10) * pi**(n01 + n11)) /
        ((1 - pi0)**n00 * pi0**n01 * (1 - pi1)**n10 * pi1**n11)
    )
    p_value = 1 - chi2.cdf(test_statistic, df=1)  # df is degrees of freedom
    return p_value


def quantile_loss(var, target, alpha=0.99):
    """Computes mean quantile loss."""
    if len(var) != len(target):
        raise ValueError('`var` and `target` must have equal lengths')
    quantile_losses = np.where(
        target < var,
        2 * alpha * (var - target),
        2 * (1 - alpha) * (target - var))
    return quantile_losses.mean()
