

def config():
    data = [
        #  - Interest rate Long Term <01> ES Monthly 156N
        # IRLTLT01{CA}M156N - 10 years
        # INTGST{ES}M193N - Трежари / Interest Rates, Government Securities, Treasury Bills
        # IRSTCI01{ES}M156N - Денежный рынок / Interest Rates: Immediate Rates (< 24 Hours): Call Money/Interbank Rate:
        # IR3TIB01{ES}M156N - 3 месяца / Interest Rates: 3-Month
        # CCUSMA02{FR}M618N - Currency Conversions: US Dollar Exchange Rate Average 02 France Montly 618N -- Важно! Тут средний доход, по хорошему нужно брать последнее значение - это CCUSSP02RUM650N, но там лаг - 2 года

        # Q{BR}N628BIS - Residential Property Prices for Russian Federation
        # CPALTT01{RU}M657N - CPI

        # PNICKUSDM - Никель
        # PALUMUSDM - Алюминии
        # PURANUSDM - Уран
        # PCOPPUSDM - Copper
        # PWHEAMTUSDM - Пшеница
        ['Canada', 'CAD', 'EWC', 'CA'],
        ['Russia', 'RUB', 'ERUS', 'RU'],
        ['USA', 'USD', 'SPY', 'US'],
        ['UK', 'GBP', 'EWU', 'GB'],
        ['Germany', 'EUR', 'EWG', 'DE'],
        # ['France', 'EUR', 'EWQ', 'FR'],
        # ['Spain', 'EUR', 'EWS', 'ES'],
        # ['Italy', 'EUR', 'EWI', 'IT'],
        ['Japan', 'JPY', 'EWJ', 'JP'],
        # ['China', 'CNY', 'MCHI', 'CN'],
        # ['Brazil', 'BRL', 'EWZ', 'BR'],
        ['South Korea', 'KRW', 'EWY', 'KR'],
        # ['Australia', 'AUD', 'EWA', 'AU'],

        ['India', 'INR', 'INDA', 'IN'],
        
        
        # ['Portugal', 'EUR', 'PGAL'],
        ['Switzerland', 'CHF', 'EWL', 'CH'],
        # ['Belgium', 'EUR', 'EWK'],
        # ['Netherlands', 'EUR', 'EWN'],
        # ['Sweden', 'SEK', 'EWD'],
        # ['Denmark', 'DKK', 'EDEN'],
        # ['Norway', 'NOK', 'NORW'],
        # ['Finland', 'EUR', 'EFNL'],
        # ['Ireland', 'EUR', 'EIRL'],
        # ['Austria', 'EUR', 'EWO'],
        # ['Poland', 'PLN', 'EPOL'],
        # # ['Hungary', 'HUF', 'EHUN'], MIHU00000PHU
        # # ['Czech Republic', 'CZK', 'ECZE'] MICZ00000PCZ
        # ['Greece', 'UER', 'GREK'],

        # 
        # ['China', 'CNY', 'MCHI'],
        # ['South Korea', 'KRW', 'EWY'],
        # ['Taiwan', 'TWD', 'EWT'],
        # ['Mexico', 'MXN', 'EWW'],

        # ['Chile', 'CLP', 'ECH'],
        # ['Israel', 'ILS', 'EIS'],
        # ['Singapore', 'SGD', 'EWS'],
        # ['Argentina', 'ARS', 'ARGT'],
        # ['Saudi Arabia', 'SAR', 'KSA'],
        # ['Hong Kong', 'HKD', 'EWH'],
        # ['Vietnam', 'VND', 'VNM'], # ?
    ]
    return data

def get_full_country():
    res = ['Russia', 'Canada', 'USA', 'UK', 'Germany', 'Japan', 'South Korea', 'Switzerland'] #'France', 'Spain', 'Italy'
    return res

def _get_country_to_rate():
    return {i[0]: i[1] for i in config()} 


def _get_country_to_stocks():
    return {i[0]: i[2] for i in config()}


def _get_country_to_indexes():
    return {i[0]: i[3] for i in config()}


def _get_country_index():
    dict_ = {
        '10_year_bond': lambda x: f'IRLTLT01{x}M156N',
        'consumer_price_index': lambda x: f'CPALTT01{x}M657N',
        'money_market': lambda x: f'IRSTCI01{x}M156N',
        'currency <avg period | M>': lambda x: f'CCUSMA02{x}M618N',
        'currency <end period | M>': lambda x: f'CCUSSP01{x}M650N',
        'currency <end period | M> 2': lambda x: f'CCUSSP02{x}M650N',
        'realty_nominal': lambda x: f'Q{x}N628BIS',
    }
    return dict_
    

def _get_general_index():
    dict_ = {
        'gold': 'IQ12260',
        'nickel': 'PNICKUSDM',
        'aluminium': 'PALUMUSDM',
        'uran': 'PURANUSDM',
        'copper': 'PCOPPUSDM',
        'wheat': 'PWHEAMTUSDM',
    }
    return dict_

def _get_general_futures():
    dict_ = {
        'gold': 'GC',
        'silver': 'SI',
        'platinum': 'PL',
        'copper': 'HG',
        'palladium': 'PA',
        'oil': 'CL',
        'gas': 'NG',
        'wheat': 'KE',
    }
    return dict_


def _get_indicators():
    return ['inflation', 'money', 'stocks', 'bonds', 'realty']