import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="trading_bot.log"):
    """
    Sets up a logger that logs both to a file and the console.
    """
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formatter for log messages
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )

        # File Handler (rotating, max 5MB, keep 3 backups)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        # Using a simpler format for console output to not clutter the CLI
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
