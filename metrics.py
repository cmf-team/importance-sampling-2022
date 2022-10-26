import numpy as np
from scipy import stats
def pof_test(var, target, alpha=0.99):
    failures = np.zeros(len(var))
    for i in range(len(var)):
        if var[i] > target[i]:
            failures[i] = 1
    N = float(len(var))
    x = float(failures.sum())
    return stats.chi2.pdf(-2*np.log(((alpha**(N-x))*((1-alpha)**x))/(((1-x/N)**(N-x))*(x/N)**x)) , 1)


def if_test(var, target):
    hits = (var>target)*1#[var<target]
    tr = hits[1:] - hits[:-1]
    n01, n10 = (tr == 1).sum(), (tr == -1).sum()
    n11, n00 = (hits[1:][tr == 0] == 1).sum(), (hits[1:][tr == 0] == 0).sum()

        # Times in the states
    n0, n1 = n01 + n00, n10 + n11
    n = n0 + n1

        # Probabilities of the transitions from one state to another
    p01, p11 = n01 / (n00 + n01), n11 / (n11 + n10)
    p = n1 / n
    #print(stats.chi2.pdf(-2*np.log(((1-p)**(n00+n10)*p**(n01+n11))/((1-p01)**(n00)*p01**(n01)*(1-p11)**n10*p11**n11)) , 1))
    return stats.chi2.pdf(-2*np.log(((1-p)**(n00+n10)*p**(n01+n11))/((1-p01)**(n00)*p01**(n01)*(1-p11)**n10*p11**n11)) , 1)
    #raise Exception(NotImplementedError)


def quantile_loss(var, target, alpha=0.99):
    loss = np.zeros(len(var))
    for i in range(len(var)):
        if (target[i] < var[i]):
            loss[i] = 2*alpha*(var[i]-target[i])
        else:
            loss[i] = 2*(1-alpha)*(target[i]-var[i])
    return loss.mean()