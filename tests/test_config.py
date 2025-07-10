"""
Test configuration for MySQL Practice Project.
"""

import os
from typing import Dict, Any


def get_test_db_config() -> Dict[str, Any]:
    """
    Get database configuration for testing.
    
    Returns:
        Dict with database configuration parameters.
    """
    # Try Docker environment first
    if os.environ.get('DB_HOST') == 'mysql':
        return {
            'host': 'mysql',
            'port': 3306,
            'user': 'practice_user',
            'password': 'practice_password',
            'database': 'practice_db'
        }
    
    # Try local Docker access (host connecting to Docker MySQL)
    if os.path.exists('/usr/bin/docker') or os.path.exists('/usr/local/bin/docker'):
        return {
            'host': 'localhost',
            'port': 3307,  # Docker mapped port
            'user': 'practice_user',
            'password': 'practice_password',
            'database': 'practice_db'
        }
    
    # Fallback to environment variables or defaults
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', 3306)),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'practice_db')
    }


def is_database_available() -> bool:
    """
    Check if test database is available.
    
    Returns:
        True if database is available, False otherwise.
    """
    try:
        import mysql.connector
        config = get_test_db_config()
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            connection.close()
            return True
    except Exception:
        pass
    return False
