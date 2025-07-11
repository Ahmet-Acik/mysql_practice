"""
Database connection configuration and utilities.
"""

import os
from typing import Any, Dict, List, Optional

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables
load_dotenv(override=True)


class DatabaseConfig:
    """Database configuration class."""

    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", 3306))
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    DATABASE = os.getenv("DB_NAME", "practice_db")
    POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
    MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))


class MySQLConnection:
    """MySQL connection manager using mysql-connector-python."""

    def __init__(self):
        self.connection: Optional[Any] = None
        self.cursor: Optional[Any] = None

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                autocommit=False,
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL database successfully!")
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query."""
        if not self.cursor:
            print("No database connection available.")
            return None

        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute INSERT, UPDATE, or DELETE query."""
        if not self.cursor or not self.connection:
            print("No database connection available.")
            return 0

        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error executing update: {e}")
            self.connection.rollback()
            return 0

    def execute_update_with_id(
        self, query: str, params: Optional[tuple] = None
    ) -> Optional[int]:
        """Execute INSERT query and return the last inserted ID."""
        if not self.cursor or not self.connection:
            print("No database connection available.")
            return None

        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error executing update: {e}")
            self.connection.rollback()
            return None

    def execute_many(self, query: str, data_list: List[tuple]) -> int:
        """Execute query with multiple data sets."""
        if not self.cursor or not self.connection:
            print("No database connection available.")
            return 0

        try:
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error executing batch query: {e}")
            self.connection.rollback()
            return 0

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


class SQLAlchemyConnection:
    """SQLAlchemy connection manager - NOT IMPLEMENTED YET."""

    def __init__(self):
        print("SQLAlchemy support coming soon...")


def create_connection():
    """Create a new database connection and return the connection object."""
    try:
        connection = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            port=DatabaseConfig.PORT,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.DATABASE,
            autocommit=False,
        )
        return connection
    except Error as e:
        print(f"Error creating database connection: {e}")
        return None


def get_db_config() -> Dict[str, Any]:
    """Get database configuration as dictionary."""
    return {
        "host": DatabaseConfig.HOST,
        "port": DatabaseConfig.PORT,
        "user": DatabaseConfig.USER,
        "password": DatabaseConfig.PASSWORD,
        "database": DatabaseConfig.DATABASE,
    }


def test_connection():
    """Test database connection."""
    print("Testing MySQL connection...")

    # Test basic connection
    with MySQLConnection() as db:
        if db.connection:
            result = db.execute_query("SELECT VERSION() as version")
            if result and len(result) > 0:
                version_info = result[0]
                if isinstance(version_info, dict) and "version" in version_info:
                    print(f"MySQL Version: {version_info['version']}")

            # Test database existence
            result = db.execute_query(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                (DatabaseConfig.DATABASE,),
            )

            if result:
                print(f"Database '{DatabaseConfig.DATABASE}' exists.")
            else:
                print(f"Database '{DatabaseConfig.DATABASE}' does not exist.")
                print("Please create the database first:")
                print(f"CREATE DATABASE {DatabaseConfig.DATABASE};")


if __name__ == "__main__":
    test_connection()
