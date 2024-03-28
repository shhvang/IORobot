import time
import platform

from telegram.ext import ApplicationBuilder

from Main import configs as config
from Main.lib.nicelogger import LOGS, enablelogging 
from Main.startup.database import Database

start_time = time.time()

enablelogging(level=logging.INFO, color=True)

LOGS.info(
    "Starting Development, (python: %s)", 
     platform.python_version(),
)

application = (
    ApplicationBuilder()
    .token(config.Token)
    .base_url(config.BASE_URL)
    .base_file_url(config.BASE_FILE_URL)
    .build()
)

db = Database(
        config.DATABASE_URI, db_type='postgresql', pool_size=10, max_overflow=20, debug=False
    )
