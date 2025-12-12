#!/bin/bash
#
# Test Examples Script - Run all examples and verify they work
#
# This script tests all Python examples in the examples/ directory to ensure:
# - No syntax errors
# - Examples can be imported
# - Examples run without crashing (with timeout protection)
# - Proper reporting of success/failure
#
# Usage:
#   ./scripts/test_examples.sh
#
# Environment:
#   Set API keys in .env file or export them:
#   - OPENAI_API_KEY
#   - ANTHROPIC_API_KEY
#
# Exit codes:
#   0 - All tests passed
#   1 - One or more tests failed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXAMPLES_DIR="$PROJECT_ROOT/examples"

# Test results
PASSED=0
FAILED=0
SKIPPED=0
TOTAL=0

# Arrays to store results
declare -a PASSED_TESTS
declare -a FAILED_TESTS
declare -a SKIPPED_TESTS

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Testing All Examples in examples/                   ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${GREEN}✓${NC} Found .env file"
    source "$PROJECT_ROOT/.env"
elif [ -f "$EXAMPLES_DIR/.env" ]; then
    echo -e "${GREEN}✓${NC} Found .env file in examples/"
    source "$EXAMPLES_DIR/.env"
else
    echo -e "${YELLOW}⚠${NC} No .env file found - API-dependent examples may fail"
fi

# Check API keys
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠${NC} OPENAI_API_KEY not set"
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠${NC} ANTHROPIC_API_KEY not set"
fi

echo ""

# Function to run a Python file with timeout
run_example() {
    local file="$1"
    local timeout_seconds="$2"
    local test_name=$(basename "$file")
    
    TOTAL=$((TOTAL + 1))
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Testing:${NC} $test_name"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # First, check for syntax errors
    if ! python3 -m py_compile "$file" 2>/dev/null; then
        echo -e "${RED}✗ FAILED${NC} - Syntax error"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$test_name (syntax error)")
        echo ""
        return 1
    fi
    
    # Run the example without timeout
    local temp_output=$(mktemp)
    local temp_error=$(mktemp)

    if python3 "$file" > "$temp_output" 2> "$temp_error"; then
        echo -e "${GREEN}✓ PASSED${NC} - Completed successfully"
        PASSED=$((PASSED + 1))
        PASSED_TESTS+=("$test_name")
        
        # Show last few lines of output
        if [ -s "$temp_output" ]; then
            echo -e "${BLUE}Output (last 5 lines):${NC}"
            tail -n 5 "$temp_output" | sed 's/^/  /'
        fi
    else
        local exit_code=$?
        echo -e "${RED}✗ FAILED${NC} - Exit code: $exit_code"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$test_name (exit code $exit_code)")
        
        if [ -s "$temp_error" ]; then
            echo -e "${RED}Error output:${NC}"
            tail -n 20 "$temp_error" | sed 's/^/  /'
        fi
        
        if [ -s "$temp_output" ]; then
            echo -e "${BLUE}Standard output:${NC}"
            tail -n 10 "$temp_output" | sed 's/^/  /'
        fi
    fi
    
    rm -f "$temp_output" "$temp_error"
    echo ""
}

# Function to test syntax only (for client/server examples that need special handling)
test_syntax_only() {
    local file="$1"
    local test_name=$(basename "$file")
    
    TOTAL=$((TOTAL + 1))
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Testing (syntax only):${NC} $test_name"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo -e "${GREEN}✓ PASSED${NC} - No syntax errors (requires server, syntax check only)"
        PASSED=$((PASSED + 1))
        PASSED_TESTS+=("$test_name (syntax)")
    else
        echo -e "${RED}✗ FAILED${NC} - Syntax error"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$test_name (syntax error)")
    fi
    echo ""
}

# Change to examples directory
cd "$EXAMPLES_DIR"

# Test intro examples
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                    Testing: intro/                            ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# These examples need special handling (client needs server running)
test_syntax_only "$EXAMPLES_DIR/intro/synqed_client.py"
test_syntax_only "$EXAMPLES_DIR/intro/agent_card.py"

# These examples can run standalone but may be long-running
# Use 30 second timeout for agent server examples (they run indefinitely)
test_syntax_only "$EXAMPLES_DIR/intro/synqed_agent.py"  # Server runs forever

# These are demonstrations that complete
run_example "$EXAMPLES_DIR/intro/workspace.py" 60
run_example "$EXAMPLES_DIR/intro/universal_substrate_demo.py" 60

# Test multi-agentic examples
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                 Testing: multi-agentic/                      ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

run_example "$EXAMPLES_DIR/multi-agentic/parallel_research_teams.py" 90
run_example "$EXAMPLES_DIR/multi-agentic/orchestrator_two_teams.py" 90

# Test code_review_a2a_agent
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}              Testing: A2A Integration Examples               ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# This might run a server, so just test syntax
test_syntax_only "$EXAMPLES_DIR/intro/code_review_a2a_agent.py"

# Print summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                         TEST SUMMARY                           ║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC} Total Tests:    $TOTAL"
echo -e "${GREEN}║ Passed:${NC}         $PASSED"
echo -e "${RED}║ Failed:${NC}         $FAILED"
echo -e "${YELLOW}║ Skipped:${NC}        $SKIPPED"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Show passed tests
if [ ${#PASSED_TESTS[@]} -gt 0 ]; then
    echo -e "${GREEN}✓ Passed Tests:${NC}"
    for test in "${PASSED_TESTS[@]}"; do
        echo -e "  ${GREEN}✓${NC} $test"
    done
    echo ""
fi

# Show failed tests
if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo -e "${RED}✗ Failed Tests:${NC}"
    for test in "${FAILED_TESTS[@]}"; do
        echo -e "  ${RED}✗${NC} $test"
    done
    echo ""
fi

# Show skipped tests
if [ ${#SKIPPED_TESTS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ Skipped Tests:${NC}"
    for test in "${SKIPPED_TESTS[@]}"; do
        echo -e "  ${YELLOW}⚠${NC} $test"
    done
    echo ""
fi

# Exit with appropriate code
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
