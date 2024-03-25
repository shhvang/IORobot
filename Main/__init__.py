import time, os
import platform

from logging import getLogger
from telegram.ext import ApplicationBuilder
from telegram import __version__

from Main.startup.database import Database
from Main import configs as config
from Main.startup import Logger

start_time = time.time()

Logger()
LOGS = getLogger('Kiyo')
LOGS.info(
    "[KIYO] Starting Development, (python: %s) - python-telegram-bot: v%s",
    platform.python_version(),
    __version__,
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
