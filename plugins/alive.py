from plugins.systool import get_readable_time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from plugins import tlang
from Main.utils.decorators import kiyocmd
from Main import start_time

alive_button = [ nvm

]

@kiyocmd('alive')
async def alive(update: Update, context: ContextTypes.DEFAULTYPE):
    return update.effective_message.reply_text(
        tlang(update.effective_chat.id, 'alive_string').format(
            context.bot.first_name, get_readable_time(int(time.time() - start_time))
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
