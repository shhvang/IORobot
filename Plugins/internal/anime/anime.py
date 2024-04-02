import requests
from IO import kiyo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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

async def anime(update: Update, context):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        await message.reply_text("Format : /anime < anime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
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
    try:
        response = requests.post(
            url, json={"query": anime_query, "variables": variables}
        )
        json_data = response.json()
        if "errors" in json_data.keys():
            await message.reply_text("Anime not found or an error occurred.")
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

            # Adding Callback Buttons for Opening and Ending Themes
            op_themes = anime_data.get("openingThemes", [])
            ed_themes = anime_data.get("endingThemes", [])
            if op_themes:
                op_buttons = [InlineKeyboardButton(f"OP {i+1}", callback_data=f"op_{i}") for i in range(len(op_themes))]
                keyboard.row(*op_buttons)
            if ed_themes:
                ed_buttons = [InlineKeyboardButton(f"ED {i+1}", callback_data=f"ed_{i}") for i in range(len(ed_themes))]
                keyboard.row(*ed_buttons)

            # Adding Callback Buttons for Sequel and Prequel
            sequel = anime_data.get("sequel", {}).get("nodes", [])
            if sequel:
                sequel_buttons = [InlineKeyboardButton(f"Sequel: {node['title']['romaji']}", url=node['siteUrl']) for node in sequel]
                keyboard.row(*sequel_buttons)

            prequel = anime_data.get("prequel", {}).get("nodes", [])
            if prequel:
                prequel_buttons = [InlineKeyboardButton(f"Prequel: {node['title']['romaji']}", url=node['siteUrl']) for node in prequel]
                keyboard.row(*prequel_buttons)

            # Adding Streaming Platforms Buttons
            streaming_sites = anime_data.get("streamingEpisodes", [])
            for site in streaming_sites:
                streaming_button = InlineKeyboardButton(f"{site['site']}", url=site['url'])
                keyboard.row(streaming_button)

            # Adding Official Site Button
            official_site = anime_data.get("officialSiteUrl")
            if official_site:
                official_site_button = InlineKeyboardButton("Official Site", url=official_site)
                keyboard.row(official_site_button)

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

kiyo.client.add_handler(
    CommandHandler('anime', anime)
)
