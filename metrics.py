import numpy as np
from scipy import stats

def pof_test(var, target, alpha=0.99): #Kupiec’s Proportion of Failures Test
    # observations
    N = len(var)  
    #failures
    x = np.sum(target < var)
    
    lr_pof = -2 * np.log(((alpha ** (N - x)) * ((1 - alpha) ** x)) / (((1 - x / N) ** (N - x)) * (x / N) ** x))
    return 1 - stats.chi2.cdf(lr_pof, 1)


def if_test(var, target): #Christoffersen’s Interval Forecast Test
    F = [int(target[i] < var[i]) for i in range(len(var))]
    n_kk = np.zeros(4)
    for i in range(1, len(F)):
        if F[i] == 0 and F[i - 1] == 0:
            n_kk[0] += 1
        if F[i] == 1 and F[i - 1] == 0:
            n_kk[1] += 1
        if F[i] == 1 and F[i - 1] == 0:
            n_kk[2] += 1
        if F[i] == 1 and F[i - 1] == 1:
            n_kk[3] += 1

    p0 = n_kk[1] / (n_kk[0] + n_kk[1])
    p1 = n_kk[3] / (n_kk[2] + n_kk[3])
    
    p = (n_kk[1] + n_kk[3]) / (np.sum(n_kk))

    log_cci = -2 * np.log(
        ((1 - p) ** (n_kk[0] + n_kk[2]) * p ** (n_kk[1] + n_kk[3]))
        / ((1 - p0) ** (n_kk[0]) * p0 ** (n_kk[1]) * (1 - p1) ** n_kk[2] * p1**n_kk[3])
    )

    return 1 - stats.chi2.cdf(log_cci, 1)


def quantile_loss(var, target, alpha=0.99): # average value quantile loss
    loss = np.zeros(len(var))
    for i in range(len(var)):
        if (target[i] < var[i]):
            loss[i] = 2*alpha*(var[i]-target[i])
        else:
            loss[i] = 2*(1-alpha)*(target[i]-var[i])
    return loss.mean()
