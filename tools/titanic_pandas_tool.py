from typing import Optional, Dict, Any
import pandas as pd
from langchain.tools import PandasDataFrameTool
from datasets import load_dataset

class TitanicPandasTool(PandasDataFrameTool):
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
- PassengerId: Unique identifier for each passenger
- Survived: Binary indicator (1 = survived, 0 = did not survive)
- Pclass: Passenger class (1 = First, 2 = Second, 3 = Third)
- Name: Passenger's full name
- Sex: Gender of the passenger
- Age: Age in years
- SibSp: Number of siblings/spouses aboard
- Parch: Number of parents/children aboard
- Ticket: Ticket number
- Fare: Passenger fare
- Cabin: Cabin number
- Embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

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
    
    def __init__(self):
        # Load the Titanic dataset directly from Hugging Face
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        
        # Calculate key statistics for the description
        total_passengers = len(df)
        survival_rate = (df['Survived'].mean() * 100)
        avg_age = df['Age'].mean()
        avg_fare = df['Fare'].mean()
        class_dist = df['Pclass'].value_counts().to_dict()
        
        # Update the description with actual statistics
        self.description = self.description.format(
            schema="\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()]),
            total_passengers=total_passengers,
            survival_rate=survival_rate,
            avg_age=avg_age,
            avg_fare=avg_fare,
            class_dist=class_dist
        )
        
        # Initialize the parent PandasDataFrameTool with our DataFrame
        super().__init__(
            df=df,
            name=self.name,
            description=self.description
        )

# Create a singleton instance
titanic_pandas_tool = TitanicPandasTool() 