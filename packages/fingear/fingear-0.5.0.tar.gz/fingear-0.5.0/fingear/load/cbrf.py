'''
Парсим данные курсов с сайта ЦБ РФ
https://cbr.ru/currency_base/dynamics/
'''


import pandas as pd


def _currency_transcription(currency):
    dict_ = {'USD': 'R01235'}
    if currency not in dict_:
        raise ValueError(f'Currency {currency} not supported')
    return dict_[currency]


def load_exchange_rate(currency, start, end, interval=None):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    currency = _currency_transcription(currency)
    path = f'''https://cbr.ru/Queries/UniDbQuery/DownloadExcel/
    98956?Posted=True&so=1&mode=1&VAL_NM_RQ={currency}&
    From={start.strftime('%d.%m.%Y')}&To={end.strftime('%d.%m.%Y')}&
    FromDate={start.strftime('%m')}%2F{start.strftime('%d')}%2F{start.strftime('%Y')}&
    ToDate={end.strftime('%m')}%2F{end.strftime('%d')}%2F{end.strftime('%Y')}'''
    df = pd.read_excel(path.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', ''))
    df = df[['data', 'curs']].rename(columns={'data':'dttm', 'curs':'rate'})
    df['dttm'] = pd.to_datetime(df['dttm'], format='%d.%m.%Y')
    return df