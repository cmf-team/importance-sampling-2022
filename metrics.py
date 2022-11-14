from scipy.stats import chi2
import numpy as np

def pof_test(var, target, alpha):
    '''Kupiec’s Proportion of Failures Test
       This statistic is asymptotically distributed as a chi-square variable with 1 degree of freedom'''
    result = target < var
    
    total_observations = len(result)
    fail_observations = np.sum(result)
    
    numerator = ((alpha)**(total_observations - fail_observations))*((1-alpha)**fail_observations)
    denominator = ((1 - fail_observations/total_observations)**(total_observations - fail_observations))*((fail_observations/total_observations)**fail_observations)
    stat = -2 * np.log(numerator/denominator)
    
    return 1 - chi2.cdf(stat, df = 1)


def if_test(var, target):
    '''Christoffersen’s Interval Forecast Test
       This statistic is asymptotically distributed as a chi-square with 1 degree of freedom'''
    n_00 = 0
    n_01 = 0
    n_10 = 0
    n_11 = 0
    
    result = target < var
    result = list(reversed(result))
    for iter_ in range(len(result)-1):
        if result[iter_]:
            if result[iter_ + 1]:
                n_11 += 1
            else:
                n_10 += 1
        else:
            if result[iter_ + 1]:
                n_01 += 1
            else:
                n_00 += 1
    pi_0 = n_01/(n_01 + n_00)
    pi_1 = n_11/(n_11 + n_10)
    pi = np.sum(result)/len(result)
    
    numerator = ((1-pi)**(n_00 + n_10))*((pi)**(n_01+n_11))
    denominator = ((1 - pi_0)**n_00)*(pi_0**n_01)*((1-pi_1)**n_10)*(pi_1**n_11)
    stat = -2 * np.log(numerator/denominator)
    
    return 1 - chi2.cdf(stat, df = 1)


def quantile_loss(var, target, alpha):
    stat = []
    result = [(m - n) for (m,n) in zip(target, var)]
    for i in result:
        if i >= 0:
            stat.append(2 * (1 - alpha) * i)
        else:
            stat.append(-2 * alpha * i)
    
    return np.average(stat)

