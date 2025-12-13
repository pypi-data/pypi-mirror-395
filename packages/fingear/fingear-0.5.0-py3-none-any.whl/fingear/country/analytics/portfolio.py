import numpy as np

def portfolio_return(data, weights):
    data['portfolio_rt'] = 0
    # print(weights)
    for i, w in enumerate(weights):
        data['portfolio_rt'] += data[w] * weights[w]
    data['portfolio_cum'] = np.exp(data['portfolio_rt'].cumsum())
    return data


def add_pension_withdraw(data, rate, inflation_col):
    data['pension_withdraw'] = np.exp(data[inflation_col].cumsum()) * rate/12
    return data