import chainlit as cl
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17")

# Initialize tools
search_tool = DuckDuckGoSearchRun()

# Create the agent with tools and memory
checkpointer = InMemorySaver()
agent = create_react_agent(
    llm=llm,
    tools=[search_tool],
    prompt=f"You are a helpful assistant. Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
    checkpointer=checkpointer
)

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    
    # Create config with thread_id for conversation history
    config = RunnableConfig(
        callbacks=[cl.AsyncLangchainCallbackHandler()],
        configurable={"thread_id": message.id}
    )
    
    # Stream the response
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": message.content}]},
        config=config,
        stream_mode="messages"
    ):
        if isinstance(chunk, dict) and "content" in chunk:
            await msg.stream_token(chunk["content"])
    
    await msg.send()

def main():
    from chainlit.cli import run_chainlit
    from chainlit.config import config as chainlit_config

    chainlit_config.run.watch = True
    run_chainlit(str(__file__))

if __name__ == "__main__":
    main()
