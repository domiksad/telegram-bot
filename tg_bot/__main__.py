from profanityfilter import ProfanityFilter

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler

from tg_bot.config import Config
from tg_bot.modules.handlers import register_handlers, register_profanity_filter


application = ApplicationBuilder().token(Config.API_KEY).build()
register_handlers(application=application)

if Config.USE_PROFANITY_FILTER:
    pf = ProfanityFilter()
    register_profanity_filter(application, pf)

application.run_polling()