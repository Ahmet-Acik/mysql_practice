#!/usr/bin/env python3
"""
MySQL Practice Project Setup Script
This script helps set up the MySQL practice environment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.7 or higher."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_mysql_installation():
    """Check if MySQL is installed and accessible."""
    try:
        # Try to find mysql command
        mysql_path = shutil.which('mysql')
        if mysql_path:
            print(f"✅ MySQL client found at: {mysql_path}")
            return True
        else:
            print("❌ MySQL client not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking MySQL: {e}")
        return False


def install_python_packages():
    """Install required Python packages."""
    print("\n📦 Installing Python packages...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def create_env_file():
    """Create .env file from template."""
    print("\n📝 Setting up environment file...")
    
    env_example = Path(__file__).parent / ".env.example"
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    try:
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your MySQL credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def test_database_connection():
    """Test database connection."""
    print("\n🔗 Testing database connection...")
    
    try:
        # Import here to avoid import errors if packages not installed
        from config.database import test_connection
        test_connection()
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages first")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


def setup_database():
    """Setup database and tables."""
    print("\n🗄️ Setting up database...")
    
    schema_file = Path(__file__).parent / "schemas" / "create_tables.sql"
    data_file = Path(__file__).parent / "schemas" / "sample_data.sql"
    
    print("To set up the database, run the following commands in MySQL:")
    print("1. CREATE DATABASE practice_db;")
    print("2. USE practice_db;")
    print(f"3. SOURCE {schema_file.absolute()};")
    print(f"4. SOURCE {data_file.absolute()};")
    print("\nOr use MySQL Workbench to execute the SQL files.")


def main():
    """Main setup function."""
    print("🚀 MySQL Practice Project Setup")
    print("=" * 40)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check MySQL installation
    if not check_mysql_installation():
        all_good = False
        print("\n📋 To install MySQL:")
        print("   • macOS: brew install mysql")
        print("   • Ubuntu: sudo apt-get install mysql-server mysql-client")
        print("   • Windows: Download from https://dev.mysql.com/downloads/mysql/")
        print("   • Docker: docker run --name mysql-practice -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0")
    
    if not all_good:
        print("\n❌ Please fix the above issues before continuing")
        return False
    
    # Install Python packages
    if not install_python_packages():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test connection (optional)
    print("\n🔍 Would you like to test the database connection? (y/n): ", end="")
    if input().lower().startswith('y'):
        test_database_connection()
    
    # Setup instructions
    setup_database()
    
    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Edit .env file with your MySQL credentials")
    print("2. Create the database and tables using the SQL files")
    print("3. Run: python examples/basic_operations.py")
    print("4. Try exercises: python exercises/beginner.py")
    
    return True


if __name__ == "__main__":
    main()
