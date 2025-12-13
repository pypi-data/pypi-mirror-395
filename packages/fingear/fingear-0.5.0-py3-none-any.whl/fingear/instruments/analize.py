import numpy as np
import pandas as pd

def stock_price_and_div_to_return(div, price, include_real=False):
    """
    Считаем полную доходность актива с учетом реинвестирования дивидендов
    """
    # Готовим данные
    data = price.copy()
    data.rename(columns={'dttm': 'dt'}, inplace=True)
    # Дожойним по дате
    data = pd.merge(data, div.copy(), how='left', on='dt')
    data['div_amt'] = data['div_amt'].infer_objects(copy=False).fillna(0)
    # Считаем, сколько акций у нас будет под конец времени
    data['stock_buy_per_stock'] = (data['div_amt'] / data['price']).astype(float)
    data['stock_buy_log'] = np.log(data['stock_buy_per_stock']+1)
    data['stock_amt'] = np.exp(data['stock_buy_log'].cumsum())
    data['full_price'] = data['price'] * data['stock_amt']
    # del data['stock_buy_per_stock'], data['stock_buy_log']
    # data['full_price'].plot()
    if include_real:
        data = data[['dt', 'full_price', 'stock_amt', 'price', 'div_amt']]
        data.columns = ['dttm', 'price', 'real_stock_amt', 'real_price', 'real_div_amt']
    else:
        data = data[['dt', 'full_price']]
        data.columns = ['dttm', 'price']
    return data



def bond_index_to_return(data):

    def calc_gain(cur_rate, future_rate, time_delta=12, years=10):
        cur_price = 100
        total_rt = (1+cur_rate)**(years)
        face_val = cur_price * total_rt
        # print(face_val)

        month_remains = years*time_delta - 1
        next_month_price = face_val / (1+future_rate)**((month_remains)/time_delta)
        # print(next_month_price)
        gain = (next_month_price - cur_price)/cur_price
        return gain
    
    data['price_prev'] = data['price'].shift(1)
    data['return'] = data.apply(lambda x: calc_gain(x['price_prev'], x['price']), axis=1).fillna(0)
    data['price_real'] = np.exp(data['return'].cumsum())

    data = data[['dt', 'price_real', 'price', 'return']]
    data.columns = ['dt', 'price', 'index', 'return']
    return data