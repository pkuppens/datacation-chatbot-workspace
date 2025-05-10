"""Main application file for the Datacation Chatbot.

This module provides the main entry point for the Chainlit chat application,
coordinating the UI, agent, and message handling components.
"""

import chainlit as cl
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from config import config
import json
from typing import Dict, List, Optional, Any
import functools
import traceback

from utils.directory_utils import ensure_directories
from utils.code_runner import CodeRunner
from utils.logger import logger
from tools.agents.pandas_agent import create_pandas_agent

# Ensure directories exist at application startup
ensure_directories()


class MessageManager:
    """Singleton class to handle message updates consistently.

    This class provides a centralized way to handle message updates in Chainlit,
    ensuring consistent behavior across the application and making it easier to
    adapt to changes in the Chainlit API.

    Attributes:
        _instance: The singleton instance of the MessageManager.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageManager, cls).__new__(cls)
        return cls._instance

    @staticmethod
    async def update_message(message: cl.Message, content: str) -> None:
        """Update a message's content safely.

        Args:
            message: The Chainlit message to update
            content: The new content for the message

        Note:
            This method handles the update in a way that's compatible with
            Chainlit 2.5.5's message update interface.
        """
        try:
            await message.update()
            message.content = content
        except Exception as e:
            logger.error(f"Error updating message: {str(e)}", exc_info=True)
            # Fallback to creating a new message if update fails
            await cl.Message(content=content, author=message.author).send()

    @staticmethod
    def log_error(func):
        """Decorator to log errors with full context.

        This decorator wraps async functions to provide detailed error logging,
        including function name, arguments, and full traceback.

        Args:
            func: The async function to wrap

        Returns:
            The wrapped function with enhanced error logging
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}: {str(e)}\nArgs: {args}\nKwargs: {kwargs}\nTraceback: {traceback.format_exc()}"
                )
                raise

        return wrapper


class ChatUI:
    """Handles all UI-related functionality for the chat interface.

    This class manages the display and updates of various UI elements,
    including technical details, thought process, and error messages.
    It uses the MessageManager for consistent message handling.

    Attributes:
        technical_msg: Message displaying token usage and tool information
        thoughts_msg: Message showing the agent's thought process
        message_manager: Instance of MessageManager for message updates
    """

    def __init__(self):
        self.technical_msg = None
        self.thoughts_msg = None
        self.message_manager = MessageManager()

    @MessageManager.log_error
    async def initialize_technical_details(self):
        """Initialize the technical details message with token usage and tool information.

        Creates a new message to display technical information about the chat session,
        including token usage statistics and tools used. This message will be updated
        throughout the conversation.
        """
        self.technical_msg = cl.Message(
            content="**Technical Details**\n\n**Token Usage**\nInput tokens: 0\nOutput tokens: 0\nTotal tokens: 0\n\n**Tools Used**\nNone",
            author="System",
        )
        await self.technical_msg.send()

    @MessageManager.log_error
    async def update_technical_details(self, token_usage: Dict[str, int], tool_calls: List[Dict]):
        """Update the technical details message with new token usage and tool information.

        Args:
            token_usage: Dictionary containing input, output, and total token counts
            tool_calls: List of tools used in the current interaction
        """
        if not self.technical_msg:
            return

        content = "**Technical Details**\n\n"
        content += "**Token Usage**\n"
        content += f"Input tokens: {token_usage.get('input_tokens', 0)}\n"
        content += f"Output tokens: {token_usage.get('output_tokens', 0)}\n"
        content += f"Total tokens: {token_usage.get('total_tokens', 0)}\n\n"
        content += "**Tools Used**\n"

        if tool_calls:
            content += "\n".join([f"• {call['name']}" for call in tool_calls])
        else:
            content += "None"

        await self.message_manager.update_message(self.technical_msg, content)

    @MessageManager.log_error
    async def display_suggested_prompts(self):
        """Display suggested prompts as interactive buttons.

        Creates a message with clickable action buttons for each suggested prompt.
        These buttons allow users to quickly start common queries.
        """
        elements = [
            cl.Action(name=prompt, label=prompt, payload={"prompt": prompt}, description=f"Click to ask: {prompt}")
            for prompt in SUGGESTED_PROMPTS
        ]

        await cl.Message(
            content="**Suggested Prompts**\nClick any prompt below to get started:", author="System", elements=elements
        ).send()

    @MessageManager.log_error
    async def start_thought_process(self):
        """Start displaying the agent's thought process.

        Creates a new message to show the agent's thinking process,
        which will be updated as the agent processes the request.

        The thought process includes:
        1. Initial "Thinking..." state
        2. Updates as the agent:
           - Analyzes the question
           - Decides which tools to use
           - Processes intermediate results
           - Formulates the final response
        3. Final "Analysis Complete" state

        This provides transparency into the agent's decision-making process
        and helps users understand how their query is being processed.
        """
        self.thoughts_msg = cl.Message(content="🤔 **Analyzing your question...**", author="Assistant")
        await self.thoughts_msg.send()

    @MessageManager.log_error
    async def update_thought_process(self, thought: str, is_tool_call: bool = False):
        """Update the thought process message with new information.

        Args:
            thought: The current thought or processing step to display
            is_tool_call: Whether this update is about a tool being called
        """
        if self.thoughts_msg:
            # Format tool calls differently
            if is_tool_call:
                content = f"🔧 **Using tool:** {thought}"
            else:
                content = f"💭 **Thinking:** {thought}"

            await self.message_manager.update_message(self.thoughts_msg, content)

    @MessageManager.log_error
    async def end_thought_process(self):
        """End the thought process display.

        Updates the thought process message to indicate completion
        and cleans up the message reference.
        """
        if self.thoughts_msg:
            await self.message_manager.update_message(self.thoughts_msg, "✅ **Analysis Complete**")
            self.thoughts_msg = None

    @MessageManager.log_error
    async def display_error(self, error_msg: str):
        """Display an error message to the user.

        Args:
            error_msg: The error message to display
        """
        await cl.Message(content=f"I apologize, but I encountered an error: {error_msg}", author="Assistant").send()


