import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os


def extract_ru_tickers_and_capitalization(url="https://smart-lab.ru/q/shares_fundamental/?field=market_cap"):
    """
    Extracts tickers and their capitalization from a given URL.

    Args:
        url: The URL of the webpage containing the table.

    Returns:
        A dictionary where keys are tickers and values are their capitalization, 
        or None if there's an error.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table (adjust selector if needed based on website structure)
        table = soup.find('table') #or a more specific selector if needed (e.g., soup.find('table', {'id': 'my-table'}))
        if table is None:
            return None  #Table not found

        tickers_cap = {}
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 5:  # Ensure there are enough columns
                ticker = cols[2].text.strip()
                capitalization = cols[5].text.strip()
                #print(ticker, capitalization)
                try:
                    capitalization = float(capitalization.replace(' ', ''))  # Clean and convert to int
                    tickers_cap[ticker] = capitalization
                except ValueError:
                    print(f"Could not parse capitalization for {ticker}.")

        tickers = [{'ticker': x, 'capitalization': y} for x, y in tickers_cap.items()]
        tickers = pd.DataFrame.from_dict(tickers)
        tickers['country'] = 'Russia'
        return tickers

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def extract_usa_tickers(url="https://smart-lab.ru/q/usa/"):
    """
    Extracts tickers from the provided HTML content.

    Args:
        html_content: The HTML content as a string.

    Returns:
        A list of tickers, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        tickers = []
        for row in soup.find_all('tr'):
            #Prioritize the 'ticker' attribute if present, otherwise, extract from the first <td>
            ticker_attr = row.get('ticker')
            if ticker_attr:
                tickers.append(ticker_attr)
            else:
                first_td = row.find('td', class_='trades-table__ticker')
                if first_td:
                  tickers.append(first_td.text.strip())
        tickers = pd.DataFrame(tickers, columns=['ticker'])
        tickers['country'] = 'USA'
        return tickers
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None
    
def extract_world_tickers(url='https://smart-lab.ru/q/world-stocks/'):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for row in soup.find_all('tr'):
            #print(row)
            ticker_attr = row.get('ticker')
            if not ticker_attr:
                ticker_attr = row.find('td', class_='trades-table__ticker')
                if ticker_attr:
                    ticker_attr = ticker_attr.text.strip()
            
            country_img = row.find('img', class_='flagicon')
            #print(dir(ticker_attr))
            #print(ticker_attr, country_img['title'] if country_img else None)
            if ticker_attr and country_img:
                country = country_img['title']
                results.append({'ticker': ticker_attr, 'country': country})

        return pd.DataFrame.from_dict(results)
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None
    

def check_webpage_exists(url, verbose=False):
    """
    Checks if a webpage exists and is accessible.

    Args:
        url: The URL of the webpage to check.

    Returns:
        True if the webpage exists and returns a successful status code (200-299), 
        False otherwise.  Prints informative messages about failures.
    """
    try:
        response = requests.get(url, timeout=5)  # Set a timeout (in seconds) to prevent indefinite hanging
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        #if 'Нет доступных отчетов' in requests.get('https://smart-lab.ru/q/SBER/f/q/GAAP/download/', timeout=5).text:
        #    return False
        return True  # Success: page exists and is accessible
    except requests.exceptions.RequestException as e:
        if verbose: print(f"Error accessing URL '{url}': {e}")
        return False  # Error accessing the URL
    except requests.exceptions.HTTPError as e:
        if verbose: print(f"HTTP error accessing URL '{url}': {e} (status code: {response.status_code})")
        return False #HTTP error
    except Exception as e:
        if verbose: print(f"An unexpected error occurred: {e}")
        return False #Other exceptions
    
def check_report_exists(ticker, report_type='MSFO', verbose=False):
    link = f'https://smart-lab.ru/q/{ticker}/f/q/{report_type}/download/'
    return check_webpage_exists(link, verbose=verbose)


def correct_date(df, fraction):
        def func(x):
            if x == 'LTM':
                return np.nan
            #print(x)
            year = x[:4]
            quarter = int(x[5])
            dict_ = {1:'01-01', 2: '04-01-', 3: '07-01', 4: '10-01'}
            date = f'{year}-{dict_[quarter]}'
            return pd.to_datetime(date)
        
        def keep_last_report(df):
            if fraction=='q': df['dt'] = df['dt'].apply(lambda x: str(x)[:6])
            else: df['dt'] = df['dt'].apply(lambda x: str(x)[:4])
            df = df[::-1]
            df['last_flg'] = df.groupby('dt').cumcount().values
            df = df[::-1]
            df.query('last_flg == 0', inplace=True) 
            del df['last_flg']
            return df
            
        data = df.reset_index()
        data['dt'] = data['index']
        del data['index']

        data = keep_last_report(data.copy())
        
        if fraction=='q': data['dt'] = data['dt'].apply(func)
        data = data[['dt'] + list(data.columns[:-1])]
        return data
    

