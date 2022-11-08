import numpy as np
import scipy as stats


def pof_test(var, target, alpha=0.99):
    x = 0
    for i in range(len(var)):
        if var[i] > target[i]:
            x += 1
    N = len(var)
    lr_pof = -2 * np.log((alpha ** (N - x) * (1 - alpha) ** x) / ((1 - x / N) ** (N - x) * (x / N) ** x))
    return 1 - stats.chi2.cdf(lr_pof, 1)


def if_test(var, target):  
    aux = [int(target[i] < var[i]) for i in range(len(var))]
    n_00, n_10, n_01, n_11 = 0, 0, 0, 0
    for i in range(1, len(aux)):
        if aux[i] == 0 and aux[i - 1] == 0:
            n_00 += 1
        if aux[i] == 1 and aux[i - 1] == 0:
            n_10 += 1
        if aux[i] == 0 and aux[i - 1] == 1:
            n_01 += 1
        if aux[i] == 1 and aux[i - 1] == 1:
            n_11 += 1

    pi_0 = n_01 / (n_00 + n_01)
    pi_1 = n_11 / (n_10 + n_11)
    pi = (n_01 + n_11) / (n_00 + n_01 + n_10 + n_11)

    lr_cci = -2 * np.log(((1 - pi) ** (n_00 + n_10) * pi ** (n_01 + n_11)) / (
                (1 - pi_0) ** n_00 * pi_0 ** n_01 * (1 - pi_1) ** n_10 * pi_1 ** n_11))

    return 1 - stats.chi2.cdf(lr_cci, 1)


def quantile_loss(var, target, alpha=0.99):  
    q_loss = np.zeros(len(var))
    N = len(var)
    for i in range(N):
        if target[i] < var[i]:
            q_loss[i] = 2 * alpha * (var[i] - target[i])
        else:
            q_loss[i] = 2 * (1 - alpha) * (target[i] - var[i])
    return q_loss.mean()
