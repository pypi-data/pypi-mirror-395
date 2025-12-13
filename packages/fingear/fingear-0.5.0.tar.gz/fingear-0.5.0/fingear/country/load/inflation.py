
from ...parse.inflation import parse_inflation, _open_page
# from .configs import _get_country_to_inflation

import numpy as np
import matplotlib.pyplot as plt

def prepare_inflation(country, start, end, headless=True, verbose=False):
    # Legacy
    inflation = parse_inflation(country=country.lower(), verbose=verbose, headless=headless)
    inflation = inflation.query('dt>=@start and dt<=@end').copy().reset_index(drop=True)
    inflation['inflation_month'] = inflation['inflation'].fillna(0) / 100
    inflation['inflation_cum'] = np.exp(inflation['inflation_month'].cumsum())
    inflation = inflation[['dt', 'inflation_month', 'inflation_cum']]
    return inflation


def plot_inflation(inflation):
    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    inflation.set_index('dt')['inflation_cum'].plot(ax=ax[0], title='Cumulative Inflation', color='red')
    inflation.set_index('dt')['inflation_month'].plot(ax=ax[1], title='Monthly Inflation', color='green')
    ax[0].set_yscale('log')
