import os
import warnings
import pathlib
from dotenv import load_dotenv, find_dotenv, set_key
from tinkoff.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX 

def local_package_path(s: str) -> str:
    """Получения пути внутри пакета из локального пути. Нужно для работы с файлами конфигурации и сохраненными моделями."""
    return os.path.join(os.path.dirname(__file__), s)


def construct_path(s):
    path = pathlib.Path(local_package_path(s))
    path.mkdir(parents=True, exist_ok=True)
    return local_package_path(s)

def config():
    ans = {
        'sql_path': 'sqlite:///db.db'
    }
    return ans

def _get_env_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))

def _init_env():
    """Создает файл .env, если он не существует."""
    config_path = _get_env_path()
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            pass


def _write_env_variable(key, value):
    """Записывает переменную в файл .env.  Проверяет на дубликаты."""
    _init_env()
    config_path = _get_env_path()
    try:
        dotenv_path = find_dotenv(config_path) # пытаемся найти файл с помощью dotenv.find_dotenv
        if dotenv_path:
            set_key(dotenv_path, key, value)
        else:
            _init_env()

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при записи в .env: {e}")
        return False
    return True


def _read_env_variable(key):
    """Читает переменную из файла .env."""
    config_path = _get_env_path()
    try:
        load_dotenv(dotenv_path=config_path)
        value = os.getenv(key)
        if value is None:
            warnings.warn(f"Пустое значение ключа {_key_to_variable(key)}. Возможно, вам стоит его задать через set_variable")
        return value
    except Exception as e:
        raise f"Ошибка при чтении ключа {_key_to_variable(key)}. Возможно, вам стоит его задать через set_variable"




def _get_t_token():
    token = _read_env_variable('fingear_tinkoff_token')
    return token

def _set_t_token(value):
    _write_env_variable('fingear_tinkoff_token', value)


def _get_t_target():
    mode = _read_env_variable('fingear_tinkoff_target')
    if mode == 'real':
        return INVEST_GRPC_API
    elif mode == 'sandbox':
        return INVEST_GRPC_API_SANDBOX
    else:
        return INVEST_GRPC_API
    
def _set_t_target(value):
    _write_env_variable('fingear_tinkoff_target', value)


def _key_to_variable(key):
    dict_ = {'fingear_tinkoff_token': 'T-TOKEN',
            'fingear_tinkoff_target': 'T-TARGET'}
    return dict[key]

def get_variable(name):
    """
    One of ['T-TOKEN', 'T-TARGET']
    """
    if name == 'T-TOKEN':
        return _get_t_token()
    if name == 'T-TARGET':
        return _get_t_target()
    

def set_variable(name, value):
    """
    One of ['T-TOKEN', 'T-TARGET']
    """
    if name == 'T-TOKEN':
        return _set_t_token(value)
    if name == 'T-TARGET':
        return _set_t_target(value)