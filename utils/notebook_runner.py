"""Utility class for running Jupyter notebooks with proper configuration.

This module provides a NotebookRunner class that handles:
1. Notebook execution with proper settings
2. In-place execution support
3. Conversion file management
4. Error handling and logging

References:
- nbconvert Documentation: https://nbconvert.readthedocs.io/
- Jupyter Documentation: https://jupyter.org/documentation
"""

import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class NotebookRunner:
    """Class to handle notebook execution with proper configuration.

    This class provides a consistent way to run notebooks with:
    - Proper environment setup
    - In-place execution support
    - Conversion file management
    - Error handling and logging

    Attributes:
        notebook_path: Path to the notebook to run
        in_place: Whether to execute in-place
        keep_convert: Whether to keep the .nbconvert file
    """

    def __init__(self, notebook_path: str, in_place: bool = True, keep_convert: bool = False):
        """Initialize the notebook runner.

        Args:
            notebook_path: Path to the notebook to run
            in_place: Whether to execute in-place
            keep_convert: Whether to keep the .nbconvert file
        """
        self.notebook_path = Path(notebook_path)
        self.in_place = in_place
        self.keep_convert = keep_convert

        # Validate notebook exists
        if not self.notebook_path.exists():
            raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    def run(self):
        """Run the notebook with proper configuration.

        This method:
        1. Attempts in-place execution if enabled
        2. Falls back to regular execution if in-place fails
        3. Manages the .nbconvert file based on settings
        4. Handles errors and provides logging

        The execution process:
        1. First tries in-place execution for better performance
        2. If that fails, falls back to regular execution
        3. Manages the .nbconvert file based on keep_convert setting
        4. Provides detailed logging of the process
        """
        try:
            # Try in-place execution first if enabled
            if self.in_place:
                try:
                    self._run_in_place()
                    return
                except Exception as e:
                    logger.warning(f"In-place execution failed: {str(e)}")
                    logger.info("Falling back to regular execution")

            # Fall back to regular execution
            self._run_regular()

        except Exception as e:
            logger.error(f"Error running notebook: {str(e)}", exc_info=True)
            raise

    def _run_in_place(self):
        """Run the notebook in-place.

        This method:
        1. Uses nbconvert to execute the notebook in-place
        2. Handles the .nbconvert file based on settings
        3. Provides detailed logging

        The in-place execution:
        - Is more efficient as it doesn't create a copy
        - Requires proper file permissions
        - May fail in some environments
        """
        # Build the command
        cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(self.notebook_path)]

        # Run the command
        logger.info(f"Running notebook in-place: {self.notebook_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            raise RuntimeError(f"Error executing notebook: {result.stderr}")

        # Handle .nbconvert file
        nbconvert_file = self.notebook_path.with_suffix(".nbconvert.ipynb")
        if nbconvert_file.exists():
            if self.keep_convert:
                logger.info(f"Keeping .nbconvert file: {nbconvert_file}")
            else:
                logger.info(f"Removing .nbconvert file: {nbconvert_file}")
                nbconvert_file.unlink()

    def _run_regular(self):
        """Run the notebook with regular execution.

        This method:
        1. Uses nbconvert to execute the notebook
        2. Creates a new file with the results
        3. Replaces the original if successful
        4. Provides detailed logging

        The regular execution:
        - Creates a copy of the notebook
        - Is more reliable but less efficient
        - Always works regardless of file permissions
        """
        # Build the command
        cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", str(self.notebook_path)]

        # Run the command
        logger.info(f"Running notebook: {self.notebook_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            raise RuntimeError(f"Error executing notebook: {result.stderr}")

        # Get the output file
        output_file = self.notebook_path.with_suffix(".nbconvert.ipynb")
        if not output_file.exists():
            raise FileNotFoundError(f"Output file not found: {output_file}")

        # Replace the original file
        logger.info("Replacing original notebook with executed version")
        output_file.replace(self.notebook_path)

        # Clean up if not keeping convert file
        if not self.keep_convert and output_file.exists():
            logger.info(f"Removing .nbconvert file: {output_file}")
            output_file.unlink()
