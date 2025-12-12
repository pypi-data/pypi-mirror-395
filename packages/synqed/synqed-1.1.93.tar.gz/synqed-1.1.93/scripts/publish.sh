#!/bin/bash
#
# Synqed Publishing Script
# Usage: ./scripts/publish.sh [--test|--prod]
#
# Environment variables (set in .env file):
#   TWINE_PASSWORD - PyPI API token for production
#   TWINE_TEST_PASSWORD - Test PyPI API token
#   TWINE_USERNAME - Username (default: __token__)
#

set -e

# Load .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if build tools are installed
check_dependencies() {
    print_info "Checking dependencies..."
    
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed"
        exit 1
    fi
    
    if ! python -c "import build" &> /dev/null; then
        print_error "build module not found. Install with: pip install build"
        exit 1
    fi
    
    if ! python -c "import twine" &> /dev/null; then
        print_error "twine not found. Install with: pip install twine"
        exit 1
    fi
    
    print_info "All dependencies are installed"
}

# Clean previous builds
clean_build() {
    print_info "Cleaning previous builds..."
    rm -rf dist/ build/ *.egg-info src/*.egg-info
    print_info "Clean complete"
}

# Build the package
build_package() {
    print_info "Building package..."
    python -m build
    
    if [ $? -ne 0 ]; then
        print_error "Build failed"
        exit 1
    fi
    
    print_info "Build successful"
}

# Check the built package
check_package() {
    print_info "Checking package with twine..."
    twine check dist/*
    
    if [ $? -ne 0 ]; then
        print_error "Package check failed"
        exit 1
    fi
    
    print_info "Package check passed"
}

# Get version from pyproject.toml
get_version() {
    python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])" 2>/dev/null || \
    python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])" 2>/dev/null || \
    grep "^version = " pyproject.toml | cut -d'"' -f2
}

# Increment version by 0.0.1
increment_version() {
    print_info "Incrementing version..."
    
    CURRENT_VERSION=$(get_version)
    print_info "Current version: $CURRENT_VERSION"
    
    # Split version into major.minor.patch
    IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"
    MAJOR="${version_parts[0]}"
    MINOR="${version_parts[1]}"
    PATCH="${version_parts[2]}"
    
    # Increment patch version
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
    
    # Update pyproject.toml
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
        # Also update __init__.py
        sed -i '' "s/^__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/synqed/__init__.py
    else
        # Linux
        sed -i "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
        # Also update __init__.py
        sed -i "s/^__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/synqed/__init__.py
    fi
    
    print_info "Version updated in pyproject.toml and __init__.py: $CURRENT_VERSION → $NEW_VERSION"
    
    # Update python-backend to use the new version
    update_python_backend "$NEW_VERSION"
}

# Update python-backend to use the new synqed version
update_python_backend() {
    NEW_VERSION="$1"
    BACKEND_DIR="../python-backend"
    
    if [ ! -d "$BACKEND_DIR" ]; then
        print_warning "python-backend directory not found at $BACKEND_DIR - skipping backend update"
        return
    fi
    
    print_info "Updating python-backend to use synqed>=$NEW_VERSION..."
    
    # Update requirements.txt
    if [ -f "$BACKEND_DIR/requirements.txt" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS - update both the comment and the actual requirement
            sed -i '' "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/requirements.txt"
        else
            # Linux
            sed -i "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/requirements.txt"
        fi
        print_info "  ✓ Updated $BACKEND_DIR/requirements.txt"
    fi
    
    # Update DEPLOY_TO_FLY.md if it exists and has version references
    if [ -f "$BACKEND_DIR/DEPLOY_TO_FLY.md" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/synqed_version\": \"[^\"]*\"/synqed_version\": \"$NEW_VERSION\"/" "$BACKEND_DIR/DEPLOY_TO_FLY.md"
            sed -i '' "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/DEPLOY_TO_FLY.md"
        else
            sed -i "s/synqed_version\": \"[^\"]*\"/synqed_version\": \"$NEW_VERSION\"/" "$BACKEND_DIR/DEPLOY_TO_FLY.md"
            sed -i "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/DEPLOY_TO_FLY.md"
        fi
        print_info "  ✓ Updated $BACKEND_DIR/DEPLOY_TO_FLY.md"
    fi
    
    # Update README.md if it has version references
    if [ -f "$BACKEND_DIR/README.md" ]; then
        if grep -q "synqed>=" "$BACKEND_DIR/README.md"; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/README.md"
            else
                sed -i "s/synqed>=.*$/synqed>=$NEW_VERSION/" "$BACKEND_DIR/README.md"
            fi
            print_info "  ✓ Updated $BACKEND_DIR/README.md"
        fi
    fi
    
    print_info "python-backend updated to synqed>=$NEW_VERSION"
}

# Upload to Test PyPI
upload_test() {
    print_info "Uploading to Test PyPI..."
    
    # Check for token
    if [ -z "$TWINE_TEST_PASSWORD" ] && [ -z "$TWINE_PASSWORD" ]; then
        print_error "TWINE_TEST_PASSWORD not set in .env file"
        print_info "Please add your Test PyPI token to .env:"
        echo "  TWINE_TEST_PASSWORD=your-test-token-here"
        exit 1
    fi
    
    # Use test token if available, otherwise fall back to production token
    TOKEN="${TWINE_TEST_PASSWORD:-$TWINE_PASSWORD}"
    USERNAME="${TWINE_USERNAME:-__token__}"
    
    twine upload --repository testpypi dist/* --username "$USERNAME" --password "$TOKEN"
    
    if [ $? -eq 0 ]; then
        VERSION=$(get_version)
        print_info "Successfully uploaded to Test PyPI"
        print_info "View at: https://test.pypi.org/project/synqed/$VERSION/"
        print_info ""
        print_info "To test installation:"
        echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple synqed"
    else
        print_error "Upload to Test PyPI failed"
        exit 1
    fi
}

# Upload to Production PyPI
upload_prod() {
    print_warning "You are about to upload to PRODUCTION PyPI"
    print_warning "This cannot be undone. Are you sure? (yes/no)"
    read -r confirmation
    
    if [ "$confirmation" != "yes" ]; then
        print_info "Upload cancelled"
        exit 0
    fi
    
    # Check for token
    if [ -z "$TWINE_PASSWORD" ]; then
        print_error "TWINE_PASSWORD not set in .env file"
        print_info "Please add your PyPI token to .env:"
        echo "  TWINE_PASSWORD=your-production-token-here"
        exit 1
    fi
    
    print_info "Uploading to Production PyPI..."
    
    USERNAME="${TWINE_USERNAME:-__token__}"
    
    twine upload dist/* --username "$USERNAME" --password "$TWINE_PASSWORD"
    
    if [ $? -eq 0 ]; then
        VERSION=$(get_version)
        print_info "Successfully uploaded to Production PyPI"
        print_info "View at: https://pypi.org/project/synqed/$VERSION/"
        print_info ""
        print_info "To install:"
        echo "  pip install synqed"
    else
        print_error "Upload to Production PyPI failed"
        exit 1
    fi
}

# Main script
main() {
    # Parse arguments
    TARGET=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --test)
                TARGET="test"
                shift
                ;;
            --prod)
                TARGET="prod"
                shift
                ;;
            --help)
                echo "Usage: $0 [--test|--prod]"
                echo ""
                echo "Options:"
                echo "  --test    Upload to Test PyPI"
                echo "  --prod    Upload to Production PyPI"
                echo "  --help    Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    if [ -z "$TARGET" ]; then
        print_error "Please specify --test or --prod"
        echo "Use --help for usage information"
        exit 1
    fi
    
    # Run the publishing pipeline
    check_dependencies
    increment_version
    clean_build
    build_package
    check_package
    
    VERSION=$(get_version)
    print_info "Package version: $VERSION"
    
    if [ "$TARGET" = "test" ]; then
        upload_test
    elif [ "$TARGET" = "prod" ]; then
        upload_prod
    fi
    
    echo ""
    print_info "=============================================="
    print_info "PUBLISH COMPLETE - Summary"
    print_info "=============================================="
    print_info "synqed version: $VERSION"
    print_info ""
    print_info "Files updated:"
    print_info "  • synqed-python/pyproject.toml"
    print_info "  • synqed-python/src/synqed/__init__.py"
    if [ -d "../python-backend" ]; then
        print_info "  • python-backend/requirements.txt"
        print_info "  • python-backend/DEPLOY_TO_FLY.md"
    fi
    print_info ""
    print_info "Next steps:"
    print_info "  1. git add -A && git commit -m 'Release synqed v$VERSION'"
    print_info "  2. git push origin main"
    print_info "  3. Deploy python-backend: cd ../python-backend && fly deploy"
    print_info "=============================================="
}

# Run main function
main "$@"

