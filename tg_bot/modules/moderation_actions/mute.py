from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_can_restrict, bot_can_restrict, is_in_chat
from tg_bot.modules.helper_funcs.extraction import fetch_target_member, extract_time_and_reason
from tg_bot.modules.helper_funcs.string_funcs import html_mention
from tg_bot.modules.language import get_dialog
from tg_bot import LOGGER


@bot_admin
@bot_can_restrict
@user_can_restrict

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Ile czasu
    if update.effective_message is None or update.effective_chat is None:
        return
    
    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    time_and_reason = await extract_time_and_reason(update.effective_message, " ".join(context.args[1:])) # type: ignore 
    
    if time_and_reason is None:
        return
    
    until_date, pretty, reason = time_and_reason

    await context.bot.restrict_chat_member(chat_id=chat_id, user_id=target_user.user.id, permissions=ChatPermissions.no_permissions(), until_date=until_date)
    await update.effective_message.reply_text(get_dialog("MUTED", update.effective_chat.id).format(user=html_mention(target_user.user), until_date=pretty, reason=reason), parse_mode="HTML")

@bot_admin
@bot_can_restrict
@user_can_restrict

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None or update.effective_chat is None:
        return

    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    if target_user.status != "restricted":
        await update.effective_message.reply_text(get_dialog("USER_ISNT_MUTED", update.effective_chat.id).format(user=html_mention(target_user.user)), parse_mode="HTML")
        return 
    
    chat = await context.bot.get_chat(update.effective_chat.id)
    if chat is None:
        LOGGER.error(f"Chat not found: {update.effective_chat.id}")
        return

    await context.bot.restrict_chat_member(chat_id=chat_id, user_id=target_user.user.id, permissions=chat.permissions) # type: ignore
    await update.effective_message.reply_text(get_dialog("UNMUTED", update.effective_chat.id).format(user=html_mention(target_user.user)), parse_mode="HTML")
