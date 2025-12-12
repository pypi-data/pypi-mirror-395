#!/bin/bash
# deploy agent email layer to fly.io
# run: bash deploy_to_cloud.sh

set -e  # exit on error

echo "🚀 deploying agent email layer to fly.io"
echo "========================================"

# check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl not found. installing..."
    curl -L https://fly.io/install.sh | sh
    echo "✅ flyctl installed"
    echo ""
    echo "⚠️  please add flyctl to your PATH and run this script again:"
    echo "   export FLYCTL_INSTALL=\"$HOME/.fly\""
    echo "   export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\""
    exit 1
fi

echo "✅ flyctl found"
echo ""

# login to fly.io
echo "🔐 logging in to fly.io..."
flyctl auth login

# create app name (you can customize this)
APP_NAME="agent-email-layer"
read -p "enter app name (default: agent-email-layer): " USER_APP_NAME
APP_NAME=${USER_APP_NAME:-$APP_NAME}

echo ""
echo "📦 creating fly.io app: $APP_NAME"

# check if app already exists
if flyctl apps list | grep -q "$APP_NAME"; then
    echo "⚠️  app $APP_NAME already exists"
    read -p "continue with existing app? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo "❌ deployment cancelled"
        exit 1
    fi
else
    # create app
    flyctl apps create "$APP_NAME" || true
fi

echo ""
echo "🐘 setting up postgres database..."

# check if postgres already exists
if flyctl postgres list | grep -q "$APP_NAME-db"; then
    echo "✅ postgres database already exists"
else
    # create postgres database
    flyctl postgres create --name "$APP_NAME-db" --region sjc --vm-size shared-cpu-1x --volume-size 1
fi

# attach postgres to app
echo "🔗 attaching postgres to app..."
flyctl postgres attach "$APP_NAME-db" --app "$APP_NAME" || echo "already attached"

echo ""
echo "🔨 building and deploying..."

# ensure we're in the project root
cd "$(dirname "$0")/.."

# create fly.toml if it doesn't exist
if [ ! -f fly.toml ]; then
    cat > fly.toml << EOF
app = "$APP_NAME"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

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
    echo "✅ created fly.toml"
fi

# deploy
flyctl deploy

echo ""
echo "✅ deployment complete!"
echo ""
echo "📍 your agent email layer is now live at:"
flyctl info --app "$APP_NAME" | grep Hostname
echo ""
echo "🔍 view logs:"
echo "   flyctl logs --app $APP_NAME"
echo ""
echo "🌐 open in browser:"
echo "   flyctl open --app $APP_NAME"
echo ""
echo "📚 api documentation:"
echo "   https://$APP_NAME.fly.dev/docs"
echo ""
echo "🧪 test it:"
echo "   curl https://$APP_NAME.fly.dev/health"
echo ""

