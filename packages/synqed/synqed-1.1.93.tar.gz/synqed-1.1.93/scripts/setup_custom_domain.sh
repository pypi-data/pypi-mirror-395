#!/bin/bash
# setup custom domain for agent email layer

set -e

echo "🌐 custom domain setup"
echo "===================="
echo ""

# get app name
read -p "enter your fly.io app name (default: agent-email-layer): " APP_NAME
APP_NAME=${APP_NAME:-agent-email-layer}

# get custom domain
echo ""
echo "what domain do you want to use?"
echo "examples: agentmail.io, agents.yourdomain.com"
read -p "enter your domain: " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ domain cannot be empty"
    exit 1
fi

echo ""
echo "📋 here's what you need to do:"
echo ""
echo "1️⃣  add ssl certificate to fly.io:"
flyctl certs add "$DOMAIN" --app "$APP_NAME"

echo ""
echo "2️⃣  update your dns records at your domain registrar:"
echo ""
echo "    if using root domain ($DOMAIN):"
echo "    --------------------------------"
echo "    type: A"
echo "    name: @"
echo "    value: (copy the IP address shown above)"
echo ""
echo "    if using subdomain (e.g., api.$DOMAIN):"
echo "    ----------------------------------------"
echo "    type: CNAME"
echo "    name: api (or whatever subdomain you chose)"
echo "    value: $APP_NAME.fly.dev"
echo ""
echo "3️⃣  wait 5-10 minutes for dns to propagate"
echo ""
echo "4️⃣  verify it works:"
echo "    curl https://$DOMAIN/health"
echo ""
echo "✅ done! your agent email layer will be available at:"
echo "   https://$DOMAIN"
echo ""

