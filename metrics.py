import pandas as pd
import numpy as np

from scipy import stats


def pof_test(var, target, alpha=0.99):
    failures = []
    for var_, target_ in zip(var, target):
        if var_ > target_:
            failures.append(1)
        else:
            failures.append(0)
    failures = np.array(failures)

    N = float(len(var))
    x = float(failures.sum())
    LR_POF = -2 * np.log(
        ((alpha ** (N - x)) * ((1 - alpha) ** x))
        / (((1 - x / N) ** (N - x)) * (x / N) ** x)
    )
    pof = 1 - stats.chi2.cdf(LR_POF, 1)
    return pof


def if_test(var, target):
    hits = (var > target).astype(float)
    changes = hits[1:] - hits[:-1]
    n00 = (hits[1:][changes == 0] == 0).sum()
    n11 = (hits[1:][changes == 0] == 1).sum()
    n01 = (changes == 1).sum()
    n10 = (changes == -1).sum()

    n0 = n01 + n00
    n1 = n10 + n11
    n = n0 + n1
    # print(hits)
    print(n11, n10, n11)

    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n11 + n10)
    pi_ = n1 / n

    LR_CCI = ((1 - pi_) ** (n00 + n10)) * (pi_ ** (n01 + n11))
    LR_CCI /= ((1 - pi0) ** n00) * (pi0 ** n01)
    LR_CCI /= ((1 - pi1) ** n10) * (pi1 ** n11)
    LR_CCI = -2 * np.log(LR_CCI)
    CCI = 1 - stats.chi2.cdf(LR_CCI, 1)
    return CCI


def quantile_loss(var, target, alpha=0.99):
    Q = []
    for var_, target_ in zip(var, target):
        if target_ < var_:
            Q.append(2 * alpha * (var_ - target_))
        else:
            Q.append(2 * (1 - alpha) * (target_ - var_))
    Q = np.mean(Q)
    return Q
