import numpy as np
from scipy import stats

def pof_test(var, target, alpha=0.99):
    """
    Return: p-value for Kupiec's Proportion of Failures Test
    """
    N = len(target) # number of observations 
    x = 0 # number of failures

    for i in range(len(var)):
        if var[i] > target[i]:
            x += 1

    LR_pof = -2 * np.log((alpha**(N-x) * (1 - alpha)**(x))/((1 - x/N)**(N-x) * (x/N)**x))

    p_value = stats.chi2.pdf(LR_pof, 1)

    return p_value


def if_test(var, target):
    """
    Return: p-value for Christoffersen's Interval Forecast Test
    """
    hits  = (var > target) * 1
    tr = hits[1:] - hits[:-1]

    n00 = (hits[1:][tr == 0] == 0).sum() #  Number of periods with no failures followed by a period with no failures
    n10 = (tr == -1).sum() # Number of periods with failures followed by a period with no failures
    n01 = (tr == 1).sum() #  Number of periods with no failures followed by a period with failures
    n11 = (hits[1:][tr == 0] == 1).sum() # Number of periods with failures followed by a period with failures

    pi0 =  n01 / (n00 + n01) # Probability of having a failure on period t, given that no failure occurred on period t − 1 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11) # Probability of having a failure on period t, given that a failure occurred on period t − 1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11) #  Probability of having a failure on period t = (n01 + n11) / (n00 + n01 + n10 + n11)

    LR_cci = -2 * np.log( (1 - pi)**(n00 + n00) * pi**(n01 + n11)/((1 - pi0)**n00 * pi0**n01 * (1 - pi1)**n11) )

    p_value = stats.chi2.pdf(LR_cci, 1)

    return p_value

def quantile_loss(var, target, alpha=0.99):
    """
    Return: Mean value for quantile loss
    """

    q_loss = np.empty(len(var)) 

    for i in range(len(var)):
        if target[i] < var[i]:
            q_loss[i] = 2 * alpha * (var[i] - target[i])
        else:
            q_loss[i] = 2 * (1 - alpha) * (target[i] - var[i])

    return q_loss.mean()