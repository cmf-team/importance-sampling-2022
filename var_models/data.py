import pandas as pd
import numpy as np
import gdown
import os

class Dataloader:
    def __init__(
            self,
            returns: pd.DataFrame,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int,
            weights: np.ndarray = None,
    ):
        """
        Dataloader is used for iterating over a sequence of returns using a
        sliding window to predict a future VaR.

        Parameters:
            returns:
                Dataframe of returns where an index is dates and columns are assets.
            window_size:
                Size of a sliding window to generate historical values.
            step_size:
                Size of a step to slide over the sequense of returns.
            horizon:
                Forecast horizon for VaR values.
            first_pred:
                Number of a first predicted VaR, should be greater than a window size.
            weights:
                Array of weights of assets in a portfolio, should be summed up to 1.
                If weights are provided, the dataloader iterates on the portfolio returns, 
                otherwise on each asset.
        """
        self.returns = returns
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        self.weights = weights
        assert self.first_pred > self.window_size
        if weights is not None:
            self.weights = np.array(weights)
            assert self.weights.sum() == 1
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.returns.shape[0], self.step_size):
            feat_idx.append(range(i-self.horizon-self.window_size+1, i-self.horizon+1))
            target_idx.append(i)
        self.feat_idx = feat_idx
        self.target_idx = target_idx

    def __len__(self):
        return len(self.feat_idx)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.feat_idx):
            feat = self.returns.iloc[self.feat_idx[self.iter]]
            target = self.returns.iloc[self.target_idx[self.iter]]
            if self.weights is not None:
                feat = feat @ self.weights
                target = target @ self.weights
            self.iter += 1
            return feat, target
        else:
            raise StopIteration


def get_returns(
        data: pd.DataFrame, 
        assets: list, 
        from_date: str, 
        to_date: str,
    ) -> pd.Series:
    """
    Calculates returns of given prices: $$r_{t} = {p_{t} - p_{t-1} \over p_{t-1}}.$$

    Parameters:
        data:
            Dataframe with prices where an index is dates and columns are assets.
        assets:
            List of assets' names to select in the dataframe.
        from_date:
            The start of a period in the format MM/DD/YYYY
        to_date:
            The end of a period in the format MM/DD/YYYY
    
    Returns:
        Returns of given prices in a given period.
    """
    portfolio = data[assets]
    from_mask = portfolio.index >= pd.to_datetime(from_date)
    to_mask = portfolio.index <= pd.to_datetime(to_date)
    return (portfolio / portfolio.shift() - 1)[from_mask & to_mask]


def get_logreturns(
        data: pd.DataFrame, 
        assets: list, 
        from_date: str, 
        to_date: str,
    ) -> pd.DataFrame:
    """
    Calculates log returns of given prices: $$r_{t} = \log p_{t} - \log p_{t-1}.$$

    Parameters:
        data:
            Dataframe with prices where an index is dates and columns are assets.
        assets:
            List of assets' names to select in the dataframe.
        from_date:
            The start of a period in the format MM/DD/YYYY
        to_date:
            The end of a period in the format MM/DD/YYYY
    
    Returns:
        Log returns of given prices in a given period.
    """
    returns = get_returns(data, assets, from_date, to_date)
    return np.log(1 + returns)


def stocks_data() -> pd.DataFrame:
    """
    Downloads an example of stock prices. Assets are: AAPL, AMD, AMZN, GOOGL,
    INTC, META, MSFT, MU, NVDA, TSLA. A period is (2019-12-31)-(2022-09-30).

    Returns:
        Stock prices.
    """
    url = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
    filename = 'stocks.csv'
    return _download_data(url, filename)


def commodities_data() -> pd.DataFrame:
    """
    Downloads an example of commodity prices. Assets are: Brent Oil, Crude Oil, 
    WTI, Gold, Copper, Heating Oil, US Coffee C, Natural Gas, Silver, US Corn. 
    A period is (2019-12-31)-(2022-09-30).

    Returns:
        Commodity prices.
    """
    url = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
    filename = 'commodities.csv'
    return _download_data(url, filename)


def cryptocurrencies_data() -> pd.DataFrame:
    """
    Downloads an example of cryptocurrency prices. Assets are: ADA, BNB, BTC, BUSD,
    DOGE, ETH, USDC, USDT, XRP. A period is (2020-01-01)-(2022-10-01).

    Returns:
        Cryptocurrency prices.
    """
    url = 'https://drive.google.com/file/d/1mPP5Vb57Jc2mYPeLYZPgAJM8ogjiguSO/view?usp=sharing'
    filename = 'cryptocurrencies.csv'
    return _download_data(url, filename)


def _download_data(url, filename):
    ref_path = 'data/'
    file_path = f'data/{filename}'
    if not os.path.exists(ref_path):
        os.makedirs(ref_path)
    if not os.path.exists(file_path):
        gdown.download(url, file_path, fuzzy=True)
    data = pd.read_csv(file_path, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data