def extract_multipliers(ticker, report_type='MSFO', fraction='q'):

    def download_mult(ticker, report_type='MSFO'): # or 'MSFO', 'GAAP', 'RSBU'
        link = f'https://smart-lab.ru/q/{ticker}/f/{fraction}/{report_type}/download/'
        #print(link)
        #import warnings
        #from urllib3.exceptions import InsecureRequestWarning

        # Отключаем конкретное предупреждение
        #warnings.simplefilter('ignore', InsecureRequestWarning)
        response = requests.get(link, stream=True)  # stream=True is good for large files
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        filename = f'tmp/{ticker}_{report_type}_data.csv'  #or get filename from headers if available

        with open(filename, 'wb') as f:  # 'wb' for writing binary data
            for chunk in response.iter_content(chunk_size=8192): #Iterate chunk-wise for memory efficiency
                f.write(chunk)
        df = pd.read_csv(filename, sep=';')  # read the downloaded file
        os.remove(filename)
        # Переворачиваем таблицу
        df = df.set_index('Unnamed: 0').T
        # Убираем 'Unnamed: 0' из столбцов
        df.columns = list(df.columns)
        return df
    
    df = download_mult(ticker, report_type)
    df = correct_date(df, fraction)
    return df

# nikkei225 = yf.download('AAPL', start='2020-01-01', end='2024-12-31', progress=False, interval='1y')
# dat = yf.Ticker("MSFT")
# dat.info
# dat.calendar
# dat.analyst_price_targets
# dat.quarterly_income_stmt


from tqdm import tqdm


def download_all_statements(all_tickers, fraction, report=None, verbose=False):
    if report is None: report = {}

    for num in tqdm(range(len(all_tickers)), desc="Загрузка данных об акциях", unit="акция"):
        row = all_tickers.iloc[num]
        ticker = row['ticker']
        country = row['country']
        for standart in ['MSFO', 'GAAP']:
            try:
                if (ticker, standart) in report:
                    continue
                if country == 'Russia' and standart == 'GAAP':
                    report[(ticker, standart)] = 'russia_gap'
                    continue
                if not check_report_exists(ticker, standart, verbose):
                    report[(ticker, standart)] = 'err_1'
                    continue
                data = extract_multipliers(ticker, standart, fraction)
                #print(ticker, standart, data.shape)
                if fraction=='q': data.query('dt == dt', inplace=True)
                report[(ticker, standart)] = data
            except requests.exceptions.RequestException as e:
                if verbose: print(f'Ошибка при запросе данных для {ticker} {standart}: {e}')
                report[(ticker, standart)] = 'err_2'
            except ValueError as e:
                if verbose: print(f'Ошибка значения для {ticker} {standart}: {e}')
                report[(ticker, standart)] = 'err_3'
            except Exception as e:
                if verbose: print(f'Неизвестная ошибка для {ticker} {standart}: {e}')
                report[(ticker, standart)] = 'err_4'
    return report

def str_to_float(df, col, type_=float):
    df[col] = df[col].apply(lambda x: type_(str(x).replace(' ', '').replace(',', '.')) if x else None)

def percent_to_float(df, col):
    df[col] = df[col].apply(lambda x: float(str(x).replace(' ', '').replace('%', ''))/100 if x else None)


def process_rus(info, dfs):
    result = []
    for num, row in info.iterrows():
        if row['country'] != 'Russia':
            continue
        df = dfs[row['df_id']].copy()
        rename = {
                'Валюта отчета': 'currency', 
                'Выручка, млрд руб': 'sales', 
                'Чистый операц доход, млрд руб': 'sales',
                'EBITDA, млрд руб': 'ebitda',
                'Баланс стоимость, млрд руб': 'book_value',
                'Капитал, млрд руб': 'book_value',
                'Чистая прибыль, млрд руб': 'earning',
                'Дивиденд, руб/акцию': 'div_per_share',
                'Цена акции ао, руб': 'stock_price', 'Число акций ао, млн': 'stock_amt', 
                'Капитализация, млрд руб': 'market_cap',
                'ROE, %': 'roe', 
                'ROA, %': 'roa', 
                }
        df = df.rename(columns=rename).copy()
        keys = list(set(key for key in rename.values() if key in df.columns))
        for col in keys:
            if col in ['sales', 'ebitda', 'book_value', 'earning', 'div_per_share',
                    'stock_price',  'market_cap', 'stock_amt']:
                str_to_float(df, col)
        if 'roe' in keys: percent_to_float(df, 'roe')
        if 'roa' in keys: percent_to_float(df, 'roa')
        if 'div_per_share' not in keys:
            keys+=['div_per_share']
            df['div_per_share'] = 0
        #print(row['ticker'], len(tmp), len(keys), [key for key in rename.values() if key not in tmp.columns])
        df = df[keys + ['dt']]
        
        df = df.rename(columns={'dt': 'year'})
        df = df.loc[df['year'].apply(lambda x: str(x).isdigit())]
        #df.query('year!="LTM"', inplace=True)
        df['year'] = df['year'].astype(int)
        df['ticker'] = row['ticker']
        df['country'] = 'Russia'
        result.append(df)
    return result


