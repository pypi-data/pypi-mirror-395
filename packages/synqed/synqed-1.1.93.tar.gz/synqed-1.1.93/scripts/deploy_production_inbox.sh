#!/bin/bash
set -e

# Synqed Production Inbox Deployment Script
# Automates setup of production-grade inbox system

echo "========================================"
echo "Synqed Production Inbox Deployment"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Error: Do not run as root${NC}"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check prerequisites
echo "Step 1: Checking prerequisites..."
echo ""

if ! command_exists python3; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

if ! command_exists docker; then
    echo -e "${YELLOW}⚠ Docker not found - you'll need to install Redis manually${NC}"
    INSTALL_REDIS=false
else
    echo -e "${GREEN}✓ Docker found${NC}"
    INSTALL_REDIS=true
fi

if ! command_exists redis-cli; then
    echo -e "${YELLOW}⚠ redis-cli not found - installing...${NC}"
fi

echo ""

# Step 2: Install dependencies
echo "Step 2: Installing Python dependencies..."
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing synqed and dependencies..."
pip install --upgrade pip > /dev/null

# Install synqed from PyPI with all dependencies
pip install synqed cryptography>=41.0.0 redis>=5.0.0 httpx>=0.24.0 uvicorn>=0.20.0 fastapi > /dev/null

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 3: Setup Redis
echo "Step 3: Setting up Redis..."
echo ""

if [ "$INSTALL_REDIS" = true ]; then
    # Check if Redis container already exists
    if docker ps -a | grep -q synqed-redis; then
        echo "Redis container exists. Starting it..."
        docker start synqed-redis
    else
        echo "Starting Redis container..."
        docker run -d \
            --name synqed-redis \
            -p 6379:6379 \
            -v synqed-redis-data:/data \
            redis:7-alpine redis-server --appendonly yes
    fi
    
    # Wait for Redis to be ready
    echo "Waiting for Redis to be ready..."
    sleep 3
    
    if docker exec synqed-redis redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis is running${NC}"
    else
        echo -e "${RED}✗ Redis failed to start${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Please ensure Redis is running on localhost:6379${NC}"
    echo "Press Enter to continue..."
    read
fi

echo ""

# Step 4: Create application files
echo "Step 4: Creating application files..."
echo ""

# Create main.py
cat > main.py << 'EOF'
"""Production Synqed Inbox Application."""

import os
import logging
from fastapi import FastAPI
from synqed.agent_email.inbox import router
from synqed.agent_email.inbox.startup import create_lifespan

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create FastAPI app
app = FastAPI(
    title="Synqed Agent Email System",
    version="2.0.0",
    description="Production-grade A2A inbox with guaranteed delivery",
    lifespan=create_lifespan(redis_url=REDIS_URL),
)

