import numpy as np
import scipy.stats as stats
def pof_test(var, target, alpha=0.99):
    # Return: p-value for Kupiec's Proportion of Failures Test  
    N = len(var)
    x = np.count_nonzero(var > target)
    LR_pof = -2 * np.log((alpha**(N-x) * (1 - alpha)**(x))/((1 - x/N)**(N-x) * (x/N)**x))
    return  1 - stats.chi2.cdf(LR_pof, df=1)
    

def if_test(var, target):
    # Return: p-value for Christoffersen's Interval Forecast Test
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
    LR_cci = -2 * (np.log(num/denum))
    return 1 - stats.chi2.cdf(LR_cci, df=1)


def quantile_loss(var, target, alpha=0.99):
    # Return: Mean value for quantile loss
    return np.array([2 * alpha * (var[i] - target[i]) if target[i] < var[i] else 2 * (1 - alpha) * (target[i] - var[i]) 
     for i in range(len(var))]).mean()

