import pandas as pd
import gdown
import numpy as np
from scipy.stats import norm

def multivariate_var(tickers, # list of tickers
                     weights, # list of weights
                     from_date,
                     to_date,
                     initial_investment, # value of initial investment (integer or float)
                     alpha, # alpha, where 1 - alpha = confidence level
                     n # number of days for n-days VaR calculation
):
    # converting weights to array
    weights = np.array(weights)
    # import returns data
    url = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
    gdown.download(url, 'stocks.csv', fuzzy=True)
    data = pd.read_csv('stocks.csv', index_col=0)[tickers]
    data.index = pd.to_datetime(data.index)
    from_mask = data.index >= pd.to_datetime(from_date)
    to_mask = data.index <= pd.to_datetime(to_date)
    data = data[from_mask & to_mask]
    returns = data.pct_change()

    # generate covariance matrix
    cov_matrix = returns.cov()

    # calculate mean and standard deviation
    port_mean = returns.mean().dot(weights)
    mean_investment = (1 + port_mean) * initial_investment
    port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
    stdev_investment = initial_investment * port_stdev

    # determine confidence level cutoff from the normal distribution
    cutoff = norm.ppf(alpha, mean_investment, stdev_investment)

    # calculate daily VaR
    VaR = initial_investment - cutoff

    # calculate n-days VaR
    VaR_n_days = np.round(VaR * np.sqrt(n), 2)

    return VaR_n_days
