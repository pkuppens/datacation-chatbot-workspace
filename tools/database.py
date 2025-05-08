import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

class TitanicDatabase:
    def __init__(self, db_path: str = "titanic.sqlite"):
        self.db_path = Path(db_path)
        self._ensure_database()
        self.schema_info = self._get_schema_info()
    
    def _ensure_database(self):
        """Ensure the database exists and has the correct schema."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found at {self.db_path}. Please run create_titanic_db.py first.")
    
    def _get_schema_info(self) -> Dict[str, Any]:
        """Get detailed schema information including column types and statistics."""
        conn = sqlite3.connect(self.db_path)
        try:
            # Get column information
            cursor = conn.execute("PRAGMA table_info(titanic)")
            columns = cursor.fetchall()
            
            # Get basic statistics
            stats = {}
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                
                # Get value counts for categorical columns
                if col_type == 'TEXT':
                    value_counts = pd.read_sql_query(
                        f"SELECT {col_name}, COUNT(*) as count FROM titanic GROUP BY {col_name} ORDER BY count DESC LIMIT 5",
                        conn
                    ).to_dict('records')
                    stats[col_name] = {
                        'type': col_type,
                        'unique_values': len(value_counts),
                        'top_values': value_counts
                    }
                # Get numeric statistics
                elif col_type in ('INTEGER', 'REAL'):
                    numeric_stats = pd.read_sql_query(
                        f"SELECT MIN({col_name}) as min, MAX({col_name}) as max, AVG({col_name}) as avg FROM titanic",
                        conn
                    ).iloc[0].to_dict()
                    stats[col_name] = {
                        'type': col_type,
                        'min': numeric_stats['min'],
                        'max': numeric_stats['max'],
                        'avg': numeric_stats['avg']
                    }
            
            return {
                'table_name': 'titanic',
                'columns': {col[1]: col[2] for col in columns},
                'statistics': stats
            }
        finally:
            conn.close()
    
    def get_schema_description(self) -> str:
        """Get a human-readable description of the database schema."""
        schema = self.schema_info
        desc = [f"Table: {schema['table_name']}"]
        desc.append("Columns:")
        for col_name, col_type in schema['columns'].items():
            desc.append(f"- {col_name}: {col_type}")
        return "\n".join(desc)
    
    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        conn = sqlite3.connect(self.db_path)
        try:
            if params:
                df = pd.read_sql_query(sql, conn, params=params)
            else:
                df = pd.read_sql_query(sql, conn)
            return df
        finally:
            conn.close()
    
    def get_survival_rate(self) -> float:
        """Get the overall survival rate."""
        df = self.query("SELECT AVG(Survived) as rate FROM titanic")
        return float(df['rate'].iloc[0] * 100)
    
    def get_passenger_count(self) -> int:
        """Get the total number of passengers."""
        df = self.query("SELECT COUNT(*) as count FROM titanic")
        return int(df['count'].iloc[0])
    
    def get_class_distribution(self) -> Dict[int, int]:
        """Get the distribution of passenger classes."""
        df = self.query("""
            SELECT Pclass, COUNT(*) as count 
            FROM titanic 
            GROUP BY Pclass 
            ORDER BY Pclass
        """)
        return dict(zip(df['Pclass'], df['count']))
    
    def get_average_age(self) -> float:
        """Get the average age of passengers."""
        df = self.query("SELECT AVG(Age) as avg_age FROM titanic")
        return float(df['avg_age'].iloc[0])

# Create a singleton instance
titanic_db = TitanicDatabase() 