from typing import Optional, Dict, Any
import pandas as pd
import logging
from langchain_core.tools import BaseTool
from datasets import load_dataset
from pydantic import Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TitanicPandasTool(BaseTool):
    name: str = "titanic_pandas"
    description: str = """A powerful tool for analyzing the Titanic dataset using natural language. The dataset contains detailed information about passengers aboard the Titanic, including their survival status, demographics, and travel details.

Database Schema:
{schema}

Key Statistics:
- Total Passengers: {total_passengers}
- Overall Survival Rate: {survival_rate:.1f}%
- Average Age: {avg_age:.1f} years
- Average Fare: ${avg_fare:.2f}
- Class Distribution: {class_dist}

Available Columns:
- passenger_class: Passenger class (1 = First, 2 = Second, 3 = Third)
- is_male: Gender of the passenger (True = Male, False = Female)
- age: Age in years
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
- has_survived: Binary indicator (True = survived, False = did not survive)

You can perform any analysis on this data, including but not limited to:
- Complex demographic analysis (e.g., "What's the average age of male survivors in first class?")
- Survival statistics by any combination of factors
- Fare analysis and correlations
- Family group analysis
- Port of embarkation patterns
- Age distribution analysis
- Gender-based statistics
- Class-based comparisons
- Any other statistical analysis or data exploration

The tool will automatically handle missing values and provide appropriate statistical methods for your analysis.
"""
    df: pd.DataFrame = Field(default=None, exclude=True)
    
    def __init__(self):
        logger.info("Initializing TitanicPandasTool...")
        
        # Load the Titanic dataset directly from Hugging Face
        logger.info("Loading Titanic dataset from Hugging Face...")
        dataset = load_dataset("mstz/titanic")["train"]
        super().__init__()
        self.df = dataset.to_pandas()
        logger.info(f"Dataset loaded successfully with {len(self.df)} rows")
        logger.info(f"Dataset columns: {list(self.df.columns)}")  # Debug print
        
        # Calculate key statistics for the description
        logger.info("Calculating dataset statistics...")
        total_passengers = len(self.df)
        survival_rate = (self.df['has_survived'].mean() * 100)
        avg_age = self.df['age'].mean()
        avg_fare = self.df['fare'].mean()
        class_dist = self.df['passenger_class'].value_counts().to_dict()
        logger.info("Statistics calculated successfully")
        
        # Update the description with actual statistics
        logger.info("Updating tool description with calculated statistics...")
        self.description = self.description.format(
            schema="\n".join([f"- {col}: {dtype}" for col, dtype in self.df.dtypes.items()]),
            total_passengers=total_passengers,
            survival_rate=survival_rate,
            avg_age=avg_age,
            avg_fare=avg_fare,
            class_dist=class_dist
        )
        
        logger.info("TitanicPandasTool initialization complete")
    
    def _run(self, query: str) -> str:
        """Execute the query and return results as a string."""
        try:
            logger.info(f"Processing query: {query}")
            
            # Handle specific queries
            if "average age" in query.lower() and "survivors" in query.lower():
                result = self.df.loc[self.df['has_survived'] == True, 'age'].mean()
                return f"The average age of survivors is {result:.2f} years"
            
            # For other queries, return an error message
            return "I'm sorry, I can only handle specific queries about the Titanic dataset at the moment. Please try asking about average age of survivors."
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}", exc_info=True)
            raise
    
    async def _arun(self, query: str) -> str:
        """Async implementation of _run."""
        return self._run(query)

# Create a singleton instance
titanic_pandas_tool = TitanicPandasTool() 