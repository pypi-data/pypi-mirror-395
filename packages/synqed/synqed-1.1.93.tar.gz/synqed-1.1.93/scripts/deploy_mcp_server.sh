#!/bin/bash

#
# deploy_mcp_server.sh
#
# Deploys the Synq Global MCP Server to Fly.io with external connector integrations.
# This server exposes Zoom, Salesforce, and Beautiful tools via MCP protocol.
#
# Usage:
#   ./deploy_mcp_server.sh [app-name]
#
# Prerequisites:
#   - flyctl installed and authenticated (flyctl auth login)
#   - At least one service credential configured (Zoom recommended for testing)
#
# Features:
#   - Original service implementations (zoom_service.py, salesforce_service.py)
#   - External MCP connectors (github.com/echelon-ai-labs/zoom-mcp, github.com/smn2gnt/MCP-Salesforce)
#   - 30+ tools available via unified MCP interface
#

set -e

echo "=========================================="
echo "🚀 Synq Global MCP Server Deployment"
echo "=========================================="
echo ""
echo "This deploys the MCP server with:"
echo "  • Zoom integration (original + connector)"
echo "  • Salesforce integration (original + connector)"
echo "  • Beautiful web scraping"
echo "  • 30+ tools via unified MCP API"
echo ""
echo "=========================================="
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ Error: flyctl is not installed"
    echo ""
    echo "Install with:"
    echo "  curl -L https://fly.io/install.sh | sh"
    echo ""
    echo "Then add to PATH:"
    echo "  export FLYCTL_INSTALL=\"\$HOME/.fly\""
    echo "  export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\""
    echo ""
    exit 1
fi

echo "✅ flyctl is installed"

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "⚠️  Not logged in to Fly.io"
    echo ""
    echo "Logging in now..."
    flyctl auth login
    echo ""
fi

echo "✅ Authenticated with Fly.io"
echo ""

# Get or set app name
DEFAULT_APP_NAME="synq-mcp-server"
if [ -n "$1" ]; then
    APP_NAME="$1"
else
    read -p "Enter app name (default: synq-mcp-server): " USER_APP_NAME
    APP_NAME=${USER_APP_NAME:-$DEFAULT_APP_NAME}
fi

echo ""
echo "📦 App name: $APP_NAME"
echo ""

# Check if app exists
APP_EXISTS=false
if flyctl apps list 2>/dev/null | grep -q "^$APP_NAME"; then
    APP_EXISTS=true
    echo "✅ App '$APP_NAME' already exists"
else
    echo "📦 Creating new app '$APP_NAME'..."
    flyctl apps create "$APP_NAME" --org personal || true
    echo "✅ App created"
fi

echo ""
echo "=========================================="
echo "🔐 Configuring Secrets"
echo "=========================================="
echo ""
echo "You need to configure at least ONE service to test."
echo "Zoom is recommended for quick testing."
echo ""

# Function to set secret if not empty
set_secret_if_provided() {
    local key=$1
    local value=$2
    if [ -n "$value" ]; then
        echo "  • Setting $key"
        flyctl secrets set "$key=$value" --app "$APP_NAME" --stage
    fi
}

