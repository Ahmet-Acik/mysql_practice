#!/usr/bin/env python3
"""
Standalone test debugging script
Run this to diagnose database connection issues
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔍 Database Test Configuration Debug")
    print("="*45)
    
    # Print environment
    print("\n📋 Environment Variables:")
    env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT', 'GITHUB_ACTIONS']
    for var in env_vars:
        value = os.environ.get(var, 'NOT_SET')
        print(f"   {var}: {value}")
    
    # Test imports
    print("\n📦 Testing Imports:")
    try:
        import mysql.connector
        print("   ✅ mysql.connector imported successfully")
    except ImportError as e:
        print(f"   ❌ mysql.connector import failed: {e}")
    
    try:
        from tests.test_config import get_test_db_config, is_database_available
        print("   ✅ test_config imported successfully")
    except ImportError as e:
        print(f"   ❌ test_config import failed: {e}")
        return
    
    # Test configuration
    print("\n⚙️  Database Configuration:")
    config = get_test_db_config()
    for key, value in config.items():
        safe_value = "***" if "password" in key.lower() else value
        print(f"   {key}: {safe_value}")
    
    # Test connection
    print("\n🔌 Database Connection Test:")
    try:
        available = is_database_available()
        if available:
            print("   ✅ Database connection successful!")
        else:
            print("   ❌ Database connection failed")
            print("   Try manually:")
            print(f"     mysql -h {config['host']} -u {config['user']} -p{config['password']} -e 'SHOW DATABASES;'")
    except Exception as e:
        print(f"   💥 Connection test error: {e}")

if __name__ == "__main__":
    main()
