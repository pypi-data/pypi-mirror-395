# logger/__init__.py
from .logging import CustomLogger
# Create a single shared logger instance
GLOBAL_LOGGER = CustomLogger().get_logger("scrapper")

