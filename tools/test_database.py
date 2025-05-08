import sys
import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Tuple
from .database import TitanicDatabase
from create_titanic_db import create_titanic_database

def verify_database_structure(conn: sqlite3.Connection) -> List[str]:
    """Verify the database structure and return any issues found."""
    issues = []
    
    # Check if titanic table exists
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='titanic'")
    if not cursor.fetchone():
        issues.append("Missing 'titanic' table")
        return issues
    
    # Get expected columns and their types
    expected_columns = {
        'PassengerId': 'INTEGER',
        'Survived': 'INTEGER',
        'Pclass': 'INTEGER',
        'Name': 'TEXT',
        'Sex': 'TEXT',
        'Age': 'REAL',
        'SibSp': 'INTEGER',
        'Parch': 'INTEGER',
        'Ticket': 'TEXT',
        'Fare': 'REAL',
        'Cabin': 'TEXT',
        'Embarked': 'TEXT'
    }
    
    # Check columns
    cursor = conn.execute("PRAGMA table_info(titanic)")
    existing_columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    # Check for missing columns
    for col, expected_type in expected_columns.items():
        if col not in existing_columns:
            issues.append(f"Missing column: {col}")
        elif existing_columns[col] != expected_type:
            issues.append(f"Column {col} has wrong type: {existing_columns[col]} (expected {expected_type})")
    
    return issues

def verify_data_integrity(conn: sqlite3.Connection) -> List[str]:
    """Verify the data integrity and return any issues found."""
    issues = []
    
    try:
        # Check if we have data
        cursor = conn.execute("SELECT COUNT(*) FROM titanic")
        count = cursor.fetchone()[0]
        if count == 0:
            issues.append("No data in titanic table")
            return issues
        
        # Check for null values in required fields
        required_fields = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex']
        for field in required_fields:
            cursor = conn.execute(f"SELECT COUNT(*) FROM titanic WHERE {field} IS NULL")
            null_count = cursor.fetchone()[0]
            if null_count > 0:
                issues.append(f"Found {null_count} null values in {field}")
        
        # Check for invalid values
        cursor = conn.execute("SELECT COUNT(*) FROM titanic WHERE Survived NOT IN (0, 1)")
        invalid_survived = cursor.fetchone()[0]
        if invalid_survived > 0:
            issues.append(f"Found {invalid_survived} invalid values in Survived column")
        
        cursor = conn.execute("SELECT COUNT(*) FROM titanic WHERE Pclass NOT IN (1, 2, 3)")
        invalid_pclass = cursor.fetchone()[0]
        if invalid_pclass > 0:
            issues.append(f"Found {invalid_pclass} invalid values in Pclass column")
    except sqlite3.OperationalError as e:
        issues.append(f"Database error: {str(e)}")
    
    return issues

def verify_database_functionality(db: TitanicDatabase) -> List[str]:
    """Verify the database functionality and return any issues found."""
    issues = []
    
    try:
        # Test basic queries
        survival_rate = db.get_survival_rate()
        if not (0 <= survival_rate <= 100):
            issues.append(f"Invalid survival rate: {survival_rate}")
        
        passenger_count = db.get_passenger_count()
        if passenger_count <= 0:
            issues.append(f"Invalid passenger count: {passenger_count}")
        
        class_dist = db.get_class_distribution()
        if not all(k in (1, 2, 3) for k in class_dist.keys()):
            issues.append(f"Invalid class distribution: {class_dist}")
        
        avg_age = db.get_average_age()
        if not (0 <= avg_age <= 100):
            issues.append(f"Invalid average age: {avg_age}")
        
        # Test schema description
        schema_desc = db.get_schema_description()
        if not schema_desc or len(schema_desc) < 100:  # Basic length check
            issues.append("Schema description seems incomplete")
            
    except Exception as e:
        issues.append(f"Error during functionality test: {str(e)}")
    
    return issues

def main():
    """Main test function."""
    print("Testing Titanic Database...")
    
    # Check if database exists, if not create it
    db_path = Path("titanic.sqlite")
    if not db_path.exists():
        print("\nDatabase not found. Creating it using create_titanic_db.py...")
        try:
            create_titanic_database()
            print("✅ Database created successfully")
        except Exception as e:
            print(f"❌ Failed to create database: {str(e)}")
            print("\nPlease ensure you have the required packages installed:")
            print("pip install datasets")
            sys.exit(1)
    
    # Initialize database connection
    print("\nInitializing database...")
    try:
        db = TitanicDatabase()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Failed to initialize database: {str(e)}")
        sys.exit(1)
    
    # Test database structure
    print("\n1. Testing database structure...")
    conn = sqlite3.connect(db_path)
    structure_issues = verify_database_structure(conn)
    if structure_issues:
        print("❌ Structure issues found:")
        for issue in structure_issues:
            print(f"  - {issue}")
    else:
        print("✅ Database structure is valid")
    
    # Test data integrity
    print("\n2. Testing data integrity...")
    integrity_issues = verify_data_integrity(conn)
    if integrity_issues:
        print("❌ Data integrity issues found:")
        for issue in integrity_issues:
            print(f"  - {issue}")
    else:
        print("✅ Data integrity is valid")
    
    conn.close()
    
    # Test database functionality
    print("\n3. Testing database functionality...")
    functionality_issues = verify_database_functionality(db)
    if functionality_issues:
        print("❌ Functionality issues found:")
        for issue in functionality_issues:
            print(f"  - {issue}")
    else:
        print("✅ Database functionality is valid")
    
    # Summary
    total_issues = len(structure_issues) + len(integrity_issues) + len(functionality_issues)
    print(f"\nTest Summary: {total_issues} issues found")
    if total_issues == 0:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        print("\nTo fix these issues:")
        print("1. Check create_titanic_db.py for correct database creation")
        print("2. Delete the existing titanic.sqlite file to recreate it")
        print("3. Ensure you have the datasets package installed")
        print("4. Run this test script again")
        sys.exit(1)

if __name__ == "__main__":
    main() 