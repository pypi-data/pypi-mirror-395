#!/bin/bash

#
# deploy_mcp_fly.sh
#
# Deploys the Synqed Global MCP Server to Fly.io.
# This server runs on the SAME Fly.io app as the email-based agent registry.
#
# Usage:
#   ./scripts/deploy_mcp_fly.sh
#
# Prerequisites:
#   - flyctl installed and authenticated (flyctl auth login)
#   - Fly.io app "synqed" already created
#

set -e

echo "=========================================="
echo "Synqed Global MCP Server - Fly.io Deploy"
echo "=========================================="
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ Error: flyctl is not installed"
    echo "   Install it from: https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "❌ Error: Not logged in to Fly.io"
    echo "   Run: flyctl auth login"
    exit 1
fi

echo "✅ flyctl is installed and authenticated"
echo ""

# Check if app exists
APP_NAME="synqed"
if ! flyctl apps list | grep -q "$APP_NAME"; then
    echo "⚠️  Warning: App '$APP_NAME' not found"
    echo ""
    echo "Creating app '$APP_NAME'..."
    flyctl apps create "$APP_NAME"
    echo ""
fi

echo "📦 Deploying to app: $APP_NAME"
echo ""
echo "🔧 Deploying unified server (Email Registry + MCP Server)"
echo ""

# Deploy using the root fly.toml (includes both email and MCP)
cd "$(dirname "$0")/.."
flyctl deploy

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "🌐 Base URL: https://$APP_NAME.fly.dev"
echo ""
echo "📧 Email Registry Endpoints:"
echo "  Health:        curl https://$APP_NAME.fly.dev/health"
echo "  List Agents:   curl https://$APP_NAME.fly.dev/v1/a2a/agents"
echo "  Inbox:         curl https://$APP_NAME.fly.dev/v1/a2a/inbox"
echo ""
echo "🔧 MCP Server Endpoints:"
echo "  Tools:         curl https://$APP_NAME.fly.dev/mcp/tools"
echo "  Agents:        curl https://$APP_NAME.fly.dev/mcp/agents"
echo "  Call Tool:     curl -X POST https://$APP_NAME.fly.dev/mcp/call_tool \\"
echo "                   -H 'Content-Type: application/json' \\"
echo "                   -d '{\"tool\":\"salesforce.query_leads\",\"arguments\":{\"query\":\"test\"}}'"
echo ""
echo "=========================================="
echo ""
echo "🚀 To use the cloud MCP server with your agents:"
echo ""
echo "  export SYNQ_MCP_MODE=cloud"
echo "  export SYNQ_MCP_ENDPOINT=https://$APP_NAME.fly.dev/mcp"
echo "  python your_agent.py"
echo ""
echo "📝 Note: Both email registry and MCP server run on the same app!"
echo ""
echo "=========================================="

