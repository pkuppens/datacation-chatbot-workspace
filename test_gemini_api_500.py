#!/usr/bin/env python
"""Diagnostic script to identify causes of Gemini API 500 errors.

This script tests the Gemini API with increasing complexity to identify
what might be causing the 500 Internal Server Error.

Usage:
    python test_gemini_api_500.py [--verbose]

The script will:
1. Test basic model initialization
2. Test simple completion
3. Test with pandas DataFrame
4. Test with agent creation
5. Test with full Titanic agent configuration
"""

import os
import sys
import logging
import argparse
import warnings
from typing import Optional
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from config import config

# Suppress deprecation warnings
warnings.filterwarnings("ignore", message="Convert_system_message_to_human will be deprecated!")
warnings.filterwarnings(
    "ignore", message="Received additional kwargs {'handle_parsing_errors': True} which are no longer supported."
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_api_key() -> str:
    """Get the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    return api_key


def create_model(
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
) -> ChatGoogleGenerativeAI:
    """Create and configure the language model with optional overrides."""
    return ChatGoogleGenerativeAI(
        model=config.model.name,
        google_api_key=get_api_key(),
        temperature=temperature or config.model.temperature,
        max_tokens=max_tokens or config.model.max_tokens,
        top_p=top_p or config.model.top_p,
        top_k=top_k or config.model.top_k,
        convert_system_message_to_human=True,
    )


def test_01_basic_model() -> None:
    """Test 1: Basic model initialization and simple completion."""
    logger.info("Test 1: Basic model initialization")
    try:
        model = create_model()
        response = model.invoke("Say hello")
        logger.info(f"Response: {response}")
        logger.info("Test 1 passed")
    except Exception as e:
        logger.error(f"Test 1 failed: {str(e)}", exc_info=True)
        raise


def test_02_simple_dataframe() -> None:
    """Test 2: Simple DataFrame without agent."""
    logger.info("Test 2: Simple DataFrame")
    try:
        # Create a minimal DataFrame
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
        logger.info(f"DataFrame created:\n{df}")
        logger.info("Test 2 passed")
    except Exception as e:
        logger.error(f"Test 2 failed: {str(e)}", exc_info=True)
        raise


def test_03_minimal_agent() -> None:
    """Test 3: Minimal pandas agent."""
    logger.info("Test 3: Minimal pandas agent")
    try:
        model = create_model()
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
        agent = create_pandas_dataframe_agent(model, df, verbose=True, allow_dangerous_code=True)
        response = agent.invoke("How many rows are there?")
        logger.info(f"Response: {response}")
        logger.info("Test 3 passed")
    except Exception as e:
        logger.error(f"Test 3 failed: {str(e)}", exc_info=True)
        raise


def test_04_titanic_dataframe() -> None:
    """Test 4: Titanic DataFrame without agent."""
    logger.info("Test 4: Titanic DataFrame")
    try:
        from datasets import load_dataset

        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        logger.info(f"Titanic DataFrame created with {len(df)} rows")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info("Test 4 passed")
    except Exception as e:
        logger.error(f"Test 4 failed: {str(e)}", exc_info=True)
        raise


def test_05_titanic_agent_minimal() -> None:
    """Test 5: Titanic agent with minimal configuration."""
    logger.info("Test 5: Titanic agent with minimal configuration")
    try:
        from datasets import load_dataset

        model = create_model()
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        agent = create_pandas_dataframe_agent(model, df, verbose=True, allow_dangerous_code=True)
        response = agent.invoke("How many rows are there?")
        logger.info(f"Response: {response}")
        logger.info("Test 5 passed")
    except Exception as e:
        logger.error(f"Test 5 failed: {str(e)}", exc_info=True)
        raise


def test_06_titanic_agent_full() -> None:
    """Test 6: Titanic agent with full configuration."""
    logger.info("Test 6: Titanic agent with full configuration")
    try:
        from datasets import load_dataset

        model = create_model()
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            allow_dangerous_code=True,
            prefix="""You are a data analysis assistant. When analyzing the Titanic dataset:

1. First, understand the data structure:
   - Print and analyze the column names
   - Understand what each column represents
   - Note any data quality issues (missing values, etc.)

2. Then, plan your analysis:
   - Identify which columns are relevant to the question
   - Determine what calculations or filters are needed
   - Consider edge cases and data quality

3. Finally, execute your analysis:
   - Use ONLY the python_repl_ast tool
   - Keep code simple and direct
   - Always use print() for output
   - Handle missing values with dropna()
   - Format numbers with round(x, 2)

The dataset has these columns:
- has_survived: Whether the passenger survived (True/False)
- passenger_class: Passenger class (1, 2, or 3)
- name: Passenger name
- is_male: Whether the passenger is male (True/False)
- age: Passenger age
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)""",
        )
        response = agent.invoke("How many rows are there?")
        logger.info(f"Response: {response}")
        logger.info("Test 6 passed")
    except Exception as e:
        logger.error(f"Test 6 failed: {str(e)}", exc_info=True)
        raise


def test_07_titanic_spanish_names() -> None:
    """Test 7: Titanic agent with Spanish names query that caused 500 error."""
    logger.info("Test 7: Titanic agent with Spanish names query")
    try:
        from datasets import load_dataset

        model = create_model()
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            allow_dangerous_code=True,
            handle_parsing_errors=True,
            prefix="""You are a data analysis assistant. When analyzing the Titanic dataset:

