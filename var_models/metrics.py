import pandas as pd
import numpy as np
from scipy.stats import chi2


def pof_test(
        var: np.ndarray, 
        target: np.ndarray, 
        alpha: int = 0.99,
    ):
    """
    Kupiec’s Proportion of Failure Test (POF). Tests that a number of exceptions 
    corresponds to the VaR confidence level.
    
    Parameters
    ----------
    var
        Predicted VaRs.
    target
        Corresponded returns.
    alpha
        VaR confidence level. Default is 0.99.
    
    Returns
    ----------
    float
        p-value of POF test.
    """
    exception = target < var
    t = len(target)
    m = exception.sum()
    nom = (1 - alpha)**m * alpha**(t-m)
    den = (1 - m/t)**(t - m) * (m / t)**m
    lr_pof = -2 * np.log(nom / den)
    pvalue = 1 - chi2.cdf(lr_pof, df=1)
    return pvalue


def if_test(
        var: np.ndarray, 
        target: np.ndarray, 
    ):
    """
    Christofferson Interval Forecast Test (IF). Tests that the probability of 
    a new exception does not depend on a previous one.

    Parameters
    ----------
    var
        Predicted VaRs.
    target
        Corresponded returns.
    
    Returns
    ----------
    float
        p-value of IF test.
    """
    exception = target < var
    pairs = [(exception[i], exception[i+1]) for i in range(len(exception) - 1)]
    pairs = np.array(pairs).astype('int')
    n00 = ((pairs[:, 0] == 0) & (pairs[:, 1] == 0)).sum()
    n01 = ((pairs[:, 0] == 0) & (pairs[:, 1] == 1)).sum()
    n10 = ((pairs[:, 0] == 1) & (pairs[:, 1] == 0)).sum()
    n11 = ((pairs[:, 0] == 1) & (pairs[:, 1] == 1)).sum()
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    pi0 = n01 / (n00 + n01)
    pi1 = n11 / (n10 + n11)
    nom = (1 - pi)**(n00 + n10) * pi**(n01 + n11)
    den = (1 - pi0)**n00 * pi0**n01 * (1 - pi1)**n10 * pi1**n11
    lr_if = -2 * np.log(nom / den)
    pvalue = 1 - chi2.cdf(lr_if, df=1)
    return pvalue


def quantile_loss(var, target, alpha=0.99):
    """
    Quantile loss also known as Pinball loss. Measures the discrepancy between 
    true values and a corresponded 1-alpha quantile.
    
    Parameters
    ----------
    var
        Predicted VaRs.
    target
        Corresponded returns.
    alpha
        VaR confidence level. Default is 0.99.
    
    Returns
    ----------
    float
        The value of the quantile loss function.
    """
    qloss = np.abs(var-target)
    qloss[target < var] = qloss[target < var] * 2 * alpha
    qloss[target >= var] = qloss[target >= var] * 2 * (1 - alpha)
    return qloss.mean()
