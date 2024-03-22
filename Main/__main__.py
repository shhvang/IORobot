from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

import logging
from . import application

txt = '''
Hey *{}*!, 
I'm *{}* An Unofficial Ex Girlfriend of @CustomUser.

I'm here to assist you and make your chat experience enjoyable! 
Click Help button to find out more about how to use me to my full potential.
━━━━━━━━━━━━━━━━━━━━━━━━
⋟ **Uptime:** 

If you have any questions, need assistance with something, or just want to have a friendly chat, don't hesitate to reach out.
'''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_video(
            video='https://i.imgur.com/BHZ1DPK.mp4', 
            caption=txt.format(update.effective_user.first_name, context.bot.first_name),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.effective_message.reply_text(f"Hi, I'm {context.bot.first_name}")

def main():
    application.add_handler(CommandHandler('start', start))
    logging.info('Successfully started!')
    application.run_polling()
    

if __name__ == '__main__':
    main()
    
