import pathlib
from logging.handlers import RotatingFileHandler, MemoryHandler
from logging import captureWarnings, basicConfig, StreamHandler, WARNING, INFO, DEBUG, getLogger

def Logger():
    path = pathlib.Path('./Main/logger') / 'kiyo.log'
    path.parent.mkdir(parents=True, exist_ok=True)

    _LOGS = getLogger('Kiyo')
    _LOG_FMT = '%(asctime)s | %(name)s [%(levelname)s] : %(messagse)s'

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
    try:
        import coloredlogs

        coloredlogs.install(level=None, logger=_LOGS, fmt=_LOG_FMT)
    except ImportError:
        pass
    
    _LOGS.info('Initialized Logger!')

def 
