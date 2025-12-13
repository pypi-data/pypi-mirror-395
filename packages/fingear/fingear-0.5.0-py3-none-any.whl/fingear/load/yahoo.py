import yfinance as yf
import pandas as pd
import numpy as np

# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
def interval_transcription():
    transcription =  {
        '1m': '1m',
        '2m': '2m',
        #'3m': '2m',
        '5m': '5m',
        #'10m': CandleInterval.CANDLE_INTERVAL_10_MIN,
        '15m': '15m',
        '30m': '30m',
        '1h': '1h',
        #'2h': 'ERR',
        #'4h': 'ERR'
        'day': '1d',
        '5d': '5d', # NO Tinkoff
        'week': '1wk',
        'month': '1mo',
    }
    return transcription

def transcript_interval(interval):
    return interval_transcription()[interval]

def process_inputs(start, end, interval=None, proxies=None):
    start = pd.to_datetime(start).strftime('%Y-%m-%d')
    end = pd.to_datetime(end).strftime('%Y-%m-%d')
    if interval is not None: interval = transcript_interval(interval)
    if proxies is not None: yf.set_config(proxy=np.random.choice(proxies))
    return start, end, interval


def load_exchange_rate(currency, start, end, interval, proxies=None):
    start, end, interval = process_inputs(start, end, interval, proxies)
    data = yf.download(f'{currency}=X', start=start, end=end, 
                       progress=False, interval=interval,
                       auto_adjust=True)
    data = pd.DataFrame(data.reset_index().values, 
                        columns=['dt', 'close', 'high', 'low', 'open', 'volume'])
    data = data[['dt', 'close']]
    data.columns = ['dt', 'rate']
    return data

def load_candles(ticker, start, end, interval, proxies=None):
    start, end, interval = process_inputs(start, end, interval, proxies)
    data = yf.download(ticker, start=start, end=end, 
                       progress=False, interval=interval, 
                       auto_adjust=True)
    data = pd.DataFrame(data.reset_index().values, 
                        columns=['datetime', 'close', 'high', 'low', 'open', 'volume'])
    data = data[['datetime', 'open', 'close', 'low', 'high', 'volume']]
    return data

def load_dividends(ticker, start, end, proxies=None):
    start, end, _ = process_inputs(start, end, None, proxies)
    data = yf.Ticker(ticker).dividends
    data = pd.DataFrame(data.reset_index().values, 
                        columns=['datetime', 'dividends'])
    data = data[['datetime', 'dividends']]
    return data