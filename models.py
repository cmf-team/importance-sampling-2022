from arch import arch_model
from scipy.stats import norm
import numpy as np


class RiskMetrics:
    
    def __init__(self, alpha):
        self.alpha = alpha
        self.lambd = 0.94
        self.window_size = 74

    def forecast(self, feat):
        dev=0
        for r in feat[:-1]:
            dev=self.lambd*dev+(1-self.lambd)*r**2 
        return norm.ppf(1-self.alpha,scale=dev**0.5)

class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

        
        
    def forecast(self, feat):
        
        
        return np.quantile(feat[-self.window_size:],q=1-self.alpha)

class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
