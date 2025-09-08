from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_can_restrict, bot_can_restrict, is_in_chat
from tg_bot.modules.helper_funcs.extraction import fetch_target_member, extract_reason
from tg_bot.modules.helper_funcs.string_funcs import html_mention
from tg_bot.modules.sql.warns import add_warn, reset_warns, del_warn
from tg_bot.modules.sql.settings import get_settings
from tg_bot.modules.language import get_dialog
from tg_bot import LOGGER


@bot_admin
@bot_can_restrict
@user_can_restrict
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Ile czasu
    if update.effective_message is None or update.effective_chat is None:
        return
    
    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    reason = await extract_reason(message=update.effective_message, args=" ".join(context.args[1:])) or get_dialog("NO_REASON_PROVIDED", chat_id=chat_id) # type: ignore

    settings = get_settings(chat_id=chat_id)
    warn_count = add_warn(chat=update.effective_chat, user=target_user.user)
    max_warn_count = settings["max_warn_count"]
    soft_warn = settings["soft_warn"]

    if warn_count >= max_warn_count:
        reset_warns(chat=update.effective_chat, user=target_user.user)
        if soft_warn is True:
            await context.bot.unban_chat_member(chat_id=chat_id, user_id=target_user.user.id, only_if_banned=False)
            await update.effective_message.reply_text(get_dialog("WARN_KICKED", chat_id).format(user=html_mention(target_user.user), reason=reason), parse_mode="HTML")
            return
        else:
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=target_user.user.id)
            await update.effective_message.reply_text(get_dialog("WARN_BANNED", chat_id).format(user=html_mention(target_user.user), reason=reason), parse_mode="HTML")
            return

    await update.effective_message.reply_text(get_dialog("WARNED", chat_id).format(user=html_mention(target_user.user), warn_count=warn_count, max_warn_count=max_warn_count, reason=reason), parse_mode="HTML")

@bot_admin
@bot_can_restrict
@user_can_restrict
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None or update.effective_chat is None:
        return

    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    warn_count = del_warn(chat=update.effective_chat, user=target_user.user)
    max_warn_count = get_settings(chat_id=chat_id)["max_warn_count"]

    await update.effective_message.reply_text(get_dialog("UNWARNED", chat_id).format(user=html_mention(target_user.user), warn_count=warn_count, max_warn_count=max_warn_count), parse_mode="HTML")
