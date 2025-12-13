import pandas as pd
from tinkoff.invest import Client
from ...settings import get_variable
from .utils import ticker_to_figi
from ...utils import handle_types

def load_dividends(ticker, start, end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    figi = ticker_to_figi(ticker)
    with Client(get_variable('T-TOKEN'), target=get_variable('T-TARGET')) as client:
        dividends = client.instruments.get_dividends(figi=figi, 
                                                     from_=start, 
                                                     to=end)
        
        df = pd.DataFrame()
        for i in dividends.dividends:
            div = {'dividend_amt': i.dividend_net,
                'payment_date': i.payment_date,
                'declared_date': i.declared_date,
                'last_buy_date': i.last_buy_date,}
            div = handle_types(div)
            df = pd.concat([df, pd.DataFrame.from_dict(div, orient='index').T])

    return df