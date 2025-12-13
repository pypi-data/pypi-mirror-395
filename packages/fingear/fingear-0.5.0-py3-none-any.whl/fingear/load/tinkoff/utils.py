from tinkoff.invest import CandleInterval

from ...sql import get_connetion

from .instruments import load_sql_instruments

def interval_transcription():
    transcription =  {
        '1m': CandleInterval.CANDLE_INTERVAL_1_MIN,
        '2m': CandleInterval.CANDLE_INTERVAL_2_MIN,
        '3m': CandleInterval.CANDLE_INTERVAL_3_MIN,
        '5m': CandleInterval.CANDLE_INTERVAL_5_MIN,
        '10m': CandleInterval.CANDLE_INTERVAL_10_MIN,
        '15m': CandleInterval.CANDLE_INTERVAL_15_MIN,
        '30m': CandleInterval.CANDLE_INTERVAL_30_MIN,
        '1h': CandleInterval.CANDLE_INTERVAL_HOUR,
        '2h': CandleInterval.CANDLE_INTERVAL_2_HOUR,
        '4h': CandleInterval.CANDLE_INTERVAL_4_HOUR,
        'day': CandleInterval.CANDLE_INTERVAL_DAY,
        'week': CandleInterval.CANDLE_INTERVAL_WEEK,
        'month': CandleInterval.CANDLE_INTERVAL_MONTH,
    }
    return transcription

def transcript_interval(interval):
    return interval_transcription()[interval]


def ticker_to_figi(ticker, engine=get_connetion()):
    df = load_sql_instruments(engine)
    return df[df['ticker'] == ticker]['figi'].iloc[0]

def figi_to_ticker(figi, engine=get_connetion()):
    df = load_sql_instruments(engine)
    return df[df['figi'] == figi]['ticker'].iloc[0]