from typing import Optional, List, Dict, Any
from langchain.tools import BaseTool
from langchain_core.tools import tool
from .database import titanic_db

class TitanicDatabaseTool(BaseTool):
    name: str = "titanic_database"
    description: str = """A tool to query the Titanic dataset. Use this to get information about passengers, survival rates, and other statistics.
    
    Database Schema:
    {schema}
    
    You can ask about:
    - Survival rates
    - Passenger counts
    - Class distribution
    - Average age
    - Any other statistics about the passengers
    """.format(schema=titanic_db.get_schema_description())
    
    def _run(self, query: str) -> str:
        """Execute the query and return results as a string."""
        try:
            # Basic query parsing
            if "survival rate" in query.lower():
                survival_rate = titanic_db.get_survival_rate()
                return f"The overall survival rate on the Titanic was {survival_rate:.2f}%"
            
            elif "passenger count" in query.lower():
                count = titanic_db.get_passenger_count()
                return f"There were {count} passengers on the Titanic"
            
            elif "class distribution" in query.lower():
                class_dist = titanic_db.get_class_distribution()
                return f"Passenger class distribution: {class_dist}"
            
            elif "average age" in query.lower():
                avg_age = titanic_db.get_average_age()
                return f"The average age of passengers was {avg_age:.2f} years"
            
            elif "schema" in query.lower() or "structure" in query.lower():
                return titanic_db.get_schema_description()
            
            else:
                return """I can help you with:
                - Survival rates
                - Passenger counts
                - Class distribution
                - Average age
                - Database schema and structure
                Please rephrase your question."""
                
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation of _run."""
        return self._run(query)

# Create a singleton instance
titanic_tool = TitanicDatabaseTool() 