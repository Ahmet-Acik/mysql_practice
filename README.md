# MySQL Practice Project

This project contains examples and exercises for practicing MySQL database operations using Python.

## Complete Command-Line Walkthrough

### 📁 **Step 1: Project Setup and Environment**

```bash
# Create project directory
mkdir mysql_practice
cd mysql_practice

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Create project structure
mkdir -p config examples exercises schemas
touch requirements.txt .env.example create_database.py setup.py README.md
```

**Achievement:** ✅ Basic project structure created

### 📦 **Step 2: Install Dependencies**

```bash
# Install MySQL connector and environment support
pip install mysql-connector-python python-dotenv

# Generate requirements.txt
pip freeze > requirements.txt

# View installed packages
cat requirements.txt
```

**Achievement:** ✅ Python dependencies installed and configured

### 🔧 **Step 3: Database Configuration**

```bash
# Create environment file
cp .env.example .env

# Edit .env file with your database credentials
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=practice_db

# Create database connection module
touch config/database.py
touch config/__init__.py
```

**Achievement:** ✅ Database connection configuration ready

### 🗄️ **Step 4: Database Schema Creation**

```bash
# Create database (run in MySQL client)
mysql -u root -p -e "CREATE DATABASE practice_db;"

# Create table schemas
touch schemas/create_tables.sql
touch schemas/sample_data.sql

# Run schema creation
python create_database.py
```

**Achievement:** ✅ Database and tables created with sample data

### 🚀 **Step 5: Learning Path Execution**

#### **Step 5.1: Basic Operations**
```bash
# Run basic CRUD operations
python examples/basic_operations.py
```
**Output:** Basic INSERT, SELECT, UPDATE, DELETE operations demonstrated
**Achievement:** ✅ Fundamental database operations mastered

#### **Step 5.2: Beginner Exercises**
```bash
# Practice beginner-level exercises
python exercises/beginner.py
```
**Output:** Customer management, order processing, basic queries
**Achievement:** ✅ Basic SQL skills applied in practical scenarios

#### **Step 5.3: Advanced Queries**
```bash
# Explore complex queries and analytics
python examples/advanced_queries.py
```
**Output:**
- ✅ Complex JOINs with customer order summaries
- ✅ Subqueries for price analysis and category filtering
- ✅ Window functions with ranking and running totals
- ✅ Analytical queries for cohort analysis
- ✅ Pivot-like queries for sales reporting

**Achievement:** ✅ Advanced SQL query techniques mastered

#### **Step 5.4: Intermediate Exercises**
```bash
# Tackle intermediate-level challenges
python exercises/intermediate.py
```
**Output:**
- ✅ Complex JOIN operations finding unordered customers and unsold products
- ✅ Subqueries and CTEs for spending analysis
- ✅ Data analysis with customer segmentation
- ✅ Performance analysis with EXPLAIN and index optimization

**Achievement:** ✅ Intermediate SQL concepts and performance optimization

#### **Step 5.5: Transaction Management**
```bash
# Learn transaction handling and safety
python examples/transactions.py
```
**Output:**
- ✅ ACID transaction properties demonstration
- ✅ Stock transfer with rollback safety
- ✅ Isolation level management
- ✅ Order processing with error handling
- ✅ Performance monitoring and optimization tips

**Achievement:** ✅ Transaction management and data integrity

#### **Step 5.6: Stored Procedures and Functions**
```bash
# Explore stored procedures and functions
python examples/stored_procedures.py
```
**Output:**
- ✅ Created procedures: GetCustomerOrders, UpdateProductStock, GetProductsByCategory
- ✅ Created functions: CalculateOrderTotal
- ✅ Parameter handling and output management
- ✅ Information schema queries for metadata

**Achievement:** ✅ Advanced database programming with stored procedures

#### **Step 5.7: Advanced Exercises - Final Challenge**
```bash
# Complete the advanced challenge exercises
python exercises/advanced.py
```
**Output:**
- ✅ Query optimization with EXPLAIN analysis
- ✅ Customer Lifetime Value (CLV) calculations
- ✅ Product affinity analysis (market basket analysis)
- ✅ Data warehousing with sales summary tables
- ✅ Database design analysis and recommendations
- ✅ Performance tuning strategies

**Achievement:** 🏆 **Master Level:** Advanced database concepts and optimization

### 📊 **Step 6: Verification and Testing**

```bash
# Quick automated test runner (recommended)
./run_tests.sh

# Or run specific test types
./run_tests.sh --docker  # Run tests in Docker
./run_tests.sh --local   # Run tests locally
```

**For detailed testing information, see:** 📖 [Testing Guide](docs/testing.md)

