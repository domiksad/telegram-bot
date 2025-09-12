from telegram.ext import ApplicationBuilder

import os

from tg_bot import LOGGER
from tg_bot.modules.commands.handlers import register_handlers


# Load api_key from ENV (docker compose injects .env values to ENV when ran)
API_KEY = os.getenv("API_KEY")

# Validate API_KEY
if API_KEY is None or API_KEY == "":
    LOGGER.critical("No api key provided. Exiting...")
    quit(1)

# Create bot
application = ApplicationBuilder().token(API_KEY).build()

# Register commands
register_handlers(application=application)

# Run bot
application.run_polling()