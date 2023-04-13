from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm


class MultivariateVaR(ABC):
    @abstractmethod
    def __init__(self, alpha, weights):
        self.alpha = alpha
        self.weights = weights
        assert self.weights.sum() == 1
        super().__init__()
    
    @abstractmethod
    def forecast(self, returns):
        assert len(returns.shape) == 2 and returns.shape[1] > 1
        assert self.weights.shape[0] == returns.shape[1]
        pass


class VarianceCovariance(MultivariateVaR):
    def __init__(self, alpha, weights):
        super().__init__(alpha, weights)

    def forecast(self, returns):
        super().forecast(returns)
        cov_matrix = returns.cov()
        loc = returns.mean() @ self.weights
        scale = np.sqrt(self.weights.T @ cov_matrix @ self.weights)
        return norm.ppf(1-self.alpha, loc=loc, scale=scale)