1. First, understand the data structure:
   - Print and analyze the column names
   - Understand what each column represents
   - Note any data quality issues (missing values, etc.)

2. Then, plan your analysis:
   - Identify which columns are relevant to the question
   - Determine what calculations or filters are needed
   - Consider edge cases and data quality

3. Finally, execute your analysis:
   - Use ONLY the python_repl_ast tool
   - Keep code simple and direct
   - Always use print() for output
   - Handle missing values with dropna()
   - Format numbers with round(x, 2)

IMPORTANT: Name-based analysis is not available and will not be performed.
This is a deliberate privacy and ethical consideration to prevent potential discrimination
and protect passenger privacy. If asked about names, ethnicity, or nationality, politely
decline and explain that such analysis is not available for privacy reasons.

The dataset has these columns:
- has_survived: Whether the passenger survived (True/False)
- passenger_class: Passenger class (1, 2, or 3)
- is_male: Whether the passenger is male (True/False)
- age: Passenger age
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)""",
        )
        response = agent.invoke("How many last names of the passengers sounded spanish?")
        logger.info(f"Response: {response}")
        logger.info("Test 7 passed")
    except Exception as e:
        logger.error(f"Test 7 failed: {str(e)}", exc_info=True)
        raise


def test_08_model_parameters() -> None:
    """Test 8: Different model parameter combinations."""
    logger.info("Test 8: Testing different model parameters")
    try:
        # Test with minimal tokens
        logger.info("Testing with minimal tokens (100)")
        model = create_model(max_tokens=100)
        response = model.invoke("Say hello")
        logger.info(f"Response: {response}")

        # Test with maximum tokens
        logger.info("Testing with maximum tokens (8192)")
        model = create_model(max_tokens=8192)
        response = model.invoke("Say hello")
        logger.info(f"Response: {response}")

        # Test with different temperature
        logger.info("Testing with temperature 0.0")
        model = create_model(temperature=0.0)
        response = model.invoke("Say hello")
        logger.info(f"Response: {response}")

        logger.info("Test 8 passed")
    except Exception as e:
        logger.error(f"Test 8 failed: {str(e)}", exc_info=True)
        raise


def test_09_cli_specific_query() -> None:
    """Test 9: Test with the specific CLI query that's failing."""
    logger.info("Test 9: Testing with CLI-specific query")
    try:
        from datasets import load_dataset

        model = create_model()
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            allow_dangerous_code=True,
            prefix="""You are a data analysis assistant. When analyzing the Titanic dataset:

1. First, understand the data structure:
   - Print and analyze the column names
   - Understand what each column represents
   - Note any data quality issues (missing values, etc.)

2. Then, plan your analysis:
   - Identify which columns are relevant to the question
   - Determine what calculations or filters are needed
   - Consider edge cases and data quality

3. Finally, execute your analysis:
   - Use ONLY the python_repl_ast tool
   - Keep code simple and direct
   - Always use print() for output
   - Handle missing values with dropna()
   - Format numbers with round(x, 2)

The dataset has these columns:
- has_survived: Whether the passenger survived (True/False)
- passenger_class: Passenger class (1, 2, or 3)
- name: Passenger name
- is_male: Whether the passenger is male (True/False)
- age: Passenger age
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)""",
        )

        # Test with simpler queries first
        logger.info("Testing with simple query: How many females are in class 1?")
        response = agent.invoke("How many females are in class 1?")
        logger.info(f"Response: {response}")

        # Break down the complex query into steps
        logger.info("Testing step 1: Can you create a DataFrame of females in class 1?")
        response = agent.invoke("Create a DataFrame containing only females in class 1 and print its shape.")
        logger.info(f"Response: {response}")

        logger.info("Testing step 2: Can you show the age column of females in class 1?")
        response = agent.invoke("Print the age column for females in class 1.")
        logger.info(f"Response: {response}")

        logger.info("Testing step 3: Can you calculate the average age of females in class 1?")
        response = agent.invoke("Calculate and print the average age of females in class 1.")
        logger.info(f"Response: {response}")

        logger.info("Testing step 4: Can you find the maximum age of females in class 1 who survived?")
        response = agent.invoke("Find and print the maximum age among females in class 1 who survived.")
        logger.info(f"Response: {response}")

        logger.info("Test 9 passed")
    except Exception as e:
        logger.error(f"Test 9 failed: {str(e)}", exc_info=True)
        raise


