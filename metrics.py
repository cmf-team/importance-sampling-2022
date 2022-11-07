import numpy as np
from scipy.stats import chi2



def pof_test(var, target, alpha=0.99):
    result = target < var
    
    total = len(result)
    failed = np.sum(result)
    
    num = (alpha ** (total - failed)) * ((1 - alpha) ** failed)
    denum = ((1 - failed / total) ** (total - failed)) * ((failed / total) ** failed)
    s = -2 * np.log(num / denum)
    
    return 1 - chi2.cdf(s, df = 1)


def if_test(var, target):
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0
    
    result = target < var
    result = list(reversed(result))
    for i in range(len(result)-1):
        if result[i]:
            if result[i + 1]:
                n11 += 1
            else:
                n10 += 1
        else:
            if result[i + 1]:
                n01 += 1
            else:
                n00 += 1
    pi0 = n01 / (n01 + n00)
    pi1 = n11 / (n11 + n10)
    pi = np.sum(result) / len(result)
    
    num = ((1 - pi) ** (n00 + n10))*((pi)**(n01 + n11))
    denum = ((1 - pi0) ** n00) * (pi0 ** n01) * ((1 - pi1) ** n10) * (pi1 ** n11)
    s = - 2 * np.log(num / denum)
    
    return 1 - chi2.cdf(s, df = 1)


def quantile_loss(var, target, alpha=0.99):
#     return 2 * alpha * (var - target) if var > target else 2 * (1 - alpha) * (target - var)
#     ar =[2 * alpha * (v - t) if v > t else 2 * (1 - alpha) * (t - v) for t, v, alpha in zip(target, var, np.ones(10)*alpha )]
#     return np.mean(ar)

    iqloss = []
    return_array = [(t - v) for (t, v) in zip(target, var)]
    for i in return_array:
        iqloss.append(2 * (1 - alpha) * i if i>=0 else -2 * alpha * i)
#         if i >= 0:
#             stats.append(2 * (1 - alpha) * i)
#         else:
#             stat.append(-2 * alpha * i)
    
    return np.average(iqloss)

#     raise Exception(NotImplementedError)