import numpy as np

from arch import arch_model
from scipy.stats import norm


class RiskMetrics:
    """
    Longerstaey, Jacques, and Martin Spencer. "Riskmetricstm—technical
    document." Morgan Guaranty Trust Company of New York: New York 51
    (1996): 54.
    """

    def __init__(self, alpha):
        self.alpha = alpha
        self.lambd = 0.94
        self.window_size = 74

        self.squared_sigma = 0

        # flag of first execution
        self.flag = 1

    def forecast(self, feat):
        if self.flag:
            feat = feat.reset_index()
            feat.columns = ["date", "return"]
            feat["squared_sigma"] = (feat["return"] ** 2) * (1 - self.lambd)
            feat["squared_sigma"] = feat["squared_sigma"].shift()
            feat["squared_sigma"] = feat["squared_sigma"].fillna(self.squared_sigma)

            for idx in range(1, len(feat)):
                feat["squared_sigma"].iloc[idx] += self.lambd * (
                    feat["squared_sigma"].iloc[idx - 1]
                )

            self.squared_sigma = feat["squared_sigma"].iloc[-1]
            self.flag = 0
        else:
            self.squared_sigma = self.lambd * self.squared_sigma + (1 - self.lambd) * (
                feat[-1] ** 2
            )

        return norm.ppf(1 - self.alpha, scale=self.squared_sigma ** 0.5)


class HistoricalSimulation:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        if self.window_size < len(feat):
            return np.quantile(feat[: -self.window_size], 1 - self.alpha)
        else:
            return np.quantile(feat, 1 - self.alpha)


class GARCH11:
    def __init__(self, alpha, window_size):
        self.alpha = alpha
        self.window_size = window_size

    def forecast(self, feat):
        model = arch_model(feat[-self.window_size :], p=1, q=1, rescale=False)
        res = model.fit(disp="off")
        sigma2 = res.forecast(horizon=1, reindex=False).variance.values[0, 0]
        return norm.ppf(1 - self.alpha, scale=sigma2 ** 0.5)
