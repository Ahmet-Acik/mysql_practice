#!/bin/bash

# MySQL Practice Project - Complete Learning Path Script
# Run this script to execute the entire learning journey

echo "🚀 MySQL Practice Project - Complete Learning Path"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to run with status
run_with_status() {
    local description="$1"
    local command="$2"
    local brief="${3:-false}"
    
    echo -e "\n${BLUE}📋 $description${NC}"
    echo "Command: $command"
    echo "----------------------------------------"
    
    if eval "$command"; then
        echo -e "${GREEN}✅ Success: $description${NC}"
    else
        echo -e "${RED}❌ Failed: $description${NC}"
        return 1
    fi
    
    if [ "$brief" = "true" ]; then
        echo "... (output truncated for brevity)"
    fi
    
    echo ""
}

# Check if virtual environment is activated
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        echo -e "${YELLOW}⚠️  Virtual environment not detected. Activating...${NC}"
        source .venv/bin/activate 2>/dev/null || {
            echo -e "${RED}❌ Virtual environment not found. Please run: python -m venv .venv && source .venv/bin/activate${NC}"
            exit 1
        }
    else
        echo -e "${GREEN}✅ Virtual environment active: $VIRTUAL_ENV${NC}"
    fi
}

# Main execution
main() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    check_venv
    
    echo -e "\n${YELLOW}🎯 Starting MySQL Practice Learning Path${NC}"
    echo "This will run all examples and exercises in sequence..."
    
    # Step 1: Basic Operations
    run_with_status "Step 1: Basic CRUD Operations" \
        "python examples/basic_operations.py | head -30" \
        true
    
    # Step 2: Beginner Exercises
    run_with_status "Step 2: Beginner Level Exercises" \
        "python exercises/beginner.py | head -30" \
        true
    
    # Step 3: Advanced Queries
    run_with_status "Step 3: Advanced Queries and Analytics" \
        "python examples/advanced_queries.py | head -40" \
        true
    
    # Step 4: Intermediate Exercises
    run_with_status "Step 4: Intermediate Level Exercises" \
        "python exercises/intermediate.py | head -40" \
        true
    
    # Step 5: Transactions
    run_with_status "Step 5: Transaction Management" \
        "python examples/transactions.py | head -30" \
        true
    
    # Step 6: Stored Procedures
    run_with_status "Step 6: Stored Procedures and Functions" \
        "python examples/stored_procedures.py | head -30" \
        true
    
    # Step 7: Advanced Exercises
    run_with_status "Step 7: Advanced Database Concepts" \
        "python exercises/advanced.py | head -40" \
        true
    
    # Final summary
    echo -e "\n${GREEN}🎉 CONGRATULATIONS! Learning Path Completed!${NC}"
    echo "=================================================="
    echo -e "${BLUE}📊 Skills Mastered:${NC}"
    echo "✅ Basic CRUD Operations"
    echo "✅ Complex JOINs and Subqueries" 
    echo "✅ Window Functions and Analytics"
    echo "✅ Transaction Management"
    echo "✅ Stored Procedures and Functions"
    echo "✅ Performance Optimization"
    echo "✅ Data Warehousing Concepts"
    echo "✅ Database Design Analysis"
    
    echo -e "\n${BLUE}📁 Project Files Created:${NC}"
    find . -name "*.py" -not -path "./.venv/*" | sort
    
    echo -e "\n${BLUE}📈 Project Statistics:${NC}"
    echo "- Python files: $(find . -name '*.py' -not -path './.venv/*' | wc -l)"
    echo "- SQL files: $(find . -name '*.sql' | wc -l)"
    echo "- Total lines of code: $(find . -name '*.py' -not -path './.venv/*' -exec wc -l {} + | tail -1 | awk '{print $1}')"
    
    echo -e "\n${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Practice with your own datasets"
    echo "2. Explore MySQL 8.0 advanced features"
    echo "3. Learn other databases (PostgreSQL, MongoDB)"
    echo "4. Build real-world applications"
    echo "5. Study data engineering and ETL processes"
}

# Run main function
main "$@"
