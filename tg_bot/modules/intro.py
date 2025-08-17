from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from tg_bot.modules.commands import COMMANDS # fix circular import error
    await update.message.reply_text("Commands:\n"+"\n".join(COMMANDS.keys()))