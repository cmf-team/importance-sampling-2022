import numpy as np
import pandas as pd
from data import stocks_returns, commodities_returns, cryptocurrencies_returns

def test_stocks_returns():
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

def test_commodities_returns():

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

def test_cryptocurrencies_returns():

    assets = ['ADA', 'BNB', 'BTC', 'BUSD', 'DOGE', 'ETH', 'USDC', 'USDT', 'XRP']
    weights = np.ones(9)
    returns = cryptocurrencies_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series(
        data=[-0.0076, -0.0072,  0.0081, -0.0063, -0.0481,  0.026 ],
        index=pd.to_datetime(['2022-09-02', '2022-09-03', '2022-09-04', '2022-09-05', '2022-09-06', '2022-09-07']),
    )
    assert np.allclose(returns, test_returns, atol=0.0001)
