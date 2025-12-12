#!/bin/bash
# Setup Git hooks for pre-push testing
# Run this script to install the pre-push hook

set -e

echo "Setting up Git hooks for synqed-python..."
echo ""

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Copy pre-push hook
if [ -f ".git/hooks/pre-push" ]; then
    echo "Pre-push hook already exists. Creating backup..."
    cp .git/hooks/pre-push .git/hooks/pre-push.backup
fi

cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Pre-push hook that runs all CI tests
# This ensures all tests pass before code is pushed to remote

set -e

echo "🔍 Running pre-push checks..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Set test API keys if not already set
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-test-key}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-test-key}"

# Track if any tests fail
FAILED=0

# Function to run tests and capture result
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo "${YELLOW}Running $test_name...${NC}"
    if eval "$test_cmd"; then
        echo "${GREEN}✓ $test_name passed${NC}"
        echo ""
        return 0
    else
        echo "${RED}✗ $test_name failed${NC}"
        echo ""
        FAILED=1
        return 1
    fi
}

# Run core tests
run_test "Core Tests" "pytest tests/ --ignore=tests/examples/ -v --tb=short -q"

# Run example tests
run_test "Example Tests" "pytest tests/examples/ -v --tb=short -q"

# Check if any tests failed
if [ $FAILED -eq 1 ]; then
    echo "${RED}========================================${NC}"
    echo "${RED}❌ PRE-PUSH CHECKS FAILED${NC}"
    echo "${RED}========================================${NC}"
    echo ""
    echo "Fix the failing tests before pushing."
    echo "To skip this check (NOT RECOMMENDED), use:"
    echo "  git push --no-verify"
    echo ""
    exit 1
fi

echo "${GREEN}========================================${NC}"
echo "${GREEN}✅ ALL PRE-PUSH CHECKS PASSED${NC}"
echo "${GREEN}========================================${NC}"
echo ""
echo "Proceeding with push..."
exit 0
EOF

chmod +x .git/hooks/pre-push

echo "✅ Pre-push hook installed successfully!"
echo ""
echo "Now all CI tests (core + examples) will run before every push."
echo "If tests fail, the push will be blocked."
echo ""
echo "To test it, run: git push --dry-run"
echo "To skip the hook (not recommended): git push --no-verify"

