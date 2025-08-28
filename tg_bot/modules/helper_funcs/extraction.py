from typing import Optional
from functools import wraps
import time
import re

from telegram import Update, User, Message, ChatMember
from telegram.ext import ContextTypes

from tg_bot.modules.language import get_dialog
from tg_bot.modules.sql.settings import get_chat_language
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_can_restrict, is_user_admin, bot_can_restrict
from tg_bot import LOGGER

def user_from_reply(effective_message: Message) -> Optional[User]:
    reply = effective_message.reply_to_message
    if reply and reply.from_user:
        return reply.from_user
    return None
    

async def extract_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message is None or update.effective_chat is None:
        return
    target_user = user_from_reply(update.effective_message)

    if target_user:
        return await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
    
    if context.args:
        arg = context.args[0]

        try:
            user_id = int(arg)
            return await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        except ValueError:
            pass

        entity = update.effective_message.entities[1]
        if entity.user:
            return await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=entity.user.id)

        if arg.startswith("@"): # Mention (mention by @)
            username = arg[1:]
            if username == context.bot.username: # Check if bot is the target
                return await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=context.bot.id)
            
            # Cant get other users by @user
            # try:
            #     target_user_chat = await context.bot.get_chat(arg) # Its not bot. Try to find user
            # except Exception:
            #     return None
            # if target_user_chat.type == "private": # Idk how it could not be private chat but better be sure
            #     return await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=target_user_chat.id) # When chat.type is "private" then chat.id == user.id
        

    return None

async def fetch_target_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[tuple[int, ChatMember]]:
    if update.effective_chat is None or update.effective_message is None:
        return None
    
    chat_id = update.effective_chat.id
    bot_id = context.bot.id
    target_user = await extract_user(update=update, context=context)

    if target_user is None:
        await update.effective_message.reply_text(text=get_dialog("NO_USER_TARGET", chat_id))
        return None

    if target_user.user.id == bot_id:
        await update.effective_message.reply_text(text=get_dialog("CANT_RESTRICT_MYSELF", chat_id))
        return None

    if await is_user_admin(chat=update.effective_chat, user_id=target_user.user.id, member=target_user):
        await update.effective_message.reply_text(text=get_dialog("CANT_RESTRICT_ADMINS", chat_id))
        return None
    
    return chat_id, target_user

async def extract_time(message: Message, args: str):
    if not args:
        await message.reply_text(get_dialog("SPECIFY_TIME", message.chat.id))
        return None, None
    
    matches = re.findall(r"(\d+)([mhd])", args)
    if not matches:
        await message.reply_text(get_dialog("INVALID_TIME", message.chat.id))
        return None, None

    total_seconds = 0
    parts = []
    for amount, unit in matches:
        amount = int(amount)
        if unit == "d":
            total_seconds += amount * 24 * 60 * 60
            parts.append(f"{amount} day{'s' if amount != 1 else ''}")
        elif unit == "h":
            total_seconds += amount * 60 * 60
            parts.append(f"{amount} hour{'s' if amount != 1 else ''}")
        elif unit == "m":
            total_seconds += amount * 60
            parts.append(f"{amount} minute{'s' if amount != 1 else ''}")

    if total_seconds == 0:
        await message.reply_text(get_dialog("TIME_GREATER_THAN_ZERO", message.chat.id))
        return None, None

    until_date = int(time.time() + total_seconds)
    pretty = ", ".join(parts)

    return until_date, pretty
