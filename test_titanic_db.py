import pandas as pd
from data_pipeline.titanic_pipeline import get_titanic_data

def test_titanic_queries():
    try:
        # Load the data using our pipeline
        df = get_titanic_data()
        
        # Test 1: Check if we have data
        assert len(df) > 0, "Dataset is empty"
        print(f"\nTotal number of passengers: {len(df)}")
        
        # Test 2: Get survival statistics
        survival_stats = df['Survived'].value_counts(normalize=True) * 100
        print("\nSurvival statistics:")
        for survived, percentage in survival_stats.items():
            status = "Survived" if survived else "Did not survive"
            count = len(df[df['Survived'] == survived])
            print(f"- {status}: {count} passengers ({percentage:.2f}%)")
        
        # Test 3: Survival rate by passenger class
        class_stats = df.groupby('Pclass').agg({
            'Survived': ['count', 'sum', lambda x: (x.sum() / len(x)) * 100]
        }).round(2)
        
        print("\nSurvival rate by passenger class:")
        for p_class in sorted(df['Pclass'].unique()):
            stats = class_stats.loc[p_class]
            total = int(stats[('Survived', 'count')])
            survived = int(stats[('Survived', 'sum')])
            rate = float(stats[('Survived', '<lambda_0>')])
            print(f"- Class {p_class}: {survived} out of {total} survived ({rate}%)")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    test_titanic_queries() 