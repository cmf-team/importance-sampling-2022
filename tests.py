import numpy as np
import pandas as pd
from var_models.data import (
    stocks_data, 
    commodities_data, 
    cryptocurrencies_data,
    Dataloader,
    get_returns,
    get_logreturns,
)
from var_models.metrics import pof_test, if_test, quantile_loss
from var_models.univariate_models import HistoricalSimulation, RiskMetrics
from var_models.multivariate_models import VarianceCovariance


class TestData:
    def setup_class(self):
        self.stocks = stocks_data()
        self.commodities = commodities_data()
        self.cryptocurrencies = cryptocurrencies_data()

    def test_stocks_returns(self):
        assets = ['AAPL']
        weights = [1.]
        returns = get_returns(self.stocks, assets, from_date='09/02/2022', to_date='09/07/2022')
        returns = np.dot(returns, weights)
        test_returns = pd.Series(
            data=[-0.0136, -0.0082, 0.0093], 
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)
    
        assets = ['AAPL', 'GOOGL']
        weights = [0.3, 0.7]
        returns = get_returns(self.stocks, assets, from_date='09/02/2022', to_date='09/07/2022')
        returns = np.dot(returns, weights)
        test_returns = pd.Series(
            data=[-0.0161, -0.0092, 0.0201], 
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

        assets = ['AAPL', 'AMD', 'AMZN', 'GOOGL', 'INTC', 'META', 'MSFT', 'MU', 'NVDA', 'TSLA']
        weights = np.ones(10) / 10
        returns = get_returns(self.stocks, assets, from_date='09/02/2022', to_date='09/07/2022')
        returns = np.dot(returns, weights)
        test_returns = pd.Series(
            data=[-0.0186, -0.0115,  0.0160],
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

    def test_commodities_returns(self):
        assets = [
            'Brent Oil', 'Crude Oil WTI', 'Natural Gas',
            'Heating Oil', 'Gold', 'Silver', 'Copper', 
            'US Coffee C', 'US Corn'
        ]
        weights = np.ones(9) / 9
        returns = get_returns(self.commodities, assets, from_date='09/02/2022', to_date='09/07/2022')
        returns = np.dot(returns, weights)
        test_returns = pd.Series(
            data=[-0.0015, -0.0049 , -0.0177],
            index=pd.to_datetime(['2022-09-02', '2022-09-06', '2022-09-07']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

    def test_cryptocurrencies_returns(self):
        assets = ['ADA', 'BNB', 'BTC', 'BUSD', 'DOGE', 'ETH', 'USDC', 'USDT', 'XRP']
        weights = np.ones(9) / 9
        returns = get_returns(self.cryptocurrencies, assets, from_date='09/02/2022', to_date='09/07/2022')
        returns = np.dot(returns, weights)
        test_returns = pd.Series(
            data=[-0.0046, 0.0057, 0.0096, -0.0004, -0.0332, 0.0275],
            index=pd.to_datetime(['2022-09-02', '2022-09-03', '2022-09-04', '2022-09-05', '2022-09-06', '2022-09-07']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)


class TestMetrics:
    def test_quantile_loss(self):
        np.random.seed(0)
        target = np.random.randn(10)
        var = np.ones(10)
        assert np.isclose(quantile_loss(var, target, alpha=0.9), 1.0461, atol=0.0001)
        assert np.isclose(quantile_loss(var, target, alpha=0.1), 0.6269, atol=0.0001)

    def test_pof_test(self):
        np.random.seed(0)
        target = np.random.randn(10)
        var = -np.ones(10) * 2
        assert np.isclose(pof_test(var, target, alpha=0.95), 0.3111, atol=0.0001)

    def test_if_test(self):
        np.random.seed(0)
        target = np.random.randn(1000)
        var = -np.ones(1000) * 2
        assert np.isclose(if_test(var, target), 0.2770, atol=0.0001)


class TestUnivariateModels:
    def setup_class(self):
        assets = ['AAPL', 'GOOGL']
        weights = [0.3, 0.7]        
        logreturns = get_logreturns(stocks_data(), assets, from_date='09/02/2020', to_date='09/02/2022')
        self.loader = Dataloader(
            returns=logreturns,
            window_size=125, # a half of trading year
            step_size=1,
            horizon=1,
            first_pred=125+1,
            weights=weights,
        )

    def test_historical_simulation(self):
        alpha = 0.95
        hs = HistoricalSimulation(alpha, window_size=125)
        var = []
        target = []
        for feat, _target in self.loader:
            var.append(hs.forecast(feat))
            target.append(_target)
        var = np.array(var)
        target = np.array(target)
        assert np.isclose(quantile_loss(var, target, alpha), 0.0038, atol=0.0001)
        assert if_test(var, target) > 0.05
    
    def test_riskmetrics(self):
        alpha = 0.95
        rm = RiskMetrics(alpha)
        var = []
        target = []
        for feat, _target in self.loader:
            var.append(rm.forecast(feat))
            target.append(_target)
        var = np.array(var)
        target = np.array(target)
        assert np.isclose(quantile_loss(var, target, alpha), 0.0036, atol=0.0001)
        assert pof_test(var, target, alpha) > 0.05


class TestMultivariateModels:
    def setup_class(self):
        assets = ['AAPL', 'GOOGL']
        self.weights = np.array([0.3, 0.7])
        logreturns = get_logreturns(stocks_data(), assets, from_date='09/02/2020', to_date='09/02/2022')
        self.loader = Dataloader(
            returns=logreturns,
            window_size=125, # a half of trading year
            step_size=1,
            horizon=1,
            first_pred=125+1,
        )
    
    def test_variance_covariance(self):
        alpha = 0.8
        vc = VarianceCovariance(alpha, self.weights)
        var = []
        target = []
        for feat, _target in self.loader:
            var.append(vc.forecast(feat))
            target.append(_target @ self.weights)
        var = np.array(var)
        target = np.array(target)
        assert np.isclose(quantile_loss(var, target, alpha), 0.0101, atol=0.0001)
        assert pof_test(var, target, alpha) > 0.05