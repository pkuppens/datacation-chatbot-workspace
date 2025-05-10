"""Directory management utilities for the application.

This module provides functions for managing application directories,
ensuring they exist and are properly configured for the application's needs.
"""

import os
from pathlib import Path
from typing import List, Optional
from utils.logger import logger


def ensure_directories(base_dir: Optional[Path] = None, dirs: Optional[List[str]] = None, create_parents: bool = True) -> None:
    """Create necessary directories for the application.

    This function ensures that all required directories exist for the application
    to function properly. It should be called at application startup, not chat start,
    as these directories are needed for the application to function.

    Args:
        base_dir: Base directory path. Defaults to the application's root directory.
        dirs: List of directory names to create. Defaults to standard application directories.
        create_parents: Whether to create parent directories if they don't exist.

    The standard directories created are:
    - .files: For Chainlit's file operations and temporary storage
    - .cache: For application caching
    - logs: For application logs
    - data: For application data files

    Note:
        This function is idempotent - calling it multiple times with the same
        parameters will not cause any issues.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    if dirs is None:
        dirs = [".files", ".cache", "logs", "data"]

    for dir_name in dirs:
        dir_path = base_dir / dir_name
        try:
            dir_path.mkdir(parents=create_parents, exist_ok=True)
            logger.debug(f"Ensured directory exists: {dir_path}")
        except Exception as e:
            logger.error(f"Failed to create directory {dir_path}: {str(e)}")
            raise
