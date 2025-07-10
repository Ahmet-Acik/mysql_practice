# MySQL Practice Project Makefile
.PHONY: help install setup test lint format check docker-up docker-down clean

# Variables
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose

# Default target
help: ## Show this help message
	@echo "MySQL Practice Project - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Development Setup
install: ## Install project dependencies
	$(PIP) install -r requirements.txt

setup: install ## Setup database and initialize data
	$(PYTHON) create_database.py

dev-install: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install pre-commit
	pre-commit install

# Database Operations
db-setup: ## Initialize database schema and sample data
	$(PYTHON) cli.py setup

db-reset: ## Reset database (drop and recreate)
	$(PYTHON) create_database.py --reset

# Testing
test: ## Run test suite
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Code Quality
lint: ## Run linting checks
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format: ## Format code with black and isort
	black .
	isort .

format-check: ## Check code formatting
	black --check --diff .
	isort --check-only --diff .

type-check: ## Run type checking with mypy
	mypy --ignore-missing-imports .

check: lint format-check type-check ## Run all code quality checks

# Examples and Exercises
examples: ## Run all example scripts
	$(PYTHON) cli.py examples

exercises: ## Run all exercise scripts
	$(PYTHON) cli.py exercises

learning-path: ## Run complete learning path
	bash run_learning_path.sh

# Services
api: ## Start REST API server
	$(PYTHON) cli.py api

jupyter: ## Start Jupyter notebook server
	jupyter notebook notebooks/

monitor: ## Start database monitoring
	$(PYTHON) monitoring/database_monitor.py

# Data Operations
generate-data: ## Generate sample data (1000 records)
	$(PYTHON) cli.py generate --count 1000

generate-large: ## Generate large dataset (10000 records)
	$(PYTHON) cli.py generate --count 10000

benchmark: ## Run performance benchmarks
	$(PYTHON) cli.py benchmark

analytics: ## Run advanced analytics
	$(PYTHON) cli.py analytics

# Docker Operations
docker-up: ## Start Docker environment
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop Docker environment
	$(DOCKER_COMPOSE) down

docker-logs: ## Show Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Access Python container shell
	$(DOCKER_COMPOSE) exec python-app bash

docker-mysql: ## Access MySQL container shell
	$(DOCKER_COMPOSE) exec mysql mysql -u practice_user -p practice_db

docker-mysql-root: ## Access MySQL container as root
	$(DOCKER_COMPOSE) exec mysql mysql -u root -p

docker-setup: docker-up ## Setup Docker environment and initialize database
	@echo "Waiting for MySQL to be ready..."
	@sleep 30
	$(DOCKER_COMPOSE) exec python-app python create_database.py
	@echo "Docker environment ready!"
	@echo "📍 MySQL is available on port 3307 (host) -> 3306 (container)"
	@echo "📍 phpMyAdmin: http://localhost:8080"
	@echo "📍 Use 'make docker-mysql' to access MySQL shell"

docker-test: ## Run tests in Docker environment
	$(DOCKER_COMPOSE) exec python-app python -m pytest tests/ -v

# Maintenance
clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -f .coverage

clean-logs: ## Clean log files
	rm -rf logs/
	find . -name "*.log" -delete
	find . -name "metrics_*.json" -delete

reset: clean ## Reset project (clean + remove database)
	$(DOCKER_COMPOSE) down -v
	rm -f .env

# Documentation
docs: ## Generate documentation
	@echo "Opening documentation..."
	@if command -v open >/dev/null; then open docs/README.md; elif command -v xdg-open >/dev/null; then xdg-open docs/README.md; fi

# Quick Start
quick-start: install setup examples ## Quick start: install, setup, and run examples
	@echo ""
	@echo "🎉 Quick start completed!"
	@echo "Next steps:"
	@echo "  make exercises    # Run learning exercises"
	@echo "  make api         # Start web API"
	@echo "  make jupyter     # Launch notebooks"
	@echo "  make help        # See all commands"

# CI Commands (for GitHub Actions)
ci-install: ## Install dependencies for CI
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

ci-test: ## Run CI test suite
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=xml

ci-check: check ## Run CI code quality checks

# Development Workflow
dev: format lint test ## Run development workflow (format, lint, test)
	@echo "✅ Development checks passed!"

pre-commit: format lint ## Run pre-commit checks
	@echo "✅ Pre-commit checks completed!"

# Status
status: ## Show project status
	@echo "📊 MySQL Practice Project Status"
	@echo "================================"
	@echo ""
	@echo "Environment:"
	@which python
	@python --version
	@echo ""
	@echo "Database Connection:"
	@$(PYTHON) -c "from config.database import test_connection; print('✅ Connected' if test_connection() else '❌ Failed')" 2>/dev/null || echo "❌ Connection test failed"
	@echo ""
	@echo "Docker Status:"
	@$(DOCKER_COMPOSE) ps 2>/dev/null || echo "Docker not running"
	@echo ""
	@echo "Available Commands: make help"
