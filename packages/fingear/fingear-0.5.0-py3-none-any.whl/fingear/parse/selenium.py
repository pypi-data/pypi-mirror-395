from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


def setup_driver(link, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    return driver

def transform_by(by):
    rules = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'class': By.CLASS_NAME, 'id': By.ID, 'tag': By.TAG_NAME}
    try:
        return rules[by]
    except KeyError:
        raise ValueError(f"Invalid locator strategy '{by}'. Must be one of: {', '.join(rules.keys())}")

def find_element_clickable(driver, pattern, wait=10, by='css'):
    return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((transform_by(by), pattern)))

def find_element(driver, pattern, wait=10, by='css'):
    return WebDriverWait(driver, wait).until(EC.presence_of_element_located((transform_by(by), pattern)))

def find_elements(driver, pattern, wait=10, by='css'):
    return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((transform_by(by), pattern)))

def click_pattern(driver, pattern, wait=10, by='css'):
    find_element_clickable(driver, pattern, wait, by).click()

def click_pattern_if_exists(driver, pattern, wait=0.5, by='css'):
    try:
        click_pattern(driver, pattern, wait, by)
    except TimeoutException:
        pass

def send_keys_pattern(driver, pattern, text, wait=10, by='css'):
    find_element_clickable(driver, pattern, wait, by).send_keys(text)

def execute_action(driver, action_list):
    actions = ActionChains(driver)
    for action in action_list:
        actions.send_keys(action)
        actions.perform()

def wait_until_page_ready(driver, wait=10):
    WebDriverWait(driver, wait).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

