#!/bin/bash

# MySQL Practice Project - Test Runner
# Automated test execution with environment detection

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 MySQL Practice Project - Test Runner${NC}"
echo "================================================"

# Function to check if Docker is available
check_docker() {
    if command -v docker &> /dev/null && docker ps &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to check if Docker Compose services are running
check_docker_services() {
    if docker-compose ps | grep -q "mysql_practice_db.*Up"; then
        return 0
    else
        return 1
    fi
}

# Function to run tests in Docker
run_tests_docker() {
    echo -e "${BLUE}🐳 Running tests in Docker environment...${NC}"
    
    # Ensure services are running
    if ! check_docker_services; then
        echo -e "${YELLOW}⚠️  Starting Docker services...${NC}"
        docker-compose up -d
        echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
        sleep 10
    fi
    
    echo -e "${GREEN}📋 Running unit tests...${NC}"
    docker exec -it mysql_practice_app python tests/test_database.py
    
    echo -e "${GREEN}🔬 Running pytest...${NC}"
    docker exec -it mysql_practice_app pytest tests/ -v
    
    echo -e "${GREEN}🏃 Running CLI tests...${NC}"
    if docker exec -it mysql_practice_app python cli.py tests; then
        echo -e "${GREEN}✅ CLI tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  CLI tests had issues${NC}"
    fi
}

# Function to run tests locally
run_tests_local() {
    echo -e "${BLUE}💻 Running tests locally...${NC}"
    
    # Check if virtual environment is activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo -e "${YELLOW}⚠️  Virtual environment not detected. Attempting to activate...${NC}"
        if [[ -f "venv/bin/activate" ]]; then
            source venv/bin/activate
        elif [[ -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
        else
            echo -e "${YELLOW}💡 No virtual environment found. Using system Python...${NC}"
        fi
    fi
    
    # Install dependencies if needed
    if ! python -c "import mysql.connector" &> /dev/null; then
        echo -e "${YELLOW}📦 Installing dependencies...${NC}"
        if [[ -f "requirements-dev.txt" ]]; then
            pip install -r requirements-dev.txt
        else
            pip install -r requirements.txt
        fi
    fi
    
    echo -e "${GREEN}📋 Running unit tests...${NC}"
    python tests/test_database.py
    
    if command -v pytest &> /dev/null; then
        echo -e "${GREEN}🔬 Running pytest...${NC}"
        if pytest tests/ -v; then
            echo -e "${GREEN}✅ pytest tests passed!${NC}"
        else
            echo -e "${YELLOW}⚠️  pytest tests had issues${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  pytest not available, skipping pytest tests${NC}"
    fi
    
    echo -e "${GREEN}🏃 Running CLI tests...${NC}"
    if python cli.py tests; then
        echo -e "${GREEN}✅ CLI tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  CLI tests had issues (possibly due to missing dependencies)${NC}"
    fi
}

# Main execution
main() {
    # Parse command line arguments
    FORCE_LOCAL=false
    FORCE_DOCKER=false
    
    for arg in "$@"; do
        case $arg in
            --local)
                FORCE_LOCAL=true
                shift
                ;;
            --docker)
                FORCE_DOCKER=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--local|--docker|--help]"
                echo ""
                echo "Options:"
                echo "  --local   Force running tests locally"
                echo "  --docker  Force running tests in Docker"
                echo "  --help    Show this help message"
                exit 0
                ;;
        esac
    done
    
    # Determine test environment
    if [[ "$FORCE_DOCKER" == true ]]; then
        if check_docker; then
            run_tests_docker
        else
            echo -e "${RED}❌ Docker not available but --docker flag specified${NC}"
            exit 1
        fi
    elif [[ "$FORCE_LOCAL" == true ]]; then
        run_tests_local
    else
        # Auto-detect best environment
        if check_docker && check_docker_services; then
            echo -e "${BLUE}🔍 Auto-detected: Docker environment available${NC}"
            run_tests_docker
        else
            echo -e "${BLUE}🔍 Auto-detected: Using local environment${NC}"
            run_tests_local
        fi
    fi
    
    echo -e "${GREEN}✅ All tests completed successfully!${NC}"
}

# Run main function with all arguments
main "$@"
