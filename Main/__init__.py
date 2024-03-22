from time import time
from Main import _config
from Main.logger import Logger
from telegram.ext import ApplicationBuilder

Logger()
start_time = time()

application = (
    ApplicationBuilder()
    .token(_config.token)
    .build()
)
