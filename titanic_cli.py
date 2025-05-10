import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.titanic_agent import create_titanic_agent, record_analysis
from tools.knowledge import knowledge_base
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_api_key() -> str:
    """Get the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    return api_key


def create_model() -> ChatGoogleGenerativeAI:
    """Create and configure the language model."""
    return ChatGoogleGenerativeAI(
        model=config.model.name,
        google_api_key=get_api_key(),
        temperature=config.model.temperature,
        max_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k,
        convert_system_message_to_human=True,
    )


def main(question: Optional[str] = None) -> None:
    """Main function to run the Titanic analysis CLI.

    Args:
        question: Optional question to analyze. If not provided, will prompt user.
    """
    try:
        # Load environment variables
        load_dotenv()

        # Create model and agent
        model = create_model()
        agent = create_titanic_agent(model)

        # Get question from user if not provided
        if not question:
            print("\nTitanic Dataset Analysis CLI")
            print("Enter your question about the Titanic dataset (or 'quit' to exit)")
            question = input("\nQuestion: ").strip()

            if question.lower() == "quit":
                print("Goodbye!")
                return

        # Run the analysis
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
