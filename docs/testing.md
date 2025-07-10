# Testing Guide

This document explains how to run tests for the MySQL Practice Project.

## Quick Start

### Option 1: Automated Test Runner (Recommended)
```bash
# Auto-detect environment and run all tests
./run_tests.sh

# Force Docker environment
./run_tests.sh --docker

# Force local environment  
./run_tests.sh --local

# Show help
./run_tests.sh --help
```

### Option 2: Manual Testing

#### Docker Environment (Recommended)
```bash
# Start services
docker-compose up -d

# Run unittest
docker exec -it mysql_practice_app python tests/test_database.py

# Run pytest
docker exec -it mysql_practice_app pytest tests/ -v

# Run CLI tests
docker exec -it mysql_practice_app python cli.py tests
```

#### Local Environment
```bash
# Install dependencies (if needed)
pip install -r requirements-dev.txt

# Run unittest (works without database)
python tests/test_database.py

# Run pytest (requires pytest)
pytest tests/ -v

# Run CLI tests
python cli.py tests
```

## Test Types

### 1. Database Operations Tests
- **Connection testing**: Validates database connectivity
- **Schema validation**: Ensures all tables exist with correct structure
- **Data integrity**: Verifies sample data and foreign key constraints
- **Query functionality**: Tests basic and advanced SQL operations

### 2. Performance Tests
- **Query execution time**: Ensures queries complete within reasonable time
- **Index usage**: Verifies proper database indexing

### 3. Integration Tests
- **CLI functionality**: Tests command-line interface
- **API endpoints**: Validates REST API (when running)

## Test Configuration

The test suite automatically handles different environments:

- **Docker**: Full database connectivity with all features
- **Local without DB**: Gracefully skips database-dependent tests
- **CI/CD**: Runs in containerized environment

## Environment Detection

The test runner automatically detects:
- Docker availability and service status
- Python virtual environment
- Available dependencies (pytest, mysql-connector, etc.)
- Database connectivity

## Troubleshooting

### Database Connection Issues
```bash
# Check Docker services
docker-compose ps

# Restart services
docker-compose restart

# Check database logs
docker-compose logs mysql
```

### Missing Dependencies
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Or install minimal requirements
pip install -r requirements.txt
```

### Test Failures
- Database tests require MySQL to be running
- Performance tests may fail on slow systems (adjust thresholds)
- CLI tests require all project dependencies

## Continuous Integration

Tests are automatically run in CI/CD pipelines:
- GitHub Actions runs full test suite in Docker
- All tests must pass before merging
- Coverage reports generated automatically
