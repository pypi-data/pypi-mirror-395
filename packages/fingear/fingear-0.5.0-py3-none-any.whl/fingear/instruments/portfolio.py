import pandas as pd
import numpy as np
from datetime import datetime

from ..load import load_asset_price


# weights = {'AAPL': 28, 'AXP': 16, 'BAC': 11, 'KO': 9, 'CVX': 6, 'OXY': 5}
class Portfolio:

    def _init_prices(self, weights):
        fraction = 'day'

        res = pd.DataFrame()
        for stock in weights.keys():
            price = load_asset_price(stock, self.begin, self.end, fraction, core=self.api)
            price['ticker'] = stock
            res = pd.concat([res, price])

        self.prices = res
        self.prices = self.prices.pivot(index='dttm', columns='ticker', values='price')

    def _init_rebalance_dates(self):
        prices = self.prices.reset_index().copy()

        rebalance_dates_reglament = pd.date_range(start=prices['dttm'].min()-pd.DateOffset(days=30),
                                    end=datetime.now(), freq=self.rebalace_period).to_numpy()

        rebalance_date_real = []
        for date in rebalance_dates_reglament:
            rebalance_date = prices.query('dttm>=@date')['dttm'].min()
            rebalance_date_real.append(rebalance_date)

        self.rebalance_dates = rebalance_date_real

    def _init_rebalance_weights(self, weights):
        rebalance_dates = self.rebalance_dates
        rebalance_weights = (self.prices.notna().astype(int).mul(weights, axis=1)
                              .reset_index().query('dttm in @rebalance_dates'))
        rebalance_weights.set_index('dttm', inplace=True)
        rebalance_weights = (rebalance_weights.T/rebalance_weights.sum(axis=1)).T
        self.rebalance_weights = rebalance_weights

    def _init_stock_amt(self):
        self.rebalance_process = []
        capital = self.capital
        date = self.rebalance_dates[0]
        stock_amt = capital*self.rebalance_weights.loc[date]/self.prices.loc[date]
        prev_prices = self.prices.loc[date]

        new_amt = pd.DataFrame(stock_amt).T
        new_amt['dttm'] = date
        res = new_amt

        for date in self.rebalance_dates[1:]:
            # Делаем шаг алгоритма - покупаем акции по цене в начале прошлой ребалансировки
            # И продаем в начале следующей.
            # Считаем, сколько у нас сейчас денег
            # На эти деньги покупаем новое количество акций по соотв новым ценам
            stock_amt = capital*self.rebalance_weights.loc[date]/prev_prices
            capital = (stock_amt*self.prices.loc[date]).sum()
            prev_prices = self.prices.loc[date]

            #print(date, capital)
            # Закидываем новое количество акций
            new_amt = pd.DataFrame(stock_amt).T
            new_amt['dttm'] = date
            res = pd.concat([res, new_amt])

        # Убираем ненужные колонки, и меняем название колонок
        res.columns.name = None
        res.set_index('dttm', inplace=True)

        # Протягиваем количество акции на дни, когда не было ребалансировки
        res = pd.merge(res.reset_index(),
                        self.prices.reset_index()['dttm'],
                        on='dttm', how='right')
        res.ffill(inplace=True)
        self.stock_amt = res.set_index('dttm')

    def _init_portfolio(self):
        portfolio = self.stock_amt * self.prices
        self.portfolio = portfolio.sum(axis=1)
        self.portfolio = self.portfolio.reset_index()
        self.portfolio.columns=['dttm', 'price']
        self.portfolio.set_index('dttm', inplace=True)


    def __init__(self, weights, initial_capital=10000, begin='1900-01-01',
                 end='2024-01-01', rebalance_period='QS', api='yahoo'):
        self.weights = weights
        self.capital = initial_capital
        self.rebalace_period = rebalance_period
        self.begin = begin
        self.end = end
        self.api = api

        self._init_prices(weights)
        self._init_rebalance_dates()
        self._init_rebalance_weights(weights)
        self._init_stock_amt()
        self._init_portfolio()


def annualized_return(price):
    start_price = price['price'].iloc[0]
    print (start_price)
    end_price = price['price'].iloc[-1]
    print (end_price)
    years = (price['dttm'].iloc[-1] - price['dttm'].iloc[0]).days / 365.25
    return (end_price / start_price) ** (1 / years) - 1

def standard_deviation(df):
    returns = df['price'].pct_change().dropna()
    return returns.std() * np.sqrt(252)  # Assuming daily prices

def best_year(df):
    yearly_returns = df.resample('Y', on='dttm').last()['price'].pct_change()
    return yearly_returns.max() * 100  # Convert to percentage

def calculate_worst_year(df):
    yearly_returns = df.resample('Y', on='dttm').last()['price'].pct_change()
    return yearly_returns.min() * 100  # Convert to percentage

# далее все в процессе-------------------------------------------------
def calculate_max_drawdown(df):
    cumulative_returns = df['price'] / df['price'].iloc[0]
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    return drawdown.min() * 100  # Convert to percentage

def calculate_sharpe_ratio(df, risk_free_rate=0.02):
    returns = df['price'].pct_change().dropna()
    excess_returns = returns - risk_free_rate / 252
    return (excess_returns.mean() / returns.std()) * np.sqrt(252)

def calculate_sortino_ratio(df, risk_free_rate=0.02):
    returns = df['price'].pct_change().dropna()
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252)
    excess_returns = returns.mean() - risk_free_rate / 252
    return excess_returns / downside_deviation if downside_deviation > 0 else np.nan

def calculate_correlation(df, benchmark_df):
    merged = df.merge(benchmark_df, on='date', suffixes=('', '_benchmark'))
    return merged['price'].pct_change().corr(merged['price_benchmark'].pct_change())
