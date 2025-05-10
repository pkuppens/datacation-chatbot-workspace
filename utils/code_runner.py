"""Python code execution utilities.

This module provides functions for safely executing Python code in a controlled environment,
with proper error handling and logging.
"""

from typing import Any, Dict, Optional
import traceback
from pathlib import Path
from utils.logger import logger


class CodeRunner:
    """Handles execution of Python code in a controlled environment.

    This class provides methods for executing Python code with proper error handling,
    logging, and result processing. It's designed to be used by agents and tools
    that need to execute Python code as part of their operation.

    Attributes:
        globals_dict: Dictionary of global variables available to executed code
        locals_dict: Dictionary of local variables available to executed code
    """

    def __init__(self, globals_dict: Optional[Dict[str, Any]] = None):
        """Initialize the code runner.

        Args:
            globals_dict: Dictionary of global variables to make available to executed code
        """
        self.globals_dict = globals_dict or {}
        self.locals_dict = {}

    async def execute_code(self, code: str) -> str:
        """Execute Python code and return the result.

        Args:
            code: The Python code to execute

        Returns:
            The string representation of the execution result

        Raises:
            Exception: If code execution fails
        """
        try:
            logger.debug(f"Executing code: {code}")

            # Execute the code
            exec(code, self.globals_dict, self.locals_dict)

            # Get the result
            result = str(self.locals_dict.get("_", ""))
            logger.debug(f"Code execution result: {result}")

            return result

        except Exception as e:
            error_msg = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def update_globals(self, new_globals: Dict[str, Any]) -> None:
        """Update the global variables available to executed code.

        Args:
            new_globals: Dictionary of new global variables to add
        """
        self.globals_dict.update(new_globals)
        logger.debug(f"Updated globals: {list(new_globals.keys())}")

    def clear_locals(self) -> None:
        """Clear the local variables dictionary."""
        self.locals_dict.clear()
        logger.debug("Cleared local variables")
