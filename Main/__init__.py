from time import time
from Main import _config
from Main.logger._setup_logger import _setup_logger

from telegram.ext import ApplicationBuilder

_setup_logger()
start_time = time()

application = (
    ApplicationBuilder()
    .token(_config.token)
    .build()
)
