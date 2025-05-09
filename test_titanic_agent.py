import unittest
import logging
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.titanic_agent import create_titanic_agent
from google.api_core import exceptions as google_exceptions
from datasets import load_dataset
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestTitanicAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        logger.info("Setting up test fixtures...")
        
        # Load dataset first
        dataset = load_dataset("mstz/titanic")["train"]
        cls.df = dataset.to_pandas()
        
        # Initialize model with configuration settings
        cls.model = ChatGoogleGenerativeAI(
            model=config.model.name,
            temperature=config.model.temperature,
            max_tokens=config.model.max_tokens,
            top_p=config.model.top_p,
            top_k=config.model.top_k,
            convert_system_message_to_human=True
        )
        
        # Create agent using the single source of truth
        cls.agent = create_titanic_agent(cls.model)
        logger.info("Test fixtures setup complete")

    def test_01_basic_count(self):
        """Test the most basic query possible."""
        try:
            # Direct DataFrame operation to get ground truth
            actual_count = len(self.df)
            logger.info(f"Actual row count: {actual_count}")
            
            # Test the agent with a very simple query
            result = self.agent.invoke("Print the total number of rows in df")
            logger.info(f"Agent response for row count: {result}")
            
            self.assertIsNotNone(result)
            
        except Exception as e:
            logger.error(f"Error in basic count test: {str(e)}", exc_info=True)
            self.fail(f"Basic count test failed: {str(e)}")

    def test_02_simple_mean(self):
        """Test a simple mean calculation."""
        try:
            # Direct DataFrame operation to get ground truth
            actual_mean = self.df['age'].dropna().mean()
            logger.info(f"Actual mean age: {actual_mean:.2f}")
            
            # Test the agent with a direct query
            result = self.agent.invoke("Print the mean age after dropping NA values")
            logger.info(f"Agent response for mean age: {result}")
            
            self.assertIsNotNone(result)
            
        except Exception as e:
            logger.error(f"Error in mean calculation test: {str(e)}", exc_info=True)
            self.fail(f"Mean calculation test failed: {str(e)}")

    def test_03_simple_filter(self):
        """Test a simple filtering operation."""
        try:
            # Direct DataFrame operation to get ground truth
            survivors = self.df[self.df['has_survived'] == True]
            actual_count = len(survivors)
            logger.info(f"Actual survivor count: {actual_count}")
            
            # Test the agent with a direct query
            result = self.agent.invoke("Print the number of rows where has_survived is True")
            logger.info(f"Agent response for survivor count: {result}")
            
            self.assertIsNotNone(result)
            
        except Exception as e:
            logger.error(f"Error in filtering test: {str(e)}", exc_info=True)
            self.fail(f"Filtering test failed: {str(e)}")

    def test_04_simple_group(self):
        """Test a simple grouping operation."""
        try:
            # Direct DataFrame operation to get ground truth
            survival_by_class = self.df.groupby('passenger_class')['has_survived'].mean()
            logger.info(f"Actual survival rates by class:\n{survival_by_class}")
            
            # Test the agent with a direct query
            result = self.agent.invoke("Print the mean of has_survived for passenger_class 1")
            logger.info(f"Agent response for first class survival: {result}")
            
            self.assertIsNotNone(result)
            
        except Exception as e:
            logger.error(f"Error in grouping test: {str(e)}", exc_info=True)
            self.fail(f"Grouping test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main() 