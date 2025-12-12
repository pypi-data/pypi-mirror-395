"""
Logging Configuration for JJF Survey Analytics
Configures structured logging for AI analysis and application debugging
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO", log_to_file: bool = True, log_dir: str = "logs") -> None:
    """
    Configure application-wide logging with console and file handlers.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to file
        log_dir: Directory for log files
    """
    # Create logs directory if it doesn't exist
    if log_to_file and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler - INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    if log_to_file:
        # Main log file - INFO and above
        main_handler = RotatingFileHandler(
            os.path.join(log_dir, "app.log"), maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        main_handler.setLevel(logging.INFO)
        main_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        main_handler.setFormatter(main_formatter)
        root_logger.addHandler(main_handler)

        # Error log file - ERROR and above only
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, "error.log"), maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s\n"
            "Extra: %(pathname)s:%(lineno)d\n",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        error_handler.setFormatter(error_formatter)
        root_logger.addHandler(error_handler)

        # Debug log file - DEBUG and above (detailed logging)
        debug_handler = RotatingFileHandler(
            os.path.join(log_dir, "debug.log"), maxBytes=10 * 1024 * 1024, backupCount=3  # 10MB
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        debug_handler.setFormatter(debug_formatter)
        root_logger.addHandler(debug_handler)

    # Set specific loggers to appropriate levels
    logging.getLogger("src.analytics.ai_analyzer").setLevel(logging.DEBUG)
    logging.getLogger("openai").setLevel(logging.WARNING)  # Reduce OpenAI SDK noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Reduce HTTP noise

    logging.info(f"Logging configured - Level: {log_level}, File logging: {log_to_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Example usage in other modules:
# from src.analytics.logging_config import get_logger
# logger = get_logger(__name__)
