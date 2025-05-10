"""Centralized logging configuration for the application.

This module provides a configured logger instance that can be used throughout
the application to ensure consistent logging format and behavior.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def get_relative_path(path: str) -> str:
    """Convert an absolute path to a path relative to the project root.

    Args:
        path: The absolute path to convert

    Returns:
        The path relative to the project root
    """
    try:
        return str(Path(path).relative_to(PROJECT_ROOT))
    except ValueError:
        return path


class RelativePathFormatter(logging.Formatter):
    """Custom formatter that shows paths relative to the project root."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with relative paths.

        Args:
            record: The log record to format

        Returns:
            The formatted log message
        """
        # Convert the path to be relative to the project root
        record.pathname = get_relative_path(record.pathname)
        return super().format(record)


def setup_logger(name: str = "datacation", level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Set up and configure the application logger.

    Args:
        name: The name of the logger
        level: The logging level
        log_file: Optional path to a log file

    Returns:
        A configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatters - a console log formatter does not need to include the date
    console_formatter = RelativePathFormatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(pathname)s:%(lineno)d | %(funcName)s | %(message)s", datefmt="%H:%M:%S"
    )

    # includes the date, because we may look into older logs
    file_formatter = RelativePathFormatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(pathname)s:%(lineno)d | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Create the default logger instance
logger = setup_logger(log_file=str(PROJECT_ROOT / "logs" / "app.log"))
