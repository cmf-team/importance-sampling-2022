import numpy as np
import scipy.stats as ss


# see https://la.mathworks.com/help/risk/overview-of-var-backtesting.html
# and https://www.value-at-risk.net/backtesting-coverage-tests/
# for tests descriptions


def pof_test(var, target, alpha=0.99):
    # note that I reversed the definitions of x here (c.f. mathworks site)
    # alpha = VaR level
    # x - number of times target < var
    # x/N should be equal to 1-alpha
    # so observe x failures ~= 1-alpha times

    N = var.shape[0]  # num of observations
    x = np.sum(target < var)  # num of failures
    lr_pof = -2 * np.log(((alpha ** (N - x)) * ((1 - alpha) ** x)) / (((1 - x / N) ** (N - x)) * (x / N) ** x))
    pvalue = 1 - ss.chi2.cdf(lr_pof, df=1)
    return pvalue


def if_test(var, target):
    x = (target < var).astype(int)  # num of failures, consistent with mathworks
    # TODO: optimize using vectorization
    n00 = 0
    n10 = 0
    n01 = 0
    n11 = 0
    for i in range(1, len(x)):
        if x[i] == 0 and x[i - 1] == 0:
            n00 += 1
        if x[i] == 1 and x[i - 1] == 0:
            n01 += 1
        if x[i] == 1 and x[i - 1] == 0:
            n10 += 1
        if x[i] == 1 and x[i - 1] == 1:
            n11 += 1

    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)

    lr_cci = -2 * np.log(
        ((1 - pi) ** (n00 + n10) * pi ** (n01 + n11))
        / ((1 - pi0) ** (n00) * pi0 ** (n01) * (1 - pi1) ** n10 * pi1**n11)
    )
    # "probability of right tail should be small to reject the null hypothesis"
    pvalue = 1 - ss.chi2.cdf(lr_cci, df=1)
    # print(f"{lr_cci=} {pvalue=}")
    return pvalue


def quantile_loss(var, target, alpha=0.99):
    x = 2 * alpha * (var - target)
    y = 2 * (1 - alpha) * (target - var)
    loss = np.where(target < var, x, y)
    return loss.mean()
