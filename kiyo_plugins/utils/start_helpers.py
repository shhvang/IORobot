from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from kiyo_plugins.external.langhelpers import tlang

def gen_start_kb(chat=None):
    if chat:
        keyboard =  [
                        [
                            InlineKeyboardButton(
                                text=f"{tlang(chat.id, 'support_btn')}", 
                                url='https://t.me/IOSupportGroup'
                            ),
                            InlineKeyboardButton(
                                text=f"{tlang(chat.id, 'update_btn')}", 
                                url='https://t.me/IOUpdate'
                            ),
                            InlineKeyboardButton(
                                text=f"{tlang(chat.id, 'source_btn')}", 
                                url='https://github.com/iOpacity/rKiyoBot'
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"{tlang(chat.id, 'inline_btn')}", 
                                switch_inline_query_current_chat=""
                            ),
                            InlineKeyboardButton(
                                text=f"{tlang(chat.id, 'add_btn')}", 
                                url='https://t.me/rKiyoBot?startgroup=true'
                            )
                        ]
                    ]
                
        return keyboard
