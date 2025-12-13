from ...load import load_exchange_rate
from .configs import _get_country_to_rate
from .indexes import _read_index
from .utils import keep_frequency

import pandas as pd
import numpy as np


def _load_currency_from_yahoo(country, start, end, interval='day', core='yahoo', proxies=None):
    if country == 'USA':
        ticker = _get_country_to_rate()['Canada']
        rate = load_exchange_rate(ticker, start, end, 'month', core=core, proxies=proxies)
        rate['rate'] = 1
    else:
        ticker = _get_country_to_rate()[country]
        rate = load_exchange_rate(ticker, start, end, 'month', core=core, proxies=proxies)

    # # Заполняем выходные тоже данными
    # rate = pd.merge(pd.DataFrame({'dt': pd.date_range(start, end, freq='D')}), 
    #                 rate, how='left', on='dt')
    rate['price'] = rate['rate'].astype('float')#.infer_objects(copy=False).ffill()
    # rate = keep_frequency(rate, 'M')
    rate = rate[['dt', 'price']].copy()
    rate['price'] = 1 / rate['price']
    return rate

def _load_currency_from_index(country, start, end):
    # Средние курсы за месяц
    index_nm = 'currency <avg period | M>'
    # Курс на конец месяца
    index_nm = 'currency <end period | M>'
    if country == 'USA':
        # Там большой лаг, так что приходится кусками
        data = _read_index('Canada', start, end, index_nm=index_nm)
        data['price'] = 1
    else:
        try:
            data = _read_index(country, start, end, index_nm=index_nm)
        except:
            # Для некоторых стран перевернутые данные
            # Warning(f'Currency is not available for {country}. Tr')
            index_nm = 'currency <end period | M> 2'
            data = _read_index(country, start, end, index_nm=index_nm)
            data['price'] = 1 / data['price'] # Делали для другого индекса -- Тут и так все норм
    return data

def prepare_currency(country, start, end, interval='month', core='yahoo', proxies=None, include_real=False):
    dt = '2020-01-01'
    if start >= dt:
        data = _load_currency_from_yahoo(country, start, end)
    elif end <= dt:
        data = _load_currency_from_index(country, start, end)
    else:
        start = _load_currency_from_index(country, start, '2020-01-01').query('dt<"2020-01-01"')
        end = _load_currency_from_yahoo(country, '2020-01-01', end)
        data = pd.concat([start, end])
    data = data.sort_values('dt').reset_index(drop=True)
    # Сколько долларов можно купить за один currency
    data['currency_cum'] = data['price']

    data['currency_rt'] = np.log(data['currency_cum']) - np.log(data['currency_cum'].shift(1))
    data = data[['dt', 'currency_rt', 'currency_cum']]
    return data


def plot_rates(rate):
    rate.set_index('dt')['rate'].plot()
