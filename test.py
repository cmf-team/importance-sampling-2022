import numpy as np
import pandas as pd
from data import stocks_returns

def test_stocks_returns():
    assets = ['APPL']
    weights = [1.]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series( 
        index=pd.to_datetime(['09/02/2022', '09/06/2022']),
	data=[0, -0.0082],
    )
    assert np.allclose(returns, test_returns, atol=0.0001)
    
    assets = ['APPL', 'GOOGL']
    weights = [0.3, 0.7]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series( 
        index=pd.to_datetime(['09/02/2022', '09/06/2022']),
	data=[0, -0.0068],
    )
    assert np.allclose(returns, test_returns, atol=0.0001)