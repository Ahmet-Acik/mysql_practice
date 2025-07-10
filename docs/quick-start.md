# Quick Start Guide 🚀

Get up and running with the MySQL Practice Project in just a few minutes!

## Prerequisites

- Python 3.9+ installed
- MySQL 8.0+ running locally or Docker
- Basic knowledge of Python and SQL

## Option 1: Local MySQL Setup (5 minutes)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd mysql_practice
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your MySQL credentials
# DB_HOST=localhost
# DB_USER=your_username
# DB_PASSWORD=your_password
```

### 3. Initialize Database
```bash
# Use the interactive CLI
python cli.py setup

# Or run manually
python create_database.py
```

### 4. Start Learning!
```bash
# Interactive mode
python cli.py

# Or run specific examples
python cli.py examples --type basic
python cli.py exercises --level beginner
```

## Option 2: Docker Setup (3 minutes)

### 1. Clone and Start
```bash
git clone <repository-url>
cd mysql_practice

# Start everything with Docker Compose
docker-compose up -d

# Wait for MySQL to be ready (about 30 seconds)
docker-compose logs mysql
```

### 2. Initialize Database
```bash
# Run setup in container
docker-compose exec python-app python create_database.py
```

### 3. Start Learning!
```bash
# Access the container
docker-compose exec python-app bash

# Run examples
python cli.py examples
python cli.py exercises
```

## What's Next?

### 🎓 Follow the Learning Path
1. **Basic Operations** - CRUD operations and simple queries
2. **Advanced Queries** - Joins, subqueries, and complex operations  
3. **Transactions** - ACID properties and transaction management
4. **Stored Procedures** - Creating and using stored procedures
5. **Performance** - Optimization and monitoring

### 📊 Try the Interactive Features
```bash
# Start Jupyter notebooks
jupyter notebook notebooks/

# Launch the REST API
python cli.py api

# Run performance benchmarks
python cli.py benchmark

# Generate sample data
python cli.py generate --count 5000
```

### 🧪 Run Tests
```bash
# Full test suite
python cli.py tests

# Or with pytest directly
pytest tests/ -v
```

### 📈 Access Analytics
```bash
# Business intelligence reports
python cli.py analytics

# Or use the web interface
python cli.py api
# Visit: http://localhost:5000/analytics
```

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `python cli.py` | Interactive mode |
| `python cli.py setup` | Initialize database |
| `python cli.py examples` | Run all examples |
| `python cli.py exercises` | Run all exercises |
| `python cli.py tests` | Run test suite |
| `python cli.py api` | Start REST API |
| `python cli.py analytics` | Generate reports |
| `python cli.py benchmark` | Performance tests |
| `python cli.py generate` | Create sample data |

## Troubleshooting

### Common Issues

**Database Connection Failed?**
```bash
# Check MySQL is running
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Test connection
python -c "from config.database import test_connection; print(test_connection())"
```

**Import Errors?**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Permission Denied?**
```bash
# Check MySQL user privileges
mysql -u your_username -p
SHOW GRANTS FOR CURRENT_USER;
```

### Need Help?

- 📖 Check the [full documentation](README.md)
- 🐛 Search [issues on GitHub](https://github.com/your-repo/issues)
- 💬 Ask questions in [discussions](https://github.com/your-repo/discussions)
- 📧 Contact maintainers

---

**You're all set! Happy learning! 🎉**

Next: [Installation & Setup →](installation.md)