def test_09_cli_specific_query_with_retry() -> None:
    """Test 10: Test with CLI-specific query and retry logic."""
    logger.info("Test 10: Testing with CLI-specific query and retry logic")
    try:
        from datasets import load_dataset

        model = create_model()
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()

        # Store the prefix separately
        agent_prefix = """You are a data analysis assistant. When analyzing the Titanic dataset:

1. First, understand the data structure:
   - Print and analyze the column names
   - Understand what each column represents
   - Note any data quality issues (missing values, etc.)

2. Then, plan your analysis:
   - Identify which columns are relevant to the question
   - Determine what calculations or filters are needed
   - Consider edge cases and data quality

3. Finally, execute your analysis:
   - Use ONLY the python_repl_ast tool
   - Keep code simple and direct
   - Always use print() for output
   - Handle missing values with dropna()
   - Format numbers with round(x, 2)

The dataset has these columns:
- has_survived: Whether the passenger survived (True/False)
- passenger_class: Passenger class (1, 2, or 3)
- name: Passenger name
- is_male: Whether the passenger is male (True/False)
- age: Passenger age
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"""

        query = "What was the age of the oldest surviving female in class 1?"
        logger.info(f"Testing with query: {query}")

        # Try with different model parameters
        for max_tokens in [2048, 4096, 8192]:
            logger.info(f"Trying with max_tokens={max_tokens}")
            model = create_model(max_tokens=max_tokens)
            agent = create_pandas_dataframe_agent(model, df, verbose=True, allow_dangerous_code=True, prefix=agent_prefix)
            try:
                response = agent.invoke(query)
                logger.info(f"Response with max_tokens={max_tokens}: {response}")
                break
            except Exception as e:
                logger.warning(f"Failed with max_tokens={max_tokens}: {str(e)}")
                continue

        logger.info("Test 10 passed")
    except Exception as e:
        logger.error(f"Test 10 failed: {str(e)}", exc_info=True)
        raise


def main() -> None:
    """Run all tests in sequence."""
    parser = argparse.ArgumentParser(description="Test Gemini API with increasing complexity")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load environment variables
    load_dotenv()

    # Run tests in sequence
    tests = [
        test_01_basic_model,
        test_02_simple_dataframe,
        test_03_minimal_agent,
        test_04_titanic_dataframe,
        test_05_titanic_agent_minimal,
        test_06_titanic_agent_full,
        test_07_titanic_spanish_names,
        test_08_model_parameters,
        test_09_cli_specific_query,
        test_09_cli_specific_query_with_retry,
    ]

    for i, test in enumerate(tests, 1):
        logger.info(f"\nRunning test {i}: {test.__name__}")
        try:
            test()
        except Exception as e:
            logger.error(f"Test {i} failed: {str(e)}")
            logger.info("Stopping tests due to failure")
            sys.exit(1)

    logger.info("\nAll tests completed successfully!")


if __name__ == "__main__":
    main()
