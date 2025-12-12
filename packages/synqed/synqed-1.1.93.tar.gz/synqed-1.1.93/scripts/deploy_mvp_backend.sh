#!/bin/bash

#
# deploy_mvp_backend.sh
#
# Deploys the Synq MVP Backend to Fly.io.
# This backend provides orchestration endpoints for the Next.js MVP frontend,
# using the Synqed library internally for multi-agent coordination.
#
# Usage:
#   ./scripts/deploy_mvp_backend.sh [--app-name NAME] [--region REGION]
#
# Prerequisites:
#   - flyctl installed and authenticated (flyctl auth login)
#   - ANTHROPIC_API_KEY set or ready to configure
#
# The MVP backend runs as a separate Fly.io app alongside the core Synqed infrastructure.
#

set -e

echo "=========================================="
echo "Synq MVP Backend - Fly.io Deployment"
echo "=========================================="
echo ""

# Default configuration
APP_NAME="${FLY_APP_NAME:-synq-mvp-backend}"
REGION="${FLY_REGION:-sjc}"
BACKEND_DIR="python-backend"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --app-name)
            APP_NAME="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--app-name NAME] [--region REGION]"
            echo ""
            echo "Options:"
            echo "  --app-name NAME    Fly.io app name (default: synq-mvp-backend)"
            echo "  --region REGION    Fly.io region (default: sjc)"
            echo "  --help             Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  FLY_APP_NAME       Override default app name"
            echo "  FLY_REGION         Override default region"
            echo "  ANTHROPIC_API_KEY  Required API key (will prompt if not set)"
            exit 0
            ;;
        *)
            echo "❌ Unknown option: $1"
            echo "   Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if flyctl is installed, install if needed
if ! command -v flyctl &> /dev/null; then
    echo "📦 flyctl is not installed. Installing now..."
    echo ""
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Detected macOS. Installing flyctl via Homebrew or curl..."
        if command -v brew &> /dev/null; then
            echo "Using Homebrew..."
            brew install flyctl
        else
            echo "Using curl installer..."
            curl -L https://fly.io/install.sh | sh
            
            # Add to PATH for current session
            export FLYCTL_INSTALL="$HOME/.fly"
            export PATH="$FLYCTL_INSTALL/bin:$PATH"
            
            echo ""
            echo "⚠️  Note: Add flyctl to your PATH permanently:"
            echo "   echo 'export FLYCTL_INSTALL=\"\$HOME/.fly\"' >> ~/.zshrc"
            echo "   echo 'export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\"' >> ~/.zshrc"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Detected Linux. Installing flyctl..."
        curl -L https://fly.io/install.sh | sh
        
        # Add to PATH for current session
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    else
        echo "❌ Error: Unsupported OS: $OSTYPE"
        echo "   Please install flyctl manually from: https://fly.io/docs/hands-on/install-flyctl/"
        exit 1
    fi
    
    echo ""
    
    # Verify installation
    if ! command -v flyctl &> /dev/null; then
        echo "❌ Error: flyctl installation failed"
        echo "   Please install manually from: https://fly.io/docs/hands-on/install-flyctl/"
        exit 1
    fi
    
    echo "✅ flyctl installed successfully!"
    echo ""
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Not logged in to Fly.io. Let's authenticate..."
    echo ""
    echo "This will open your browser to log in."
    read -p "Press Enter to continue..."
    echo ""
    
    flyctl auth login
    
    echo ""
    
    # Verify login succeeded
    if ! flyctl auth whoami &> /dev/null; then
        echo "❌ Error: Authentication failed"
        echo "   Please try: flyctl auth login"
        exit 1
    fi
    
    echo "✅ Successfully authenticated!"
    echo ""
fi

echo "✅ flyctl is installed and authenticated"
echo ""

# Navigate to backend directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_PATH="$PROJECT_ROOT/../$BACKEND_DIR"

if [ ! -d "$BACKEND_PATH" ]; then
    echo "❌ Error: Backend directory not found at $BACKEND_PATH"
    echo "   Make sure you're running this from synqed-python/scripts/"
    exit 1
fi

cd "$BACKEND_PATH"
echo "📂 Working directory: $BACKEND_PATH"
echo ""

# Check if app exists
echo "🔍 Checking if app '$APP_NAME' exists..."
if flyctl apps list 2>/dev/null | grep -q "^$APP_NAME"; then
    echo "✅ App '$APP_NAME' already exists"
    EXISTING_APP=true
else
    echo "⚠️  App '$APP_NAME' not found"
    EXISTING_APP=false
fi
echo ""

# Create app if it doesn't exist
if [ "$EXISTING_APP" = false ]; then
    echo "🆕 Creating new Fly.io app..."
    echo "   Name:   $APP_NAME"
    echo "   Region: $REGION"
    echo ""
    
    flyctl apps create "$APP_NAME" --org personal
    
    # Initialize fly.toml if needed
    if [ ! -f fly.toml ]; then
        echo "📝 Generating fly.toml configuration..."
        flyctl launch --name "$APP_NAME" --region "$REGION" --no-deploy --yes
    fi
    
    echo ""
fi

# Check and set secrets
echo "🔐 Configuring secrets..."
echo ""

# Check if ANTHROPIC_API_KEY is set
if flyctl secrets list --app "$APP_NAME" 2>/dev/null | grep -q "ANTHROPIC_API_KEY"; then
    echo "✅ ANTHROPIC_API_KEY already configured"
