from .indexes import _read_index, _read_index_data
from .configs import _get_general_index, _get_general_futures
from ...load import load_asset_price

import numpy as np
import pandas as pd

def prepare_comodity(comodity, start, end, method='index', interval='month', core='yahoo', proxies=None):
    if method == 'index':
        index = _get_general_index()[comodity]
        data = _read_index_data(index, start, end, proxies=proxies)
        # Тут цена активна указана, как среднее за месяц
        # Уменьшаем дату, чтобы сдвинуть на месяц назад
        data['dt'] -= pd.DateOffset(months=1)

    # if method == 'ETF':
    #     data = load_asset_price('GLD', start, end, interval, core, proxies, include_real)
    #     data.rename(columns={'dttm': 'dt'}, inplace=True)
    if method == 'Futures':
        index = _get_general_futures()[comodity]
        data = load_asset_price(f'{index}=F', start, end, interval, core, proxies)
        data.rename(columns={'dttm': 'dt'}, inplace=True)
        # Есть пропуски в данных
        data = pd.merge(pd.DataFrame({'dt': pd.date_range(start, end, freq='MS')}), data, how='left', on='dt')
        data['price'] = data['price'].astype(float).interpolate(method='linear')
    
    # data = _fill_gaps(data, 'interpolate')
    data[f'{comodity}_rt'] = np.log(data['price'].astype(float)) - np.log(data['price'].astype(float).shift(1))
    data[f'{comodity}_cum'] = np.exp(data[f'{comodity}_rt'].cumsum())
    data = data[['dt', f'{comodity}_rt', f'{comodity}_cum']]

    return data

# def prepare_gold(start, end, method='ETF', interval='month', core='yahoo', proxies=None, include_real=False):
#     if method == 'index':
#         index = _get_general_index()['gold']
#         data = _read_index_data(index, start, end)
#     if method == 'ETF':
#         data = load_asset_price('GLD', start, end, interval, core, proxies, include_real)
#         data.rename(columns={'dttm': 'dt'}, inplace=True)
#     if method == 'Futures':
#         data = load_asset_price('GC=F')
#         data.rename(columns={'dttm': 'dt'}, inplace=True)

#     comodity = 'gold'
#     data[f'{comodity}_rt'] = np.log(data['price']) - np.log(data['price'].shift(1))
#     data[f'{comodity}_cum'] = np.exp(data[f'{comodity}_rt'].cumsum())
#     data = data[['dt', f'{comodity}_rt', f'{comodity}_cum']]

#     return data

# def prepara_silver(start, end, method='ETF', interval='month', core='yahoo', proxies=None, include_real=False):
#     if method == 'index':
#         pass
#         # index = _get_general_index()['silver']
#         # data = _read_index_data(index, start, end)
#     if method == 'ETF':
#         data = load_asset_price('SLV', start, end, interval, core, proxies, include_real)
#         data.rename(columns={'dttm': 'dt'}, inplace=True)
#     if method == 'Futures':
#         data = load_asset_price('SI=F')
#         data.rename(columns={'dttm': 'dt'}, inplace=True)

#     comodity = 'silver'
#     data[f'{comodity}_rt'] = np.log(data['price']) - np.log(data['price'].shift(1))
#     data[f'{comodity}_cum'] = np.exp(data[f'{comodity}_rt'].cumsum())
#     data = data[['dt', f'{comodity}_rt', f'{comodity}_cum']]

#     return data