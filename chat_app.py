import chainlit as cl
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from tools.pandas_tools import create_pandas_agent
import logging
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the model
model = ChatGoogleGenerativeAI(
    model=config.model.name,
    temperature=config.model.temperature,
    max_tokens=config.model.max_tokens,
    top_p=config.model.top_p,
    top_k=config.model.top_k,
    convert_system_message_to_human=True
)

# Initialize search tool
search_tool = DuckDuckGoSearchRun(max_results=3)
logger.info("Initialized search tool")

# Initialize pandas agent
logger.info("Initializing pandas agent...")
pandas_agent = create_pandas_agent(model)
logger.info("Pandas agent initialized successfully")

# Create the agent with tools and memory
# See: https://langchain-ai.github.io/langgraph/agents/agents/#basic-configuration
checkpointer = InMemorySaver()  # In-memory conversation history
agent = create_react_agent(
    model=model,  # LLM to use for reasoning
    tools=[search_tool, pandas_agent],  # List of tools the agent can use
    prompt=f"""You are a helpful assistant. Today's date is {datetime.now().strftime('%Y-%m-%d')}.
    When answering questions:
    1. Be concise and to the point
    2. Avoid raw search results or lengthy descriptions
    3. Focus on the most relevant information
    4. Use bullet points for multiple data points
    5. For Titanic-related questions:
       - Use the pandas agent for data analysis (age, survival, class, etc.)
       - Use the search tool for general knowledge questions
    6. For data analysis:
       - Show your work and explain your reasoning
       - Handle missing values appropriately
       - Format numbers to 2 decimal places where appropriate""",
    checkpointer=checkpointer  # For conversation history
)
logger.info("Initialized main agent with search tool and pandas agent")

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    try:
        logger.info(f"Processing message: {message.content}")
        
        # Configure the agent with thread_id for conversation history
        config = RunnableConfig(
            configurable={
                "thread_id": message.id,  # Use message ID as thread ID
                "checkpoint_ns": "chat",  # Namespace for checkpoints
                "checkpoint_id": message.id  # Use message ID as checkpoint ID
            }
        )
        
        # Use the main agent for all queries
        logger.info("Using main agent with all tools")
        response = await agent.ainvoke(message.content, config=config)
        logger.info("Agent response received")
        
        # Send the response
        await cl.Message(
            content=response,
            author="Assistant"
        ).send()
        logger.info("Response sent to user")
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        await cl.Message(
            content="I apologize, but I encountered an error processing your request. Please try again.",
            author="Assistant"
        ).send()

def main():
    # See: https://docs.chainlit.io/get-started/run-your-app
    from chainlit.cli import run_chainlit
    from chainlit.config import config as chainlit_config

    chainlit_config.run.watch = True  # Auto-reload on file changes
    run_chainlit(str(__file__))

if __name__ == "__main__":
    main()
