import pandas as pd
import numpy as np


def _get_returns(asset_type, assets, weights, from_date, to_date):
    """

    :param asset_type: one of 'stocks', 'commodities', 'crypto'
    :param assets:
    :param weights:
    :param from_date: beginning of the period in the format MM/DD/YYYY.
        Must be in range 01/02/2020 - 10/01/2022.
    :param to_date: end of the period in the format MM/DD/YYYY.
        Must be in range 01/02/2020 - 10/01/2022.
    :return:
    """
    if asset_type not in ['stocks', 'commodities', 'crypto']:
        raise ValueError('`asset_type` must be one of: stocks, commodities, crypto')
    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)



def stocks_returns(assets, weights, from_date, to_date):
    """ Gets returns for stocks """
    raise Exception(NotImplementedError)


def commodities_returns(assets, weights, from_date, to_date):
    """ Gets returns for commodities """
    raise Exception(NotImplementedError)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    """ Gets returns for cryptocurrencies """
    raise Exception(NotImplementedError)
