import time
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode

from kiyo import kiyo

def get_readable_time(seconds: int) -> str:
    intervals = [(' days, ', 86400), ('h:', 3600), ('m:', 60), ('s', 1)]
    time_string = ''
    for name, count in intervals:
        value = seconds // count
        if value > 0:
            seconds -= value * count
            time_string += f'{value}{name}'

    return time_string

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    await message.reply_text(
        "Hi, I'm {}\nuptime: `{}`".format(
            context.bot.first_name, get_readable_time(int(time.time() - kiyo.startTime))
        ),
        parse_mode=ParseMode.MARKDOWN,
        )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    start = datetime.now()
    ass = await message.reply_text("Pong!")
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await ass.edit_text(f"Pong!\n`{m_s}ms`", parse_mode=ParseMode.MARKDOWN)


kiyo.client.add_handler(CommandHandler('start', start))
kiyo.client.add_handler(CommandHandler('ping', ping))