class ChatAgent:
    """Handles agent-related functionality for processing user queries.

    This class manages the AI agent, its tools, and the processing of user messages.
    It coordinates with the ChatUI class to display progress and results.

    Attributes:
        model: The language model used for processing
        search_tool: Tool for web searches
        pandas_agent: Tool for data analysis
        pandas_tool: Wrapped pandas agent for the agent system
        checkpointer: For saving agent state
        agent: The main agent instance
    """

    def __init__(self):
        """Initialize the chat agent with tools and configuration.

        The agent is configured with:
        - Python REPL tool for data analysis
        - Detailed logging of thought process
        - Port mapping for embarkation locations
        - Error handling and retry logic
        """
        # Configure logging for the agent
        self.logger = logging.getLogger("chat_agent")
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler for detailed logging
        fh = logging.FileHandler("agent.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Port mapping for embarkation locations
        self.port_mapping = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}

        # Initialize tools
        self.tools = [
            Tool(
                name="python_repl_ast",
                func=self._run_python_code,
                description="""Use this tool to run Python code for data analysis.
                The code should be a complete, executable Python statement.
                Use pandas (df) for data manipulation.
                Always print the results of your analysis.""",
            )
        ]

        # Create the agent with enhanced configuration
        self.agent = AgentExecutor.from_agent_and_tools(
            agent=self._create_agent(),
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            return_intermediate_steps=True,
        )

    def _create_agent(self) -> Agent:
        """Create the agent with enhanced configuration.

        Returns:
            An agent configured with:
            - Detailed thought process logging
            - Port mapping awareness
            - Error handling
        """
        return Agent(
            llm_chain=self._create_llm_chain(),
            allowed_tools=[tool.name for tool in self.tools],
            handle_parsing_errors=True,
            verbose=True,
            return_intermediate_steps=True,
            thought_logger=self.logger,
        )

    async def _run_python_code(self, code: str) -> str:
        """Run Python code and log the execution.

        Args:
            code: The Python code to execute

        Returns:
            The output of the code execution

        Note:
            This method logs the code execution and any errors that occur.
            It also handles port mapping for embarkation locations.
        """
        try:
            self.logger.debug(f"Executing Python code: {code}")
            result = await self._execute_python_code(code)

            # Check if the result contains port codes
            if isinstance(result, str) and any(port in result for port in self.port_mapping.keys()):
                self.logger.info(f"Detected port codes in result: {result}")
                # Log the mapping for debugging
                for code, name in self.port_mapping.items():
                    if code in result:
                        self.logger.info(f"Mapped port code {code} to {name}")

            return result
        except Exception as e:
            self.logger.error(f"Error executing Python code: {str(e)}", exc_info=True)
            raise e

    async def process_message(self, message: cl.Message, ui: ChatUI) -> tuple[Optional[str], List[Dict], Dict[str, int]]:
        """Process a user message and return the response, tool calls, and token usage.

        Args:
            message: The user's message to process
            ui: The ChatUI instance for displaying progress

        Returns:
            A tuple containing:
            - The final answer (str or None)
            - List of tool calls made
            - Dictionary of token usage statistics
        """
        config = RunnableConfig(configurable={"thread_id": message.id, "checkpoint_ns": "chat", "checkpoint_id": message.id})

        try:
            # Update thought process with initial analysis
            await ui.update_thought_process("Analyzing your question...")

            response = await self.agent.ainvoke({"messages": message.content}, config=config)

            final_answer = None
            tool_calls = []
            token_usage = {}

            if isinstance(response, dict) and "messages" in response:
                messages = response["messages"]
                for msg_obj in messages:
                    # Handle thought process
                    if hasattr(msg_obj, "thought"):
                        await ui.update_thought_process(msg_obj.thought)

                    # Handle tool calls
                    if hasattr(msg_obj, "tool_calls"):
                        tool_calls.extend(msg_obj.tool_calls)
                        for call in msg_obj.tool_calls:
                            # Format tool call parameters if available
                            params = call.get("parameters", {})
                            param_str = f" with parameters: {json.dumps(params)}" if params else ""
                            await ui.update_thought_process(f"{call['name']}{param_str}", is_tool_call=True)

                    # Handle tool outputs
                    if hasattr(msg_obj, "tool_output"):
                        await ui.update_thought_process(f"Tool output: {msg_obj.tool_output}")

                    # Handle final answer
                    if hasattr(msg_obj, "content") and msg_obj.content:
                        final_answer = msg_obj.content
                        await ui.update_thought_process(f"Formulating response: {msg_obj.content[:100]}...")

                    # Handle token usage
                    if hasattr(msg_obj, "usage_metadata"):
                        token_usage = msg_obj.usage_metadata

            return final_answer, tool_calls, token_usage

        except Exception as e:
            raise e


