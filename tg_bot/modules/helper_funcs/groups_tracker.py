from functools import wraps

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, error
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from tg_bot.modules.sql.groups_tracker import add_group


def track_group(func):
    @wraps(func)
    async def track(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat and update.effective_chat.type != "private": # ignore private chats
            add_group(update.effective_chat.id)
        return await func(update, context, *args, **kwargs)
    return track