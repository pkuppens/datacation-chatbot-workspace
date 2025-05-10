"""Titanic agent module - single source of truth for Titanic dataset analysis."""
import logging
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from data_pipeline.titanic_pipeline import get_titanic_data
from tools.knowledge import knowledge_base, DataInsight, AnalysisStep
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_titanic_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Create a pandas DataFrame agent for Titanic dataset analysis.
    
    This is the single source of truth for creating the Titanic analysis agent.
    All other modules should use this function to create the agent.
    
    Args:
        model: The language model to use for reasoning
        
    Returns:
        A pandas DataFrame agent configured for Titanic analysis
    """
    logger.info("Loading Titanic dataset from data pipeline")
    df = get_titanic_data()
    
    logger.info("Creating pandas DataFrame agent")
    agent = create_pandas_dataframe_agent(
        model,
        df,
        verbose=True,
        handle_parsing_errors=True,
        allow_dangerous_code=True,  # Required for pandas agent to work
        prefix="""You are a data analysis assistant. When analyzing the Titanic dataset:

1. First, understand the data structure:
   - Print and analyze the column names
   - Understand what each column represents
   - Note any data quality issues (missing values, etc.)
   - Store insights about the data structure

2. Then, plan your analysis:
   - Identify which columns are relevant to the question
   - Determine what calculations or filters are needed
   - Consider edge cases and data quality
   - Check for similar past analyses

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
- Survived: Whether the passenger survived (1 = Yes, 0 = No)
- Pclass: Passenger class (1, 2, or 3)
- Sex: Passenger sex (male or female)
- Age: Passenger age
- SibSp: Number of siblings/spouses aboard
- Parch: Number of parents/children aboard
- Ticket: Ticket number
- Fare: Passenger fare
- Cabin: Cabin number
- Embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"""
    )
    
    return agent

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
            source="direct_analysis"
        )
    ]
    
    # Record the analysis step
    step = AnalysisStep(
        timestamp=datetime.now().isoformat(),
        question=question,
        approach=approach,
        code=code,
        result=result,
        insights=insights
    )
    
    knowledge_base.record_analysis(step) 