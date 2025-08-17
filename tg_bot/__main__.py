from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler

from tg_bot.config import Config
from tg_bot.modules.handlers import register_handlers, register_profanity_filter


application = ApplicationBuilder().token(Config.API_KEY).build()

# Handlers
register_handlers(application=application)
if Config.USE_PROFANITY_FILTER:
    register_profanity_filter(application=application)

application.run_polling()