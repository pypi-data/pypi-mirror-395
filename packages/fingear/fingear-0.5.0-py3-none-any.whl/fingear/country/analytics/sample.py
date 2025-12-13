import pandas as pd
import numpy as np

def get_portion(data, batch_size=24, seed=None):
    if seed is not None:
        np.random.seed(seed)
    start = np.random.choice(data['dt'].values[:-batch_size])
    end = start + pd.DateOffset(months=batch_size)
    return data.query('dt>=@start and dt<@end').copy()

def get_sample(data, size=15, batch_size=24, start_dt='2000-01-01'):
    data = pd.concat([get_portion(data, batch_size=batch_size) for _ in range(size)]).reset_index(drop=True)
    data['dt'] = pd.date_range(start_dt, periods=size*batch_size, freq='MS')
    return data

