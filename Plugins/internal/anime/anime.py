import requests, pathlib
from IO import kiyo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

url = "https://graphql.anilist.co"

def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:550] + "...."
        msg += f"\n*Description*: _{description}_[Read More]({info})"
    else:
        msg += f"\n*Description*: _{description}_"
    return msg

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
            relations {
                edges {
                    relationType
                    node {
                        title {
                            romaji
                        }
                        coverImage {
                            large
                        }
                        siteUrl
                    }
                }
            }
            openingThemes
            endingThemes
            nextAiringEpisode {
                airingAt
            }
            prevAiringEpisode {
                airingAt
            }
            nextAiringEpisode {
                timeUntilAiring
            }
            airingSchedule {
                nodes {
                    episode
                    timeUntilAiring
                }
            }
            streamingEpisodes {
                title
                url
                site
            }
            trailer {
                id
                site
            }
            officialSiteUrl
        }
    }
'''

def get_anime_results(search_query):
    variables = {
        "search": search_query
    }
    response = requests.post(url, json={"query": anime_query, "variables": variables})
    if response.status_code == 200:
        return response.json()["data"]["Media"]
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
        results = get_anime_results(search_query)
        if results:
            keyboard = []
            for anime in results:
                title = anime["title"]["romaji"]
                url = anime["siteUrl"]
                button = InlineKeyboardButton(title, callback_data=url)
                keyboard.append([button])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await message.reply_text("Here are the search results:", reply_markup=reply_markup)
        else:
            await message.reply_text("No anime found for that query.")
            

kiyo.client.add_handler(
    CommandHandler('anime', anime)
)

