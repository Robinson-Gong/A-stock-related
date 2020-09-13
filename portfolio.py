import random
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import Getdata

ds = '20190911'
de = '20200911'
path = 'F:\stock data'
market_value_list = []
df = pd.read_csv('F:\stock data\Stock\stock_basic.csv')
result = pd.DataFrame(columns=('Index', 'Stock1', 'Stock2', 'Stock3', 'Stock4', 'Stock5', 'Portfolio Return'))
for i in range(50):
    ticker_list = list(range(5))
    StockPrices = pd.DataFrame()
    for j in range(5):
        random.seed(a=None)
        temp = random.randint(0, df.shape[0] - 1)
        tscode = df.iloc[temp, 0]
        GD = Getdata.getdata(tscode=tscode, path=path, ds=ds, de=de)
        GD.getkdata()
        stock_data = GD.readdata('k')
        StockPrices[tscode] = stock_data['close']
        ticker_list[j] = tscode
    StockPrices = StockPrices.dropna(axis=0, how='any')
    StockReturns = StockPrices.pct_change().dropna()
    stock_return = StockReturns.copy()
    cov_mat = stock_return.cov()
    cov_mat_annual = cov_mat * 252
    number = 10000
    random_p = np.empty((number, 7))
    np.random.seed(7)
    for k in range(number):
        random5 = np.random.random(5)
        random_weight = random5 / np.sum(random5)
        mean_return = stock_return.mul(random_weight, axis=1)
        mean_return = mean_return.sum(axis=1)
        mean_return = mean_return.mean()
        annual_return = (1 + mean_return) ** 252 - 1
        random_volatility = np.sqrt(np.dot(random_weight.T, np.dot(cov_mat_annual, random_weight)))
        random_p[k][:5] = random_weight
        random_p[k][5] = annual_return
        random_p[k][6] = random_volatility
    RandomPortfolios = pd.DataFrame(random_p)
    RandomPortfolios.columns = [ticker + '_weight' for ticker in ticker_list] + ['Returns', 'Volatility']
    min_index = RandomPortfolios.Volatility.idxmin()
    GMV_weights = np.array(RandomPortfolios.iloc[min_index, 0:5])
    Portfolio_min_index_GMV = stock_return.mul(GMV_weights, axis=1).sum(axis=1).mean()*252
    risk_free = 1.4
    RandomPortfolios['Sharpe'] = (RandomPortfolios.Returns - risk_free) / RandomPortfolios.Volatility
    max_index = RandomPortfolios.Sharpe.idxmax()
    MSR_weights = np.array(RandomPortfolios.iloc[max_index, 0:5])
    Portfolio_max_index_MSR = stock_return.mul(MSR_weights, axis=1).sum(axis=1).mean()*252
    new = pd.DataFrame({'Index': 'Stock',
                        'Stock1': ticker_list[0],
                        'Stock2': ticker_list[1],
                        'Stock3': ticker_list[2],
                        'Stock4': ticker_list[3],
                        'Stock5': ticker_list[4],
                        'Portfolio Return': ' '}, index=[1])
    result = result.append(new, ignore_index=True)
    new = pd.DataFrame({'Index': 'MinRisk',
                        'Stock1': GMV_weights[0],
                        'Stock2': GMV_weights[1],
                        'Stock3': GMV_weights[2],
                        'Stock4': GMV_weights[3],
                        'Stock5': GMV_weights[4],
                        'Portfolio Return': Portfolio_min_index_GMV}, index=[1])
    result = result.append(new, ignore_index=True)
    new = pd.DataFrame({'Index': 'MaxSharp',
                        'Stock1': MSR_weights[0],
                        'Stock2': MSR_weights[1],
                        'Stock3': MSR_weights[2],
                        'Stock4': MSR_weights[3],
                        'Stock5': MSR_weights[4],
                        'Portfolio Return': Portfolio_max_index_MSR}, index=[1])
    result = result.append(new, ignore_index=True)
    new = pd.DataFrame({'Index': ' ',
                        'Stock1': ' ',
                        'Stock2': ' ',
                        'Stock3': ' ',
                        'Stock4': ' ',
                        'Stock5': ' ',
                        'Portfolio Return': ' '}, index=[1])
    result = result.append(new, ignore_index=True)
result.to_csv('F:\stock data\Portfolio_50.csv')