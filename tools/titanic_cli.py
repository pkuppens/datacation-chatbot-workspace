import sys
import logging
from typing import List

# See: https://github.com/google/generative-ai-python/blob/main/google/generativeai/client.py
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.pandas_tools import create_pandas_agent
from google.api_core import exceptions as google_exceptions
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
        # Initialize the model and pandas agent
        logger.info("Initializing model and pandas agent...")
        # See: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini
        model = ChatGoogleGenerativeAI(
            model=config.model.name,
            temperature=config.model.temperature,
            max_tokens=config.model.max_tokens,
            top_p=config.model.top_p,
            top_k=config.model.top_k,
            convert_system_message_to_human=True,  # Required for Gemini
        )
        pandas_agent = create_pandas_agent(model)
        logger.info("Model and pandas agent initialized successfully")

        # Run the query using the pandas agent
        logger.info("Executing query using pandas agent...")
        result = pandas_agent.invoke(query)
        logger.info("Query executed successfully")
        print(result)
    except google_exceptions.InternalServerError as e:
        # See: https://developers.generativeai.google/guide/troubleshooting
        logger.error("Gemini API internal server error: %s", str(e))
        print("\nGemini API is currently experiencing issues. This is a temporary problem with the service.")
        print("For more information, please visit: https://developers.generativeai.google/guide/troubleshooting")
        print("Suggested actions:")
        print("1. Wait a few minutes and try again")
        print("2. Check the Gemini API status page")
        print("3. If the problem persists, try simplifying your query")
        sys.exit(1)
    except Exception as e:
        logger.error("Error executing query: %s", str(e), exc_info=True)
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    logger.info("Titanic CLI tool execution complete")


if __name__ == "__main__":
    main()
