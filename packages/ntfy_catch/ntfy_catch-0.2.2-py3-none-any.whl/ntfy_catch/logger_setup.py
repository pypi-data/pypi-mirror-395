"""Logging setup for ntfy_catch"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(config):
    """Setup logging configuration

    Args:
        config: ConfigParser object with logging configuration

    Returns:
        logging.Logger: Configured logger instance
    """
    log_level = config.get('logging', 'log_level', fallback='INFO')

    #log_dir = config.get('logging', 'log_dir', fallback='./logs')

    # Create log directory if it doesn't exist
    #log_dir_path = Path(log_dir)
    #log_dir_path.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    logger = logging.getLogger('ntfy_catch')
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers
    logger.handlers.clear()

    # File handler with rotation
    #log_file = log_dir_path / 'ntfy_catch.log'
    log_file = os.path.expanduser('~/ntfy-catch-poller.log')

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Console handler (for errors and critical messages)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger():
    """Get the ntfy_catch logger instance

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger('ntfy_catch')
