"""Script to inspect and validate the Titanic dataset from Hugging Face.
This script focuses on validating the dataset structure and data quality before it enters our pipeline."""

from datasets import load_dataset
import pandas as pd
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def validate_titanic_dataset() -> Dict[str, Any]:
    """Validate the Titanic dataset from Hugging Face.

    Returns:
        Dict containing validation results including:
        - shape: Dataset dimensions
        - columns: List of column names
        - dtypes: Data types of columns
        - missing_values: Count of missing values per column
        - name_columns: List of name-related columns (for privacy review)
    """
    # Load the dataset
    logger.info("Loading mstz/titanic dataset from Hugging Face...")
    dataset = load_dataset("mstz/titanic")

    # Convert to pandas for easier inspection
    df = dataset["train"].to_pandas()

    # Basic information
    validation_results = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }

    # Check for name-related columns
    name_cols = [col for col in df.columns if "name" in col.lower()]
    validation_results["name_columns"] = name_cols

    # Log validation results
    logger.info(f"\nDataset shape: {validation_results['shape']}")
    logger.info(f"\nColumns: {validation_results['columns']}")
    logger.info("\nData types:")
    for col, dtype in validation_results["dtypes"].items():
        logger.info(f"- {col}: {dtype}")

    logger.info("\nMissing values:")
    for col, count in validation_results["missing_values"].items():
        if count > 0:
            logger.info(f"- {col}: {count} missing values")

    if name_cols:
        logger.warning(f"\nFound name-related columns: {name_cols}")
        logger.warning("Note: These columns will be removed in the pipeline for privacy reasons")
    else:
        logger.info("\nNo name-related columns found in the dataset")

    return validation_results


if __name__ == "__main__":
    validate_titanic_dataset()
