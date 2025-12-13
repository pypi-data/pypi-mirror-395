import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import io
import requests

from ...instruments.analize import bond_index_to_return
from ...load import load_exchange_rate
from .configs import _get_country_to_indexes, _get_country_index, _get_country_to_rate


def _fill_gaps(data, method='ffill'):
    frame = pd.DataFrame(pd.date_range(data['dt'].min(), 
                      pd.to_datetime(datetime.now(), format='%Y-%m-%d'), 
                      freq='MS'), columns=['dt'])
    data = pd.merge(frame, data, how='left', on='dt')
    if method == 'ffill':
        data = data.ffill()
    elif method == 'interpolate':
        data = data.interpolate(method='linear')
    elif method == 'none':
        data = data
    return data

def _read_canada_bonds():
    data = pd.read_csv('data/canada_bonds.csv')
    data['dt'] = pd.to_datetime(data['Date'])
    data['price'] = data['Price']
    data = data[['dt', 'price']]
    data.sort_values('dt', inplace=True)
    data.reset_index(drop=True, inplace=True)
    data['price']/=100
    data = _fill_gaps(data)
    return data

def _read_russia_bonds():
    data = pd.read_csv('data/russia_bonds.csv')
    data['dt'] = pd.to_datetime(data['Date'])
    data['price'] = data['Price']
    data = data[['dt', 'price']]
    data.sort_values('dt', inplace=True)
    data.reset_index(drop=True, inplace=True)
    data['price']/=100
    data = _fill_gaps(data)
    return data

def _read_index_data(ticker, start, end, proxies=None):
    url = f"""https://fred.stlouisfed.org/graph/fredgraph.csv"""
    params = {
        'id': ticker,
        'cosd': start,
        'coed': end,
        'fq': 'Monthly',
        'fam': 'avg',
        'fgst': 'lin',
        'fgsnd': '2020-02-01',
        'vintage_date': end,
        'revision_date': end,
        'nd': start
    }
    full_url = url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])

    if proxies is None:
        s = requests.get(full_url).text
    elif isinstance(proxies, dict):
        s = requests.get(full_url, proxies=proxies).text
    elif isinstance(proxies, tuple):
        dict_ = {}
        for num, proxy in enumerate(proxies):
            dict_[f'http{num}'] = proxy
        s = requests.get(full_url, proxies=dict_).text
        
    df = pd.read_csv(io.StringIO(s))

    df.columns = ['dt', 'price']
    df['dt'] = pd.to_datetime(df['dt'])
    df = df.sort_values('dt').reset_index(drop=True)
    return df



def _read_index(country, start, end, index_nm='10_year_bond', proxies=None):
    country_ind = _get_country_to_indexes()[country]
    ticker = _get_country_index()[index_nm](country_ind)
    return _read_index_data(ticker, start, end, proxies=proxies)
    # if country == 'Canada':
    #     data = _read_canada_bonds()
    # elif country == 'russia':
    #     data = _read_russia_bonds()
    # return data.query('dt>=@start and dt<=@end').copy().reset_index(drop=True)
    

def _read_bonds_russia(start, end):
    data = pd.read_excel('fingear/datasets/Russia/bonds.xlsx')
    data['dt'] = pd.to_datetime(data['dt'], format='%d.%m.%Y')
    # Цены в тысячах процентов
    data['price']/=1000
    data = pd.merge(pd.DataFrame({'dt': pd.date_range(data['dt'].min(), data['dt'].max(), freq='MS')}), 
                    data, how='left', on='dt')
    data['price'] = data['price'].interpolate(method='linear')
    data.sort_values('dt', inplace=True)
    return data

def prepare_bonds(country, start, end, interval='month', core='yahoo', proxies=None, include_real=False):
    if country == 'Russia':
        bonds = _read_bonds_russia(start, end)
    else:
        bonds = _read_index(country, start, end, index_nm='10_year_bond', proxies=proxies)
    
    bonds['price'] /= 100
    bonds = bond_index_to_return(bonds)
    if include_real:
        bonds.rename(columns={'price': 'bonds_cum', 'index': 'bond_index', 'return': 'bond_return'}, 
                     inplace=True)
    else:
        bonds = bonds[['dt', 'price']]
        bonds.rename(columns={'price': 'bonds_cum'}, inplace=True)
    bonds['bonds_rt'] = np.log(bonds['bonds_cum']) - np.log(bonds['bonds_cum'].shift(1))
    return bonds

