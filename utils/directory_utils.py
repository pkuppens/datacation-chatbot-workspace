"""Directory and file management utilities for the application.

This module provides functions for managing application directories and files,
ensuring they exist and are properly configured for the application's needs.
"""

from pathlib import Path
from typing import List, Optional
import logging


def get_project_root() -> Path:
    """Get the absolute path to the project root directory.

    This function determines the project root by looking for the pyproject.toml file,
    starting from the current directory and moving up until it's found.

    Returns:
        Path: Absolute path to the project root directory

    Raises:
        FileNotFoundError: If pyproject.toml cannot be found in any parent directory
    """
    current_dir = Path.cwd()
    while current_dir != current_dir.parent:  # Stop at root directory
        if (current_dir / "pyproject.toml").exists():
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError("Could not find project root (pyproject.toml) in any parent directory")


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
    logger = logging.getLogger(__name__)

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


def ensure_file(file_path: Path, create_parents: bool = True) -> None:
    """Ensure a file exists and is writable.

    This function ensures that a file exists and is writable. If the file doesn't exist,
    it will be created. If the parent directory doesn't exist, it will be created if
    create_parents is True.

    Args:
        file_path: Path to the file to ensure exists
        create_parents: Whether to create parent directories if they don't exist

    Raises:
        OSError: If the file cannot be created or is not writable
    """
    logger = logging.getLogger(__name__)

    try:
        # Ensure parent directory exists
        if create_parents:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create file if it doesn't exist
        if not file_path.exists():
            file_path.touch()
            logger.debug(f"Created file: {file_path}")

        # Test if file is writable
        with open(file_path, "a"):
            pass
        logger.debug(f"Verified file is writable: {file_path}")

    except Exception as e:
        logger.error(f"Failed to ensure file {file_path}: {str(e)}")
        raise
