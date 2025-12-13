from .currencies import prepare_currency
from .stocks import prepare_stocks
from .indexes import prepare_bonds, prepare_cpi, prepare_money_market
from .indexes import prepare_realty
from .comodities import prepare_comodity
from .configs import _get_general_futures, get_full_country

import pandas as pd


def _load_country(country, start, end, interval='day', core='yahoo', proxies=None, verbose=False):
    if verbose: print(f'Country: {country} | Start: {start} | End: {end} | Interval: {interval} | Core: {core} | Proxies: {proxies}')
    if verbose: print('\tInflation loading...', end=' ')
    # inflation = prepare_inflation(country, start, end)
    inflation = prepare_cpi(country, start, end, interval, core=core, proxies=proxies)

    if verbose: print('Done!'); print('\tMoney market loading...', end=' ')
    money = prepare_money_market(country, start, end, interval, core=core, proxies=proxies)

    if verbose: print('Done!'); print('\tRates loading...', end=' ')

    currency = prepare_currency(country, start, end, interval, core=core, proxies=proxies)

    if verbose: print('Done!'); print('\tStocks loading...', end=' ')
    # Данные на конец месяца - ОК
    stocks = prepare_stocks(country, start, end, interval, core=core, proxies=proxies)

    if verbose: print('Done!'); print('\tBonds loading...', end=' ')
    bonds = prepare_bonds(country, start, end, interval, core=core, proxies=proxies)

    if verbose: print('Done!'); print('\tRealty loading...', end=' ')
    realty = prepare_realty(country, start, end, interval, core=core, proxies=proxies)
    
    if verbose: print('Done!')
    return inflation, money, currency, stocks, bonds, realty

def _merge_country(start, end, dfs):
    frame = pd.DataFrame(pd.date_range(start, end, freq='MS'), columns=['dt'])
    for df in dfs: 
        frame = pd.merge(frame, df, how='left', on='dt')
    return frame

def _cunstruct_cols(df, country):
    res = df[['dt']].copy()

    for col in ['inflation_rt']:
        res[f'{country}_{col}'] = df[col].values

    for col in ['stocks_rt', 'currency_rt']:
        res[f'{country}_{col}'] = df[col].values

    for col in ['bonds_rt', 'money_rt', 'realty_rt']:
        res[f'{country}_{col}'] = df[col] + df[f'currency_rt']

    return res


def prepare_country(country, start, end, interval='day', core='yahoo', 
                    proxies=None, verbose=False, construct=True):
    dfs = _load_country(country, start, end, interval, core, proxies, verbose)

    data = _merge_country(start, end, dfs)
    if construct: data = _cunstruct_cols(data, country)
    
    return data


def prepare_general(start, end, interval='day', core='yahoo', proxies=None, verbose=False):
    data = pd.DataFrame(pd.date_range(start, end, freq='MS'), columns=['dt'])
    for com in _get_general_futures().keys():
        if verbose: print(f'Comodity: {com} | Start: {start} | End: {end} | Interval: {interval} | Core: {core}')
        part = prepare_comodity(com, start, end, method='Futures', interval=interval, core=core, proxies=proxies)
        if verbose: print(f"\t{com} Done!")
        del part[f'{com}_cum']
        data = pd.merge(data, part, how='left', on='dt')
    return data


def prepare_data(start, end, interval='day', core='yahoo', proxies=None, verbose=False, construct=True):
    data = prepare_general(start, end, interval, core, proxies, verbose=verbose)

    for country in get_full_country():
        part = prepare_country(country=country, start=start, end=end, interval='month', 
                                core='yahoo', proxies=proxies, verbose=verbose, construct=construct)
        data = pd.merge(data, part, on='dt')

    return data