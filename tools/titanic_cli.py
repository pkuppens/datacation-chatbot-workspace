import sys
import logging
from typing import List
from tools.titanic_pandas_tool import titanic_pandas_tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main(args: List[str] = None) -> None:
    """
    CLI tool for querying the Titanic dataset.
    
    Usage:
        titanic [query words...]
        
    If no query is provided, runs a default example query.
    Multiple words are concatenated into a single query string.
    """
    logger.info("Starting Titanic CLI tool...")
    
    if args is None:
        args = sys.argv[1:]
    
    # If no arguments provided, use a default example query
    if not args:
        query = "What is the average age of survivors by passenger class?"
        logger.info("No query provided, using default query: %s", query)
    else:
        # Concatenate all arguments into a single query string
        query = " ".join(args)
        logger.info("Processing user query: %s", query)
    
    try:
        # Run the query using the pandas tool
        logger.info("Executing query using TitanicPandasTool...")
        result = titanic_pandas_tool.run(query)
        logger.info("Query executed successfully")
        print(result)
    except Exception as e:
        logger.error("Error executing query: %s", str(e), exc_info=True)
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    logger.info("Titanic CLI tool execution complete")

if __name__ == "__main__":
    main() 