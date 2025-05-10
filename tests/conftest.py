"""Test configuration and fixtures.

This module contains pytest fixtures and configuration that are shared across
all test modules.
"""

import os
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_data_dir(project_root):
    """Return the test data directory."""
    return project_root / "tests" / "data"


@pytest.fixture(scope="session")
def test_logs_dir(project_root):
    """Return the test logs directory."""
    return project_root / "tests" / "logs"


@pytest.fixture(autouse=True)
def setup_test_env(project_root, test_data_dir, test_logs_dir):
    """Set up test environment before each test."""
    # Create test directories if they don't exist
    test_data_dir.mkdir(parents=True, exist_ok=True)
    test_logs_dir.mkdir(parents=True, exist_ok=True)

    # Set up test environment variables
    os.environ["TESTING"] = "true"
    os.environ["PROJECT_ROOT"] = str(project_root)

    yield

    # Cleanup after tests
    os.environ.pop("TESTING", None)
    os.environ.pop("PROJECT_ROOT", None)
