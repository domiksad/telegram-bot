from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.modules.language import get_dialog


async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message is None or update.effective_chat is None:
        return
    
    if len(context.args) == 1:
        sticker_id = context.args[0]
        await update.effective_chat.send_sticker(sticker=sticker_id)
        return
    else:
        await update.effective_message.reply_text(text=get_dialog("USAGE", update.effective_chat.id).format(command="sticker", args="sticker_id"))
        return