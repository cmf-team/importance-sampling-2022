from abc import ABC, abstractmethod
import numpy as np
from arch import arch_model
from scipy.stats import norm


class UnivariateVaR(ABC):
    @abstractmethod
    def __init__(self, alpha):
        self.alpha = alpha
        super().__init__()
    
    @abstractmethod
    def forecast(self, returns):
        assert len(returns.shape) == 1
        pass


class RiskMetrics(UnivariateVaR):
    '''
    Longerstaey, Jacques, and Martin Spencer. "Riskmetricstm—technical
    document." Morgan Guaranty Trust Company of New York: New York 51
    (1996): 54.
    '''
    def __init__(self, alpha):
        super().__init__(alpha)
        self.lambd = 0.94
        self.window_size = 74

    def forecast(self, returns):
        super().forecast(returns)
        sigma2 = 0
        for r in returns[-self.window_size:]:
            sigma2 = self.lambd * sigma2 + (1 - self.lambd) * r**2
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)


class HistoricalSimulation(UnivariateVaR):
    def __init__(self, alpha, window_size):
        super().__init__(alpha)
        self.window_size = window_size

    def forecast(self, returns):
        super().forecast(returns)
        return np.quantile(returns[-self.window_size:], q=1-self.alpha)


class GARCH11(UnivariateVaR):
    def __init__(self, alpha, window_size):
        super().__init__(alpha)
        self.window_size = window_size

    def forecast(self, returns):
        super().forecast(returns)
        model = arch_model(returns[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