# Check if .env file exists for reference
if [ -f .env ]; then
    echo "📄 Found .env file - would you like to use these credentials?"
    read -p "Copy secrets from .env? (y/n): " USE_ENV
    echo ""
    
    if [ "$USE_ENV" = "y" ]; then
        echo "📋 Copying secrets from .env file..."
        
        # Source .env and set secrets
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            [[ $key =~ ^#.*$ ]] && continue
            [[ -z $key ]] && continue
            
            # Remove quotes and whitespace
            value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e 's/^'"'"'//' -e 's/'"'"'$//' | xargs)
            
            # Skip placeholder values
            if [[ $value == *"your_"* ]] || [[ $value == *"_here"* ]]; then
                continue
            fi
            
            # Set non-empty values
            if [ -n "$value" ]; then
                set_secret_if_provided "$key" "$value"
            fi
        done < .env
        
        echo "✅ Secrets copied from .env"
    fi
else
    echo "⚠️  No .env file found"
    echo ""
    echo "You'll need to set secrets manually after deployment:"
    echo ""
    echo "Zoom (required for testing):"
    echo "  flyctl secrets set ZOOM_API_KEY=xxx --app $APP_NAME"
    echo "  flyctl secrets set ZOOM_API_SECRET=xxx --app $APP_NAME"
    echo "  flyctl secrets set ZOOM_ACCOUNT_ID=xxx --app $APP_NAME"
    echo ""
    echo "Salesforce (optional):"
    echo "  flyctl secrets set SALESFORCE_CLIENT_ID=xxx --app $APP_NAME"
    echo "  flyctl secrets set SALESFORCE_CLIENT_SECRET=xxx --app $APP_NAME"
    echo "  flyctl secrets set SALESFORCE_REFRESH_TOKEN=xxx --app $APP_NAME"
    echo "  flyctl secrets set SALESFORCE_INSTANCE_URL=https://xxx.salesforce.com --app $APP_NAME"
    echo ""
    echo "Beautiful (optional):"
    echo "  flyctl secrets set BEAUTIFUL_API_KEY=xxx --app $APP_NAME"
    echo ""
    
    read -p "Set secrets manually now? (y/n): " SET_MANUAL
    echo ""
    
    if [ "$SET_MANUAL" = "y" ]; then
        echo "📝 Setting Zoom credentials (required):"
        read -p "ZOOM_API_KEY: " ZOOM_KEY
        read -p "ZOOM_API_SECRET: " ZOOM_SECRET
        read -p "ZOOM_ACCOUNT_ID: " ZOOM_ACCOUNT
        
        set_secret_if_provided "ZOOM_API_KEY" "$ZOOM_KEY"
        set_secret_if_provided "ZOOM_API_SECRET" "$ZOOM_SECRET"
        set_secret_if_provided "ZOOM_ACCOUNT_ID" "$ZOOM_ACCOUNT"
        
        echo ""
        read -p "Configure Salesforce? (y/n): " CONFIG_SF
        if [ "$CONFIG_SF" = "y" ]; then
            echo ""
            echo "📝 Setting Salesforce credentials:"
            read -p "SALESFORCE_CLIENT_ID: " SF_CLIENT_ID
            read -p "SALESFORCE_CLIENT_SECRET: " SF_CLIENT_SECRET
            read -p "SALESFORCE_REFRESH_TOKEN: " SF_REFRESH
            read -p "SALESFORCE_INSTANCE_URL: " SF_URL
            
            set_secret_if_provided "SALESFORCE_CLIENT_ID" "$SF_CLIENT_ID"
            set_secret_if_provided "SALESFORCE_CLIENT_SECRET" "$SF_CLIENT_SECRET"
            set_secret_if_provided "SALESFORCE_REFRESH_TOKEN" "$SF_REFRESH"
            set_secret_if_provided "SALESFORCE_INSTANCE_URL" "$SF_URL"
        fi
        
        echo ""
        read -p "Configure Beautiful? (y/n): " CONFIG_BEAUTIFUL
        if [ "$CONFIG_BEAUTIFUL" = "y" ]; then
            echo ""
            echo "📝 Setting Beautiful credentials:"
            read -p "BEAUTIFUL_API_KEY: " BEAUTIFUL_KEY
            set_secret_if_provided "BEAUTIFUL_API_KEY" "$BEAUTIFUL_KEY"
        fi
    fi
fi

echo ""
echo "=========================================="
echo "📋 Checking Configuration"
echo "=========================================="
echo ""

# Check fly.toml exists
if [ ! -f fly.toml ]; then
    echo "⚠️  No fly.toml found. Creating default configuration..."
    cat > fly.toml << EOF
app = "$APP_NAME"
primary_region = "lax"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  HOST = "0.0.0.0"
  LOG_LEVEL = "info"
  ENVIRONMENT = "production"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
EOF
    echo "✅ Created fly.toml"
else
    echo "✅ fly.toml exists"
fi

# Check Dockerfile exists
if [ ! -f Dockerfile ]; then
    echo "❌ Error: Dockerfile not found"
    echo "   Make sure you're in the synq-mcp-server directory"
    exit 1
fi
echo "✅ Dockerfile exists"

# Check requirements.txt
if [ ! -f requirements.txt ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi
echo "✅ requirements.txt exists"

# Check external connectors
if [ ! -d external_connectors ]; then
    echo "❌ Error: external_connectors directory not found"
    exit 1
fi
echo "✅ external_connectors directory exists"

echo ""
echo "=========================================="
echo "🚀 Deploying to Fly.io"
echo "=========================================="
echo ""

# Deploy
echo "🔨 Building and deploying..."
echo ""
flyctl deploy --app "$APP_NAME"

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""

# Get app info
APP_URL="https://$APP_NAME.fly.dev"

echo "🌐 Your MCP Server is live at:"
echo "   $APP_URL"
echo ""

echo "📡 Endpoints:"
echo "   Root:          curl $APP_URL/"
echo "   Health:        curl $APP_URL/health"
echo "   List Tools:    curl $APP_URL/mcp/tools"
echo "   Call Tool:     curl -X POST $APP_URL/mcp/call_tool \\"
echo "                    -H 'Content-Type: application/json' \\"
echo "                    -d '{\"tool\":\"zoom.connector.create_meeting\",\"arguments\":{\"topic\":\"Test\",\"start_time\":\"2025-12-01T15:00:00Z\",\"duration\":30}}'"
echo ""

echo "=========================================="
echo "🧪 Testing Deployment"
echo "=========================================="
echo ""

# Wait a moment for deployment to be ready
echo "⏳ Waiting for server to start..."
sleep 5

# Test health endpoint
echo ""
echo "Testing health endpoint..."
if curl -s --max-time 10 "$APP_URL/health" | grep -q "healthy"; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed or server still starting"
    echo "   Check logs: flyctl logs --app $APP_NAME"
fi

echo ""
echo "Testing tools endpoint..."
TOOL_COUNT=$(curl -s --max-time 10 "$APP_URL/mcp/tools" | grep -o '"count":[0-9]*' | grep -o '[0-9]*' || echo "0")
if [ "$TOOL_COUNT" -gt "0" ]; then
    echo "✅ Tools endpoint working! Found $TOOL_COUNT tools"
else
    echo "⚠️  Could not retrieve tools"
    echo "   Check logs: flyctl logs --app $APP_NAME"
fi

echo ""
echo "=========================================="
echo "📚 Next Steps"
echo "=========================================="
echo ""

echo "1️⃣  View logs:"
echo "   flyctl logs --app $APP_NAME"
echo ""

echo "2️⃣  Test with curl:"
echo "   curl $APP_URL/health"
echo "   curl $APP_URL/mcp/tools | jq '.'"
echo ""

echo "3️⃣  Use with dynamic_agents_email.py:"
echo "   export SYNQ_GLOBAL_MCP_ENDPOINT=$APP_URL"
echo "   export ANTHROPIC_API_KEY=your_key"
echo "   cd ../synqed-samples/api/examples/email"
echo "   python dynamic_agents_email.py"
echo ""

echo "4️⃣  Configure additional services (if needed):"
echo "   flyctl secrets set SALESFORCE_CLIENT_ID=xxx --app $APP_NAME"
echo "   flyctl secrets set BEAUTIFUL_API_KEY=xxx --app $APP_NAME"
echo ""

echo "5️⃣  Monitor your deployment:"
echo "   flyctl status --app $APP_NAME"
echo "   flyctl dashboard --app $APP_NAME"
echo ""

echo "=========================================="
echo "📖 Documentation"
echo "=========================================="
echo ""
echo "• Quick Start: QUICKSTART.md"
echo "• Integration Guide: INTEGRATION_GUIDE.md"
echo "• Test Connectors: python test_connectors.py"
echo "• README: README.md"
echo ""

echo "=========================================="
echo "🎉 Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Global MCP Server URL:"
echo "  $APP_URL"
echo ""
echo "Happy building! 🚀"
echo ""

