import pandas as pd

class Candle:

    def __init__(self, open, high, low, close, volume, datetime, interval=None):
        self.open = open; self.high = high; self.low = low; 
        self.close = close; self.volume = volume
        self.interval = interval

        self.datetime = datetime
        self.date = datetime.date()
        self.time = datetime.time()

    @classmethod
    def from_t_candle(cls, historic_candle, interval=None):
        price_open = historic_candle.open.units + historic_candle.open.nano / 1e9
        price_high = historic_candle.high.units + historic_candle.high.nano / 1e9
        price_low = historic_candle.low.units + historic_candle.low.nano / 1e9
        price_close = historic_candle.close.units + historic_candle.close.nano / 1e9
        volume = historic_candle.volume
        datetime = historic_candle.time
        return cls(price_open, price_high, price_low, price_close, volume, datetime, interval)
    
    def to_dict(self):
        dict_ = {
            'open': self.open, 'high': self.high, 'low': self.low,
            'close': self.close, 'volume': self.volume, 
            'date': self.date, 'time': self.time, 'datetime': self.datetime
        }
        return dict_
    
    def to_df(self):
        return pd.DataFrame([self.to_dict()])