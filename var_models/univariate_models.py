from abc import ABC, abstractmethod
import numpy as np
from arch import arch_model
from scipy.stats import norm
import pandas as pd


class UnivariateVaR(ABC):
    @abstractmethod
    def __init__(self, alpha):
        self.alpha = alpha
        super().__init__()
    
    @abstractmethod
    def forecast(self, returns: pd.Series):
        """
        Forecasts VaR by given returns of a portfolio.

        Parameters
        ----------
        returns
            Series with returns of a portfolio where an index is dates.
        
        Returns
        ----------
        float
            Calculated VaR.
        """
        assert len(returns.shape) == 1
        pass


class RiskMetrics(UnivariateVaR):    
    def __init__(self, alpha: float):
        """
        The RiskMetrics method is used to calculate VaR based on returns 
        of a portfolio.
        
        Longerstaey, Jacques, and Martin Spencer. "Riskmetricstm—technical
        document." Morgan Guaranty Trust Company of New York: New York 51
        (1996): 54.
        
        Parameters
        ----------
        alpha
            VaR confidence level
        """
        super().__init__(alpha)
        self.lambd = 0.94
        self.window_size = 74

    def forecast(self, returns : pd.Series):
        super().forecast(returns)
        sigma2 = 0
        for r in returns[-self.window_size:]:
            sigma2 = self.lambd * sigma2 + (1 - self.lambd) * r**2
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)


class HistoricalSimulation(UnivariateVaR):
    def __init__(self, alpha : float, window_size : int):
        """
        The historical simulation method is used to calculate VaR based on the 
        emperical quantile of returns of a portfolio.
        
        Parameters
        ----------
        alpha
            VaR confidence level
        window_size
            A size of a window to calculate the empirical quantile.
        """
        super().__init__(alpha)
        self.window_size = window_size

    def forecast(self, returns : pd.Series):
        super().forecast(returns)
        return np.quantile(returns[-self.window_size:], q=1-self.alpha)


class GARCH11(UnivariateVaR):
    def __init__(self, alpha : float, window_size : int):
        """
        The GARCH(1, 1) model is used to calculate VaR based on 
        returns of a portfolio.
        
        Parameters
        ----------
        alpha
            VaR confidence level
        window_size
            A size of a window to fit the GARCH(1, 1) model.
        """
        super().__init__(alpha)
        self.window_size = window_size

    def forecast(self, returns : pd.Series):
        super().forecast(returns)
        model = arch_model(returns[-self.window_size:], p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2**0.5)
