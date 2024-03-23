import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from plugins import tlang
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
    if update.effective_chat.type == "private":
        return await update.effective_message.reply_text(
            tlang(update.effective_chat.id, 'private_start').format(
               update.effective_user.first_name, context.bot.first_name 
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await update.effective_message.reply_text(
            tlang(update.effective_chat.id, 'start_string').format(
                context.bot.first_name, get_readable_time(int(time.time() - start_time))
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
