"""Titanic agent module - single source of truth for Titanic dataset analysis."""
import logging
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from datasets import load_dataset
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
    logger.info("Loading Titanic dataset from Hugging Face")
    dataset = load_dataset("mstz/titanic")["train"]
    df = dataset.to_pandas()
    
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

4. Document your findings:
   - Explain your reasoning
   - Note any interesting patterns
   - Store insights for future reference
   - Record the analysis step

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
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

Example workflow:
1. First, verify the data structure:
```python
print("Columns:", df.columns.tolist())
print("\nSample data:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
```

2. Then, analyze the data:
```python
# Example: Count survivors by class
result = df.groupby('passenger_class')['has_survived'].mean()
print(result)
```

3. Finally, document findings:
- Note any patterns in the data
- Store insights for future questions
- Consider data quality issues

Remember to:
1. Always start by understanding the data structure
2. Plan your analysis before writing code
3. Document your findings and insights
4. Learn from past analyses"""
    )
    logger.info("Successfully created pandas DataFrame agent")
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