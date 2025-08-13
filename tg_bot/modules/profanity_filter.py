from profanityfilter import ProfanityFilter

from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.config import Config

def make_profanity_filter_handler(profanity_filter_instance):
    return lambda u, c: profanity_filter_function(u, c, profanity_filter_instance)

async def profanity_filter_function(update: Update, context: ContextTypes.DEFAULT_TYPE, profanity_filter: ProfanityFilter):
    message = update.message or update.edited_message
    if not message or not message.text:
        return
    text = message.text
    if(profanity_filter().is_profane(text) & Config.NOTIFY_ABOUT_PROFANITY):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Config.PROFANITY_NOTIFICATION_TEXT, reply_to_message_id=update.message.message_id)