else
    echo "⚠️  ANTHROPIC_API_KEY not found in secrets"
    
    # Check if available in environment
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo ""
        echo "Please enter your Anthropic API key:"
        echo "(Get it from: https://console.anthropic.com/)"
        echo ""
        read -s -p "API Key: " ANTHROPIC_API_KEY
        echo ""
    fi
    
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo "Setting ANTHROPIC_API_KEY secret..."
        flyctl secrets set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" --app "$APP_NAME"
        echo "✅ Secret configured"
    else
        echo "❌ Error: ANTHROPIC_API_KEY is required"
        echo "   Set it with: flyctl secrets set ANTHROPIC_API_KEY=sk-ant-... --app $APP_NAME"
        exit 1
    fi
fi

echo ""

# Verify required files exist
echo "📋 Verifying deployment files..."
REQUIRED_FILES=("main.py" "requirements.txt" "Dockerfile" "fly.toml")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        echo ""
        echo "❌ Error: Required file '$file' not found"
        exit 1
    fi
done
echo ""

# Show what will be deployed
echo "=========================================="
echo "🚀 Ready to Deploy"
echo "=========================================="
echo ""
echo "App Name:     $APP_NAME"
echo "Region:       $REGION"
echo "Source:       $BACKEND_PATH"
echo ""
echo "This will deploy the Synq MVP Backend which provides:"
echo "  • Multi-agent task orchestration"
echo "  • Real-time workspace management"
echo "  • SSE event streaming"
echo "  • User prompt handling"
echo ""
read -p "Continue with deployment? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "=========================================="
echo "📦 Deploying to Fly.io..."
echo "=========================================="
echo ""

# Deploy
flyctl deploy --app "$APP_NAME" --strategy immediate

echo ""
echo "=========================================="
echo "🔧 Ensuring Single Machine (Required for In-Memory State)"
echo "=========================================="
echo ""

# Scale to exactly 1 machine - critical for in-memory state consistency
echo "Setting scale to exactly 1 machine..."
flyctl scale count 1 --app "$APP_NAME" --yes 2>/dev/null || true

# Check for and destroy extra machines
MACHINE_COUNT=$(flyctl machines list --app "$APP_NAME" --json 2>/dev/null | grep -c '"id"' || echo "0")
if [ "$MACHINE_COUNT" -gt 1 ]; then
    echo "⚠️  Found $MACHINE_COUNT machines running. Destroying extras..."
    
    # Get all machine IDs except the first one
    MACHINE_IDS=$(flyctl machines list --app "$APP_NAME" --json 2>/dev/null | grep '"id"' | sed 's/.*: "//;s/".*//' | tail -n +2)
    
    for MACHINE_ID in $MACHINE_IDS; do
        echo "   Destroying machine: $MACHINE_ID"
        flyctl machines destroy "$MACHINE_ID" --app "$APP_NAME" --force 2>/dev/null || true
    done
    
    echo "✅ Extra machines destroyed"
else
    echo "✅ Single machine confirmed"
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""

# Get the deployed URL
APP_URL="https://$APP_NAME.fly.dev"

echo "🌐 Base URL: $APP_URL"
echo ""
echo "📊 Health Check:"
echo "  curl $APP_URL/health"
echo ""
echo "🤖 MVP Orchestration Endpoints:"
echo ""
echo "  Start Task:"
echo "    curl -X POST $APP_URL/api/start_task \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{\"user_task\":\"Create a marketing plan\",\"user_id\":\"user123\"}'"
echo ""
echo "  Get Workspace Tree:"
echo "    curl $APP_URL/api/workspaces/{task_id}/tree"
echo ""
echo "  Stream Events (SSE):"
echo "    curl $APP_URL/api/workspaces/{workspace_id}/events"
echo ""
echo "  Submit User Input:"
echo "    curl -X POST $APP_URL/api/workspaces/{workspace_id}/user_input \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{\"response\":\"Budget: $10k\",\"data\":{}}'"
echo ""
echo "=========================================="
echo "🔗 Integration with Frontend"
echo "=========================================="
echo ""
echo "Update your Next.js frontend (.env.local):"
echo ""
echo "  NEXT_PUBLIC_PYTHON_BACKEND_URL=$APP_URL"
echo ""
echo "=========================================="
echo "📝 Useful Commands"
echo "=========================================="
echo ""
echo "  View logs:       flyctl logs --app $APP_NAME"
echo "  Follow logs:     flyctl logs --app $APP_NAME -f"
echo "  SSH access:      flyctl ssh console --app $APP_NAME"
echo "  App status:      flyctl status --app $APP_NAME"
echo "  Scale memory:    flyctl scale memory 2048 --app $APP_NAME"
echo "  List machines:   flyctl machines list --app $APP_NAME"
echo ""
echo "⚠️  IMPORTANT: Keep exactly 1 machine for in-memory state consistency!"
echo "  If multiple machines appear, destroy extras with:"
echo "    flyctl machines destroy <MACHINE_ID> --app $APP_NAME --force"
echo ""
echo "=========================================="
echo "🏗️  Architecture"
echo "=========================================="
echo ""
echo "Your Synqed ecosystem now includes:"
echo ""
echo "  1. Core Synqed Infrastructure"
echo "     └─ https://synqed.fly.dev"
echo "        ├─ A2A Email Registry"
echo "        └─ Global MCP Server"
echo ""
echo "  2. MVP Backend (This Deployment)"
echo "     └─ $APP_URL"
echo "        ├─ Task Orchestration"
echo "        ├─ Multi-Agent Workspaces"
echo "        └─ Real-time Event Streaming"
echo ""
echo "  3. Next.js Frontend"
echo "     └─ Your deployment (Vercel/localhost)"
echo "        ├─ Clarification UI"
echo "        └─ Workspace Visualization"
echo ""
echo "=========================================="
echo ""
echo "🎉 Success! Your MVP backend is live at:"
echo "   $APP_URL"
echo ""
echo "Test it now:"
echo "  curl $APP_URL/health"
echo ""
echo "=========================================="

