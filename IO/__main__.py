from IO import kiyo, logger
from telegram.constants import ParseMode
from telegram.error import BadRequest, Unauthorized

SUPPORT_CHAT = -1002146661683

def send_boot_message():
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
            try:
                kiyo.client.send_photo(
                    chat_id=f"@{SUPPORT_CHAT}",
                    photo="https://telegra.ph/file/26ef5a0b523c9a52977ad.jpg",
                    caption=f"⚡ Successfully Rebooted",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except Unauthorized:
                logger.warning(
                    f"Bot is unable to send message to @{SUPPORT_CHAT}, go and check!"
                )
            except BadRequest as e:
                logger.warning(e.message)

if __name__ == "__main__":
    kiyo.run()
    send_boot_message()