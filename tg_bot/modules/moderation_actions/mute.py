from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_can_restrict, bot_can_restrict, is_in_chat
from tg_bot.modules.helper_funcs.extraction import fetch_target_member
from tg_bot.modules.language import get_dialog


@bot_admin
@bot_can_restrict
@user_can_restrict
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Ile czasu
    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    await context.bot.ban_chat_member(chat_id=chat_id, user_id=target_user.user.id) # ban user

@bot_admin
@bot_can_restrict
@user_can_restrict
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    # effective_chat and effective_message are already checked in fetch_target_member
    if await is_in_chat(chat=update.effective_chat, user_id=target_user.user.id): # type: ignore
        await update.effective_message.reply_text(get_dialog("WHY_UNBAN_USER_ALREADY_IN_CHAT", update.effective_chat.id)) # type: ignore
        return

    await context.bot.unban_chat_member(chat_id=chat_id, user_id=target_user.user.id) # unban user