import pandas as pd
import gdown
import zipfile
import os
from typing import List

# The data was obtained from investing.com using `investiny` on 2022-10-13 UTC+0.
GDRIVE_URL = 'https://drive.google.com/uc?id=1Z8zpuf6mKZcxiEAH9Q04vTdpKeurFQWe'
# name of the archive that will be downloaded
ARCHIVE_NAME = 'historical_data.zip'
# path to the local directory to extract the data into.
DATA_DIR = 'historical_data'


def download_data(keep_archive=False):
    """Downloads historical data from Google Drive.

    This function will download the archive with historical data and
    extract it to the directory 'historical_data', if this directory is not found.
    Otherwise, the function will do nothing.

    :param keep_archive: if `True`, the downloaded archive will not be deleted
        after extraction.
    """
    if not os.path.exists(DATA_DIR) and not os.path.exists(ARCHIVE_NAME):
        gdown.download(GDRIVE_URL, ARCHIVE_NAME)
        with zipfile.ZipFile(ARCHIVE_NAME, 'r') as zip_file:
            zip_file.extractall()
        if not keep_archive:
            os.remove(ARCHIVE_NAME)
    elif os.path.exists(DATA_DIR):
        print(f'Loading data from existing directory \'{DATA_DIR}\'')
    elif os.path.exists(ARCHIVE_NAME):
        print(f'Loading data from existing archive \'{ARCHIVE_NAME}\'')


def get_returns(asset_type: str, assets: List[str], weights: List[float],
                from_date: str, to_date: str) -> pd.Series:
    """Downloads daily historical data for specified assets and calculates returns.

    This function will download the archive with historical data and extract it to the
    directory 'historical_data', if this directory is not found. See `download_data()`.
    If the directory already exists, the data will not be downloaded.

    :param asset_type: one of 'stocks', 'commodities', 'crypto'.
    :param assets: list of assets. Possible asset names correspond to the names of
        csv files (without the extension) downloaded by this function. If you don't
        know the possible asset names, you can first download historical data using
        the function `download_data()`.
    :param weights: list of weights for corresponding asset
    :param from_date: beginning of the period in the format MM/DD/YYYY.
        Must be greater or equal to 01/02/2020.
    :param to_date: end of the period in the format MM/DD/YYYY.
        Must be less or equal to 10/01/2022.
    :return:
    """
    from_date = pd.to_datetime(from_date, format='%m/%d/%Y')
    to_date = pd.to_datetime(to_date, format='%m/%d/%Y')
    if from_date > to_date:
        raise ValueError('`from_date` cannot be greater than `to_date`')
    if from_date < pd.Timestamp('2020-01-02'):
        raise ValueError('`from_date` must be greater or equal to 01/02/2020')
    if to_date > pd.Timestamp('2022-10-01'):
        raise ValueError('`to_date` must be less or equal to 10/01/2022')

    if asset_type not in ['stocks', 'commodities', 'crypto']:
        raise ValueError("`asset_type` must be one of: 'stocks', 'commodities', 'crypto'")
    if len(assets) != len(weights):
        raise ValueError('Lists `assets` and `weights` must have equal lengths')

    download_data()

    portfolio_price = None
    df = pd.read_csv(os.path.join(DATA_DIR, asset_type + '.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    for i in range(len(assets)):
        asset_price = df[assets[i]] * weights[i]
        if i == 0:
            portfolio_price = asset_price.copy()
        else:
            portfolio_price += asset_price
    returns = portfolio_price / portfolio_price.shift() - 1
    returns = returns.rename('return')
    returns = returns.loc[from_date:to_date]
    return returns


def stocks_returns(assets, weights, from_date, to_date):
    """ Gets returns for stocks """
    return get_returns('stocks', assets, weights, from_date, to_date)


def commodities_returns(assets, weights, from_date, to_date):
    """ Gets returns for commodities """
    return get_returns('commodities', assets, weights, from_date, to_date)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    """ Gets returns for cryptocurrencies """
    return get_returns('crypto', assets, weights, from_date, to_date)


class Dataloader:
    def __init__(
            self,
            series: pd.Series,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int
    ):
        self.series = series
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        assert self.first_pred > self.window_size
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.series.shape[0], self.step_size):
            feat_idx.append(range(i - self.horizon - self.window_size, i - self.horizon))
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
            feat = self.series.iloc[self.feat_idx[self.iter]]
            target = self.series.iloc[self.target_idx[self.iter]]
            self.iter += 1
            return feat, target
        else:
            raise StopIteration
