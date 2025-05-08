import sqlite3

def test_titanic_queries():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('titanic.sqlite')
        cursor = conn.cursor()
        
        # Test query 1: Get total number of passengers
        cursor.execute("SELECT COUNT(*) FROM titanic")
        total_passengers = cursor.fetchone()[0]
        print(f"\nTotal number of passengers: {total_passengers}")
        
        # Test query 2: Get survival statistics
        cursor.execute("""
            SELECT 
                has_survived,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
            FROM titanic
            GROUP BY has_survived
        """)
        print("\nSurvival statistics:")
        for survived, count, percentage in cursor.fetchall():
            status = "Survived" if survived else "Did not survive"
            print(f"- {status}: {count} passengers ({percentage}%)")
        
        # Test query 3: Survival rate by passenger class
        cursor.execute("""
            SELECT 
                passenger_class,
                COUNT(*) as total,
                SUM(has_survived) as survived,
                ROUND(SUM(has_survived) * 100.0 / COUNT(*), 2) as survival_rate
            FROM titanic
            GROUP BY passenger_class
            ORDER BY passenger_class
        """)
        print("\nSurvival rate by passenger class:")
        for p_class, total, survived, rate in cursor.fetchall():
            print(f"- Class {p_class}: {survived} out of {total} survived ({rate}%)")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
        # Let's check if the table exists
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("\nTables in the database:")
            for table in tables:
                print(f"- {table[0]}")
                
                # Print schema for each table
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                print("  Columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
        except sqlite3.Error as e2:
            print(f"Error while checking tables: {e2}")
    
    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_titanic_queries() 