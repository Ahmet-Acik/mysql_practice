# MySQL Practice Project

This project contains examples and exercises for practicing MySQL database operations using Python.

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
