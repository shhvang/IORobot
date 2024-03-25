from typing import Optional
import Main.sql.rules_sql as sql

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    User,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, filters, CommandHandler
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
from Main.utils.string_handler import markdown_parser

from plugins import tlang
from Main import application
from Main.utils.decorators import kiyocmd, rate_limit

async def get_rules(update: Update, _: CallbackContext):
    chat_id = update.effective_chat.id
    await send_rules(update, chat_id)

async def send_rules(update: Update, chat_id, from_pm=False):
    bot = application.updater.bot
    message = update.effective_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message != "Chat not found" or not from_pm:
            raise

        await bot.send_message(
            update.effective_user.id,
            "The rules shortcut for this chat hasn't been set properly! Ask admins to "
            "fix this.\nMaybe they forgot the hyphen in ID",
        )
        return
    rules = sql.get_rules(chat_id)
    text = f"The rules for *{escape_markdown(chat.title)}* are:\n\n{rules}"

    if from_pm and rules:
        await bot.send_message(
            update.effective_user.id, text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
    elif from_pm:
        await bot.send_message(
            update.effective_user.id,
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!",
        )
    elif rules:
        btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules", url=f"t.me/{bot.username}?start={chat_id}"
                        )
                    ]
                ]
        )
        txt = "Please click the button below to see the rules."
        if not message.reply_to_message:
            await message.reply_text(txt, reply_markup=btn)

        if message.reply_to_message:
            await message.reply_to_message.reply_text(txt, reply_markup=btn)
    else:
        await update.effective_message.reply_text(
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!"
        )

@kiyocmd('setrules')
@rate_limit(40, 60)
async def set_rules(update: Update, context: CallbackContext):
  chat_id = update.effective_chat.id
  message = update.effective_message  # type: Optional[Message]
  raw_text = message.text
  args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
  if len(args) == 2:
      txt = args[1]
      offset = len(txt) - len(raw_text)  # set correct offset relative to command
      markdown_rules = markdown_parser(
          txt, entities=message.parse_entities(), offset=offset
      )

      sql.set_rules(chat_id, markdown_rules)
      await update.effective_message.reply_text("Successfully set rules for this group.")

application.add_handler(CommandHandler(get_rules, 'rules', filters=filters.ChatType.GROUPS))
