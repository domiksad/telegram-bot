from typing import Optional
from functools import wraps

from telegram import Update, ChatMember, Chat, constants
from telegram.ext import ContextTypes

from tg_bot.modules.language import get_dialog


# Functions
async def is_bot_admin(chat: Chat, bot_id: int, bot_member: Optional[ChatMember] = None) -> bool:
    if chat.type == 'private':
        return True

    if bot_member is None:
        bot_member = await chat.get_member(bot_id)
    return bot_member.status in ['administrator', 'creator']

async def is_user_admin(chat: Chat, user_id: int, member: Optional[ChatMember] = None) -> bool:
    if chat.type == 'private':
        return True
    
    if member is None:
        member = await chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

async def can_restrict(chat: Chat, user_id: int, member: Optional[ChatMember] = None) -> bool:
    if chat.type == 'private':
        return False # Cant restrict in DMs
    
    if member is None:
        member = await chat.get_member(user_id)
    return member.status == "creator" or (member.status == "administrator" and getattr(member, "can_restrict_members", False))

async def is_in_chat(chat: Chat, user_id: int) -> bool:
    member = await chat.get_member(user_id=user_id)
    return member.status not in [constants.ChatMemberStatus.LEFT, constants.ChatMemberStatus.BANNED]

# Decorators
def bot_admin(func):
    @wraps(func)
    async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat is None or update.effective_message is None:
            return
        
        if await is_bot_admin(update.effective_chat, context.bot.id):
            return await func(update, context, *args, **kwargs)
        else:
            await update.effective_message.reply_text(get_dialog("BOT_IS_NOT_AN_ADMIN", chat_id=update.effective_chat.id))

    return is_admin

def bot_can_restrict(func):
    @wraps(func)
    async def bot_restrict(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat is None or update.effective_message is None:
            return
        
        if await can_restrict(update.effective_chat, context.bot.id):
            return await func(update, context, *args, **kwargs)
        else:
            await update.effective_message.reply_text(get_dialog("BOT_CANT_RESTRICT", chat_id=update.effective_chat.id))

    return bot_restrict

def user_admin(func):
    @wraps(func)
    async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat is None or update.effective_message is None:
            return
        
        if await is_user_admin(update.effective_chat, context.bot.id):
            return await func(update, context, *args, **kwargs)
        else:
            await update.effective_message.reply_text(get_dialog("USER_IS_NOT_AN_ADMIN", chat_id=update.effective_chat.id))

    return is_admin

def user_can_restrict(func):
    @wraps(func)
    async def bot_restrict(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat is None or update.effective_message is None or update.effective_user is None:
            return
        
        if await can_restrict(update.effective_chat, update.effective_user.id):
            return await func(update, context, *args, **kwargs)
        else:
            await update.effective_message.reply_text(get_dialog("USER_CANT_RESTRICT", chat_id=update.effective_chat.id))

    return bot_restrict