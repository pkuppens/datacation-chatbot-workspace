"""Script to run the second workshop notebook with proper configuration.

This script ensures that the notebook runs with the correct environment setup,
including Chainlit configuration and dependencies. It shares common functionality
with notebook_1.py through utility modules.

The script follows these steps:
1. Load environment variables
2. Set up Chainlit configuration
3. Run the notebook with proper settings
4. Handle any conversion files

The script uses the following environment variables if set:
- CHAINLIT_WORKSPACE_DIR: Base directory for Chainlit (defaults to project root)
- CHAINLIT_TRANSLATIONS_PATH: Where to store translations (defaults to .chainlit/translations)
- CHAINLIT_CONFIG_PATH: Path to config.toml (defaults to .chainlit/config.toml)
- NOTEBOOK_KEEP_CONVERT: If set to 'true', keeps the .nbconvert file instead of overwriting (default: false)

References:
- LangChain SQL Database Integration: https://python.langchain.com/docs/integrations/tools/sql_database/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Chainlit Plotly Integration: https://docs.chainlit.io/api-reference/elements/plotly
- nbconvert Documentation: https://nbconvert.readthedocs.io/
- Jupyter Documentation: https://jupyter.org/documentation
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from utils.directory_utils import get_project_root
from utils.notebook_runner import NotebookRunner


def load_environment():
    """Load environment variables from .env file.

    This function:
    1. Looks for .env file in the project root
    2. Loads variables if found
    3. Provides feedback on the loading status
    """
    env_path = get_project_root() / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    else:
        print("Warning: No .env file found, using default environment")


def setup_chainlit_environment():
    """Set up the Chainlit environment for notebook execution.

    This function ensures that:
    1. The workspace directory is set to the project root
    2. The Chainlit configuration is properly initialized
    3. The translations path is set to a shared location

    The configuration is managed in a way that:
    - Uses existing environment variables if set
    - Falls back to defaults if not set
    - Maintains a single source of truth for configuration
    """
    # Get absolute paths for default configuration
    workspace_root = get_project_root()
    chainlit_dir = workspace_root / ".chainlit"
    translations_dir = chainlit_dir / "translations"
    config_file = chainlit_dir / "config.toml"

    # If environment variables are set, use those paths instead
    if "CHAINLIT_WORKSPACE_DIR" in os.environ:
        workspace_root = Path(os.environ["CHAINLIT_WORKSPACE_DIR"]).resolve()
        chainlit_dir = workspace_root / ".chainlit"
        translations_dir = chainlit_dir / "translations"
        config_file = chainlit_dir / "config.toml"
        print(f"Using custom workspace directory: {workspace_root}")

    # Ensure directories exist
    chainlit_dir.mkdir(parents=True, exist_ok=True)
    translations_dir.mkdir(parents=True, exist_ok=True)

    # Set environment variables with absolute paths
    os.environ["CHAINLIT_WORKSPACE_DIR"] = str(workspace_root)
    os.environ["CHAINLIT_TRANSLATIONS_PATH"] = str(translations_dir)
    os.environ["CHAINLIT_CONFIG_PATH"] = str(config_file)

    # Copy config.toml from notebooks only if it doesn't exist in the root
    # This is a one-time setup to ensure the root config exists
    if not config_file.exists():
        notebook_config = workspace_root / "notebooks/.chainlit/config.toml"
        if notebook_config.exists():
            shutil.copy2(notebook_config, config_file)
            print("Initialized root config.toml from notebooks directory")
            print("Note: Future changes should be made to the root config.toml only")


def main():
    """Main function to run the notebook with proper configuration.

    This function:
    1. Loads environment variables
    2. Sets up the Chainlit environment
    3. Creates a NotebookRunner instance
    4. Runs the notebook with proper settings

    The notebook is run with:
    - In-place execution enabled
    - Proper environment variables set
    - Error handling and logging
    """
    try:
        # Load environment variables
        load_environment()

        # Set up Chainlit environment
        setup_chainlit_environment()

        # Create notebook runner
        runner = NotebookRunner(
            notebook_path="notebooks/workshop_part_2.ipynb",
            in_place=True,
            keep_convert=os.getenv("NOTEBOOK_KEEP_CONVERT", "").lower() == "true",
        )

        # Run the notebook
        runner.run()

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
