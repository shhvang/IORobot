import time
from telegram import Update
from telegram.ext import ContextTypes

from Main.utils.decorators import kiyocmd
from Main import start_time

def get_readable_time(seconds: int) -> str:
    intervals = [(' days, ', 86400), ('h:', 3600), ('m:', 60), ('s', 1)]
    time_string = ''
    for name, count in intervals:
        value = seconds // count
        if value > 0:
            seconds -= value * count
            time_string += f'{value}{name}'

    return time_string

@kiyocmd('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        f"Hi, I'm {context.bot.first_name}\nuptime: {get_readable_time(int(time.time() - start_time))}"
    )