# Initialize UI and Agent
ui = ChatUI()
agent = ChatAgent()


@cl.on_chat_start
@MessageManager.log_error
async def start():
    """Initialize the chat session.

    This function is called when a new chat session starts.
    It sets up the technical details display and shows suggested prompts.
    """
    # Ensure directories exist
    ensure_directories()

    # Initialize technical details
    await ui.initialize_technical_details()

    # Display suggested prompts
    await ui.display_suggested_prompts()


@cl.on_message
@MessageManager.log_error
async def handle_message(message: cl.Message):
    """Handle incoming messages from users and process them through the agent.

    This function coordinates the entire message processing pipeline:
    1. Receives user input
    2. Creates a response message for streaming
    3. Processes the message through the agent
    4. Streams the agent's response
    5. Updates technical details

    The agent's response is processed in several stages:
    1. Question analysis and tool selection
    2. Data processing and analysis
    3. Response generation
    4. Privacy and formatting checks

    Args:
        message: The user's message to process

    Note:
        The agent's response is streamed in real-time, allowing users to see
        the response as it's generated. This provides immediate feedback and
        a more interactive experience.
    """
    try:
        logger.info(f"Processing message: {message.content}")

        # Start the thought process before any processing
        await ui.start_thought_process()

        # Process the message through the agent
        # This includes question analysis, tool selection, and response generation
        final_answer, tool_calls, token_usage = await agent.process_message(message, ui)

        # Create a message for the response
        # This message will be updated with the streaming response
        msg = cl.Message(content="", author="Assistant")
        await msg.send()

        # Stream the agent's response
        # The response is generated with proper formatting and privacy checks
        if final_answer:
            await msg.stream_token(final_answer)

        # End the thought process after the response is complete
        await ui.end_thought_process()

        # Update technical details with token usage and tool information
        if token_usage:
            await ui.update_technical_details(token_usage, tool_calls)

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        await ui.display_error(str(e))


@cl.action_callback("Analyze the survival rate by passenger class")
@cl.action_callback("What was the average age of survivors?")
@cl.action_callback("What was the name and age of the oldest female survivor?")
@cl.action_callback("What was the most common embarkation port?")
@cl.action_callback("Analyze the relationship between fare and survival")
@MessageManager.log_error
async def on_action(action: cl.Action):
    """Handle action callbacks for suggested prompts.

    This function processes clicks on the suggested prompt buttons.
    It creates a new message with the selected prompt and processes it.

    Args:
        action: The action that was clicked, containing the prompt
    """
    try:
        # Get the prompt from the action payload
        prompt = action.payload.get("prompt")
        if not prompt:
            logger.error("No prompt found in action payload")
            return

        # Create a new message with the prompt
        message = cl.Message(content=prompt)

        # Process the message using the message handler
        await handle_message(message)

    except Exception as e:
        logger.error(f"Error handling action: {str(e)}", exc_info=True)
        await ui.display_error(str(e))


def main():
    """Run the Chainlit application.

    This function configures and starts the Chainlit server.
    It uses the default port (8000) and enables auto-reload
    for development.
    """
    from chainlit.cli import run_chainlit
    from chainlit.config import config as chainlit_config

    chainlit_config.run.watch = True  # Auto-reload on file changes
    run_chainlit(str(__file__))


if __name__ == "__main__":
    main()
