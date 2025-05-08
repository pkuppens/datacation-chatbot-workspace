from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from datasets import load_dataset
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_pandas_agent(model: ChatGoogleGenerativeAI):
    """Create a pandas DataFrame agent for the Titanic dataset.
    
    Args:
        model: The language model to use for the agent
        
    Returns:
        A pandas DataFrame agent configured for the Titanic dataset
    """
    try:
        # Load Titanic dataset
        logger.info("Loading Titanic dataset from Hugging Face")
        dataset = load_dataset("mstz/titanic")["train"]
        df = dataset.to_pandas()
        
        # Add helpful column descriptions
        df.attrs['description'] = """
        Titanic dataset with the following columns:
        - passenger_class: Passenger class (1 = First, 2 = Second, 3 = Third)
        - is_male: Gender of the passenger (True = Male, False = Female)
        - age: Age in years
        - sibsp: Number of siblings/spouses aboard
        - parch: Number of parents/children aboard
        - ticket: Ticket number
        - fare: Passenger fare
        - cabin: Cabin number
        - embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
        - has_survived: Binary indicator (True = survived, False = did not survive)
        """
        
        # Create agent with simpler configuration
        logger.info("Creating pandas DataFrame agent")
        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            include_df_in_prompt=False,
            allow_dangerous_code=True,
            prefix="""You are a helpful data analysis assistant. When analyzing the Titanic dataset:

1. ALWAYS use the python_repl_ast tool to execute your code
2. For finding maximum/minimum values:
   - Use df['column'].max() or df['column'].min()
   - Example: df[df['has_survived'] == True]['age'].max()
3. For filtering data:
   - Use boolean indexing: df[condition]
   - Example: df[df['is_male'] == False]
4. For combining conditions:
   - Use & for AND, | for OR
   - Example: df[(df['is_male'] == False) & (df['has_survived'] == True)]
5. For handling missing values:
   - Use .dropna() to remove rows with missing values
   - Example: df['age'].dropna().mean()
6. For grouping and aggregation:
   - Use .groupby() and aggregation functions
   - Example: df.groupby('pclass')['age'].mean()

The dataset has these columns:
- has_survived: Whether the passenger survived (True/False)
- pclass: Passenger class (1, 2, or 3)
- name: Passenger name
- is_male: Whether the passenger is male (True/False)
- age: Passenger age
- sibsp: Number of siblings/spouses aboard
- parch: Number of parents/children aboard
- ticket: Ticket number
- fare: Passenger fare
- cabin: Cabin number
- embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

IMPORTANT: When using the python_repl_ast tool:
1. Always format your code as a complete Python statement
2. Use print() to display results
3. Keep the code simple and focused on one task
4. Avoid complex expressions or chaining multiple operations
5. If you need multiple operations, break them into separate steps

Example correct usage:
Action: Use the python_repl_ast tool
Action Input:
```python
print(len(df))
```

Example incorrect usage:
Action: Use the python_repl_ast tool
Action Input:
```python
df.shape[0]
```

Always show your work and explain your reasoning step by step.
Remember to:
1. ALWAYS use the python_repl_ast tool
2. Show your work and explain your reasoning
3. Handle missing values appropriately
4. Format numbers to 2 decimal places where appropriate"""
        )
        
        logger.info("Successfully created pandas DataFrame agent")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating pandas DataFrame agent: {str(e)}", exc_info=True)
        raise 