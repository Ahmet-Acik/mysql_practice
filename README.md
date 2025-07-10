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
# Run all examples in sequence to verify everything works
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

1. Start with `examples/basic_operations.py`
2. Practice with `exercises/beginner.py`
3. Move to `examples/advanced_queries.py`
4. Continue with `exercises/intermediate.py`
5. Explore `examples/transactions.py` and `examples/stored_procedures.py`
6. Challenge yourself with `exercises/advanced.py`

## Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python MySQL Tutorial](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
