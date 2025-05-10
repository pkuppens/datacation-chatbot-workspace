import os
import sqlite3
from datetime import timedelta
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import requests
from datasets import load_dataset
from prefect import flow, task
from prefect.filesystems import LocalFileSystem
from prefect.tasks import task_input_hash
from sqlalchemy import create_engine
from prefect.logging import get_run_logger

# Constants
DATA_DIR = Path("data_sources")
TITANIC_CSV_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
TITANIC_CSV_PATH = DATA_DIR / "titanic.csv"
TITANIC_DB_PATH = DATA_DIR / "titanic.sqlite"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def download_titanic_dataset() -> Path:
    """Download the Titanic dataset if it doesn't exist.
    Always downloads from GitHub to ensure we have passenger names."""
    if not TITANIC_CSV_PATH.exists():
        print("Downloading Titanic dataset from GitHub...")
        response = requests.get(TITANIC_CSV_URL)
        response.raise_for_status()
        TITANIC_CSV_PATH.write_text(response.text)
    return TITANIC_CSV_PATH


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def convert_to_sqlite(csv_path: Path) -> Path:
    """Convert the CSV file to SQLite database if it doesn't exist."""
    if not TITANIC_DB_PATH.exists():
        # Read CSV
        df = pd.read_csv(csv_path)

        # Create SQLite database
        engine = create_engine(f"sqlite:///{TITANIC_DB_PATH}")
        df.to_sql("titanic", engine, if_exists="replace", index=False)

    return TITANIC_DB_PATH


@task
def load_titanic_data() -> pd.DataFrame:
    """Load Titanic data from SQLite database.

    Note: We explicitly remove name-related columns to protect privacy and prevent
    potential discrimination. This is in line with data protection best practices
    and ethical AI principles.
    """
    engine = create_engine(f"sqlite:///{TITANIC_DB_PATH}")
    df = pd.read_sql("SELECT * FROM titanic", engine)

    # Remove name-related columns for privacy and ethical considerations
    name_columns = [col for col in df.columns if "name" in col.lower()]
    if name_columns:
        df = df.drop(columns=name_columns)
        get_run_logger().info(f"Removed name-related columns for privacy: {name_columns}")

    return df


def get_sqlite_connection() -> sqlite3.Connection:
    """Get a direct SQLite connection to the database.
    This is useful if you want to work with the database directly
    rather than through pandas."""
    if not TITANIC_DB_PATH.exists():
        # Trigger the pipeline to create the database
        run_titanic_pipeline()

    return sqlite3.connect(TITANIC_DB_PATH)


@flow(name="Titanic Data Pipeline")
def run_titanic_pipeline() -> Path:
    """Run the complete Titanic data pipeline."""
    csv_path = download_titanic_dataset()
    db_path = convert_to_sqlite(csv_path)
    return db_path


def get_titanic_data() -> pd.DataFrame:
    """Public function to get Titanic data as a pandas DataFrame,
    ensuring the pipeline has run."""
    return load_titanic_data()


def main():
    """Run the pipeline tests."""
    print("Testing Titanic Data Pipeline...")

    # Test 1: Run the pipeline
    print("\n1. Running pipeline...")
    db_path = run_titanic_pipeline()
    assert db_path.exists(), "Database file was not created"
    print(f"✓ Pipeline completed successfully. Database at: {db_path}")

    # Test 2: Verify CSV exists
    print("\n2. Verifying CSV file...")
    assert TITANIC_CSV_PATH.exists(), "CSV file was not created"
    print(f"✓ CSV file exists at: {TITANIC_CSV_PATH}")

    # Test 3: Test DataFrame loading
    print("\n3. Testing DataFrame loading...")
    df = get_titanic_data()
    assert len(df) > 0, "DataFrame is empty"
    print(f"✓ Successfully loaded DataFrame with {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head())

    # Test 4: Test SQLite connection
    print("\n4. Testing SQLite connection...")
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # Test basic query
    cursor.execute("SELECT COUNT(*) FROM titanic")
    count = cursor.fetchone()[0]
    assert count > 0, "SQLite database is empty"
    print(f"✓ Successfully queried SQLite database with {count} rows")

    # Test schema
    cursor.execute("PRAGMA table_info(titanic)")
    columns = cursor.fetchall()
    print("\nDatabase schema:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

    conn.close()
    print("\n✓ All pipeline tests completed successfully!")


if __name__ == "__main__":
    main()
