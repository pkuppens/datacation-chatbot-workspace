# Building an Agent-Based Chatbot

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

### Part 2: Advanced Agent Capabilities 🚀

#### 1. Enhanced Tool Integration

- [ ] Implement custom tools:
  - [ ] Weather tool with structured output
  - [ ] Calculator with math operations
  - [ ] File operations tool
  - [ ] Custom search tool with better formatting

#### 2. Improved Response Handling

- [ ] Implement response formatting:
  - [ ] Markdown support
  - [ ] Code block highlighting
  - [ ] Table formatting
  - [ ] List formatting
- [ ] Add response validation
- [ ] Implement error handling and recovery

#### 3. Advanced Memory Management

- [ ] Implement long-term memory:
  - [ ] File-based storage
  - [ ] Database integration
  - [ ] Memory summarization
- [ ] Add context management:
  - [ ] Context window optimization
  - [ ] Relevant memory retrieval
  - [ ] Memory pruning

#### 4. Agent Reasoning and Planning

- [ ] Implement ReAct framework:
  - [ ] Thought process visualization
  - [ ] Action planning
  - [ ] Result evaluation
- [ ] Add multi-step reasoning:
  - [ ] Break down complex tasks
  - [ ] Tool chaining
  - [ ] Result aggregation

#### 5. User Experience Enhancements

- [ ] Add interactive elements:
  - [ ] Buttons for common actions
  - [ ] File upload support
  - [ ] Image generation/display
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

1. Enhanced tool development
2. Response formatting
3. Advanced memory
4. Agent reasoning
5. UX improvements
6. Testing framework

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

## Notes

- The notebooks are for experimentation
- Final implementation should be in `chat_app.py`
- Remember to handle API keys securely
- Consider implementing proper error handling
- Add logging for better debugging
- Use `notebook_1.py` to run notebooks with proper configuration

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Chainlit Documentation](https://docs.chainlit.io/)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
