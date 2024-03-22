import time
from Main import Configurations as config
from Main.logger import Logger
from telegram.ext import ApplicationBuilder

Logger()
starttime = time.time()

application = (
    ApplicationBuilder()
    .token(config.Token)
    .base_url(config.BaseUrl)
    .base_file_url(config.BaseFileUrl)
    .build()
)
