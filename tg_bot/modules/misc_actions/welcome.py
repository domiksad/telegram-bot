# type: ignore
from typing import Callable
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, error
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from tg_bot.modules.sql.settings import * 
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_admin
from tg_bot.modules.helper_funcs.array_funcs import get_next_key, get_prev_key
from tg_bot.modules.language import get_dialog, LANG
from tg_bot import LOGGER


async def do_nothing(*_):
    None

async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str):
    await update.effective_chat.send_message(text=content)

async def send_img(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str):
    await update.effective_chat.send_photo(photo=content)

async def send_gif(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str):
    await update.effective_chat.send_animation(animation=content)

async def send_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str):
    await update.effective_chat.send_sticker(sticker=content)

TYPES_OF_MSG = {
    "none": do_nothing,
    "text": send_text,
    "img": send_img,
    "gif": send_gif,
    "sticker": send_sticker,
}

async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return
    
    settings = get_settings(update.effective_chat.id)
    welcome_message = settings["welcome_message"]

    data = json.loads(welcome_message)

    handler = TYPES_OF_MSG[data["type"]]
    if handler:
        await handler(update, context, data["content"])
    else:
        LOGGER.error(f"No handler specified: {json.dumps(data)}")