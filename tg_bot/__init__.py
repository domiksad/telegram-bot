import logging
import sys

# Setting logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set up logger for other files
LOGGER = logging.getLogger(__name__)

# Check python version
if sys.version_info < (3, 13):
    LOGGER.error("You need at least Python 3.13 to run this project")
    quit(-1)