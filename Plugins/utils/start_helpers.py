from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Plugins.external.langhelpers import _

def gen_start_kb(chat=None):
    if chat:
        keyboard =  [
                        [
                            InlineKeyboardButton(
                                text=f"{_(chat.id, 'support_btn')}", 
                                url='https://t.me/IOSupportGroup'
                            ),
                            InlineKeyboardButton(
                                text=f"{_(chat.id, 'update_btn')}", 
                                url='https://t.me/IOUpdate'
                            ),
                            InlineKeyboardButton(
                                text=f"{_(chat.id, 'source_btn')}", 
                                url='https://github.com/iOpacity/rKiyoBot'
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text=f"{_(chat.id, 'inline_btn')}", 
                                switch_inline_query_current_chat=""
                            ),
                            InlineKeyboardButton(
                                text=f"{_(chat.id, 'add_btn')}", 
                                url='https://t.me/rKiyoBot?startgroup=true'
                            )
                        ]
                    ]
                
        return keyboard
