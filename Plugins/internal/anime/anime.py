import requests
from IO import kiyo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

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

async def anime(update: Update, context):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        await message.reply_text("Format : /anime < anime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
    url = "https://graphql.anilist.co"
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
    except Exception as e:
        print(f"An error occurred: {e}")

kiyo.client.add_handler(
    CommandHandler('anime', anime)
)
