import pandas as pd
import os

def _join_module_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def _load_by_name(name, ext='pickle'):
    if ext=='pickle':
        return pd.read_pickle(_join_module_path(f'data/{name}.pkl'))
    if ext=='csv':
        return pd.read_csv(_join_module_path(f'data/{name}.csv'))

def ticker_sample(country, ext='pickle'):
    """
    country in ['Japan', 'Russia', 'USA']
    """
    if country == 'Japan':
        return _load_by_name('japan_stocks', ext)
    if country == 'Russia':
        return _load_by_name('russia_stocks', ext)
    if country == 'USA':
        return _load_by_name('usa_stocks', ext)
    raise "country should be in ['Japan', 'Russia', 'USA']"