import chainlit as cl
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from tools import titanic_tool

# Initialize the LLM with Gemini Pro model
# See: https://python.langchain.com/docs/integrations/chat/google_generative_ai
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17")

# Initialize DuckDuckGo search tool
# See: https://python.langchain.com/docs/integrations/tools/ddg
# Parameters: max_results (int, default=5) - Number of results to return
search_tool = DuckDuckGoSearchRun(max_results=3)

# Create the agent with tools and memory
# See: https://langchain-ai.github.io/langgraph/agents/agents/#basic-configuration
checkpointer = InMemorySaver()  # In-memory conversation history
agent = create_react_agent(
    model=llm,  # LLM to use for reasoning
    tools=[search_tool, titanic_tool],  # List of tools the agent can use
    prompt=f"""You are a helpful assistant. Today's date is {datetime.now().strftime('%Y-%m-%d')}.
    When answering questions:
    1. Be concise and to the point
    2. Avoid raw search results or lengthy descriptions
    3. Focus on the most relevant information
    4. Use bullet points for multiple data points
    5. For Titanic-related questions, use the titanic_database tool""",
    checkpointer=checkpointer  # For conversation history
)

@cl.on_message
async def on_message(message: cl.Message):
    # See: https://docs.chainlit.io/concepts/message
    msg = cl.Message(content="")
    await msg.send()  # Send empty message first to start the stream
    
    # Configure streaming with thread_id for conversation history
    # See: https://langchain-ai.github.io/langgraph/agents/memory/#short-term-memory
    config = RunnableConfig(
        callbacks=[cl.AsyncLangchainCallbackHandler()],  # For streaming UI updates
        configurable={"thread_id": message.id}  # Unique ID for conversation thread
    )
    
    # Stream the response token by token
    # See: https://langchain-ai.github.io/langgraph/agents/agents/#streaming
    full_response = ""
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": message.content}]},  # Format: {"role": "user/assistant", "content": "..."}
        config=config,
        stream_mode="messages"
    ):
        # Handle AIMessageChunk tuple (message, metadata)
        if isinstance(chunk, tuple) and len(chunk) == 2:
            message_chunk, metadata = chunk
            if hasattr(message_chunk, 'content'):
                content = message_chunk.content
                full_response += content
                await msg.stream_token(content)
    
    # Add the full response as a separate message for reference
    if full_response:
        # Format the response in a more readable way
        formatted_response = full_response.replace("...", "").strip()
        await cl.Message(
            content=f"Full response:\n```\n{formatted_response}\n```",
            parent_id=msg.id
        ).send()
    else:
        # If no response was captured, show the raw chunk for debugging
        await cl.Message(
            content="No response content was captured. Please check the console for chunk structure.",
            parent_id=msg.id
        ).send()

def main():
    # See: https://docs.chainlit.io/get-started/run-your-app
    from chainlit.cli import run_chainlit
    from chainlit.config import config as chainlit_config

    chainlit_config.run.watch = True  # Auto-reload on file changes
    run_chainlit(str(__file__))

if __name__ == "__main__":
    main()
