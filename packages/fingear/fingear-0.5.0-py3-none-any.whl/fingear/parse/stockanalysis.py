from tqdm import tqdm
from .selenium import find_elements, click_pattern_if_exists, wait_until_page_ready, setup_driver
from selenium.webdriver.common.by import By
import pandas as pd
import time


def open_page(link='https://stockanalysis.com/list/biggest-companies/'):
    driver = setup_driver(link)
    # wait for the page to load
    wait_until_page_ready(driver)
    print('Page ready')
    # Убираем рекламку
    click_pattern_if_exists(driver, "svg.w-6.h-6.text-icon", 25, 'css')
    return driver

def parse_one_page(driver, verbose=True):
    table_xpath = '//*[@id="main-table-wrap"]'
    rows = find_elements(driver, f"{table_xpath}//tr", by='xpath')

    # Создать пустой список для хранения тикеров
    tickers = []

    # Проход по каждой строке таблицы
    for row in tqdm(rows, desc="Считывание тикеров", unit="тикер", disable=not verbose):
        cells = row.find_elements(By.TAG_NAME, "td")  # находим все ячейки в строке
        if not len(cells):
            continue
        ticker = cells[1].find_element(By.TAG_NAME, "a").text  # получаем текст ссылки (тиккер)
        name = cells[2].text
        market_cap = cells[3].text
        stock_price = cells[4].text
        revenue = cells[6].text
        tickers.append([ticker, name, market_cap, stock_price,revenue])  # добавляем тиккер в список
    tickers = pd.DataFrame(tickers, columns=['ticker', 'name', 'market_cap', 'stock_price', 'revenue'])
    return tickers

def click_next_page(driver):
    # Найти все кнопки с классом .controls-btn
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.controls-btn")
    for button in buttons:
        if "Next" in button.text:
            if button.is_enabled():  # Проверяем, активна ли кнопка
                button.click()
                return True
            else:
                return False
    return False


def parse_all_tickers(driver, verbose=True):
    page_num = 1
    df_res = pd.DataFrame()
    while True:
        if verbose: print(f'Считывание страницы {page_num}')
        df = parse_one_page(driver, verbose=verbose)
        df_res = pd.concat([df_res, df])
        if verbose: print(f'Было считано {len(df)} тикеров | Итого: {len(df_res)}')

        if not click_next_page(driver):
            if verbose: print('Все страницы прочитаны!')
            break
        page_num += 1
        time.sleep(2)
        wait_until_page_ready(driver, 10)
    return df_res