import time

from . import (
    db,
    application,
    LOGS,
    start_time,
    config,
)

from Main.langs import setup_localization
from Main.utils.decorators import kiyocmd
from telegram import Update
from telegram.ext import ContextTypes

@kiyocmd('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(f"Hi, I'm {context.bot.first_name}")
    

def main():
    setup_localization()
    LOGS.info('[KIYO] Started Using long polling.')
    application.run_polling()

if __name__ == '__main__':
    main()