```bash
# Manual verification - run all examples in sequence
echo "=== COMPLETE LEARNING PATH VERIFICATION ==="

echo "1. Basic Operations:"
python examples/basic_operations.py | head -20

echo "2. Beginner Exercises:"
python exercises/beginner.py | head -20

echo "3. Advanced Queries:"
python examples/advanced_queries.py | head -20

echo "4. Intermediate Exercises:"
python exercises/intermediate.py | head -20

echo "5. Transactions:"
python examples/transactions.py | head -20

echo "6. Stored Procedures:"
python examples/stored_procedures.py | head -20

echo "7. Advanced Exercises:"
python exercises/advanced.py | head -20

echo "🎉 LEARNING PATH COMPLETED SUCCESSFULLY!"
```

**Achievement:** ✅ Full learning path verification completed

### 🏁 **Final Project Status**

```bash
# Show project structure
find . -name "*.py" -o -name "*.sql" -o -name "*.md" | sort

# Check all Python files for syntax
python -m py_compile examples/*.py exercises/*.py config/*.py

# Display project statistics
echo "Project Statistics:"
echo "- Python files: $(find . -name '*.py' | wc -l)"
echo "- SQL files: $(find . -name '*.sql' | wc -l)"
echo "- Total lines of code: $(find . -name '*.py' -exec wc -l {} + | tail -1)"

echo "✅ MySQL Practice Project Complete!"
echo "🎓 Skills Mastered: CRUD, JOINs, Subqueries, Transactions, Stored Procedures, Performance Optimization"
```

## 🎯 **Learning Outcomes Achieved**

| Step | Skill Area | Commands Used | Key Achievements |
|------|------------|---------------|------------------|
| 1-4  | **Setup & Configuration** | `mkdir`, `python -m venv`, `pip install`, `mysql` | ✅ Environment setup, database connection |
| 5.1-5.2 | **Fundamentals** | `python examples/basic_operations.py`, `python exercises/beginner.py` | ✅ CRUD operations, basic queries |
| 5.3 | **Advanced Queries** | `python examples/advanced_queries.py` | ✅ JOINs, subqueries, window functions, analytics |
| 5.4 | **Intermediate Skills** | `python exercises/intermediate.py` | ✅ Complex queries, performance analysis |
| 5.5 | **Transactions** | `python examples/transactions.py` | ✅ ACID properties, transaction safety |
| 5.6 | **Stored Procedures** | `python examples/stored_procedures.py` | ✅ Database programming, procedures, functions |
| 5.7 | **Master Level** | `python exercises/advanced.py` | ✅ Optimization, data warehousing, design analysis |

## Setup

