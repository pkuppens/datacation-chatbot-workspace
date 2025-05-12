"""Pandas tools for data analysis."""

import warnings
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.titanic_agent import create_titanic_agent

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Convert_system_message_to_human will be deprecated!")


def create_pandas_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Create a pandas DataFrame agent for data analysis.

    This is a wrapper around create_titanic_agent for backward compatibility.
    New code should use create_titanic_agent directly.

    Args:
        model: The language model to use for reasoning

    Returns:
        A pandas DataFrame agent
    """
    return create_titanic_agent(model)
