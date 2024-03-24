import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from plugins import tlang
from Main.utils.decorators import kiyocmd
from Main.utils.string_handlers import get_readable_time
from Main import start_time

@kiyocmd('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    if chat.type == "private":
        return await message.reply_video(
            video='https://i.imgur.com/wf7DcAh.mp4',
            caption=tlang(chat.id, 'private_start').format(
               update.effective_user.first_name, context.bot.first_name, 
               get_readable_time(int(time.time() - start_time))
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        f'{(tlang(chat.id, 'support_btn'))}', 
                        url='https://t.me/AyakaSupport'
                    ),
                    InlineKeyboardButton(
                        f'{(tlang(chat.id, 'update_btn'))}', 
                        url='https://t.me/AyakaUpdates'
                    ),
                    InlineKeyboardButton(
                        f'{((tlang(chat.id, 'source_btn')))}', 
                        url='https://github.com/iOpacity/rKiyoBot'
                    )
                ],
                [
                    InlineKeyboardButton(
                        f'{(tlang(chat.id, 'inline_btn'))}', 
                        switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        f'{(tlang(chat.id, 'add_btn'))}', 
                        url='https://t.me/ayaka_robot?startgroup=true'
                    )
                ]
            ]
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