# Include inbox router
app.include_router(router)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/")
async def root():
    return {
        "service": "Synqed Agent Email System",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
EOF

echo -e "${GREEN}✓ Created main.py${NC}"

# Update .env file (append if exists, create if not)
if [ -f .env ]; then
    echo "Updating existing .env file..."
    # Check if keys exist, only add if missing
    grep -q "REDIS_URL=" .env 2>/dev/null || echo "REDIS_URL=redis://localhost:6379" >> .env
    grep -q "LOG_LEVEL=" .env 2>/dev/null || echo "LOG_LEVEL=INFO" >> .env
    grep -q "SENDER_RATE_LIMIT=" .env 2>/dev/null || echo "SENDER_RATE_LIMIT=100" >> .env
    grep -q "IP_RATE_LIMIT=" .env 2>/dev/null || echo "IP_RATE_LIMIT=500" >> .env
    grep -q "MAX_RETRIES=" .env 2>/dev/null || echo "MAX_RETRIES=5" >> .env
    grep -q "INITIAL_BACKOFF_MS=" .env 2>/dev/null || echo "INITIAL_BACKOFF_MS=100" >> .env
    grep -q "MAX_BACKOFF_MS=" .env 2>/dev/null || echo "MAX_BACKOFF_MS=30000" >> .env
    grep -q "HTTP_TIMEOUT=" .env 2>/dev/null || echo "HTTP_TIMEOUT=30.0" >> .env
    echo -e "${GREEN}✓ Updated .env${NC}"
else
    echo "Creating .env file..."
    cat > .env << EOF
# Synqed Configuration
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO

# Rate Limiting
SENDER_RATE_LIMIT=100
IP_RATE_LIMIT=500

# Queue Configuration
MAX_RETRIES=5
INITIAL_BACKOFF_MS=100
MAX_BACKOFF_MS=30000

# HTTP Configuration
HTTP_TIMEOUT=30.0
EOF
    echo -e "${GREEN}✓ Created .env${NC}"
fi

# Create init_agents.py
cat > init_agents.py << 'EOF'
"""Initialize agents with keypairs."""

import asyncio
import json
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry
from synqed.agent_email.inbox import generate_keypair

async def main():
    print("Initializing demo agents...")
    
    registry = get_registry()
    keypairs = {}
    
    # Demo agents
    agents = [
        {
            "agent_id": "agent://demo/alice",
            "email_like": "alice@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0", "echo"],
        },
        {
            "agent_id": "agent://demo/bob",
            "email_like": "bob@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0", "echo"],
        },
    ]
    
    for agent in agents:
        private_key, public_key = generate_keypair()
        
        registry.register(AgentRegistryEntry(
            agent_id=agent["agent_id"],
            email_like=agent["email_like"],
            inbox_url=agent["inbox_url"],
            public_key=public_key,
            capabilities=agent["capabilities"],
        ))
        
        keypairs[agent["agent_id"]] = {
            "private_key": private_key,
            "public_key": public_key,
        }
        
        print(f"✓ Registered: {agent['agent_id']}")
    
    # Save keypairs
    with open("keypairs.json", "w") as f:
        json.dump(keypairs, f, indent=2)
    
    print(f"\n✓ Registered {len(agents)} agents")
    print("⚠️  Keypairs saved to keypairs.json - store securely!")

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo -e "${GREEN}✓ Created init_agents.py${NC}"

echo ""

# Step 5: Initialize agents
echo "Step 5: Initializing demo agents..."
echo ""

python3 init_agents.py

echo ""

# Step 6: Create systemd service (optional)
echo "Step 6: Creating systemd service (optional)..."
echo ""

read -p "Install systemd service? (requires sudo) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    CURRENT_DIR=$(pwd)
    VENV_PATH="$CURRENT_DIR/venv"
    
    sudo tee /etc/systemd/system/synqed.service > /dev/null << EOF
[Unit]
Description=Synqed Agent Email Service
After=network.target

[Service]
Type=notify
User=$USER
Group=$USER
WorkingDirectory=$CURRENT_DIR
Environment="REDIS_URL=redis://localhost:6379"
Environment="LOG_LEVEL=INFO"
ExecStart=$VENV_PATH/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable synqed
    
    echo -e "${GREEN}✓ Systemd service installed${NC}"
    echo "  Start with: sudo systemctl start synqed"
    echo "  Status: sudo systemctl status synqed"
    echo "  Logs: sudo journalctl -u synqed -f"
fi

echo ""

# Step 7: Done!
echo "========================================"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the application:"
echo "   python3 main.py"
echo "   OR"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "2. View API docs:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. Test health endpoint:"
echo "   curl http://localhost:8000/health"
echo ""
echo "4. Send a test message (see examples/production_inbox_demo.py)"
echo ""
echo "Important files:"
echo "  - main.py: Application entry point"
echo "  - .env: Configuration"
echo "  - keypairs.json: Agent keypairs (KEEP SECURE!)"
echo "  - init_agents.py: Agent initialization"
echo ""
echo "Documentation:"
echo "  - DEPLOYMENT_GUIDE.md: Full deployment guide"
echo "  - src/synqed/agent_email/inbox/README.md: API reference"
echo ""
echo "For production deployment, see DEPLOYMENT_GUIDE.md"
echo ""

# Optionally start the server
read -p "Start the server now? [Y/n]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "Checking port 8000..."
    # Kill any process using port 8000
    lsof -ti :8000 | xargs kill -9 2>/dev/null || true
    echo "Starting server on http://localhost:8000..."
    echo "Press Ctrl+C to stop"
    echo ""
    sleep 2
    python3 main.py
fi

