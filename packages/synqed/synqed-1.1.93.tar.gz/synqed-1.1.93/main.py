"""
Synqed Production Infrastructure - Unified Email + MCP Server
Hosts both the agent email system and global MCP server on same Fly.io app
"""
import os
import logging
import sys

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

from synqed.agent_email.inbox import router
from synqed.agent_email.inbox.startup import create_lifespan
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry

# Import MCP server components

HAS_MCP = False
try:
    from synqed import MessageRouter
    from synqed_mcp.a2a.client import A2AClient
    from synqed_mcp.registry import get_tool_config, get_tool_registry, list_tools
    HAS_MCP = True
    logger.info("✅ MCP modules imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import MCP modules: {e}")
    logger.error(f"   Python path: {sys.path}")
    logger.error(f"   This will disable MCP endpoints")
    HAS_MCP = False

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
PORT = int(os.getenv("PORT", "8000"))
MCP_ENABLED = os.getenv("ENABLE_MCP", "true").lower() == "true"

# Log startup configuration
logger.info("="*60)
logger.info("SYNQED CLOUD INFRASTRUCTURE STARTING")
logger.info("="*60)
logger.info(f"Redis URL: {REDIS_URL}")
logger.info(f"Port: {PORT}")
logger.info(f"MCP Enabled (env): {MCP_ENABLED}")
logger.info(f"MCP Available (imports): {HAS_MCP}")
logger.info("="*60)

# Create FastAPI app with lifespan management
app = FastAPI(
    title="Synqed Cloud Infrastructure",
    version="3.0.0",
    description="Unified platform: A2A email inbox + Global MCP server for agent-to-agent communication",
    lifespan=create_lifespan(redis_url=REDIS_URL),
)

# Add CORS for cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.fly.dev",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include inbox router (email system)
app.include_router(router)

# Global MCP server state (if enabled)
mcp_router = None
mcp_a2a_client = None
mcp_agent_registry: Dict[str, Dict[str, Any]] = {}

if MCP_ENABLED and HAS_MCP:
    # Initialize MCP infrastructure
    logger.info("🔧 Initializing MCP infrastructure...")
    mcp_router = MessageRouter()
    mcp_a2a_client = A2AClient(mcp_router, workspace_id="cloud")
    logger.info("✅ MCP infrastructure initialized")
elif MCP_ENABLED and not HAS_MCP:
    logger.warning("⚠️  MCP enabled but modules not available - check imports above")
else:
    logger.info("ℹ️  MCP disabled via ENABLE_MCP=false")

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
    endpoints = {
        "health": "/health",
        "docs": "/docs",
        "inbox": "/v1/a2a/inbox",
        "register": "POST /v1/a2a/register",
        "list_agents": "GET /v1/a2a/agents",
        "lookup_agent": "GET /v1/a2a/agents/{email}",
    }
    
    if MCP_ENABLED:
        endpoints.update({
            "mcp_tools": "GET /mcp/tools",
            "mcp_agents": "GET /mcp/agents",
            "mcp_call_tool": "POST /mcp/call_tool",
            "mcp_register": "POST /mcp/register_agent",
        })
    
    return {
        "service": "Synqed Cloud Infrastructure",
        "version": "3.0.0",
        "status": "operational",
        "components": {
            "email_inbox": True,
            "mcp_server": MCP_ENABLED and HAS_MCP,
        },
        "endpoints": endpoints,
        "features": {
            "cryptographic_identity": "Ed25519 signatures",
            "guaranteed_delivery": "Redis Streams queue",
            "rate_limiting": "100/min per sender, 500/min per IP",
            "distributed_tracing": "trace_id propagation",
            "retry_policy": "5 retries with exponential backoff",
            "dead_letter_queue": "Failed messages after max retries",
            "mcp_global_server": "Universal agent-to-agent MCP bridge" if MCP_ENABLED else "disabled",
        }
    }

@app.get("/health")
async def health():
    """Health check for monitoring and load balancers."""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "redis": REDIS_URL,
        "email_inbox": True,
        "mcp_server": MCP_ENABLED and HAS_MCP,
    }

# ============================================================
# MCP SERVER ROUTES (if enabled)
# ============================================================

if MCP_ENABLED and HAS_MCP:
    from synqed import AgentId
    
    @app.get("/mcp/agents")
    async def list_mcp_registered_agents():
        """List all agents registered with MCP server."""
        return {
            "agents": [
                {
                    "agent_uri": agent_uri,
                    "org": info["org"],
                    "name": info["name"],
                    "tools": info.get("tools", []),
                    "registered_at": info.get("registered_at", "unknown")
                }
                for agent_uri, info in mcp_agent_registry.items()
            ]
        }
    
    @app.post("/mcp/register_agent")
    async def register_mcp_agent(payload: Dict[str, Any]):
        """
        Register an agent with the global MCP server.
        
        Request body:
            {
                "agent_uri": "agent://tools/salesforce",
                "org": "tools",
                "name": "salesforce",
                "tools": ["query_leads", "update_lead"]
            }
        """
        agent_uri = payload.get("agent_uri")
        if not agent_uri:
            raise HTTPException(status_code=400, detail="agent_uri required")
        
        org = payload.get("org", "unknown")
        name = payload.get("name", "unknown")
        tools = payload.get("tools", [])
        
        # Store in registry
        from datetime import datetime
        mcp_agent_registry[agent_uri] = {
            "org": org,
            "name": name,
            "tools": tools,
            "registered_at": datetime.utcnow().isoformat() + "Z"
        }
        
        return {
            "status": "ok",
            "agent_uri": agent_uri,
            "tools_count": len(tools)
        }
    
    @app.get("/mcp/tools")
    async def list_mcp_tools():
        """List all available MCP tools."""
        tool_registry = get_tool_registry()
        return {
            "tools": [
                {
                    "name": tool_name,
                    "agent": config["agent"],
                    "task_type": config["task_type"],
                    "description": config.get("description", "")
                }
                for tool_name, config in tool_registry.items()
            ]
        }
    
    @app.post("/mcp/call_tool")
    async def call_mcp_tool(request: Dict[str, Any]):
        """
        Call an MCP tool.
        
        Request body:
            {
                "tool": "tool_name",
                "arguments": {...},
                "caller": "agent_name" (optional)
            }
        """
        tool_name = request.get("tool")
        arguments = request.get("arguments", {})
        caller = request.get("caller", "external")
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="tool name required")
        
        try:
            # Get tool configuration
            tool_config = get_tool_config(tool_name)
            agent_name = tool_config["agent"]
            task_type = tool_config["task_type"]
            
            # Create agent id
            agent_id = AgentId(org="tools", name=agent_name)
            agent_uri = agent_id.to_uri()
            
            # Check if agent is registered
            if agent_uri not in mcp_agent_registry:
                # Log warning but don't fail - agent might be local
                pass
            
            # Add metadata
            payload = dict(arguments)
            payload["_mcp_origin"] = {
                "caller": caller,
                "tool": tool_name,
                "mode": "cloud"
            }
            
            # Call agent via a2a bridge
            result = await mcp_a2a_client.send_task_and_wait(
                agent=agent_id,
                task_type=task_type,
                payload=payload,
                timeout=30.0
            )
            
            return result
        
        except KeyError:
            raise HTTPException(
                status_code=404,
                detail=f"tool '{tool_name}' not found"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"tool execution failed: {str(e)}"
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
