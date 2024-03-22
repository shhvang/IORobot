from time import time
from Main import _config
from Main._logger import init_logger
from telegram.ext import ApplicationBuilder

init_logger()
start_time = time()

application = (
    ApplicationBuilder()
    .token(_config.token)
    .build()
)