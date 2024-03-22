import time
from Main import Configurations as config
from Main.logger import Logger
from telegram.ext import ApplicationBuilder

Logger()
starttime = time.time()

application = (
    ApplicationBuilder()
    .token(config.Token)
    .build()
)
