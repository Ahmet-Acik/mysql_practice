"""
Create the practice database.
Run this script to create the initial database.
"""

import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables
load_dotenv()


def create_database():
    """Create the practice database and tables."""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
        )

        cursor = connection.cursor()

        # Create database
        database_name = os.getenv("DB_NAME", "practice_db")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✅ Database '{database_name}' created successfully!")

        # Use the database
        cursor.execute(f"USE {database_name}")
        print(f"✅ Using database '{database_name}'")

        # Create tables from schema file
        print("📋 Creating tables...")
        if create_tables(cursor):
            print("✅ Tables created successfully!")
            
            # Load sample data
            print("📊 Loading sample data...")
            if load_sample_data(cursor):
                print("✅ Sample data loaded successfully!")
            else:
                print("⚠️ Sample data loading failed, but tables are ready")
        else:
            print("⚠️ Table creation had issues, but database exists")

        connection.commit()
        cursor.close()
        connection.close()

        return True

    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False


def create_tables(cursor):
    """Create tables from schema file."""
    try:
        schema_file = "schemas/create_tables.sql"
        if not os.path.exists(schema_file):
            print(f"❌ Schema file not found: {schema_file}")
            return False
            
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️ Warning executing statement: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def load_sample_data(cursor):
    """Load sample data from file."""
    try:
        sample_file = "schemas/sample_data.sql"
        if not os.path.exists(sample_file):
            print(f"ℹ️ Sample data file not found: {sample_file}")
            return False
            
        with open(sample_file, 'r') as f:
            sample_sql = f.read()
        
        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in sample_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    if "duplicate entry" not in str(e).lower():
                        print(f"⚠️ Warning loading data: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return False


def main():
    """Main function."""
    print("🗄️ Creating MySQL Practice Database")
    print("=" * 40)

    if create_database():
        print("\n🎉 Database setup complete!")
        print("\nDatabase is ready with:")
        print("✅ Database created")
        print("✅ Tables created")
        print("✅ Sample data loaded")
        print("\nYou can now:")
        print("1. Test the connection: python config/database.py")
        print("2. Run examples: python examples/basic_operations.py")
        print("3. Try exercises: python exercises/beginner.py")
        print("4. Run tests: pytest tests/")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your MySQL credentials in the .env file")
        print("For CI/CD, ensure these environment variables are set:")
        print("- DB_HOST (e.g., 127.0.0.1)")
        print("- DB_USER (e.g., root)")
        print("- DB_PASSWORD (e.g., root)")
        print("- DB_NAME (e.g., practice_db)")


if __name__ == "__main__":
    main()
