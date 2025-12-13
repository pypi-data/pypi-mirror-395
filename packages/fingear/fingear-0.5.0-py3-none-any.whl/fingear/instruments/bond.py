from ..load import load_bond_info, load_bond_coupons
from ..load import load_single_price
from ..utils import normalize_date

import pandas as pd
from datetime import datetime


class Bond:

    def _init_info(self):
        info = load_bond_info(self.ticker)
        self.name = info['name']
        self.placement_date = info['placement_date']
        self.maturity_date = info['maturity_date']
        self.nominal = info['nominal']
        self.frequency = info['frequency']
        # self.nkd = self.get_nkd_by_dt(datetime.now())

    def _init_coupons(self):
        self.coupons_df = load_bond_coupons(self.ticker, '2000-01-01', '2100-01-01').sort_values('dt')

    def __init__(self, ticker):
        self.ticker = ticker
        self._init_info()
        self._init_coupons()

    def _check_date(self, date):
        date = normalize_date(date)
        if date < self.placement_date or date > self.maturity_date:
            raise ValueError(f'Неверная дата {date}')
        return date

    def _get_nkd_by_dt(self, date=datetime.now()):
        full_coupon = self.coupons_df.query('dt>@date').head(1)['rub_amt'].values[0]
        period = self.coupons_df.query('dt>@date').head(1)['period_in_days'].values[0]
        last_coupon_dt = self.coupons_df.query('dt<=@date')['dt'].max()
        if last_coupon_dt is None:
            last_coupon_dt = self.placement_date
        nkd = full_coupon * ((date - last_coupon_dt).days/period)
        return nkd
    
    def get_nkd_by_dt(self, date=datetime.now()):
        try:
            date = self._check_date(date)
        except ValueError:
            Warning('There is not coupon for this date')
            return -1

        return self._get_nkd_by_dt(date)
    
    def get_price_by_dt(self, date):
        try:
            date = self._check_date(date)
        except ValueError:
            Warning('Bond does not exist for this date')
            return -1

        return load_single_price(self.ticker, date)/100*self.nominal
    
    def about(self):
        res = {'ticker': self.ticker, 'name': self.name, 'placement_date': self.placement_date,
               'maturity_date': self.maturity_date, 'nominal': self.nominal, 'frequency': self.frequency}
        return res
    
    def get_rt_any(self, rt, days):
        rt_day = (rt+1)**(1/365)
        return rt_day**days-1
    
    def _try_ytm(self, price, ytm, date):
        coupone_df = self.coupons_df.query('dt>=@date')
        for row in coupone_df.itertuples():
            days = (row.dt-date).days # Days to next coupon
            nkd = self._get_nkd_by_dt(date) # Calculate nkd to date
            clear_coupon = row.rub_amt-nkd
            price = price*(1+self.get_rt_any(ytm, days))-clear_coupon # clear coupone + increas in bond body
            date = row.dt
        return price
    
    def calculate_ytm(self, date=pd.to_datetime('today')):
        date = self._check_date(date)

        price = self.get_price_by_dt(date)
        ytm = 0.5
        step = 0.25
        while True:
            final_price = self._try_ytm(price, ytm, date)
            #print(price, final_price, ytm)
            if abs(self.nominal-final_price)<0.001:
                return ytm

            if 1000>final_price:
                ytm+=step
            else:
                ytm-=step

            step/=2