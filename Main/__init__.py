from time import time
from Main import configurations as config
from Main.logger import Logger
from telegram.ext import ApplicationBuilder

Logger()
start_time = time()

application = (
    ApplicationBuilder()
    .token(config.Token)
    .build()
)
