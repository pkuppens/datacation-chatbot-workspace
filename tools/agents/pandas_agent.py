"""Pandas agent for data analysis.

This module provides a pandas agent configured for analyzing the Titanic dataset,
with proper tools and error handling.
"""

from langchain.agents import create_pandas_dataframe_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from config import config
import pandas as pd
from utils.logger import logger


def create_pandas_agent(model: ChatGoogleGenerativeAI, df: pd.DataFrame) -> Tool:
    """Create a pandas agent for data analysis.

    Args:
        model: The language model to use
        df: The DataFrame to analyze

    Returns:
        A Tool configured for pandas analysis
    """
    try:
        # Create the pandas agent
        agent = create_pandas_dataframe_agent(llm=model, df=df, verbose=True, handle_parsing_errors=True, max_iterations=3)

        # Create the tool
        return Tool(
            name="pandas_analysis",
            description="""Use this tool for analyzing the Titanic dataset.
            It can perform statistical analysis, filtering, and data exploration.
            Always show your work and explain your reasoning.""",
            func=agent.run,
        )

    except Exception as e:
        logger.error(f"Error creating pandas agent: {str(e)}")
        raise
