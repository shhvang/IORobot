import pathlib
from logging.handlers import RotatingFileHandler, MemoryHandler
from logging import captureWarnings, basicConfig, StreamHandler, WARNING, INFO, DEBUG, getLogger

def Logger():
    _LOGS = getLogger('Kiyo')
    log_path = pathlib.Path('./Main/logger/') / f'kiyo.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    captureWarnings(True)
    basicConfig(format='[%(asctime)s] - [IOpacity] << %(levelname)s >> %(name)s - %(message)s',
                datefmt='%d-%b-%y %H:%M:%S',
                handlers=[
                    RotatingFileHandler(
                        log_path, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
                    ),
                    MemoryHandler(1024 * 1024, WARNING),
                        StreamHandler(),
                    ],
                    level=INFO,
                )
    
    getLogger('sqlalchemy.engine').setLevel(WARNING)
    getLogger('psycopg2').setLevel(WARNING)
    getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(WARNING)
    getLogger('apscheduler.scheduler').setLevel(INFO)
    getLogger("httpx").setLevel(WARNING)
    
    _LOGS.info('Initialized Logger!')
