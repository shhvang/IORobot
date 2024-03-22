from time import time
from Main import _config
from Main.logger import _SetupLogger
from telegram.ext import ApplicationBuilder

_SetupLogger()
start_time = time()

application = (
    ApplicationBuilder()
    .token(_config.token)
    .build()
)
