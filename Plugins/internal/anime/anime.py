import requests
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler
from IO import kiyo

def scrape_anime_results(search_query):
    url = f"https://vmdb.net/search?q={search_query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="entry-content")
        anime_list = []
        for result in results:
            title = result.find("h2", class_="entry-title").text.strip()
            description = result.find("div", class_="entry-excerpt").text.strip()
            anime_url = result.find("a")["href"]
            anime_list.append({"title": title, "description": description, "url": anime_url})
        return anime_list
    else:
        return None

async def anime(update: Update, context):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        await message.reply_text("Format : /anime < anime name >")
        return
    else:
        search_query = search[1]
        results = scrape_anime_results(search_query)
        if results:
            keyboard = []
            for anime in results:
                title = anime["title"]
                description = anime["description"]
                url = anime["url"]
                button = InlineKeyboardButton(title, callback_data=f"{title}|{description}|{url}")
                keyboard.append([button])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await message.reply_text("Here are the search results:", reply_markup=reply_markup)
        else:
            await message.reply_text("No anime found for that query.")

kiyo.client.add_handler(CommandHandler('anime', anime))
