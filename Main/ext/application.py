from telegram.ext import ApplicationBuilder

Application = (
    ApplicationBuilder()
    .token(config.Token)
    .build()
)
