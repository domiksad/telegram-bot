from profanityfilter import ProfanityFilter

from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.config import Config


async def profanity_filter_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.edited_message
    if not message or not message.text:
        return
    text = message.text
    if(Config.pf.is_profane(text) & Config.NOTIFY_ABOUT_PROFANITY):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Config.PROFANITY_NOTIFICATION_TEXT, reply_to_message_id=update.message.message_id)
