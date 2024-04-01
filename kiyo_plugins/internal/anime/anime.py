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
        await message.reply_text("Format : /anime < anime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
    url = "https://graphql.anilist.co"
    anime_query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
            title {
                romaji
                native
            }
            format
            status
            episodes
            duration
            averageScore
            genres
            studios {
                nodes {
                    name
                }
            }
            siteUrl
            trailer {
                id
                site
            }
            description
            bannerImage
        }
    }
    '''
    try:
        response = requests.post(
            url, json={"query": anime_query, "variables": variables}
        )
        json_data = response.json()
        if "errors" in json_data.keys():
            await message.reply_text("Anime not found")
            return
        if json_data:
            anime_data = json_data["data"]["Media"]
            msg = f"<b>{anime_data['title']['romaji']}</b> (`{anime_data['title']['native']}`)\n\n"
            msg += f"🎥 Type: {anime_data['format']} | Status: {anime_data.get('status', 'N/A').replace('_', ' ')}\n"
            msg += f"🌟 Score: {anime_data['averageScore']} | By- {anime_data['id']}\n"
            msg += f"🔢 Episodes: {anime_data.get('episodes', 'N/A')} | {anime_data.get('duration', 'N/A')} Per Epis\n"
            msg += f"🗓 Aired: {anime_data.get('startDate', 'N/A')} - {anime_data.get('endDate', 'N/A')}\n\n"
            msg += f"🗿 Genres: "
            for genre in anime_data["genres"]:
                msg += f"{genre}, "
            msg = msg[:-2] + "\n"
            msg += f"🏢 Studios: "
            if not anime_data["studios"]["nodes"]:
                msg += "N/A"
            else:
                for studio in anime_data["studios"]["nodes"]:
                    msg += f"{studio['name']}, "
                msg = msg[:-2] + "\n"

            description = anime_data.get("description", "N/A").replace("<i>", "").replace("</i>", "").replace("<br>", "")
            msg += f"\n{description[:500]}..."
            site_url = anime_data.get("siteUrl")
            trailer = anime_data.get("trailer", None)
            if trailer and trailer["site"] == "youtube":
                trailer_url = f"https://youtu.be/{trailer['id']}"
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton("More Info", url=site_url),
                             InlineKeyboardButton("Trailer 🎬", url=trailer_url))
            else:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton("More Info", url=site_url))

            banner_image = anime_data.get("bannerImage") or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"

            try:
                await message.reply_photo(
                    photo=banner_image,
                    caption=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                )
            except:
                msg += f"\n[〽️]({banner_image})"
                await message.reply_text(
                    msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                )
        else:
            await message.reply_text("Anime not found")
    except Exception as e:
        print(e)
        await message.reply_text("An error occurred while processing the request.")

