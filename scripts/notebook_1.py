#!/usr/bin/env python3
"""Script to run the workshop notebook with proper Chainlit configuration.

This script ensures that Chainlit is properly configured before running the notebook.
It follows this flow:
1. Load environment variables from .env file
2. Set up Chainlit environment with proper paths
3. Run the notebook with in-place execution

The script uses the following environment variables if set:
- CHAINLIT_WORKSPACE_DIR: Base directory for Chainlit (defaults to project root)
- CHAINLIT_TRANSLATIONS_PATH: Where to store translations (defaults to .chainlit/translations)
- CHAINLIT_CONFIG_PATH: Path to config.toml (defaults to .chainlit/config.toml)
- NOTEBOOK_KEEP_CONVERT: If set to 'true', keeps the .nbconvert file instead of overwriting (default: false)
"""

import sys
import subprocess
import os
import shutil
from pathlib import Path
from utils.directory_utils import get_project_root
from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file."""
    env_path = get_project_root() / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    else:
        print("Warning: No .env file found, using default environment")


def setup_chainlit_environment():
    """Configure Chainlit environment variables and ensure proper directory structure.

    This function sets up the Chainlit environment with the following priority:
    1. Use existing environment variables if set
    2. Fall back to project root-based defaults if not set

    The function ensures that:
    - All necessary directories exist
    - Environment variables are set with absolute paths
    - Configuration is consistent across the project
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
            print(f"Initialized root config.toml from notebooks directory")
            print("Note: Future changes should be made to the root config.toml only")


def run_notebook():
    """Run the workshop notebook with in-place execution.

    This function:
    1. Uses the configured workspace directory for notebook path
    2. Executes the notebook in-place (modifies the original file)
    3. Captures and reports any execution errors

    If in-place execution fails, it will:
    1. Create a .nbconvert file
    2. Move it over the original file unless NOTEBOOK_KEEP_CONVERT is set to 'true'
    """
    workspace_root = Path(os.environ["CHAINLIT_WORKSPACE_DIR"])
    notebook_path = workspace_root / "notebooks/workshop_part_1.ipynb"

    if not notebook_path.exists():
        print(f"Error: Notebook not found at {notebook_path}")
        sys.exit(1)

    print(f"Running notebook: {notebook_path}")

    # Try in-place execution first
    result = subprocess.run(
        [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(notebook_path)],
        capture_output=True,
        text=True,
    )

    # If in-place execution fails, try regular execution and move the file
    if result.returncode != 0:
        print("In-place execution failed, trying regular execution...")
        result = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", str(notebook_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Get the .nbconvert file path
            nbconvert_path = notebook_path.with_suffix(".nbconvert.ipynb")
            if nbconvert_path.exists():
                if os.environ.get("NOTEBOOK_KEEP_CONVERT", "").lower() == "true":
                    print(f"Keeping .nbconvert file at {nbconvert_path}")
                else:
                    # Move the .nbconvert file over the original
                    shutil.move(nbconvert_path, notebook_path)
                    print(f"Moved {nbconvert_path} to {notebook_path}")
        else:
            print("Error running notebook:")
            print(result.stderr)
            sys.exit(1)

    print("Notebook executed successfully!")


def main():
    """Main entry point for the script."""
    try:
        load_environment()
        setup_chainlit_environment()
        run_notebook()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
