import logging
import sys
from pathlib import Path
from dotenv import load_dotenv 
from tg_bot.config import Config

import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

if sys.version_info < (3, 13):
    LOGGER.error("You need at least Python 3.13 to run this project")
    quit(-1)

# Load values from .env
load_dotenv(Path(__file__).parent / ".env") # non elegant way to fix a bug
Config.API_KEY = os.getenv("TOKEN")
if Config.API_KEY is None:
    LOGGER.error("No api key provided")
    quit(-1)

# Validate config
if Config.BAN_AFTER_REACHING_MAX_WARN_COUNT and Config.KICK_AFTER_REACHING_MAX_WARN_COUNT:
    LOGGER.error("Both BAN_AFTER_REACHING_MAX_WARN_COUNT and KICK_AFTER_REACHING_MAX_WARN_COUNT are enabled\n Only one action can be active at a time")
    quit(-1)