import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from plugins import tlang
from Main.utils.decorators import kiyocmd
from Main.utils.tools import get_readable_time
from Main import start_time

@kiyocmd('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    if chat.type == "private":
        return await message.reply_text(
            tlang(chat.id, 'private_start').format(
               update.effective_user.first_name, context.bot.first_name 
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await message.reply_text(
            tlang(chat.id, 'start_string').format(
                context.bot.first_name, get_readable_time(int(time.time() - start_time))
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
