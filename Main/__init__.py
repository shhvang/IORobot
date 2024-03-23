import time, os
import platform

from logging import getLogger

from Main import configs as config
from Main.startup.database import Database
from Main.startup import Logger

from telegram.ext import ApplicationBuilder
from telegram import __version__

start_time = time.time()

Logger()
LOGS = getLogger('Kiyo')
LOGS.info(
    f"Starting Development, Kiyo (python-telegram-bot: {__version__})\n",
    f"Python version - {platform.python_version()}"
)

def isLocalHost():
    return os.path.exists("./localhost.txt")

application = (
    ApplicationBuilder()
    .token(config.Token)
    .base_url(config.BaseUrl)
    .base_file_url(config.BaseFileUrl)
    .build()
)

uri = config.DATABASE_URI
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

db = Database(
        uri, db_type='postgresql', pool_size=10, max_overflow=20, debug=False
    )
