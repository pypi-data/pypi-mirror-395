"""AutoPR package - minimal MVP"""

__version__ = "0.4.0-beta"

# Logging configuration
from loguru import logger
import sys
import os
from datetime import datetime

# Remove default handler
logger.remove()

# Add console handler with custom format
logger.add(
    sys.stdout,
    format="[AutoPR] [{level}] [{time:YYYY-MM-DD HH:mm}] {message}",
    level="DEBUG" if os.getenv("AUTOPR_DEBUG") else "INFO",
    colorize=True
)

# Add file handler
log_file = os.path.join(os.getcwd(), "autopr.log")
logger.add(
    log_file,
    format="[AutoPR] [{level}] [{time:YYYY-MM-DD HH:mm:ss}] {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="1 week"
)
