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
        sigma2 = [0] * len(feat)
        for i in range(len(feat)):
            if i !=0:
                sigma2[i] = sigma2[i-1] * self.lambd + (1 - self.lambd)*(pow(feat[i-1], 2))
        sigma = sigma2[-1]
        ret = norm.ppf(1 - self.alpha, scale=pow(sigma, 0.5))
        return ret

class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        ret = np.quantile(feat[-self.window_size:], q = 1-self.alpha)
        return ret
    
class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        ret = norm.ppf(1 - self.alpha, scale=sigma2**0.5)
        return ret
