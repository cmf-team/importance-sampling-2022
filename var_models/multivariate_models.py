from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm
import pandas as pd

class MultivariateVaR(ABC):
    @abstractmethod
    def __init__(self, alpha, weights):
        self.alpha = alpha
        self.weights = weights
        assert self.weights.sum() == 1
        super().__init__()
    
    @abstractmethod
    def forecast(
            self, 
            returns: pd.DataFrame,
        ):
        """
        Forecasts VaR by given returns of assets.

        Parameters
        ----------
        returns
            A dataframe with returns where an index is dates and columns are assets.
        
        Returns
        ----------
        float
            Calculated VaR.
        """
        assert len(returns.shape) == 2 and returns.shape[1] > 1
        assert self.weights.shape[0] == returns.shape[1]
        pass


class VarianceCovariance(MultivariateVaR):
    def __init__(
            self, 
            alpha : float, 
            weights: np.ndarray,
        ):
        """
        The variance-covariance method is used to calculate VaR based on returns 
        of each asset in a portfolio.

        Parameters
        ----------
        alpha
            VaR confidence level
        weights
            An array of weights of assets in a portfolio, should be summed up to 1.
            If not provided, the dataloader iterates over all assets' returns.
        """
        super().__init__(alpha, weights)

    def forecast(self, returns: pd.DataFrame):
        super().forecast(returns)
        cov_matrix = returns.cov()
        loc = returns.mean() @ self.weights
        scale = np.sqrt(self.weights.T @ cov_matrix @ self.weights)
        return norm.ppf(1-self.alpha, loc=loc, scale=scale)
