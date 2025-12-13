from ...load import load_dividends, load_asset_price, load_exchange_rate
from ...instruments import stock_price_and_div_to_return
from .configs import _get_country_to_stocks
from .utils import keep_frequency, add_comission

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def _load_div_price(ticker, start, end, interval, core='yahoo', proxies=None):
    div = load_dividends(ticker, start, end, core=core, proxies=proxies)
    price = load_asset_price(ticker, start, end, interval, core=core, proxies=proxies)
    return div, price
    
def _prepare_stocks_russia(start, end, interval='day', proxies=None):
    data = pd.read_excel('fingear/datasets/Russia/stocks.xlsx')
    data = data[['TRADEDATE', 'CLOSE']]
    data.columns = ['dt', 'price']
    data['dt'] = pd.to_datetime(data['dt'])

    data = add_comission(data, 0.008, freq='day') # Средняя комиссия российских фондов

    rate = load_exchange_rate('RUB', start, end, 'day', core='yahoo', proxies=proxies)
    data = pd.merge(data, rate, how='inner', on='dt')
    data['stocks_price'] = data['price'] / data['rate']
    data = data[['dt', 'stocks_price']]
    return data
     

def prepare_stocks(country, start, end, interval='day', core='yahoo', proxies=None, include_real=False):
    # Данные на конец месяца - ОК
    if country == 'Russia':
        data = _prepare_stocks_russia(start, end, interval=interval, proxies=proxies)
    else:
        ticker = _get_country_to_stocks()[country]
        div, price = _load_div_price(ticker, start, end, interval,
                                    core=core, proxies=proxies)
        data = stock_price_and_div_to_return(div, price, include_real=include_real)
        data.rename(columns={'price': 'stocks_price', 'dttm': 'dt'}, inplace=True)

    # Заполняем выходные тоже данными
    data = pd.merge(pd.DataFrame({'dt': pd.date_range(start, end, freq='D')}), 
                    data, how='left', on='dt')
    data['stocks_cum'] = data['stocks_price'].infer_objects(copy=False).ffill()
    # Ставим нужную частоту
    data = keep_frequency(data, freq=interval, end_of_period=True)
    # Делаем первое значени равное 1
    data['stocks_cum'] /= data.query('stocks_cum==stocks_cum')['stocks_cum'].values[0]
    # Вычисляем доходность
    data['stocks_rt'] = np.log(data['stocks_cum']) - np.log(data['stocks_cum'].shift(1))
    data = data[['dt', 'stocks_cum', 'stocks_rt']].copy()
    return data


def plot_stocks(stock):
    fix, ax = plt.subplots(1,2, figsize=(15,5))
    stock.set_index('dt')['real_div_amt'].plot(ax=ax[0], kind='bar', 
                                        color='green', title='Dividends', xticks=range(0, len(stock), 500))
    stock.set_index('dt')['real_price'].plot(ax=ax[1], kind='line', 
                                            color='red', title='Price', )