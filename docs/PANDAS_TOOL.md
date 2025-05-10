# LangChain Pandas Tool Documentation

## Overview

LangChain provides a pandas DataFrame agent through the `langchain_experimental` package. This agent enables natural language
interaction with pandas DataFrames and is optimized for question answering.

**Note**: This agent calls the Python agent under the hood, which executes LLM generated Python code. Use cautiously as this can be
harmful if the generated code is malicious.

## Package Installation

First, ensure you have the necessary packages installed:

```bash
# Install with active environment flag to avoid warnings
uv add --active langchain-experimental>=0.0.49
uv add --active pandas>=2.2.3
```

## Implementation

The pandas DataFrame agent is available in `langchain_experimental.agents.agent_toolkits` and provides a simple way to interact
with DataFrames using natural language.

### Key Features

- Natural language to pandas operations translation
- Built-in error handling
- Support for multiple DataFrames
- Integration with LangChain's agent framework

### Example Implementation

```python
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd

# Load your DataFrame
df = pd.read_csv("your_data.csv")

# Create agent with OpenAI Functions
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# Or create agent with Zero Shot React Description
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0),
    df,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Use the agent
response = agent.invoke("how many rows are there?")
```

## Working with Multiple DataFrames

The agent can work with multiple DataFrames by passing them as a list:

```python
# Create multiple DataFrames
df1 = pd.read_csv("data1.csv")
df2 = pd.read_csv("data2.csv")

# Create agent with multiple DataFrames
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0),
    [df1, df2],
    verbose=True
)

# Use the agent to compare DataFrames
response = agent.invoke("how many rows in the age column are different?")
```

## Data Safety and Manipulation

The pandas DataFrame agent is designed with data safety in mind:

### Safety Features

1. **Read-Only Operations**: By default, the agent performs read-only operations on DataFrames
2. **Data Copying**: Agent works on copies of the DataFrames, not the original data
3. **Operation Restrictions**: Certain operations (like `drop`, `delete`, etc.) are restricted

### Example of Safety Measures

```python
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd

# Original DataFrame
original_df = pd.DataFrame({'A': [1, 2, 3]})

# Create agent with safety measures
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0),
    original_df.copy(),  # Work with a copy
    verbose=True
)

# The following operations are safe:
# - Reading data
# - Filtering
# - Aggregations
# - Statistical calculations

# The following operations are restricted:
# - Modifying original data
# - Deleting rows/columns
# - Writing to files
```

## Migration Plan

### Phase 1: Setup and Dependencies

1. Install required packages:

   ```bash
   uv add --active langchain-experimental>=0.0.49
   uv add --active pandas>=2.2.3
   ```

2. Create new agent implementation:

   ```python
   # tools/pandas_tools.py
   from langchain.agents.agent_types import AgentType
   from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
   from datasets import load_dataset

   def create_pandas_agent(llm):
       # Load Titanic dataset
       dataset = load_dataset("mstz/titanic")["train"]
       df = dataset.to_pandas()
       
       # Create agent
       return create_pandas_dataframe_agent(
           llm,
           df,
           verbose=True,
           agent_type=AgentType.OPENAI_FUNCTIONS
       )
   ```

### Phase 2: Integration

1. Update `chat_app.py`:

   ```python
   from tools.pandas_tools import create_pandas_agent

   # Create agent with pandas tools
   agent = create_pandas_agent(llm)
   ```

### Phase 3: Testing and Validation

1. Test basic operations:
   - DataFrame filtering
   - Statistical calculations
   - Error handling

2. Validate results against existing implementation:
   - Compare output formats
   - Verify accuracy
   - Check performance

### Phase 4: Cleanup

1. Remove old implementation:
   - Delete `tools/titanic_pandas_tool.py`
   - Update imports in affected files
   - Remove unused dependencies

2. Update documentation:
   - Update README.md
   - Update API documentation
   - Add usage examples

## Best Practices

1. **Error Handling**
   - Use built-in error handling from the agent
   - Add custom error messages for specific cases
   - Implement proper logging

2. **Performance**
   - Use appropriate agent type for your use case
   - Cache frequently used results
   - Optimize DataFrame operations

3. **Documentation**
   - Document agent capabilities
   - Provide usage examples
   - Include error handling guidelines

## References

- [LangChain Pandas Tools Documentation](https://python.langchain.com/docs/integrations/tools/pandas)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Community Tools](https://python.langchain.com/docs/integrations/tools/)
