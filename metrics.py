from scipy.stats import chi2
import numpy as np


def pof_test(var, target, alpha=0.99):
    N = len(var)
    X = 0
    for i in range(N):
        if target[i] < var[i]:
            X += 1
    a = alpha ** (N - X) * (1 - alpha) ** X
    b = (1 - X / N) ** (N - X) * (X / N) ** X
    POF = -2 * np.log(a / b)
    p_value = 1 - chi2.cdf(POF, df=1)
    return  p_value


def if_test(var, target):
    fails = target > var
    n_00, n_01, n_10, n_11 = 0, 0, 0, 0
    for i in range(len(var) - 1):
        if target[i] <= var[i] and target[i + 1] <= var[i + 1]:
            n_00 += 1
        elif target[i] > var[i] and target[i + 1] <= var[i + 1]:
            n_10 += 1
        elif target[i] <= var[i] and target[i + 1] > var[i + 1]:
            n_01 += 1
        else:
            n_11 += 1
    pi_0 = n_01 / (n_00 + n_01)
    pi_1 = n_11 / (n_10 + n_11)
    pi = (n_01 + n_11) / (n_00 + n_01 + n_10 + n_11)
    a = (1 - pi) ** (n_00 + n_10) * pi ** (n_01 + n_11)
    b = (1 - pi_0) ** n_00 * pi_0 ** n_01 * (1 - pi_1) ** n_10 * pi_1 ** n_11
    CCI = -2 * (np.log(a / b))
    p_value = 1 - chi2.cdf(CCI, df=1)
    return p_value


def quantile_loss(var, target, alpha=0.99):
    res = []
    for i in range(len(var)):
        if target[i] < var[i]:
            res.append(2 * alpha * (var[i] - target[i]))
        else:
            res.append(2 * (1 - alpha) * (target[i] - var[i]))
    p_value = np.average(res)
    return p_value
