import numpy as np
import scipy.stats as stats
from math import pow

def pof_test(var, target, alpha=0.99):
    """
    Computes Kupiec’s POF p-value
    """
    # Count the number of samples, failures, and
    # successes below VaR
    n_observations = len(target)
    num_fails = sum(target < var)
    num_success = sum(target >= var)

    proportion_fails  = num_fails / n_observations
    proportion_success = num_success / n_observations

    # Construct statistic
    statistic = (alpha ** num_success) * ((1 - alpha) ** num_fails) / \
                 ((proportion_success ** num_success) * (proportion_fails ** num_fails))

    statistic = - 2 * np.log(statistic)
    p_value = stats.chi2.cdf(statistic, df=1)

    return 1 - p_value


def if_test(var, target):
    """
    Computes Christoffersen’s Interval Forecast
    p_value
    """
    fails_days = target <= var

    counts_falis = {'n00' : 0, 'n10' : 0,
                    'n01' : 0, 'n11' : 0}

    # 1 if days has failed and 0 otherwise
    for idx, value in enumerate(fails_days[:-1]):
        next_value = fails_days[idx + 1]
        sum_failures = value + next_value
        if (value == 0) and (next_value == 0):
            counts_falis['n00'] += 1
        elif (value == 1) and (next_value == 1):
            counts_falis['n11'] += 1
        elif (value == 1) and (next_value == 0):
            counts_falis['n10'] += 1
        else:
            counts_falis['n01'] += 1

    # Calculate probabilities used in statistic
    prob_0 = counts_falis['n01'] / (counts_falis['n00'] + counts_falis['n01'])
    prob_1 = counts_falis['n11'] / (counts_falis['n10'] + counts_falis['n11'])
    prob =  (counts_falis['n01'] + counts_falis['n11']) / \
                        (counts_falis['n00'] + counts_falis['n01'] + \
                         counts_falis['n10'] + counts_falis['n11'])

    statistic = pow(1 - prob, counts_falis['n00'] + counts_falis['n10']) * \
                pow(prob, counts_falis['n01'] + counts_falis['n11'])

    statistic /=  pow(1 - prob_0, counts_falis['n00'])  * \
                  pow(prob_0, counts_falis['n01']) * \
                  pow(1 - prob_1, counts_falis['n10']) * \
                  pow(prob_1, counts_falis['n11'])

    statistic = - 2 * np.log(statistic)

    p_value = stats.chi2.cdf(statistic, df=1)

    return 1 - p_value

def quantile_loss(var, target, alpha=0.99):
    """
    Computes quantile_loss
    """
    # Functions (var, target)
    loss1 = lambda x, y: 2 * alpha * (x - y)
    loss2 = lambda x, y: 2 * (1 - alpha) * (y - x)

    loss = [loss1(var_, target_) if target_ < var_ else loss2(var_, target_) \
                                    for var_, target_ in zip(var, target)]
    return np.array(loss).mean()
