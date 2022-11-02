import numpy as np
from scipy.stats import chi2

def pof_test(var, target, alpha=0.99):
    x= 0
    for i in range(len(var)):
        if var[i] > target[i]:
            x+= 1
    N = len(target)
    nom =(pow(alpha, N-x) * pow(1 - alpha, x))
    denom = (pow(1 - x / N, N-x)*pow(x/N, x))
    LR = -2*np.log(nom/denom)
    return 1 - chi2.cdf(LR, 1)

def if_test(var, target):
    var = np.array(var)
    target = np.array(target)
    scores = (var - target > 0).astype(int)
    thresh = scores[1:] - scores[:-1]

    n01 = (thresh == 1).sum()
    n10 = (thresh == -1).sum()
    n11 = (thresh[thresh == 0] == True).sum()
    n00 = (thresh[thresh == 0] == False).sum()

    pi0 = n01/(n00 + n01)
    pi1 = n11/(n00 + n11)
    pi = (n01 + n11)/(n00 + n10 + n01 + n11)

    nom = pow(1-pi, n00 + n10) * pow(pi, n01 + n11)
    denom = pow(1 - pi0, n00) * pow(pi0, n01) * pow(1-pi1, n10) * pow(pi1, n11)
    LR = -2*np.log(nom/denom)
    return chi2.pdf(LR, 2)

def quantile_loss(var, target, alpha=0.95):
    Q = []
    for i in range(len(target)):
        y = target[i]
        var_i = var[i]
        if y >= var_i:
            val = 2 * (1-alpha) * (y - var_i)
        else:
            val = 2 * alpha * (var_i - y)
        Q.append(val)
    return np.array(Q).mean()