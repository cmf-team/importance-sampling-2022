import numpy as np
import scipy.stats as stats

def pof_test(var, target, alpha=0.99):
    N = 0
    for i in range(len(var)):
        if var[i] > target[i]:
            N += 1
    T = len(target)
    noLong = -2*np.log((pow(alpha, T-N) * pow(1 - alpha, N))/(pow(1 - N/T, T-N)*pow(N/T, N)))
    #ret = stats.norm.ppf(noLong, 1)
    ret =  1 - stats.chi2.cdf(noLong, 1)
    return ret

def if_test(var, target):
    hits = (var>target)*1
    tr = hits[1:] - hits[:-1]
    n01 = (tr == 1).sum()
    n10 = (tr == -1).sum()
    n11 = (hits[1:][tr == 0] == 1).sum()
    n00 = (hits[1:][tr == 0] == 0).sum()
    
    n0 = n01 + n00
    n1 = n10 + n11
    n = n0 + n1
    
    p01, p11 = n01 / (n00 + n01), n11 / (n11 + n10)
    p = n1 / n
    noLong = -2*np.log((pow(1- p, n00+n10)*pow(p, n01+n11))/(pow(1-p01, n00)*pow(p01, n01)*pow(1-p11, n10)*pow(p11, n11)))
    ret = stats.chi2.pdf(noLong, 2)
    return ret

def quantile_loss(var, target, alpha=0.99):
    loss = [0] * len(var)
    for i in range(len(var)):
        if target[i] < var[i]:
            loss[i] = 2 * alpha*(var[i] - target[i])
        else:
            loss[i] = 2 * (1 - alpha)*(target[i] - var[i])
    loss = np.array(loss)
    ret = loss.mean()
    return ret