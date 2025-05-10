"""Data pipeline package for managing datasets."""

from .titanic_pipeline import get_titanic_data, run_titanic_pipeline, get_sqlite_connection

__all__ = ["get_titanic_data", "run_titanic_pipeline", "get_sqlite_connection"]
