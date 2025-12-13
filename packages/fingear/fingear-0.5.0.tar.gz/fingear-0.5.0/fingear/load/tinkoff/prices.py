from tinkoff.invest import Client
import pandas as pd
from ...settings import get_variable
from .utils import ticker_to_figi
from .candle import Candle
from .utils import transcript_interval


def load_candles(ticker, start, end, interval):
    candles = pd.DataFrame()
    figi = ticker_to_figi(ticker)
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    with Client(get_variable('T-TOKEN'), target=get_variable('T-TARGET')) as client:
        for candle in client.get_all_candles(
            figi=figi,
            from_=start,
            to=end,
            interval=transcript_interval(interval),
        ):
            candle = Candle.from_t_candle(candle, interval)
            candles = pd.concat([candles, candle.to_df()])
    candles['datetime'] = pd.to_datetime(candles['datetime'])
    candles.reset_index(drop=True, inplace=True)
    candles = candles[['datetime', 'open', 'close', 'low', 'high', 'volume']]
    candles.sort_values('datetime', inplace=True)
    return candles