1. **Install MySQL Server**
   - Download and install MySQL Server from [mysql.com](https://dev.mysql.com/downloads/mysql/)
   - Or use Docker: `docker run --name mysql-practice -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0`

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Connection**
   - Copy `.env.example` to `.env`
   - Update the database credentials in `.env`

4. **Create Database**
   ```sql
   CREATE DATABASE practice_db;
   ```

## Project Structure

```
mysql_practice/
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── mysql_practice_notebook.ipynb # Interactive MySQL practice notebook
├── config/
│   └── database.py          # Database connection configuration
├── schemas/
│   ├── create_tables.sql    # SQL scripts to create tables
│   └── sample_data.sql      # Sample data insertion
├── examples/
│   ├── basic_operations.py  # Basic CRUD operations
│   ├── advanced_queries.py  # Complex queries and joins
│   ├── transactions.py      # Transaction handling
│   └── stored_procedures.py # Stored procedures examples
├── exercises/
│   ├── beginner.py          # Beginner level exercises
│   ├── intermediate.py      # Intermediate level exercises
│   └── advanced.py          # Advanced level exercises
└── utils/
    ├── connection.py        # Database connection utilities
    └── helpers.py           # Helper functions
```

## 📓 **Interactive MySQL Practice Notebook**

We've created a comprehensive **hands-on MySQL practice notebook** that provides a complete learning experience from beginner to advanced level!

### 🎯 **Access the Notebook:**
```bash
# Open in Jupyter Lab (recommended)
jupyter lab mysql_practice_notebook.ipynb

# Or open in VS Code with Jupyter extension
code mysql_practice_notebook.ipynb

# Or start Jupyter Notebook
jupyter notebook mysql_practice_notebook.ipynb
```

### 🌟 **What's Inside:**
The notebook contains **12 progressive sections** with:
- **📖 Clear Instructions** for each MySQL concept
- **💡 Helpful Tips** and best practices
- **📝 Empty Code Cells** for hands-on practice
- **🔧 SQL Examples** and syntax references
- **✅ Expected Outputs** to guide your learning

### 📚 **Learning Path:**
1. **📦 Install MySQL Connector** - Setup and configuration
2. **🔌 Connect to Database** - Establish database connections
3. **🗃️ Create Database** - Database creation and management
4. **📋 Create Tables** - Table design with proper relationships
5. **➕ Insert Data** - Adding sample data with best practices
6. **🔍 Query Data** - SELECT queries with conditions and sorting
7. **✏️ Update Data** - Safe data modification techniques
8. **🗑️ Delete Data** - Safe deletion with proper WHERE clauses
9. **🔗 Join Tables** - INNER/LEFT joins and relationship queries
10. **📊 Aggregate Data** - GROUP BY, COUNT, SUM, AVG functions
11. **🚀 Advanced Queries** - Subqueries, EXISTS, CTEs, window functions
12. **🔒 Close Connections** - Proper resource cleanup

### 🎓 **Perfect For:**
- **Beginners** starting with MySQL
- **Students** learning database concepts
- **Developers** refreshing SQL skills
- **Anyone** who prefers interactive learning

### ✨ **Key Features:**
- **Progressive difficulty** from basic to advanced
- **Real-world e-commerce database** example
- **Safety-focused** with warnings about dangerous operations
- **Complete CRUD** operations coverage
- **Advanced topics** like subqueries and window functions
- **Best practices** throughout each section

**🚀 Start your MySQL journey with the interactive notebook!**

## Topics Covered

### Basic Operations
- Creating databases and tables
- INSERT, SELECT, UPDATE, DELETE operations
- Data types and constraints

### Intermediate Topics
- JOINs (INNER, LEFT, RIGHT, FULL)
- Subqueries and CTEs
- Indexes and performance
- Views and triggers

### Advanced Topics
- Stored procedures and functions
- Transactions and ACID properties
- Database normalization
- Performance optimization

## Sample Exercises

1. **E-commerce Database**: Create tables for products, customers, orders
2. **Library Management**: Books, authors, borrowers, loans
3. **Employee Management**: Departments, employees, salaries, projects
4. **Social Media**: Users, posts, comments, likes, followers

## Running Examples

```bash
# Run basic operations
python examples/basic_operations.py

# Run advanced queries
python examples/advanced_queries.py

# Start with beginner exercises
python exercises/beginner.py
```

## Learning Path

### 🎯 **Quick Start (One Command)**
```bash
# Run the complete learning path
./run_learning_path.sh
```

### 📚 **Step-by-Step Learning**
1. **Basic Operations**: `python examples/basic_operations.py`
   - ✅ CRUD operations, data types, basic queries
2. **Beginner Practice**: `python exercises/beginner.py`
   - ✅ Customer management, order processing exercises
3. **Advanced Queries**: `python examples/advanced_queries.py`
   - ✅ Complex JOINs, subqueries, window functions, analytics
4. **Intermediate Practice**: `python exercises/intermediate.py`
   - ✅ Complex analysis, performance optimization
5. **Transactions**: `python examples/transactions.py`
   - ✅ ACID properties, transaction safety, isolation levels
6. **Stored Procedures**: `python examples/stored_procedures.py`
   - ✅ Database programming, procedures, functions
7. **Advanced Challenge**: `python exercises/advanced.py`
   - ✅ Query optimization, data warehousing, design analysis

### 📊 **Progress Tracking**
- **Beginner** (Steps 1-2): Basic SQL operations
- **Intermediate** (Steps 3-4): Complex queries and analysis
- **Advanced** (Steps 5-7): Professional database development

## 🚀 **Quick Commands Reference**

```bash
# Setup (one-time)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your DB credentials
python create_database.py

# Run complete learning path
./run_learning_path.sh

# Run individual steps
python examples/basic_operations.py      # Step 1
python exercises/beginner.py            # Step 2  
python examples/advanced_queries.py     # Step 3
python exercises/intermediate.py        # Step 4
python examples/transactions.py         # Step 5
python examples/stored_procedures.py    # Step 6
python exercises/advanced.py            # Step 7
```

## Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python MySQL Tutorial](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🆕 **New Features Added**

This project now includes several professional-grade enhancements:

### 🐳 **Docker Integration**
- Complete Docker Compose setup with MySQL, phpMyAdmin, and Python app
- One-command environment setup: `docker-compose up -d`
- Isolated development environment with automatic database initialization

### 🖥️ **Interactive CLI Tool**  
- Comprehensive command-line interface: `python cli.py`
- Interactive mode for guided learning
- Direct command execution: `python cli.py examples --type basic`
- Built-in help and status checking

### 📊 **Jupyter Notebook Tutorials**
- Interactive data analysis and visualization notebooks
- Step-by-step MySQL learning with real-time execution
- Integration with pandas, matplotlib, and seaborn
- Located in `notebooks/mysql_tutorial.ipynb`

### 🔍 **Advanced Monitoring System**
- Real-time database performance monitoring
- Query profiling with optimization suggestions  
- System resource tracking (CPU, memory, disk)
- Comprehensive logging and alerting
- Performance reports and metrics collection

### 🚀 **CI/CD Pipeline**
- GitHub Actions workflow for automated testing
- Multi-Python version compatibility testing
- Code quality checks (black, flake8, mypy, isort)
- Docker integration testing
- Coverage reporting with Codecov

### 📖 **Professional Documentation**
- Comprehensive documentation hub in `docs/` directory
- Quick start guide for immediate setup
- API documentation and troubleshooting guides
- Contributing guidelines and FAQ

### 🛠️ **Enhanced Development Tools**
- Automated test suite with pytest
- Code formatting and linting setup
- Type checking with mypy
- Import sorting with isort
- Performance benchmarking utilities
