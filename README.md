# Building an Agent-Based Chatbot

This project guides you through building a powerful agent-based chatbot using LangChain and LangGraph. The implementation progresses from a basic LLM-powered chatbot to a sophisticated agent with tools and memory.

## Project Plan

### 1. Basic Chatbot Setup
#### Environment and Dependencies
- [x] Create virtual environment
- [x] Install core dependencies:
  - [x] langchain
  - [x] langgraph
  - [x] chainlit
  - [x] python-dotenv
  - [x] langchain-google-genai
- [x] Set up development environment (IDE, linting, etc.)

### Additional Setup Steps Taken

#### Code Quality and Security
- [x] Added pre-commit hooks:
  - nbstripout: Strips output from notebooks before commit
  - ruff: Lightweight Python linter with permissive settings
    - Line length set to 132 characters
    - Only basic whitespace and error checks
    - No import sorting enforced
  - detect-secrets: Prevents accidental commit of secrets
    - Baseline scan created
    - Configured to ignore baseline file
    - Active monitoring for new secrets

#### Development Environment
- [x] Configured pyproject.toml with:
  - Core dependencies and versions
  - Build system configuration
  - Development tools configuration
  - Ruff linter settings
  - Python version requirements

#### Security Measures
- [x] Implemented secrets detection
- [x] Created secrets baseline
- [x] Added pre-commit hook for ongoing secret detection
- [x] Configured to prevent accidental API key commits

#### API Configuration
- [x] Create `.env` file
- [x] Obtain Google API key from AI Studio
- [x] Test API key configuration
- [x] Implement secure key handling

#### Basic Chatbot Implementation
- [ ] Create basic `chat_app.py` structure
- [ ] Implement `ChatGoogleGenerativeAI` initialization
- [ ] Set up basic message handling
- [ ] Test basic conversation flow

#### Streaming Implementation
- [ ] Implement `astream` method
- [ ] Set up `AsyncLangchainCallbackHandler`
- [ ] Configure response streaming
- [ ] Test streaming functionality

### 2. LangGraph Integration
#### Basic Setup
- [ ] Migrate existing code to LangGraph structure
- [ ] Set up basic agent configuration
- [ ] Implement message history handling
- [ ] Test basic agent functionality

#### Thread Management
- [ ] Implement thread ID generation
- [ ] Set up thread-based message history
- [ ] Configure thread persistence
- [ ] Test thread management

#### Context Enhancement
- [ ] Add current date to system prompts
- [ ] Implement context management
- [ ] Set up prompt templates
- [ ] Test context handling

### 3. Response Handling
#### Async Implementation
- [ ] Set up async message handling
- [ ] Implement streaming response processing
- [ ] Configure metadata handling
- [ ] Test async functionality

#### Synchronous Fallback
- [ ] Implement synchronous response handling
- [ ] Set up fallback mechanisms
- [ ] Configure response formatting
- [ ] Test fallback scenarios

### 4. Memory and State Management
#### Checkpointing
- [ ] Implement `InMemorySaver`
- [ ] Configure checkpoint intervals
- [ ] Set up state recovery
- [ ] Test checkpoint functionality

#### Session Management
- [ ] Implement session handling
- [ ] Configure session persistence
- [ ] Set up session recovery
- [ ] Test session management

#### Chainlit Integration
- [ ] Set up Chainlit configuration
- [ ] Implement chat history integration
- [ ] Configure UI elements
- [ ] Test Chainlit functionality

### 5. Tool Integration
#### Basic Tools
- [ ] Implement calculator tool
- [ ] Set up DuckDuckGo search
- [ ] Configure tool selection
- [ ] Test basic tools

#### Advanced Tools
- [ ] Implement custom tools
- [ ] Set up tool chaining
- [ ] Configure tool response handling
- [ ] Test advanced tools

## Quick Implementation Steps

### 1. Initial Setup
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate environment: 
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies using uv:
   ```bash
   # Install uv if not already installed
   pip install uv
   
   # Install project dependencies
   uv add -r requirements.txt
   
   # Install development dependencies
   uv add ipykernel -U --force-reinstall --active
   ```

### 2. Configuration
1. Create `.env` file in project root
2. Add Google API key: `GOOGLE_API_KEY=your_key_here`
3. Test configuration with simple script

### 3. Basic Chatbot
1. Create `chat_app.py`
2. Implement basic LLM initialization
3. Add message handling
4. Test basic conversation

### 4. LangGraph Migration
1. Update imports to include LangGraph
2. Modify message handling
3. Add thread support
4. Test conversation flow

### 5. Tool Addition
1. Add calculator tool
2. Implement search functionality
3. Test tool integration
4. Add more tools as needed

## Project Structure
```
.
├── .env                    # Environment variables
├── chat_app.py            # Main application file
├── notebooks/             # Jupyter notebooks for development
│   └── workshop_part_1.ipynb
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Dependencies
- langchain
- langgraph
- chainlit
- python-dotenv
- langchain-google-genai

## Notes
- The notebook (`workshop_part_1.ipynb`) is for experimentation
- Final implementation should be in `chat_app.py`
- Remember to handle API keys securely
- Consider implementing proper error handling
- Add logging for better debugging

## Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Chainlit Documentation](https://docs.chainlit.io/)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
