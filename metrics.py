import numpy as np
from scipy import stats


def pof_test(var, target, alpha=0.99):
    fails_count = (target < var).sum()
    n = len(target)
    p = fails_count / n
    num = alpha ** (n - fails_count) * (1 - alpha) ** fails_count
    denum = (1 - p) ** (n - fails_count) * p ** fails_count
    lr_pof = -2 * (np.log(num) - np.log(denum))
    return 1 - stats.chi2.cdf(lr_pof, df=1)


def if_test(var, target):
    fails = target > var
    n00, n10, n01, n11 = 0, 0, 0, 0
    for i in range(len(target) - 1):
        if not fails[i] and not fails[i + 1]:
            n00 += 1
        elif fails[i] and not fails[i + 1]:
            n10 += 1
        elif not fails[i] and fails[i + 1]:
            n01 += 1
        else:
            n11 += 1
    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    num = (1 - pi) ** (n00 + n10) * pi ** (n01 + n11)
    denum = (1 - pi0) ** n00 * pi0 ** n01 * (1 - pi1) ** n10 * pi1 ** n11
    lr_cci = -2 * (np.log(num) - np.log(denum))
    return 1 - stats.chi2.cdf(lr_cci, df=1)


def quantile_loss(var, target, alpha=0.99):
    n = len(target)
    q_loss = np.zeros(n)
    for i in range(n):
        if target[i] < var[i]:
            q_loss[i] = 2 * alpha * (var[i] - target[i])
        else:
            q_loss[i] = 2 * (1 - alpha) * (target[i] - var[i])
    return q_loss.mean()