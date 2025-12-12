import os
import sys

from loguru import logger

# Remove default logger configuration
logger.remove()

# Configure a stdout logger
log_level = os.getenv("LOG_LEVEL", "INFO")
logger.add(
    sys.stderr,
    level=log_level,
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
