import numpy as np
import math
import scipy.stats as st


def pof_test(var, target, alpha=0.99):
    k = np.sum(target < var)
    l = len(target)
    a0 = k/l
    s = 2*math.log( (1-a0)**(l-k) * a0**k ) - 2*math.log( (1-alpha)**(l-k) * alpha**k )

    return 1 - st.chi2.cdf(s)
    

def if_test(var, target):

    n00 = 0
    n10 = 0
    n01 = 0
    n11 = 0

    for i in range (len(target) - 1):
        if (target[i] > var[i]) and (target[i + 1] > var[i + 1]):
            n00 += 1
        elif (target[i] < var[i]) and (target[i + 1] > var[i + 1]):
            n10 += 1
        elif (target[i] > var[i]) and (target[i + 1] < var[i + 1]):
            n01 += 1
        elif (target[i] < var[i]) and (target[i + 1] < var[i + 1]):
            n11 += 1

    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)

    s = 2 * math.log((1 - pi0)**n00 * pi0**n01 * (1 - pi1)**n10 * pi1**n11) - 2 * math.log((1 - pi)**(n00 + n10) * pi**(n01 + n11))

    return 1 - st.chi2.cdf(s)


def quantile_loss(var, target, alpha=0.99):

    q = np.zeros(len(target))
    
    for i in range(len(target)):
        if (target[i] < var[i]):
            q[i] = 2 * alpha * (var[i] - target[i])
        if (target[i] >= var[i]):
            q[i] = 2 * (1 - alpha) * (target[i] - var[i])

    return np.mean(q)
