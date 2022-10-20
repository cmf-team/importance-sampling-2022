import numpy as np
import pandas as pd
from data import stocks_returns

def test_stocks_returns():
    assets = ['APPL']
    weights = [1.]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series(
        data=[-0.0136, -0.0082, 0.0093], 
        index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
    )
    assert np.allclose(returns, test_returns, atol=0.0001)
    
    assets = ['APPL', 'GOOGL']
    weights = [0.3, 0.7]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series(
        data=[-0.0158, -0.0091, 0.0188], 
        index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
    )
    assert np.allclose(returns, test_returns, atol=0.0001)