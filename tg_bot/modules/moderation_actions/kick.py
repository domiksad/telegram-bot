from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_can_restrict, bot_can_restrict
from tg_bot.modules.helper_funcs.extraction import fetch_target_member
from tg_bot.modules.helper_funcs.string_funcs import html_mention
from tg_bot.modules.language import get_dialog

@bot_admin
@bot_can_restrict
@user_can_restrict
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = await fetch_target_member(update=update, context=context)
    
    if result is None:
        return
    
    [chat_id, target_user] = result

    await context.bot.unban_chat_member(chat_id=chat_id, user_id=target_user.user.id) # kick user
    await update.effective_message.reply_text(get_dialog("KICKED", update.effective_chat.id).format(user=html_mention(target_user.user)), parse_mode="HTML") # type: ignore