def rename_gaap(df):
    names = {'currency': 'Валюта отчета', 'sales': 'Выручка, млн $',
            'operational_revenue': 'Операционная прибыль, млн $', 'ebitda': 'EBITDA, млн $',
            'earning': 'Чистая прибыль, млн $', 'operational_cf': 'Операционный денежный поток, млн $',
            'capex': 'CAPEX, млн $', 'fcf': 'FCF, млн $', 'div': 'Див.выплата, млн $', 
            'div_yield_%': 'Див доход, ао, %', 'div_por': 'Дивиденды/прибыль, %',
            'operational_cost': 'Опер. расходы, млн $', 'net_cap': 'Себестоимость, млн $',
            'rnd': 'НИОКР, млн $', 'percent_cost': 'Процентные расходы, млн $',
            'assets': 'Активы, млн $', 'clear_assets': 'Чистые активы, млн $', 'debt': 'Долг, млн $',
            'cash': 'Наличность, млн $', 'clear_debt': 'Чистый долг, млн $',
            'stock_price': 'Цена акции ао, руб', 'stock_amt': 'Число акций ао, млн',
            'market_cap': 'Капитализация, млн $', 'EV': 'EV, млн $', 'book_value': 'Баланс стоимость, млн $',
            'eps': 'EPS, $', 'fcf_per_share': 'FCF/акцию, руб', 'bv_per_share': 'BV/акцию, руб',
            'rent_ebitda': 'Рентаб EBITDA, %', 'rent_clear': 'Чистая рентаб, %', 
            'profitability_fcf': 'Доходность FCF, %', 'roe': 'ROE, %', 'roa': 'ROA, %',
            'p_e': 'P/E', 'p_fcf':'P/FCF', 'p_s':'P/S', 'p_b': 'P/BV', 'ev_ebitda': 'EV/EBITDA',
            'debt_ebitda': 'Долг/EBITDA', 'rnd_capex': 'R&D/CAPEX, %', 'capex_s': 'CAPEX/Выручка, %'}
    currency = df['Валюта отчета'].unique()[0]
    if currency == 'USD':
        df['unit'] = 'USD 1kk'
        pass
    elif currency == 'CNY':
        names = {key:val.replace('млн $', 'млн юаней') for key,val in names.items()}
        df['unit'] = 'CNY 1kk'
    elif currency == 'EUR':
        names = {key:val.replace('млн $', '€') for key,val in names.items()}
        df['unit'] = 'EUR 1'
    name_rev = {val:key for key,val in names.items()}
    data = df.rename(columns=name_rev)
    return data

def process_world(info, dfs):
    result = []
    for num, row in info.iterrows():
        if row['country'] == 'Russia':
            continue
        #print(row['ticker'])
        df = dfs[row['df_id']].copy()
        df = rename_gaap(df)
        #if 'dt' not in df.columns: df = correct_date(df, 'y')
        columns = ['year', 'sales', 'book_value', 'earning', 'div_per_share',
                   'stock_price', 'stock_amt', 'market_cap', 'roe', 'roa']
        keys = list(set(key for key in columns if key in df.columns))
        for col in keys:
            if col in ['sales', 'ebitda', 'book_value', 'earning', 'div_per_share',
                    'stock_price',  'market_cap', 'stock_amt']:
                str_to_float(df, col)
        if 'roe' in keys: percent_to_float(df, 'roe')
        if 'roa' in keys: percent_to_float(df, 'roa')
        if 'div_per_share' not in keys:
            keys+=['div_per_share']
            df['div_per_share'] = 0

        df['year'] = df['dt']
        df = df.loc[df['year'].apply(lambda x: str(x).isdigit())]
        df = df[keys + ['year']]

        #df.query('year!="LTM"', inplace=True)
        df['year'] = df['year'].astype(int)
        df['ticker'] = row['ticker']
        df['country'] = row['country']
        result.append(df)
    return result


from .load.yahoo import load_exchange_rate
def add_currency_rate(df):
    currency = df['currency'].unique()[0]
    if currency=='USD':
        return df
    if currency=='RUB':
        rates = load_exchange_rate('RUB', '2000-01-01', '2027-02-01', '1mo')
    elif currency=='EUR':
        rates = load_exchange_rate('EUR', '2000-01-01', '2027-02-01', '1mo')
    else:
        return df
    rates['year'] = rates['dt'].dt.year
    rates['month'] = rates['dt'].dt.month
    rates.query('month == 1', inplace=True)
    df = pd.merge(df, rates[['year', 'rate']], on='year', how='inner')
    return df