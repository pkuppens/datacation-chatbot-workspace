# Building an Agent-Based Chatbot

## Project Description

A workshop, templated from [@DatacationOrg/chatbot-workshop](https://github.com/DatacationOrg/chatbot-workshop),
to learn to build capable agents using LangChain and Gemini.

This project guides you through building a powerful agent-based chatbot using LangChain and LangGraph.
The implementation progresses from a basic LLM-powered chatbot to a sophisticated agent with tools and memory.

## Project Plan

### Part 1: Basic Setup and Integration ✅

- [x] Environment and dependencies setup
- [x] Basic chatbot implementation
- [x] LangGraph integration
- [x] Streaming response handling
- [x] Basic tool integration (DuckDuckGo search)
- [x] Memory and checkpointing
- [x] Code quality and security measures
- [x] Notebook execution and configuration management
  - [x] In-place notebook execution
  - [x] Chainlit configuration centralization
  - [x] Environment variable management
  - [x] Project root detection

### Part 2: Data Analysis Agent 🚀

#### 1. Enhanced Tool Integration

- [x] Implement core tools:
  - [x] SQL Database integration (SQLite)
  - [x] DuckDuckGo search tool
  - [x] Python REPL for data analysis
- [ ] Optional tools:
  - [ ] Weather tool with structured output
  - [ ] Calculator with math operations
  - [ ] File operations tool
  - [ ] Custom search tool with better formatting

#### 2. Data Analysis Capabilities

- [ ] Implement dataset handling:
  - [ ] Load and process Titanic dataset
  - [ ] Convert to SQLite database
  - [ ] Basic statistical analysis
- [ ] Add visualization support:
  - [ ] Bar charts for categorical data
  - [ ] Histograms for numerical data
  - [ ] Scatter plots for relationships
- [ ] Implement advanced analysis:
  - [ ] Survival rate analysis
  - [ ] Demographic insights
  - [ ] Correlation studies

#### 3. Memory and Context Management

- [x] Implement conversation memory:
  - [x] Message history tracking
  - [x] Context window management
  - [x] Checkpointing for state persistence
- [ ] Add context optimization:
  - [ ] Relevant memory retrieval
  - [ ] Memory summarization
  - [ ] Context pruning

#### 4. Agent Reasoning and Planning

- [x] Implement ReAct framework:
  - [x] Thought process visualization
  - [x] Action planning
  - [x] Result evaluation
- [ ] Add multi-step reasoning:
  - [ ] Break down complex queries
  - [ ] Tool chaining
  - [ ] Result aggregation

#### 5. User Experience Enhancements

- [x] Add interactive elements:
  - [x] Suggested prompts
  - [x] Technical details display
  - [x] Thought process visualization
- [ ] Implement feedback system:
  - [ ] Response rating
  - [ ] Error reporting
  - [ ] Usage analytics

#### 6. Testing and Monitoring

- [ ] Add comprehensive testing:
  - [ ] Unit tests for tools
  - [ ] Integration tests
  - [ ] End-to-end tests
- [ ] Implement monitoring:
  - [ ] Performance metrics
  - [ ] Error tracking
  - [ ] Usage statistics

## Quick Implementation Steps

### Part 1 (Completed) ✅

1. Basic setup and configuration
2. LangGraph integration
3. Basic tool implementation
4. Memory management
5. Security measures
6. Notebook execution and configuration
   - In-place execution with fallback
   - Centralized Chainlit configuration
   - Environment variable management
   - Project root detection

### Part 2 (In Progress) 🚀

1. Data analysis tools
   - SQLite integration
   - Dataset processing
   - Statistical analysis
2. Visualization capabilities
3. Advanced analysis features
4. Testing framework
5. Monitoring system

## Project Structure

```text
.
├── .env                  # Environment variables
├── env.example           # Example environment configuration
├── chainlit.yaml         # Chainlit configuration
├── chat_app.py           # Main application file
├── notebooks/            # Jupyter notebooks for development
│   ├── workshop_part_1.ipynb
│   └── workshop_part_2.ipynb
├── scripts/              # Utility scripts
│   └── notebook_1.py     # Notebook execution script
├── tools/                # Custom tool implementations
├── tests/                # Test suite
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Dependencies

- langchain
- langgraph
- chainlit
- python-dotenv
- langchain-google-genai
- jupyter
- nbconvert
- datasets
- pandas
- sqlalchemy

## Notes

- The notebooks are for experimentation
- Final implementation should be in `chat_app.py`
- Remember to handle API keys securely
- Consider implementing proper error handling
- Add logging for better debugging
- Use `notebook_1` or `notebook_2` to execute notebooks in place via cli.

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Chainlit Documentation](https://docs.chainlit.io/)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [LangChain SQL Database Integration](https://python.langchain.com/docs/integrations/tools/sql_database/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Chainlit Plotly Integration](https://docs.chainlit.io/api-reference/elements/plotly)

## About ReAct

ReAct does not refer to a React.js application, but rather a Python-based agent system that follows the ReAct pattern for
intelligent decision-making.

ReAct (Reasoning and Acting) is a framework for building AI agents that combines:

1. Reasoning: The agent thinks through problems step by step
2. Acting: The agent uses tools to gather information and perform actions
3. Observing: The agent learns from the results of its actions

In this project, ReAct is implemented using:

- Chainlit for the chat interface
- LangChain for the agent framework
- Custom tools for data analysis and search
