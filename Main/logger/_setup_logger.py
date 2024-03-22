import logging, pathlib
from logging.handlers import RotatingFileHandler, MemoryHandler

def init_logger():
    log_path = pathlib.Path('./Main/startup/logs/') / f'kiyo.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.captureWarnings(True)
    logging.basicConfig(format='[%(asctime)s] - [Ayaka] << %(levelname)s >> %(name)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[
                            RotatingFileHandler(
                            log_path, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
                        ),
                            MemoryHandler(1024 * 1024, logging.WARNING),
                            logging.StreamHandler(),
                        ],
                        level=logging.INFO,
    
                        )
    logging.getLogger('psycopg2').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO)
    logging.getLogger('telegram.ext.Application').setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    logging.info('Initialized Logger!')
