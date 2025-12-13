
from ..load.configs import _get_indicators
import numpy as np
import pandas as pd

def add_cummulative(data, prefix, col=_get_indicators()):
    for col in col:
        data[f'{prefix}_{col}_cum'] = np.exp(data[f'{prefix}_{col}_rt'].cumsum())
    return data

# def add_prefix(data, prefix, col=_get_indicators()+['currency'], postfix='rt', del_origonal=True):
#     for col in col:
#         data[f'{prefix}_{col}_{postfix}'] = data[f'{col}_{postfix}']
#         if del_origonal:
#             del data[f'{col}_{postfix}']
#     return data

def describe_longivity(df, prefix=None, columns=_get_indicators()+['currency'], postfix='rt'):
    if prefix:
        columns = [f'{prefix}_{col}' for col in columns]
    if postfix:
        columns = [f'{col}_{postfix}' for col in columns]
    res = {}
    for col in columns:
        res[col] = {'first': df[~df[col].isna()]['dt'].min().strftime('%Y-%m-%d'), 
                    'last': df[~df[col].isna()]['dt'].max().strftime('%Y-%m-%d')}
    res = pd.DataFrame.from_dict(res, orient='index')
    return res