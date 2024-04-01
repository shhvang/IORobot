import datetime
import html
import textwrap
import json
import time
import bs4
import jikanpy
import requests
from kiyo import kiyo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode

def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:550] + "...."
        msg += f"\n*Description*: _{description}_[Read More]({info})"
    else:
        msg += f"\n*Description*: _{description}_"
    return msg


def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]

async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    search = message.text.split(" ", 1)
