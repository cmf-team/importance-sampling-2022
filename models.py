import numpy as np
from arch import arch_model
from scipy.stats import norm


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
        feat.reset_index(drop=True, inplace=True)
        sigmas_sq = np.zeros((len(feat)))
        for i in range(1, len(feat)):
            sigmas_sq[i] = self.lambd * sigmas_sq[i - 1] + (1 - self.lambd) * feat[i - 1] ** 2
        return norm.ppf(1 - self.alpha, scale=sigmas_sq[-1] ** 0.5)


class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        return np.percentile(feat[-self.window_size:], (1 - self.alpha) * 100)


class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
