from arch import arch_model
from scipy.stats import norm
import numpy as np


class RiskMetrics:
    def __init__(self, alpha):
        self.alpha = alpha
        self.lambd = 0.94
        self.window_size = 74

    def forecast(self, feat):
        distribution = feat[-self.window_size:]
        sigma2 = 0
        for i in range(len(distribution)):
            sigma2 = self.lambd * sigma2 + (1 - self.lambd) * distribution[i] ** 2
        VaR = norm.ppf(1 - self.alpha, scale=np.sqrt(sigma2))
        return VaR


class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        distribution = feat[-self.window_size:]
        VaR = np.quantile(distribution, 1 - self.alpha)
        return VaR


class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        VaR = norm.ppf(1 - self.alpha, scale=np.sqrt(sigma2))
        return VaR
