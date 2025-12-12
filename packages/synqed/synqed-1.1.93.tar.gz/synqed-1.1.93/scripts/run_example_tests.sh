#!/bin/bash
# Run all example tests with proper environment setup

set -e

echo "=========================================="
echo "Running Example Tests for synqed-python"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Must run from synqed-python root directory"
    exit 1
fi

# Set default API keys if not set (for testing structure)
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-test-key}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-test-key}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Environment:"
echo "  Python: $(python --version)"
echo "  pytest: $(pytest --version | head -n 1)"
echo ""

# Run different test categories
echo "${YELLOW}Running intro example tests...${NC}"
pytest tests/examples/intro/ -v --tb=short

echo ""
echo "${YELLOW}Running email example tests...${NC}"
pytest tests/examples/email/ -v --tb=short

echo ""
echo "${YELLOW}Running multi-agentic example tests...${NC}"
pytest tests/examples/multi_agentic/ -v --tb=short

echo ""
echo "${YELLOW}Running universal demo tests...${NC}"
pytest tests/examples/universal_demo/ -v --tb=short

echo ""
echo "${YELLOW}Running maker hanoi test...${NC}"
pytest tests/examples/test_maker_hanoi.py -v --tb=short

echo ""
echo "${GREEN}=========================================="
echo "All Example Tests Complete!"
echo "==========================================${NC}"
echo ""

# Run with coverage (optional)
if [ "$1" = "--coverage" ]; then
    echo "${YELLOW}Running tests with coverage...${NC}"
    pytest tests/examples/ -v --cov=src/synqed --cov-report=term-missing --cov-report=html
    echo ""
    echo "Coverage report generated in htmlcov/"
fi

# Run integration tests if API keys are real (optional)
if [ "$1" = "--integration" ] && [ "$ANTHROPIC_API_KEY" != "test-key" ]; then
    echo ""
    echo "${YELLOW}Running integration tests with real API calls...${NC}"
    pytest tests/examples/ -v -m "integration" --tb=short
fi

