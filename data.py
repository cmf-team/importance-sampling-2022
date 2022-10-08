import pandas as pd
import numpy as np
from investiny import historical_data, search_assets
from datetime import datetime, timedelta

def stocks_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    allowedStocks = ['AAPL','AMD','TSLA','AMZN','NVDA','INTC','MU','MSFT','META','GOOGL']
    return get_portfolio(assets=assets, weights=weights, from_date=from_date, to_date=to_date, 
                         allowed_assets=allowedStocks, remove_weekends=True, 
                         type='Stock', exchange='NASDAQ'
                        )['return']

def commodities_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    allowedCommodities = ['Brent Oil Futures','Crude Oil WTI Futures','Natural Gas Futures','Heating Oil Futures', \
                          'Gold Futures','Silver Futures','Copper Futures','Platinum Futures','US Coffee C Futures','US Corn Futures'
                         ]
    return get_portfolio(assets=assets, weights=weights, from_date=from_date, to_date=to_date, 
                         allowed_assets=allowedCommodities, remove_weekends=True,
                         type='Comodity'
                        )['return']

def cryptocurrencies_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    allowedCryptocurrencies = ['BTC','ETH','USDT','USDC','BNB','XRP','BUSD','ADA','SOL','DOGE']
    return get_portfolio(assets=assets, weights=weights, from_date=from_date, to_date=to_date, 
                         allowed_assets=allowedCryptocurrencies, remove_weekends=True,
                         type='FX' 
                        )['return']



def get_portfolio(assets: list[str], weights: list[float], from_date: str, to_date: str, 
                  allowed_assets: list[str], remove_weekends=True,
                  **kwargs
                 ) -> pd.DataFrame:
    """
    Get prices of portfolio which contains assets from Investing.com.
    Args:
        assets (list[str]): a list of symbols of assets.
        weights (list[str]): a list of float numbers. Sum of weights should equal to one. 
        from_date (str): initial date to retrieve historical data (formatted as m/d/Y).
        to_date (str): final date to retrieve historical data (formatted as m/d/Y).
        allowed_assets (list[str]): a list of allowed assets.
        remove_weekends (bool): should we remove information about prices on weekends from output dataframe.
    Optional:
        type (str): type of assets.
        exchange (str): exchange to search information about assets.
    Returns:
        Dataframe: a dataframe wich contains prices of portfolio.
    """
    sDate = datetime.strptime(from_date, '%m/%d/%Y') - timedelta(days=1)
    eDate = datetime.strptime(to_date, '%m/%d/%Y') + timedelta(days=1)
    
    check_dates(sDate, eDate)
    check_assets(assets, allowed_assets)
    check_weights(assets, weights)

    dfs = [get_asset_data(asset, sDate, eDate, **kwargs) for asset in assets]

    portfolio = sum([df*w for df, w in zip(dfs,weights)])
    portfolio['return'] = (portfolio['close'] - portfolio['close'].shift(1))/portfolio['close'].shift(1)
    portfolio = portfolio[(portfolio.index > sDate)]
    if remove_weekends:
        portfolio = portfolio[portfolio.index.dayofweek < 5]
    return portfolio
        

def get_asset_data(asset: str, sDate: datetime, eDate: datetime, **kwargs) -> pd.DataFrame:
    """
    Get prices of an asset from Investing.com.
    Args:
        asset (str): a symbol of asset.
        sDate (datetime): initial date to retrieve historical data of an asset.
        eDate (datetime): final date to retrieve historical data of an asset.
    Optional:
        type (str): type of assets.
        exchange (str): exchange to search information about assets.
    Returns:
        Dataframe: Aadataframe wich contains information about prices of an asset.
    """
    search_results = search_assets(query=asset, limit=1, **kwargs)
    if not len(search_results):
        RuntimeError('Didn\'t find information about ' + asset + ' asset')
    dt = historical_data(investing_id=int(search_results[0]['ticker']),
                         from_date=datetime.strftime(sDate, '%m/%d/%Y'), to_date=datetime.strftime(eDate, '%m/%d/%Y')
                        )
    dt = pd.DataFrame.from_dict(dt).set_index('date')
    dt.index = pd.to_datetime(dt.index)
    return dt


def check_weights(assets: list[str], weights: list[float]) -> None:
    """
    Check if weights are valid.
    Args:
        assets (list[str]): a list of symbols of assets.
        weights (list[str]): a List of float numbers. Sum of weights should equal to one .
    Returns:
        None.
    """
    if len(assets) != len(weights):
        raise ValueError('Number of weights should be equal to number of assets')
    if sum(weights) != 1:
        raise ValueError('Sum of weights should be equal to 1') 

def check_dates(sDate: datetime, eDate: datetime) -> None:
    """
    Check if input dates are valid.
    Args:
        sDate (datetime): start date.
        eDate (datetime): end date.
    Returns:
        None.
    """
    if sDate >= eDate:
        raise ValueError('from_date is equal or bigger than to_date')
    if sDate < datetime.strptime('01/02/2020', '%m/%d/%Y'):
        raise ValueError('from_date should be more than "01/02/2020"')
    if eDate > datetime.strptime('10/01/2022', '%m/%d/%Y'):
        raise ValueError('to_date should be less than "10/01/2022"')

def check_assets(assets: list[str], allowedAssets: list[str]) -> None:
    """
    Check if a list of assets is in a list of allowed ones.
    Args:
        assets (list[str]): a list of assets.
        allowed_assets (list[str]): a list of allowed assets.
    Returns:
        None.
    """
    lst = np.setdiff1d(assets, allowedAssets)
    if lst.size:
        raise ValueError(', '.join(lst) + (' is ' if lst.size == 1 else ' are ') + 'not allowed asset' + ('' if lst.size == 1 else 's'))
