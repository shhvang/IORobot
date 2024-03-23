from telegram import Update
from telegram.ext import ContextTypes

from Main.utils.decorators import kiyocmd

@kiyocmd('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(f"Hi, I'm {context.bot.first_name}")
