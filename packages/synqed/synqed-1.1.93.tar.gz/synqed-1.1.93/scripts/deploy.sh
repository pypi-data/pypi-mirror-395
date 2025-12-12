#!/bin/bash
set -e

#######################################################################
# SYNQED PRODUCTION INBOX - COMPLETE DEPLOYMENT SCRIPT
# 
# Deploys Synqed inbox to:
# - Local development
# - Fly.io (production cloud)
# - Railway (production cloud)
# - Docker (self-hosted)
# - Custom server (VPS/dedicated)
#######################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Version
VERSION="2.0.0"

clear
echo ""
echo "========================================================================"
echo -e "${CYAN}              SYNQED PRODUCTION INBOX DEPLOYMENT v${VERSION}${NC}"
echo "========================================================================"
echo ""
echo "Deploy production-grade agent email infrastructure with:"
echo "  • Ed25519 cryptographic signatures"
echo "  • Redis queue with guaranteed delivery"
echo "  • Rate limiting & abuse protection"
echo "  • Distributed tracing"
echo "  • Dead letter queue"
echo ""
echo "========================================================================"
echo ""

#######################################################################
# SELECT DEPLOYMENT TARGET
#######################################################################

echo -e "${BLUE}Select deployment target:${NC}"
echo ""
echo "  1) Local development (localhost:8000)"
echo "  2) Fly.io (production cloud - free tier available)"
echo "  3) Railway (production cloud - auto-deploy)"
echo "  4) Docker (containerized - portable)"
echo "  5) Custom VPS/server (manual setup)"
echo ""
read -p "Enter choice [1-5]: " DEPLOY_TARGET

case $DEPLOY_TARGET in
    1) DEPLOY_TYPE="local" ;;
    2) DEPLOY_TYPE="flyio" ;;
    3) DEPLOY_TYPE="railway" ;;
    4) DEPLOY_TYPE="docker" ;;
    5) DEPLOY_TYPE="custom" ;;
    *) echo -e "${RED}Invalid choice${NC}"; exit 1 ;;
esac

echo ""
echo -e "${GREEN}✓ Selected: ${DEPLOY_TYPE}${NC}"
echo ""

#######################################################################
# STEP 1: Check Prerequisites
#######################################################################

echo -e "${BLUE}STEP 1: Checking prerequisites...${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
else
    PLATFORM="unknown"
fi
echo -e "${GREEN}✓ Platform: ${PLATFORM}${NC}"

# Check deployment-specific tools
if [ "$DEPLOY_TYPE" == "flyio" ]; then
    if ! command -v flyctl &> /dev/null; then
        echo -e "${YELLOW}⚠ flyctl not found. Installing...${NC}"
        curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="$HOME/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    fi
    echo -e "${GREEN}✓ flyctl installed${NC}"
