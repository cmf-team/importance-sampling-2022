from arch import arch_model
from scipy.stats import norm
import math
import numpy as np



class RiskMetrics:
    '''
    Longerstaey, Jacques, and Martin Spencer. "Riskmetricstm—technical
    document." Morgan Guaranty Trust Company of New York: New York 51
    (1996): 54.
    '''
    def __init__(self, alpha):
        self.alpha = alpha
        self.lambd = 0.94
        self.window_size = 74

    def forecast(self, feat):
        returns = list(reversed(feat.tolist()))[:self.window_size]
        next_sigma = np.sum([(returns[i] ** 2) * self.lambd * (1 - self.lambd) ** i for i in range(self.window_size)])
        variance = np.sqrt(next_sigma)
        
        return norm.ppf(1 - self.alpha) * variance


class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        returns = list(reversed(feat.tolist()))[:self.window_size]
        return np.quantile(returns, 1 - self.alpha)
        # raise Exception(NotImplementedError)


class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)