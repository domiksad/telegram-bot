import os
import sys
import dotenv

from telegram.ext import ApplicationBuilder

from tg_bot import LOGGER
from tg_bot.modules.commands.handlers import register_handlers


# Load api_key from ENV (docker compose injects .env values to PATH/ENV when ran)
API_KEY = os.getenv("API_KEY")

# Get .env file path from arguments
if API_KEY is None and "--env" in sys.argv:
    env_index = sys.argv.index("--env")
    dotenv_path = os.path.abspath(sys.argv[env_index + 1])

    # If a directory is provided, assume the .env file is inside it
    if os.path.isdir(dotenv_path):
        dotenv_path = os.path.join(dotenv_path, ".env")

    if not os.path.exists(dotenv_path):
        LOGGER.critical(f".env file not found at {dotenv_path} Exiting...")
        quit(1)

    dotenv.load_dotenv(dotenv_path)

    API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    LOGGER.critical("No api key provided. Exiting...")
    quit(1)

# Create bot
application = ApplicationBuilder().token(API_KEY).build()

# Register commands
register_handlers(application=application)

# Run bot
application.run_polling()