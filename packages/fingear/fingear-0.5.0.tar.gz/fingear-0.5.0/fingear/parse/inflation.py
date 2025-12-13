"""
Тут мы достаем данные по инфляции по месяцам

"""

from tqdm import tqdm
from .selenium import find_elements, click_pattern_if_exists, wait_until_page_ready, setup_driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd


def _get_link_by_country(country='russia'):
    return f'https://www.inflationtool.com/rates/{country}/historical'

def _open_page(link='https://www.inflationtool.com/rates/russia/historical', headless=False, verbose=False):
    driver = setup_driver(link, headless=headless)
    # wait for the page to load
    wait_until_page_ready(driver)
    if verbose: print('Page ready')
    # Убираем куки
    click_pattern_if_exists(driver, "ez-accept-all", 15, 'id')
    # click_pattern_if_exists(driver, "svg.w-6.h-6.text-icon", 25, 'css')
    return driver


def _parse_data(driver, verbose=True):

    res = []

    while True:

        table = driver.find_element(By.ID, "gtable3")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")
            
            if not cells:
                continue  # Пропускаем пустые строки
                
            values = [cell.text for cell in cells]
            
            if verbose: print(values)

            res.append(values)
        
        elements = driver.find_elements(By.XPATH, '//button[contains(text(), "›")]')

        # Нажатие на третий элемент
        if len(elements) >= 3:
            if elements[2].is_enabled():  # Проверяем, активна ли кнопка
                try:
                    elements[2].click()  # третий элемент в списке        
                except ElementClickInterceptedException:
                    break
            else: 
                break
        else:
            break
    return res


def _process_data(data):
    df = pd.DataFrame(data)
    # Берем название колонок из первой строки таблицы
    df.columns = df.iloc[0]
    # Удаляем строки с названием колонок
    df.query('Year!="Year"', inplace=True)
    # Делаем колонки нормальными
    df.columns = list(map(lambda x: x.strip().lower(), df.columns))
    # Убираем ненужные столбцы и пропуски заполняем, чтобы потом эти значения заполнить
    df = df.drop(columns=['avg.']).fillna('')
    # Превращаем во временной ряд
    df = df.melt(id_vars=['year'], var_name='month', value_name='inflation')
    # Делаем нормальную дату
    df['dt'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'], format='%Y-%b')
    del df['month'], df['year']
    # Верный порядок дат
    df.sort_values('dt', inplace=True)
    df.reset_index(drop=True, inplace=True)
    # Меняем тип данных и обрабатываем пропуски
    df['inflation'] = df['inflation'].replace('', 'NaN').astype(float)
    return df

def parse_inflation(country='russia',
                    verbose=False, headless=False):
    link = _get_link_by_country(country)
    driver = _open_page(link=link, headless=headless, verbose=verbose)
    data = _parse_data(driver=driver, verbose=verbose)
    df = _process_data(data)
    return df