def plot_bonds(bonds, tail=10000):
    fig, ax = plt.subplots(1, 2, figsize=(10,4))
    bonds['Индекс'] = bonds['bond_index']
    bonds['Доходность'] = bonds['bond_return']
    bonds['Накопленная доходность'] = bonds['bonds_cum']
    bonds.tail(tail).set_index('dt')[['Индекс']].plot(ax=ax[0]) # , 'Доходность'
    bonds.tail(tail).set_index('dt')[['Накопленная доходность']].plot(ax=ax[1])
    avg_price = bonds.tail(tail).set_index('dt')[['Накопленная доходность']].mean().values[0]
    avg_index = bonds.tail(tail).set_index('dt')[['Индекс']].mean().values[0]
    # (bonds.tail(tail).set_index('dt')[['Доходность']]/avg_index*avg_price).plot(ax=ax[1])
    return None


def prepare_cpi(country, start, end, interval='month', core='yahoo', proxies=None, include_real=False):
    # Инфляция к этому месяцу, 
    # то есть большой скачок за февраль, приведет к большим значением индекса в марте
    inflation = _read_index(country, start, end, index_nm='consumer_price_index', proxies=proxies)
    # Сдвинем инфляцию на месяц назаж
    inflation['price'] = inflation['price'].shift(-1)
    inflation['inflation_rt'] = inflation['price'].fillna(0) / 100
    inflation['inflation_cum'] = np.exp(inflation['inflation_rt'].cumsum())
    inflation = inflation[['dt', 'inflation_rt', 'inflation_cum']]
    return inflation


def prepare_money_market(country, start, end, interval='month', core='yahoo', proxies=None, include_real=False):
    # Ставка ЦБ на конец месяца
    data = _read_index(country, start, end, index_nm='money_market', proxies=proxies)
    # Считаем ставку за день
    day_rt = (1 + data['price'].fillna(0) / 100 / 365)
    # Считаем через сложный процент
    data['money_rt'] =  day_rt ** (data['dt'].dt.days_in_month) - 1
    data['money_cum'] = np.exp(data['money_rt'].cumsum())
    data = data[['dt', 'money_rt', 'money_cum']]
    return data





def _process_quarterly_avg_data(data):
    # Добавляем пустые месяца
    data = _fill_gaps(data, 'none')
    # Двигаем середину квартала на средний месяц
    data['price'] = data['price'].shift(1)
    # Делаем двойной датасет, чтобы у нас получилось по 6 периодов в квартале
    # Данные за среднее в квартале поставим на середину второго месяца - 4 строчку
    data['priority'] = 1
    portion = data.copy()
    portion['price'] = np.nan
    portion['priority'] = 0
    data = pd.concat([data, portion]).sort_values(['dt', 'priority']).reset_index(drop=True)
    # Теперь линейно интерполируем
    data['price'] = data['price'].interpolate(method='linear').bfill().ffill()
    # Оставляем только данные, где указаны значение на начало\конец месяца
    data.query('priority==0', inplace=True)
    # По договоренности приводим все значения на dt как цену в конце этого месяца
    # Поэтому двигаем на месяц назад
    data['price'] = data['price'].shift(-1)
    return data

def prepare_realty(country, start, end, interval='month', core='yahoo', proxies=None, include_real=False):
    # Данные поквартальные, дают среднее арифметическое за 3 месяца этого квартала
    data = _read_index(country, start, end, index_nm='realty_nominal', proxies=proxies)
    # Превращаем в помесячные данные, где данные на конец месяца
    data = _process_quarterly_avg_data(data)
    data['realty_rt'] = np.log(data['price']) - np.log(data['price'].shift(1))
    data['realty_rt'] += 0.02 / 12
    data['realty_cum'] = np.exp(data['realty_rt'].cumsum())
    data = data[['dt', 'realty_rt', 'realty_cum']]
    return data