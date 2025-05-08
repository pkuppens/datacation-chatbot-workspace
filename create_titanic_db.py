import pandas as pd
from datasets import load_dataset
from sqlalchemy import create_engine

def create_titanic_database():
    # Load the Titanic dataset from Hugging Face
    dataset = load_dataset("mstz/titanic")["train"]
    titanic_df = dataset.to_pandas()
    
    # Create SQLite database engine
    engine = create_engine('sqlite:///titanic.sqlite')
    
    # Store the DataFrame in SQLite
    titanic_df.to_sql('titanic', engine, if_exists='replace', index=False)
    
    print("Titanic dataset has been successfully stored in titanic.sqlite")
    print(f"Number of records: {len(titanic_df)}")
    print("\nColumns in the database:")
    for col in titanic_df.columns:
        print(f"- {col}")

if __name__ == "__main__":
    create_titanic_database() 