import matplotlib.pyplot as plt

from ..analytics.core import add_cummulative, describe_longivity


def country_to_color():
    dict_ = {
    'Russia': 'r',
    'USA': 'b',
    'Germany': 'g',
    'France': 'c',
    'Italy': 'm',
    'Spain': 'y',
    'UK': 'k',
    'Canada': 'orange',
    'Switzerland': 'brown',
    'South Korea': 'pink',
    'Japan': 'gray',
    }
    return dict_



def _plot_country(data, country_nm, ax=None, postfix='cum'):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(15,5))
    # data.set_index('dt')['_'.join([country_nm, 'inflation', postfix])].plot(label='Inflation', ax=ax)
    data.set_index('dt')['_'.join([country_nm, 'money', postfix])].plot(label='Money Market', ax=ax)
    data.set_index('dt')['_'.join([country_nm, 'stocks', postfix])].plot(label='Stocks', ax=ax)
    data.set_index('dt')['_'.join([country_nm, 'bonds', postfix])].plot(label='Bonds', ax=ax)
    data.set_index('dt')['_'.join([country_nm, 'realty', postfix])].plot(label='Realty', ax=ax)
    # data.set_index('dt')['_'.join([country_nm, 'currency', postfix])].plot(label='Currency', ax=ax)
    # ax.set_yscale('log')
    ax.set_title(f'{country_nm}')
    ax.legend()


def plot_country(data, country_nm, ax=None):
    data = data.copy()
    start = describe_longivity(data, prefix=country_nm, postfix='rt').max()['first']
    part = data.query(f'dt > "{start}"').copy()
    part = add_cummulative(part, country_nm)
    _plot_country(part, country_nm, postfix='cum', ax=ax)

def plot_all_countries(data, countries):
    rows = (len(countries)-1) // 4 + 1
    fig, ax = plt.subplots(rows, 4, figsize=(30, rows*5))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    for num, country in enumerate(countries):
        plot_country(data, country, ax=ax[num//4, num%4])

def plot_active(data, active, countries):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    for num, country in enumerate(countries):

        start = describe_longivity(data, prefix=country).max()['first']
        part = data.query(f'dt > "{start}"').copy()
        part = add_cummulative(part, country)

        part[country] = part[f'{country}_{active.lower()}_cum']
        part.set_index('dt')[[country]].plot(ax=ax, kind='line', title=active, label=country, 
                                             grid=True, color=country_to_color()[country])