import numpy as np
from scipy.stats import chi2

def pof_test(var, target, alpha=0.99):
    N = len(var)
    x = 0
    for i in range(len(var)):
        if target[i] < var[i]:
            x += 1
    LR_pof = -2*np.log((alpha)**(N-x)*(1-alpha)**x /(1-x/N)**(N-x)/(x/N)**x)
    return 1 - chi2.cdf(LR_pof, 1)
    
def if_test(var, target):
    hits = (var>target)
    n00, n10, n01, n11 = 0, 0, 0, 0
    for i in range(len(target)-1):
        if hits[i] == False and hits[i+1] == False:
            n00 += 1
        elif hits[i] == True and hits[i+1] == False:
            n10 += 1
        elif hits[i] == False and hits[i+1] == True:
            n01 += 1
        else:
            n11 += 1
            
    pi0 = n01/(n01 + n00)
    pi1 = n11/(n11 + n10)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    
    LR_cci = -2*np.log((1-pi)**(n00+n10)*pi**(n01+n11)/(1-pi0)**n00/pi0**n01/(1-pi1)**n10/pi1**n11)
    return 1 - chi2.cdf(LR_cci, 1)


def quantile_loss(var, target, alpha=0.99):
    Q_loss = np.zeros(len(var))
    for i in range(len(var)):
        if target[i] < var[i]:
            Q_loss[i] = 2 * alpha * (var[i] - target[i])
        else:
            Q_loss[i] = 2 * (1 - alpha) * (target[i] - var[i])
    return Q_loss.mean()