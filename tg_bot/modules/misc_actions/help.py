from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.modules.language import get_dialog

async def help(update: Update, context: ContextTypes):
    if update.effective_chat is None or update.effective_message is None:
        return
    
    from tg_bot.modules.commands.commands import COMMANDS
    msg = get_dialog(key="COMMANDS", chat_id=update.effective_chat.id)
    for i in COMMANDS.keys():
        msg += "\n"+i
    await update.effective_message.reply_text(text=msg)