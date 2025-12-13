from tinkoff.invest import Client
from ...settings import get_variable
from ...utils import handle_types, normalize_date
from .utils import ticker_to_figi

import pandas as pd


def load_bond_coupons(ticker, start='2020-01-01', end='2030-01-01'):
    figi = ticker_to_figi(ticker)
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    with Client(get_variable('T-TOKEN'), target=get_variable('T-TARGET')) as client:
        coupons = client.instruments.get_bond_coupons(figi=figi, 
                                                      from_=start, 
                                                      to=end)
        res = pd.DataFrame()
        for num, cup in enumerate(coupons.events):
            data = {'dt': cup.coupon_date,
                   'rn': cup.coupon_number,
                   'rub_amt': cup.pay_one_bond,
                   'period_in_days': cup.coupon_period}
            data = handle_types(data, to_dt=True)
            data = pd.DataFrame.from_dict(data, orient='index').T
            res = pd.concat([res, data])
        res['dt'] = normalize_date(res['dt'])
        return res
    

def load_bond_info(ticker):
    figi = ticker_to_figi(ticker)
    with Client(get_variable('T-TOKEN'), target=get_variable('T-TARGET')) as client:
        data = client.instruments.bond_by(id_type=1, id=figi)
        res = {'figi': data.instrument.figi,
            'ticker': data.instrument.ticker,
            'name': data.instrument.name,
            'placement_date': data.instrument.placement_date,
            'maturity_date': data.instrument.maturity_date,
            'nominal': data.instrument.nominal,
            'nkd': data.instrument.aci_value,
            'frequency': data.instrument.coupon_quantity_per_year,
            }
        res = handle_types(res, to_dt=True)
        res['maturity_date'] = normalize_date(res['maturity_date'])
        res['placement_date'] = normalize_date(res['placement_date'])
        return res
    

