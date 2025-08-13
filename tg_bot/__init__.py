import logging
import sys
from dotenv import dotenv_values

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1:2] < 13:
    LOGGER.error("This bot requires Python 3.13 or higher. Please upgrade your Python")
    quit(1)

TOKEN = dotenv_values(".env")["TOKEN"]

if not TOKEN:
    LOGGER.error("Variable TOKEN cannot be empty")