"""Command line interface for Titanic dataset analysis.

This script provides a command-line interface for analyzing the Titanic dataset
using the project's data analysis tools. It focuses specifically on data analysis
capabilities and does not handle general queries about the Titanic.
"""

import sys
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.titanic_agent import create_titanic_agent, record_analysis
from tools.knowledge import knowledge_base
from config import config
from utils.logger import setup_logger

# Set up project-wide logger
logger = setup_logger(name="titanic_data_analyst_cli", log_file="logs/titanic_data_analyst_cli.log")


def create_model() -> ChatGoogleGenerativeAI:
    """Create and configure the language model."""
    return ChatGoogleGenerativeAI(
        model=config.model.name,
        google_api_key=config.google_api_key,
        temperature=config.model.temperature,
        max_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k,
        convert_system_message_to_human=True,
    )


def main(args: Optional[List[str]] = None) -> None:
    """Main function to run the Titanic data analysis CLI.

    Args:
        args: Optional list of command line arguments. If not provided, sys.argv[1:] is used.
    """
    try:
        # Load environment variables
        load_dotenv()

        if args is None:
            args = sys.argv[1:]

        # Create model and agent
        model = create_model()
        agent = create_titanic_agent(model)

        # Get question from user if not provided
        if not args:
            print("\nTitanic Dataset Analysis CLI")
            print("Enter your question about the Titanic dataset (or 'quit' to exit)")
            question = input("\nQuestion: ").strip()

            if question.lower() == "quit":
                print("Goodbye!")
                return
        else:
            question = " ".join(args)

        # Run the analysis
        logger.info(f"Processing query: {question}")
        print("\nAnalyzing...")
        result = agent.run(question)

        # Record the analysis
        record_analysis(
            question=question,
            approach="pandas_analysis",
            code=result,  # Note: This is simplified, in practice we'd want to extract the actual code used
            result=result,
        )

        # Print result
        print("\nResult:")
        print(result)

        # Show similar past analyses
        similar = knowledge_base.get_similar_analyses(question)
        if similar:
            print("\nSimilar past analyses:")
            for analysis in similar:
                print(f"\nQuestion: {analysis.question}")
                print(f"Result: {analysis.result}")

    except Exception as e:
        logger.error(f"Error in Titanic analysis: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
