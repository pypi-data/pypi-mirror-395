import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm

from ..sql.cbonds import CompanyRawData, CompanyInfoData
from ..sql import get_session
from ..settings import construct_path


def parse_company_by_id(id):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    url = f"https://cbonds.ru/company/{id}/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"No company: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        # Ищем строку, содержащую нашу переменную
        pattern = r'var\s+graphStocksList\s*=\s*(.*?);'
        match = re.search(pattern, str(script_tag.string))
        if match:
            # Преобразуем найденную строку в объект Python
            data_json = match.group(1)
            data = json.loads(data_json)
            break
    else:
        raise ValueError("Variable 'graphStocksList' was not found on the page.")
    
    if not data:
        raise ValueError(f"No stock.")

    return data, response.text

def save_company_html_text(text, company_id):
    path = f'cbonds/company/{company_id}.txt'
    path = construct_path(path)
    with open(path, 'w') as file:
        file.write(text)
    return path


def parse_all_companies(start=20000, end=30000, verbose=False):
    session = get_session()
    company_ids = range(start, end)
    skipped_cnt, failed_cnt, successful_cnt, status = 0, 0, 0, ''
    for company_id in (pbar := tqdm(company_ids, desc=f"Progress (Success: {successful_cnt} / Fail: {failed_cnt}) / Skip: {skipped_cnt}", unit="company")):
        pbar.set_description(f"Качаем отчеты (Success: {successful_cnt} / Fail: {failed_cnt} / Skip: {skipped_cnt}). Last status ({company_id}): {status}")
        if CompanyRawData.get_by_id(session, company_id):
            if verbose: print(f'Company {company_id} is already in table')
            skipped_cnt+=1
            status='Skipped'
            continue
        try:
            data, text = parse_company_by_id(company_id)
            path = save_company_html_text(text, company_id)
            data = CompanyRawData(
                id_company=company_id,
                data=json.dumps(data),
                status='OK',
                file_path=path
            )
            data.add(session)
            if verbose: print(f'Company {company_id} has been saved.')
            successful_cnt+=1
            status='OK'
        except ValueError as e:
            data = CompanyRawData(
                id_company=company_id,
                data=None,
                status=str(e),
                file_path='/path/to/sample/data.json',
                success_flg=False
            )
            data.add(session)
            if verbose: print(f'Company {company_id} error: {e}')
            failed_cnt+=1
            status = str(e)


def process_companies_raw_data():
    session = get_session()
    CompanyInfoData.truncate_table(session)

    df = CompanyRawData.get_successful_records(session)
    for num, row in df.iterrows():
        data = json.loads(row['data'])[0]
        id_company = row['id_company']
        name = data.get('entity_name', None)
        ticker = data.get('ticker', None)
        url = data.get('url', None)
        isin = data.get('isin', None)
        currency_name = data.get('currency_name', '')

        sql_data = CompanyInfoData(
                    id_company=id_company,
                    name=name,
                    ticker=ticker,
                    url=url,
                    isin=isin,
                    currency_name=currency_name
                )
        sql_data.add(session)