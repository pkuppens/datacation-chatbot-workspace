# LangChain Pandas Tool Documentation

## Overview
LangChain provides a pandas tool through the `langchain-community` package. This tool enables natural language interaction with pandas DataFrames and is more feature-rich than custom implementations.

## Package Installation

First, ensure you have the necessary packages installed:

```bash
uv add langchain-community>=0.3.22
uv add pandas>=2.2.3
```

## Implementation

The Pandas tools are available in `langchain_community.tools.pandas` and provide several key features:

1. **PandasDataFrameTool**: A tool for executing pandas operations on DataFrames
2. **PandasDataFrameQueryTool**: A tool for executing SQL-like queries on DataFrames
3. **PandasDataFrameStatsTool**: A tool for generating statistical summaries

### Key Features
- Natural language to pandas operations translation
- SQL-like query support
- Statistical analysis capabilities
- Built-in error handling
- Async support
- Integration with LangChain's agent framework

### Example Implementation
```python
from langchain_community.tools.pandas import (
    PandasDataFrameTool,
    PandasDataFrameQueryTool,
    PandasDataFrameStatsTool
)
import pandas as pd

# Load your DataFrame
df = pd.DataFrame(...)

# Create tool instances
pandas_tool = PandasDataFrameTool(df=df)
query_tool = PandasDataFrameQueryTool(df=df)
stats_tool = PandasDataFrameStatsTool(df=df)

# Use in LangChain agent
agent = create_react_agent(
    model=llm,
    tools=[pandas_tool, query_tool, stats_tool],
    prompt="You are a helpful data analysis assistant."
)
```

## Working with Multiple DataFrames

When dealing with multiple related DataFrames, you can create separate tool instances for each DataFrame and combine them in your agent. Here's how to handle complex scenarios:

### Example with Multiple DataFrames
```python
from langchain_community.tools.pandas import PandasDataFrameTool
import pandas as pd

def create_multi_df_tools():
    # Load multiple related datasets
    customers_df = pd.read_csv('customers.csv')
    orders_df = pd.read_csv('orders.csv')
    products_df = pd.read_csv('products.csv')
    
    # Create tools for each DataFrame
    tools = []
    
    # Individual DataFrame tools
    tools.append(PandasDataFrameTool(
        df=customers_df,
        name="customers_tool",
        description="Tool for customer data analysis"
    ))
    tools.append(PandasDataFrameTool(
        df=orders_df,
        name="orders_tool",
        description="Tool for order data analysis"
    ))
    tools.append(PandasDataFrameTool(
        df=products_df,
        name="products_tool",
        description="Tool for product data analysis"
    ))
    
    # Create merged DataFrame tools
    customer_orders = pd.merge(
        customers_df, 
        orders_df, 
        on='customer_id', 
        how='inner'
    )
    tools.append(PandasDataFrameTool(
        df=customer_orders,
        name="customer_orders_tool",
        description="Tool for analyzing customer orders"
    ))
    
    return tools

# Use in agent
agent = create_react_agent(
    model=llm,
    tools=create_multi_df_tools(),
    prompt="""You are a data analysis assistant. You can analyze:
    1. Customer data
    2. Order data
    3. Product data
    4. Combined customer-order data
    Use the appropriate tool for each analysis."""
)
```

## Data Safety and Manipulation

The LangChain pandas tools are designed with data safety in mind:

### Safety Features
1. **Read-Only Operations**: By default, the tools perform read-only operations on DataFrames
2. **Data Copying**: Tools work on copies of the DataFrames, not the original data
3. **Query Validation**: SQL-like queries are validated before execution
4. **Operation Restrictions**: Certain operations (like `drop`, `delete`, etc.) are restricted

### Example of Safety Measures
```python
from langchain_community.tools.pandas import PandasDataFrameTool
import pandas as pd

# Original DataFrame
original_df = pd.DataFrame({'A': [1, 2, 3]})

# Create tool with safety measures
tool = PandasDataFrameTool(
    df=original_df.copy(),  # Work with a copy
    name="safe_tool",
    description="Tool with safety measures"
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

### Additional Safety Measures
1. **Data Validation**:
   ```python
   def validate_df(df: pd.DataFrame) -> bool:
       """Validate DataFrame before creating tool."""
       # Check for sensitive columns
       sensitive_cols = ['password', 'ssn', 'credit_card']
       if any(col in df.columns for col in sensitive_cols):
           raise ValueError("DataFrame contains sensitive columns")
       
       # Check data types
       if not all(df.dtypes.isin([np.number, np.bool_, np.object_])):
           raise ValueError("DataFrame contains unsupported data types")
       
       return True
   ```

2. **Access Control**:
   ```python
   class SecurePandasTool(PandasDataFrameTool):
       def __init__(self, df: pd.DataFrame, allowed_operations: List[str]):
           super().__init__(df=df.copy())
           self.allowed_operations = allowed_operations
       
       def _run(self, query: str) -> str:
           # Validate operation is allowed
           if not any(op in query for op in self.allowed_operations):
               raise ValueError("Operation not allowed")
           return super()._run(query)
   ```

## Migration Plan

### Phase 1: Setup and Dependencies
1. Install required packages:
   ```bash
   uv add langchain-community>=0.3.22
   uv add pandas>=2.2.3
   ```

2. Create new tool implementation:
   ```python
   # tools/pandas_tools.py
   from langchain_community.tools.pandas import (
       PandasDataFrameTool,
       PandasDataFrameQueryTool,
       PandasDataFrameStatsTool
   )
   from datasets import load_dataset

   def create_pandas_tools():
       # Load Titanic dataset
       dataset = load_dataset("mstz/titanic")["train"]
       df = dataset.to_pandas()
       
       # Create tool instances
       return [
           PandasDataFrameTool(df=df),
           PandasDataFrameQueryTool(df=df),
           PandasDataFrameStatsTool(df=df)
       ]
   ```

### Phase 2: Integration
1. Update `chat_app.py`:
   ```python
   from tools.pandas_tools import create_pandas_tools

   # Create agent with pandas tools
   agent = create_react_agent(
       model=llm,
       tools=[search_tool] + create_pandas_tools(),
       prompt="""You are a helpful data analysis assistant. 
       When analyzing data:
       1. Use pandas tools for DataFrame operations
       2. Use query tool for SQL-like queries
       3. Use stats tool for statistical analysis
       4. Format results clearly and concisely"""
   )
   ```

### Phase 3: Testing and Validation
1. Test basic operations:
   - DataFrame filtering
   - Statistical calculations
   - SQL-like queries
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
   - Use built-in error handling from tools
   - Add custom error messages for specific cases
   - Implement proper logging

2. **Performance**
   - Use appropriate tool for each operation type
   - Cache frequently used results
   - Optimize DataFrame operations

3. **Documentation**
   - Document tool capabilities
   - Provide usage examples
   - Include error handling guidelines

## References

- [LangChain Pandas Tools Documentation](https://python.langchain.com/docs/integrations/tools/pandas)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) 