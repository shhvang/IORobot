import requests
from IO import kiyo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler
from telegram.constants import ParseMode

def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:550] + "...."
        msg += f"{description}[Read More]({info})"
    else:
        msg += f"{description}"
    return msg

async def anime(update: Update, context):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        await update.effective_message.reply_text("Format: /anime <anime name>")
        return
    else:
        search = search[1]
    
    url = "https://graphql.anilist.co"
    anime_query = """
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
        startDate {
          year
          month
          day
        }
        endDate {
          year
          month
          day
        }
      }
    }
    """
    
    variables = {"search": search}
    response = requests.post(url, json={"query": anime_query, "variables": variables})
    json_data = response.json()
    
    if "errors" in json_data:
        await update.effective_message.reply_text("Anime not found")
        return
    
    if json_data:
        anime_data = json_data["data"]["Media"]
        title_romaji = anime_data["title"]["romaji"]
        title_native = anime_data["title"]["native"]
        anime_format = anime_data["format"]
        anime_status = anime_data.get("status", "N/A").replace('_', ' ')
        anime_episodes = anime_data.get("episodes", "N/A")
        anime_duration = anime_data.get("duration", "N/A")
        anime_score = anime_data["averageScore"]
        anime_genres = ', '.join(anime_data["genres"])
        
        studios = anime_data["studios"]["nodes"]
        studios_str = ', '.join([studio["name"] for studio in studios]) if studios else "N/A"
        
        info_url = anime_data.get("siteUrl")
        
        trailer = anime_data.get("trailer")
        trailer_url = None
        if trailer and trailer["site"] == "youtube":
            trailer_url = "https://youtu.be/" + trailer["id"]
        
        description = (
            anime_data.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        

        
        # Check if description is None or empty before trying to replace
        if description:
            description = description.replace("<i>", "").replace("</i>", "").replace("<br>", "")
        
 # Debug print
        
        img = f"https://img.anili.st/media/{anime_data.get('id')}" or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"
        
        msg = f"*{title_romaji}* (`{title_native}`)\n\n"
        msg += f"🎥 *Type:* {anime_format} | *Source:* MANGA\n"
        msg += f"📺 *Status:* {anime_status} | *NSFW:* False\n"
        msg += f"🌟 *Score:* {anime_score} | *By-:* {anime_data['id']}\n"
        msg += f"🔢 *Episodes:* {anime_episodes} | {anime_duration} Per Epis\n"
        if "startDate" in anime_data and "endDate" in anime_data:
            msg += f"🗓 *Aired:* {anime_data['startDate']['year']}/{anime_data['startDate']['month']}/{anime_data['startDate']['day']} - {anime_data['endDate']['year']}/{anime_data['endDate']['month']}/{anime_data['endDate']['day']}\n\n"
        msg += f"🗿 *Genres:* {anime_genres}\n"
        msg += f"🖋 *Authors:* Hajime Isayama, Tetsurou Araki\n"
        msg += f"🏢 *Studios:* {studios_str}\n\n"
        msg += shorten(description, info_url)
        
        if trailer_url:
            buttons = [
                [
                    InlineKeyboardButton("More Info", url=info_url),
                    InlineKeyboardButton("Trailer 🎬", url=trailer_url),
                ]
            ]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info_url)]]

        if "externalLinks" in anime_data:
            for link in anime_data["externalLinks"]:
                buttons.append([InlineKeyboardButton(link["site"], url=link["url"])])
        try:
            await update.effective_message.reply_photo(
                photo=img,
                caption=msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except:
            msg += f" [〽️]({img})"
            await update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )

kiyo.client.add_handler(
    CommandHandler('anime', anime)
)
