"""Pandas tools for data analysis."""

import warnings
import logging
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.titanic_agent import create_titanic_agent, record_analysis

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Convert_system_message_to_human will be deprecated!")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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


def record_analysis(question: str, approach: str, code: str, result: str) -> None:
    """Record an analysis step in the knowledge base.

    Args:
        question: The question being analyzed
        approach: The approach taken
        code: The code used
        result: The result obtained
    """
    # Create insights from the analysis
    insights = [
        DataInsight(
            timestamp=datetime.now().isoformat(),
            category="data_structure",
            description="Column names and data types",
            evidence=code,
            confidence=1.0,
            source="direct_analysis",
        )
    ]

    # Record the analysis step
    step = AnalysisStep(
        timestamp=datetime.now().isoformat(), question=question, approach=approach, code=code, result=result, insights=insights
    )

    knowledge_base.record_analysis(step)
