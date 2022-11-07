from arch import arch_model
from scipy.stats import norm
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
        """
        Calculation of VaR based on \sigma_i^2 = \lambda * \sigma_{i-1}^2 + (1 - \alpha) * r_{t-1}^2

        \sigma_0^2=0

        """

        sigma2 = np.zeros(len(feat))

        for i in range(1, len(feat)):
            sigma2[i] = self.lambd * sigma2[i-1] + (1 - self.lambd) * feat[i - 1] * feat[i - 1]

        sigma2 = sigma2[-1]

        return norm.ppf(1 - self.alpha, scale = sigma2**0.5)

class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        """
        Calculation of VaR based on counting quantile
        """
        return np.quantile(feat[-self.window_size:], q = 1 - self.alpha)


class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