elif [ "$DEPLOY_TYPE" == "docker" ]; then
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker not found. Please install Docker Desktop${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker installed${NC}"
fi

echo ""

#######################################################################
# STEP 2: Configuration
#######################################################################

echo -e "${BLUE}STEP 2: Configuration...${NC}"
echo ""

# Get app name
read -p "App name (default: synqed-inbox): " APP_NAME
APP_NAME=${APP_NAME:-synqed-inbox}
echo -e "${GREEN}✓ App name: ${APP_NAME}${NC}"

# Get domain (for production)
if [ "$DEPLOY_TYPE" == "flyio" ] || [ "$DEPLOY_TYPE" == "railway" ] || [ "$DEPLOY_TYPE" == "custom" ]; then
    read -p "Custom domain (optional, press Enter to skip): " CUSTOM_DOMAIN
    if [ -n "$CUSTOM_DOMAIN" ]; then
        echo -e "${GREEN}✓ Domain: ${CUSTOM_DOMAIN}${NC}"
    fi
fi

# Redis configuration
if [ "$DEPLOY_TYPE" == "local" ]; then
    REDIS_URL="redis://localhost:6379"
elif [ "$DEPLOY_TYPE" == "flyio" ]; then
    REDIS_URL="redis://synqed-redis.internal:6379"
elif [ "$DEPLOY_TYPE" == "railway" ]; then
    REDIS_URL="\${{REDIS_URL}}"
elif [ "$DEPLOY_TYPE" == "docker" ]; then
    REDIS_URL="redis://redis:6379"
else
    read -p "Redis URL (e.g., redis://host:6379): " REDIS_URL
fi

echo ""

#######################################################################
# STEP 3: Setup Project
#######################################################################

echo -e "${BLUE}STEP 3: Setting up project files...${NC}"
echo ""

# Ensure we're in project root
cd "$(dirname "$0")/.."

# Create main.py
cat > main.py << 'EOF'
"""
Synqed Production Inbox - Complete Agent Email Infrastructure
"""
import os
from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

from synqed.agent_email.inbox import router
from synqed.agent_email.inbox.startup import create_lifespan
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
PORT = int(os.getenv("PORT", "8000"))

# Create FastAPI app with lifespan management
app = FastAPI(
    title="Synqed Agent Email System",
    version="2.0.0",
    description="Production-grade A2A inbox with cryptographic identity, guaranteed delivery, and distributed tracing",
    lifespan=create_lifespan(redis_url=REDIS_URL),
)

# Include inbox router
app.include_router(router)

# Registration models
class AgentRegistrationRequest(BaseModel):
    agent_id: str
    email_like: str
    inbox_url: HttpUrl
    public_key: str
    capabilities: List[str] = ["a2a/1.0"]
    metadata: Dict[str, Any] = {}

class AgentRegistrationResponse(BaseModel):
    status: str
    agent_id: str
    email_like: str
    message: str

# Registration endpoints
@app.post("/v1/a2a/register", response_model=AgentRegistrationResponse, tags=["registration"])
async def register_agent(request: AgentRegistrationRequest):
    """Register a new agent - anyone can register!"""
    registry = get_registry()
    
    try:
        registry.get_by_uri(request.agent_id)
        raise HTTPException(status_code=409, detail="Agent already registered")
    except KeyError:
        pass
    
    entry = AgentRegistryEntry(
        agent_id=request.agent_id,
        email_like=request.email_like,
        inbox_url=request.inbox_url,
        public_key=request.public_key,
        capabilities=request.capabilities,
        metadata=request.metadata,
    )
    registry.register(entry)
    
    return AgentRegistrationResponse(
        status="registered",
        agent_id=request.agent_id,
        email_like=request.email_like,
        message=f"Agent {request.email_like} registered successfully!"
    )

@app.get("/v1/a2a/agents", tags=["registration"])
async def list_agents():
    """List all registered agents."""
    registry = get_registry()
    agents = registry.list_all()
    return {
        "count": len(agents),
        "agents": [{"agent_id": a.agent_id, "email_like": a.email_like, "inbox_url": str(a.inbox_url)} for a in agents]
    }

@app.get("/v1/a2a/agents/{email_like}", tags=["registration"])
async def lookup_agent(email_like: str):
    """Lookup agent by email address."""
    registry = get_registry()
    try:
        agent = registry.get_by_email(email_like)
        return {"agent_id": agent.agent_id, "email_like": agent.email_like, "inbox_url": str(agent.inbox_url)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/")
async def root():
    """Service information."""
    return {
        "service": "Synqed Agent Email System",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "inbox": "/v1/a2a/inbox",
            "register": "POST /v1/a2a/register",
        "list_agents": "GET /v1/a2a/agents",
        "lookup_agent": "GET /v1/a2a/agents/{email}",
        },
        "features": {
            "cryptographic_identity": "Ed25519 signatures",
            "guaranteed_delivery": "Redis Streams queue",
            "rate_limiting": "100/min per sender, 500/min per IP",
            "distributed_tracing": "trace_id propagation",
            "retry_policy": "5 retries with exponential backoff",
            "dead_letter_queue": "Failed messages after max retries",
        }
    }

@app.get("/health")
async def health():
    """Health check for monitoring and load balancers."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "redis": REDIS_URL,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
EOF

echo -e "${GREEN}✓ Created main.py${NC}"

# Create requirements.txt
cat > requirements.txt << 'EOF'
synqed>=1.1.4
cryptography>=41.0.0
redis>=5.0.0
httpx>=0.24.0
uvicorn>=0.20.0
fastapi>=0.100.0
EOF

echo -e "${GREEN}✓ Created requirements.txt${NC}"

# Create or update .env (preserve existing content)
if [ -f .env ]; then
    echo "Updating .env (preserving existing content)..."
    
    # Only add missing keys
    grep -q "^REDIS_URL=" .env 2>/dev/null || echo "REDIS_URL=${REDIS_URL}" >> .env
    grep -q "^PORT=" .env 2>/dev/null || echo "PORT=8000" >> .env
    grep -q "^LOG_LEVEL=" .env 2>/dev/null || echo "LOG_LEVEL=INFO" >> .env
    grep -q "^OPENAI_API_KEY=" .env 2>/dev/null || echo "OPENAI_API_KEY=" >> .env
    grep -q "^SENDER_RATE_LIMIT=" .env 2>/dev/null || echo "SENDER_RATE_LIMIT=100" >> .env
    grep -q "^IP_RATE_LIMIT=" .env 2>/dev/null || echo "IP_RATE_LIMIT=500" >> .env
    grep -q "^MAX_RETRIES=" .env 2>/dev/null || echo "MAX_RETRIES=5" >> .env
    grep -q "^INITIAL_BACKOFF_MS=" .env 2>/dev/null || echo "INITIAL_BACKOFF_MS=100" >> .env
    grep -q "^MAX_BACKOFF_MS=" .env 2>/dev/null || echo "MAX_BACKOFF_MS=30000" >> .env
    grep -q "^HTTP_TIMEOUT=" .env 2>/dev/null || echo "HTTP_TIMEOUT=30.0" >> .env
    
    echo -e "${GREEN}✓ Updated .env${NC}"
else
    # Create new .env file
    cat > .env << 'EOF'
# Synqed Production Configuration
REDIS_URL=redis://localhost:6379
PORT=8000
LOG_LEVEL=INFO

# OpenAI API Key (for AI agent demos)
# Get yours at: https://platform.openai.com/api-keys
OPENAI_API_KEY=

# Rate Limiting
SENDER_RATE_LIMIT=100
IP_RATE_LIMIT=500

# Queue Configuration
MAX_RETRIES=5
INITIAL_BACKOFF_MS=100
MAX_BACKOFF_MS=30000
HTTP_TIMEOUT=30.0
EOF
    
    echo -e "${GREEN}✓ Created .env${NC}"
fi

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY .env .

# Create non-root user
RUN useradd -m -u 1000 synqed && \
    chown -R synqed:synqed /app

USER synqed

# Health check - use PORT env var
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, httpx; httpx.get(f'http://localhost:{os.getenv(\"PORT\", \"8000\")}/health')"

EXPOSE 8080

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
EOF

echo -e "${GREEN}✓ Created Dockerfile${NC}"

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  synqed:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - PORT=8000
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  redis-data:
EOF

echo -e "${GREEN}✓ Created docker-compose.yml${NC}"

# Create fly.toml (for Fly.io)
if [ "$DEPLOY_TYPE" == "flyio" ]; then
    cat > fly.toml << EOF
app = "${APP_NAME}"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  REDIS_URL = "redis://synqed-redis.internal:6379"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

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
    echo -e "${GREEN}✓ Created fly.toml${NC}"
fi

# Create railway.json (for Railway)
if [ "$DEPLOY_TYPE" == "railway" ]; then
    cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
    echo -e "${GREEN}✓ Created railway.json${NC}"
fi

echo ""

#######################################################################
# STEP 4: Install Dependencies (Local only)
#######################################################################

if [ "$DEPLOY_TYPE" == "local" ]; then
    echo -e "${BLUE}STEP 4: Installing dependencies...${NC}"
    echo ""
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Created virtual environment${NC}"
    fi
    
    # Activate and install
    source venv/bin/activate
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
fi

#######################################################################
# STEP 5: Setup Redis
#######################################################################

if [ "$DEPLOY_TYPE" == "local" ]; then
    echo -e "${BLUE}STEP 5: Setting up Redis...${NC}"
    echo ""
    
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✓ Redis already running${NC}"
    else
        if [[ "$PLATFORM" == "macos" ]]; then
            if ! command -v brew &> /dev/null; then
                echo "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install redis 2>/dev/null || true
            brew services start redis
        elif [[ "$PLATFORM" == "linux" ]]; then
            sudo apt update
            sudo apt install -y redis-server
            sudo systemctl start redis
        fi
        
        sleep 2
        if redis-cli ping &> /dev/null; then
            echo -e "${GREEN}✓ Redis started${NC}"
        else
            echo -e "${RED}✗ Redis failed to start${NC}"
            exit 1
        fi
    fi
    echo ""
fi

#######################################################################
# STEP 6: Deploy Based on Target
#######################################################################

echo -e "${BLUE}STEP 6: Deploying to ${DEPLOY_TYPE}...${NC}"
echo ""

case $DEPLOY_TYPE in
    local)
        # Kill any existing process on port 8000
        lsof -ti :8000 | xargs kill -9 2>/dev/null || true
        echo -e "${GREEN}✓ Port 8000 cleared${NC}"
        ;;
        
    flyio)
        # Login to Fly.io
        echo "Logging in to Fly.io..."
        flyctl auth login
        
        # Create app if doesn't exist
        if ! flyctl apps list | grep -q "$APP_NAME"; then
            flyctl apps create "$APP_NAME" --org personal || true
        fi
        
        # Create Redis
        if ! flyctl redis list | grep -q "synqed-redis"; then
            echo "Creating Redis instance..."
            flyctl redis create --name synqed-redis --region sjc --no-replicas || true
        fi
        
        # Deploy
        echo "Deploying to Fly.io..."
        flyctl deploy --app "$APP_NAME"
        
        # Get URL
        FLY_URL=$(flyctl info --app "$APP_NAME" | grep Hostname | awk '{print $3}')
        echo ""
        echo -e "${GREEN}✓ Deployed to https://${FLY_URL}${NC}"
        
        # Setup custom domain if provided
        if [ -n "$CUSTOM_DOMAIN" ]; then
            echo ""
            echo "Setting up custom domain..."
            flyctl certs add "$CUSTOM_DOMAIN" --app "$APP_NAME"
        fi
        ;;
        
    railway)
        echo "Railway deployment requires GitHub integration."
        echo ""
        echo "Steps:"
        echo "1. Push your code to GitHub"
        echo "2. Go to https://railway.app"
        echo "3. Click 'New Project' → 'Deploy from GitHub'"
        echo "4. Select your repository"
        echo "5. Add Redis plugin"
        echo ""
        echo "Files created for Railway:"
        echo "  ✓ Dockerfile"
        echo "  ✓ railway.json"
        echo "  ✓ requirements.txt"
        echo ""
        read -p "Press Enter after pushing to GitHub..."
        ;;
        
    docker)
        echo "Building Docker images..."
        docker-compose build
        
        echo "Starting services..."
        docker-compose up -d
        
        # Wait for health check
        echo "Waiting for services to be healthy..."
        sleep 10
        
        if docker-compose ps | grep -q "healthy"; then
            echo -e "${GREEN}✓ Services are healthy${NC}"
        else
            echo -e "${YELLOW}⚠ Services may still be starting...${NC}"
        fi
        ;;
        
    custom)
        echo "Custom VPS deployment steps:"
        echo ""
        echo "1. Copy these files to your server:"
        echo "   - main.py"
        echo "   - requirements.txt"
        echo "   - .env"
        echo ""
        echo "2. On your server, run:"
        echo "   sudo apt update && sudo apt install -y python3 python3-pip redis-server"
        echo "   sudo systemctl start redis"
        echo "   pip3 install -r requirements.txt"
        echo ""
        echo "3. Create systemd service:"
        echo "   sudo nano /etc/systemd/system/synqed.service"
        echo ""
        echo "4. Add this content:"
        cat << 'SYSTEMD'
[Unit]
Description=Synqed Agent Email Service
After=network.target redis.service

[Service]
Type=notify
User=synqed
WorkingDirectory=/opt/synqed
EnvironmentFile=/opt/synqed/.env
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
SYSTEMD
        echo ""
        echo "5. Enable and start:"
        echo "   sudo systemctl daemon-reload"
        echo "   sudo systemctl enable synqed"
        echo "   sudo systemctl start synqed"
        ;;
esac

echo ""

#######################################################################
# STEP 7: Initialize Demo Agents (Optional)
#######################################################################

if [ "$DEPLOY_TYPE" == "local" ]; then
    echo -e "${BLUE}STEP 7: Initialize demo agents? [y/N]${NC}"
    read -p "> " INIT_AGENTS
    
    if [[ $INIT_AGENTS =~ ^[Yy]$ ]]; then
        cat > init_agents.py << 'EOF'
import asyncio
import json
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry
from synqed.agent_email.inbox import generate_keypair

async def main():
    registry = get_registry()
    keypairs = {}
    
    agents = [
        {
            "agent_id": "agent://demo/alice",
            "email_like": "alice@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0"],
        },
        {
            "agent_id": "agent://demo/bob",
            "email_like": "bob@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0"],
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
        keypairs[agent["agent_id"]] = {"private_key": private_key, "public_key": public_key}
        print(f"✓ {agent['agent_id']}")
    
    with open("keypairs.json", "w") as f:
        json.dump(keypairs, f, indent=2)
    print(f"\n✓ Saved to keypairs.json")

asyncio.run(main())
EOF
        python3 init_agents.py
        echo ""
    fi
fi

#######################################################################
# DEPLOYMENT COMPLETE
#######################################################################

echo ""
echo "========================================================================"
echo -e "${GREEN}                    ✓ DEPLOYMENT COMPLETE!${NC}"
echo "========================================================================"
echo ""

# Show deployment-specific info
case $DEPLOY_TYPE in
    local)
        echo -e "${YELLOW}🚀 Local Development:${NC}"
        echo ""
        echo "  Start server:"
        echo -e "    ${CYAN}python main.py${NC}"
        echo ""
        echo "  Access:"
        echo "    • Web: http://localhost:8000"
        echo "    • Docs: http://localhost:8000/docs"
        echo "    • Health: curl http://localhost:8000/health"
        ;;
        
    flyio)
        echo -e "${YELLOW}🚀 Fly.io Production:${NC}"
        echo ""
        echo "  URL: https://${FLY_URL}"
        echo "  Docs: https://${FLY_URL}/docs"
        echo ""
        echo "  Manage:"
        echo "    • Logs: flyctl logs --app $APP_NAME"
        echo "    • SSH: flyctl ssh console --app $APP_NAME"
        echo "    • Scale: flyctl scale count 2 --app $APP_NAME"
        
        if [ -n "$CUSTOM_DOMAIN" ]; then
            echo ""
            echo "  Custom domain setup:"
            echo "    Add DNS record:"
            echo "      Type: CNAME"
            echo "      Name: $CUSTOM_DOMAIN"
            echo "      Value: ${FLY_URL}"
        fi
        ;;
        
    docker)
        echo -e "${YELLOW}🚀 Docker Deployment:${NC}"
        echo ""
        echo "  Manage:"
        echo "    • Logs: docker-compose logs -f"
        echo "    • Stop: docker-compose down"
        echo "    • Restart: docker-compose restart"
        echo ""
        echo "  Access:"
        echo "    • Web: http://localhost:8000"
        echo "    • Docs: http://localhost:8000/docs"
        ;;
esac

echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "  • Complete guide: DEPLOY.md"
echo "  • API reference: src/synqed/agent_email/inbox/README.md"
echo ""
echo -e "${YELLOW}🔐 Security (Production):${NC}"
echo "  • Store keypairs in secrets manager"
echo "  • Enable Redis AUTH"
echo "  • Use HTTPS only"
echo "  • Configure rate limits"
echo "  • Set up monitoring"
echo ""
echo "========================================================================"
echo ""

# Start local server if requested
if [ "$DEPLOY_TYPE" == "local" ]; then
    read -p "Start server now? [Y/n]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        echo -e "${GREEN}Starting server...${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        sleep 1
        python3 main.py
    fi
fi
