"""
Create the practice database.
Run this script to create the initial database.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the practice database."""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database
        database_name = os.getenv('DB_NAME', 'practice_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✅ Database '{database_name}' created successfully!")
        
        # Use the database
        cursor.execute(f"USE {database_name}")
        print(f"✅ Using database '{database_name}'")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def main():
    """Main function."""
    print("🗄️ Creating MySQL Practice Database")
    print("=" * 40)
    
    if create_database():
        print("\n🎉 Database setup complete!")
        print("\nNext steps:")
        print("1. Run the table creation script:")
        print("   mysql -u root -p practice_db < schemas/create_tables.sql")
        print("\n2. Load sample data:")
        print("   mysql -u root -p practice_db < schemas/sample_data.sql")
        print("\n3. Test the connection:")
        print("   python config/database.py")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your MySQL credentials in the .env file")

if __name__ == "__main__":
    main()
