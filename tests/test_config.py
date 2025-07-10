"""
Test configuration for MySQL Practice Project.
"""

import os
from typing import Any, Dict


def get_test_db_config() -> Dict[str, Any]:
    """
    Get database configuration for testing.

    Returns:
        Dict with database configuration parameters.
    """
    # Always use environment variables first (for CI/CD compatibility)
    config = {
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("DB_PORT", 3306)),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", "root"),
        "database": os.environ.get("DB_NAME", "practice_db"),
    }
    
    # Special handling for CI/CD environments
    if os.environ.get("GITHUB_ACTIONS"):
        # GitHub Actions environment
        config.update({
            "host": "127.0.0.1",
            "user": "root", 
            "password": "root",
            "database": "practice_db"
        })
    elif os.environ.get("DB_HOST") == "mysql":
        # Docker Compose environment
        config.update({
            "host": "mysql",
            "user": "practice_user",
            "password": "practice_password",
        })
    
    return config


def is_database_available() -> bool:
    """
    Check if test database is available.

    Returns:
        True if database is available, False otherwise.
    """
    try:
        import mysql.connector

        config = get_test_db_config()
        
        # Debug info for CI
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"Testing database connection with config: {config}")
        
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            connection.close()
            if os.environ.get("GITHUB_ACTIONS"):
                print("✅ Database connection successful")
            return True
    except Exception as e:
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"❌ Database connection failed: {e}")
        pass
    return False
