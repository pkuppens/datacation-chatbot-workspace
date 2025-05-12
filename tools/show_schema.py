import sys
from data_pipeline.titanic_pipeline import get_sqlite_connection


def format_schema_description(schema_desc: str) -> str:
    """Format the schema description to show only column names and types."""
    # Split into lines and add proper indentation
    lines = schema_desc.split("\n")
    formatted_lines = []

    for line in lines:
        if line.startswith("Table:"):
            formatted_lines.append(line)
        elif line.startswith("Columns:"):
            formatted_lines.append(line)
        elif line.startswith("- "):
            # Extract just the column name and type
            parts = line.split(":")
            if len(parts) >= 2:
                col_def = parts[0].strip("- ").strip()
                # Get just the type from the first part before any statistics
                col_type = parts[1].split(",")[0].strip()
                # Remove any statistics that might be in parentheses
                col_type = col_type.split("(")[0].strip()
                formatted_lines.append(f"  - {col_def}: {col_type}")

    return "\n".join(formatted_lines)


def get_schema_description() -> str:
    """Get the schema description from the SQLite database."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # Get table info
    cursor.execute("PRAGMA table_info(titanic)")
    columns = cursor.fetchall()

    schema_desc = "Table: titanic\nColumns:\n"
    for col in columns:
        schema_desc += f"- {col[1]}: {col[2]}\n"

    conn.close()
    return schema_desc


def main():
    """Display the database schema."""
    try:
        # Get and format schema description
        schema = get_schema_description()
        formatted_schema = format_schema_description(schema)

        # Print with a nice header
        print("\n=== Titanic Database Schema ===\n")
        print(formatted_schema)
        print("\n==============================\n")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
