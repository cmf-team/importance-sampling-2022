import numpy as np
import pandas as pd
from data import (
    stocks_returns, 
    commodities_returns, 
    cryptocurrencies_returns, 
    Dataloader
)
from metrics import pof_test, if_test, quantile_loss
from models import HistoricalSimulation, RiskMetrics

class TestData:
    def test_stocks_returns(self):
        assets = ['AAPL']
        weights = [1.]
        returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
        test_returns = pd.Series(
            data=[-0.0136, -0.0082, 0.0093], 
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)
    
        assets = ['AAPL', 'GOOGL']
        weights = [0.3, 0.7]
        returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
        test_returns = pd.Series(
            data=[-0.0158, -0.0091, 0.0188], 
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

        assets = ['AAPL', 'AMD', 'AMZN', 'GOOGL', 'INTC', 'META', 'MSFT', 'MU', 'NVDA', 'TSLA']
        weights = np.ones(10)
        returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
        test_returns = pd.Series(
            data=[-0.0193, -0.0068,  0.0196],
            index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

    def test_commodities_returns(self):
        assets = [
            'Brent Oil', 'Crude Oil WTI', 'Natural Gas',
            'Heating Oil', 'Gold', 'Silver', 'Copper', 
            'US Coffee C', 'US Corn'
        ]
        weights = np.ones(9)
        returns = commodities_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
        test_returns = pd.Series(
            data=[ 0.0075,  0.001 , -0.0021],
            index=pd.to_datetime(['2022-09-02', '2022-09-06', '2022-09-07']),
        )
        assert np.allclose(returns, test_returns, atol=0.0001)

    def test_cryptocurrencies_returns(self):
        assets = ['ADA', 'BNB', 'BTC', 'BUSD', 'DOGE', 'ETH', 'USDC', 'USDT', 'XRP']
        weights = np.ones(9)
        returns = cryptocurrencies_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
        test_returns = pd.Series(
            data=[-0.0076, -0.0072,  0.0081, -0.0063, -0.0481,  0.026 ],
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


class TestModels:
    def setup_class(self):
        assets = ['AAPL', 'GOOGL']
        weights = [0.3, 0.7]
        returns = stocks_returns(assets, weights, from_date='09/02/2020', to_date='09/02/2022')
        logreturns = np.log(returns + 1)
        self.loader =  Dataloader(
            series=logreturns,
            window_size=125, # a half of trading year
            step_size=1,
            horizon=1,
            first_pred=125+1
        )
        #for i in self.loader:
        #    print(i, '\n')

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
        assert if_test(var, target) > 0.05
#a = TestModels()
#a.setup_class()
#a.test_riskmetrics()
#a.test_historical_simulation()
# quantile_loss(var, target, alpha)
#target - посчитали с окном в полгода доходности, получили временной ряд, у него взяли (1-alpha) квантиль 
# и сравнили с тем, который модели предсказала