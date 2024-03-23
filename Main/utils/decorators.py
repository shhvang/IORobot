import time, logging
from cachetools import LRUCache
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, CallbackContext, filters, ContextTypes
from telegram.ext.filters import BaseFilter
from Main import application
from Main import config

from typing import Callable, Optional

log = logging.getLogger(__name__)
user_history_cache = LRUCache(maxsize=1000) 

def rate_limit(messages_per_window: int, window_seconds: int):
    def decorator(func):
        async def wrapper(update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            current_time = time.time()

            message_history = user_history_cache[user_id] if user_id in user_history_cache else []
            message_history = [t for t in message_history if current_time - t <= window_seconds]

            if len(message_history) >= messages_per_window:
                log.info(f"Rate limit exceeded for user {user_id}. Allowed {messages_per_window} updates in {window_seconds} seconds.")
                return

            message_history.append(current_time)
            user_history_cache[user_id] = message_history

            await func(update, context)
        return wrapper
    return decorator

def kiyocmd(command):
    def decorator(func):
        handler = CommandHandler(command, func)
        application.add_handler(handler)
        return func
    return decorator

def kiyocallback(pattern: str = None) -> Callable:
    def decorator(func):
        async def wrapper(update: Update, context: CallbackContext):
            application.add_handler(CallbackQueryHandler(pattern=pattern, callback=func))
            return await func(update, context)
        return wrapper
    return decorator

def kiyoinlinequery(pattern: str = None) -> Callable:
    def decorator(func):
        async def wrapper(update: Update, context: CallbackContext):
            application.add_handler(InlineQueryHandler(pattern=pattern, callback=func))
            return await func(update, context)
        return wrapper
    return decorator
