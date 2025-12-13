from tinkoff.invest import Client
from ...settings import get_variable
from ...sql import has_table, get_connetion, to_sql
import pandas as pd

def _get_dataframe_of_instruments():
    """Получаем таблицу соответствия figi, тикера и названия инструмента"""
    l=[]
    with Client(get_variable('T-TOKEN'), target=get_variable('T-TARGET')) as client:
        instruments = client.instruments
        for method in ['shares', 'bonds', 'etfs', 'currencies', 'futures']:
            #len_ = len(l)
            #print(f'Получение инструментов {method}...', end='\n')
            for item in getattr(instruments, method)().instruments:
                l.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name,
                })
            #print(f'\tБыло получено {len(l) - len_} инструментов.')
        l = pd.DataFrame(l)
    
    return l

def load_sql_instruments(engine=get_connetion(), force=False):
    if force or not has_table('instruments', engine):
        df = _get_dataframe_of_instruments()
        to_sql('instruments', df, engine)
    else:
        df = pd.read_sql_table('instruments', con=engine)
    return df

