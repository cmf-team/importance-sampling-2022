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
        prev_sigm = 0

        for feat_ in feat[1:]:
            current_sigm = self.lambd * prev_sigm + (1- self.lambd) * (feat_ ** 2)
            prev_sigm = current_sigm

        return norm.ppf(1 - self.alpha, scale=current_sigm ** .5)


class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        # get features corresponding to window size
        feat_current = feat[-self.window_size:]
        return np.quantile(feat_current, q=(1 - self.alpha))




class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
