import pathlib, os, configparser
from logging.handlers import RotatingFileHandler, MemoryHandler
from logging import captureWarnings, basicConfig, StreamHandler, WARNING, INFO, DEBUG, getLogger
from colorama import init, Fore, Style

def Logger():
    path = pathlib.Path('./Main/logger') / 'kiyo.log'
    path.parent.mkdir(parents=True, exist_ok=True)

    _LOGS = getLogger(__name__)
    _LOG_FMT = f'{Fore.GREEN}%(asctime)s{Style.RESET_ALL} | {Fore.CYAN}%(name)s{Style.RESET_ALL} [{Fore.YELLOW}%(levelname)s{Style.RESET_ALL}] : %(message)s'

    getLogger('sqlalchemy.engine').setLevel(WARNING)
    getLogger('psycopg2').setLevel(WARNING)
    getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(WARNING)
    getLogger('apscheduler.scheduler').setLevel(INFO)
    getLogger("httpx").setLevel(WARNING)
    captureWarnings(True)
    
    
    basicConfig(format=_LOG_FMT,
                datefmt='%d-%b-%y %H:%M:%S',
                handlers=[
                    RotatingFileHandler(
                        path, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
                    ),
                    MemoryHandler(1024 * 1024, WARNING),
                        StreamHandler(),
                    ],
                    level=INFO,
                )
    
    init(autoreset=True)
    _LOGS.info('Initialized Logger!')

def isLocalHost():
    return os.path.exists("./localhost.txt")

def get_config(key, fallback=None, cast_func=str):
    config = configparser.ConfigParser()
    config.read("config.ini")
    value = os.getenv(key)
    if value is not None:
        return cast_func(value)

    if config.has_option("kiyo", key):
        return cast_func(config.get("kiyo", key))

    return fallback
