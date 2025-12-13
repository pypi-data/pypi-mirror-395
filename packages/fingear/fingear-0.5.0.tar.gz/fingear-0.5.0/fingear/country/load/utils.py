import pandas as pd
import numpy as np

def keep_frequency(data, freq='D', end_of_period=True):
    data['dt'] = pd.to_datetime(data['dt'])
    if end_of_period:
        if freq == 'day':
            data = data
        elif freq == 'month':
            data = data[data['dt'].dt.day==data['dt'].dt.days_in_month].copy()
            data['dt'] = data['dt'] + pd.DateOffset(days=1) - pd.DateOffset(months=1)
        elif freq == 'year':
            data = data[data['dt'].dt.month==12].copy()
            data = data[data['dt'].dt.day==31].copy()
            data['dt'] = data['dt'] + pd.DateOffset(days=1) - pd.DateOffset(years=1)
        elif freq == 'week':
            data = data[data['dt'].dt.dayofweek==6].copy()
            data['dt'] = data['dt'] + pd.DateOffset(days=1) - pd.DateOffset(weeks=1)
        elif freq == 'quarter':
            data = data[data['dt'].dt.month%3==0].copy()
            data = data[data['dt'].dt.day==data['dt'].dt.days_in_month].copy()
            data['dt'] = data['dt'] + pd.DateOffset(days=1) - pd.DateOffset(months=3)
    else:
        if freq == 'day':
            data = data
        elif freq == 'month':
            data = data[data['dt'].dt.day==data['dt'].dt].copy()
        elif freq == 'year':
            data = data[data['dt'].dt.month==1].copy()
            data = data[data['dt'].dt.day==1].copy()
        elif freq == 'week':
            data = data[data['dt'].dt.dayofweek==0].copy()
        elif freq == 'quarter':
            data = data[data['dt'].dt.month%3==1].copy()
            data = data[data['dt'].dt.day==1].copy()
    return data


def add_comission(data, rate=0.008, freq='day'):
    if freq == 'day':
        f = 356
    elif freq == 'week':
        f = 52
    elif freq == 'month':
        f = 12
    data['delta'] = -rate/f
    data['delta_cum'] = np.exp(data['delta'].cumsum())
    data['price'] = data['price']*data['delta_cum']
    # data['delta_cum'].plot()
    # print(data.describe())
    del data['delta'], data['delta_cum']
    return data