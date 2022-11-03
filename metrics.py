import numpy as np
from scipy import stats

def pof_test(var, target, alpha=0.99):
    Number_of_Fail = 0
    T = len(target)
    for i in range (T):
        if target[i] < var[i]:
            Number_of_Fail += 1
    N = Number_of_Fail
    t = (1-N/T)**(T-N)*(N/T)**N
    c = ((alpha)**(T-N))*((1-alpha)**N)
    LR_POF = 2*np.log(t)-2*np.log(c)
    res = 1 - stats.chi2.cdf(LR_POF, df=1)
    return res


def if_test(var, target):
    TF = [target[i] > var[i] for i in range(len(target))]
    n00 = 0
    n10 = 0
    n01 = 0
    n11 = 0
    for i in range(len(TF) - 1):
        if TF[i] == True and TF[i + 1] == True:
            n00 = n00 + 1
    for m in range(len(TF) - 1):
        if TF[m] == False and TF[m + 1] == True:
            n10 = n10 + 1
    for q in range(len(TF) - 1):
        if TF[q] == True and TF[q + 1] == False:
            n01 = n01 + 1
    for f in range(len(TF) - 1):
        if TF[f] == False and TF[f + 1] == False:
            n11 = n11 + 1

    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    Numeritor = ((1 - pi) ** (n00 + n10)) * (pi ** (n01 + n11))
    Denominator = ((1 - pi0) ** (n00)) * (pi0 ** n01) * ((1 - pi1) ** (n10)) * (pi1 ** n11)
    LR_CCI = -2 * np.log(Numeritor / Denominator)
    return 1 - stats.chi2.cdf(LR_CCI, df=1)



def quantile_loss(var, target, alpha=0.99):
    T = len(target)
    Q_loss = np.zeros(T)
    for i in range(T):
        if target[i] < var[i]:
            Q_loss[i] = 2 * alpha * (var[i] - target[i])
        else:
            Q_loss[i] = 2 * (1 - alpha) * (target[i] - var[i])
    return Q_loss.mean()

