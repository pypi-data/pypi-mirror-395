"""
global mcp server for cloud deployment.

single server instance that:
- exposes mcp tools via http
- bridges mcp tool calls to a2a tasks
- supports multiple concurrent agents and clients
- uses synqed's existing a2a infrastructure

architecture:
    external mcp clients (cursor, claude, etc)
            │
            ▼
    http endpoint (/mcp/call_tool)
            │
            ▼
    mcp tool handler
            │
            ▼
    a2a bridge (A2AClient)
            │
            ▼
    synq routing → agents
"""

import asyncio
import logging
import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from synqed import AgentId, MessageRouter
from synqed_mcp.a2a.client import A2AClient
from synqed_mcp.registry import get_tool_config, get_tool_registry, list_tools

logger = logging.getLogger(__name__)

# Global agent registry - tracks registered agents and their capabilities
AGENT_REGISTRY: Dict[str, Dict[str, Any]] = {}
# key: agent_uri (e.g., "agent://tools/salesforce")
# value: {"org": "tools", "name": "salesforce", "tools": ["query_leads", "update_lead"], "registered_at": "..."}


class GlobalMCPServer:
    """
    global mcp server for cloud deployment.
    
    runs as single instance, exposes mcp tools over http,
    and bridges to synqed agents via a2a.
    """
    
    def __init__(self, router: MessageRouter, workspace_id: str = "cloud"):
        """
        initialize global mcp server.
        
        args:
            router: message router for a2a communication
            workspace_id: workspace identifier
        """
        self.router = router
        self.workspace_id = workspace_id
        self.a2a_client = A2AClient(router, workspace_id)
        self.app = FastAPI(title="Synqed Global MCP Server")
        
        # add CORS middleware for Fly.io and other cloud deployments
        self.app.add_middleware(
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
        
        # register routes
        self._setup_routes()
        
        logger.info(f"global mcp server initialized (workspace={workspace_id})")
    
    def _setup_routes(self):
        """setup http routes for mcp server."""
        
        @self.app.get("/")
        async def root():
            """root endpoint with service info."""
            return {
                "service": "synqed-global-mcp-server",
                "status": "running",
                "tools": len(list_tools()),
                "registered_agents": len(AGENT_REGISTRY)
            }
        
        @self.app.get("/health")
        async def health_check():
            """health check endpoint for Fly.io and load balancers."""
            return {
                "status": "healthy",
                "service": "synqed-global-mcp-server",
                "workspace": self.workspace_id,
                "tools_count": len(list_tools()),
                "agents_count": len(AGENT_REGISTRY)
            }
        
        @self.app.get("/mcp/agents")
        async def list_registered_agents():
            """list all registered agents."""
            return {
                "agents": [
                    {
                        "agent_uri": agent_uri,
                        "org": info["org"],
                        "name": info["name"],
                        "tools": info.get("tools", []),
                        "registered_at": info.get("registered_at", "unknown")
                    }
                    for agent_uri, info in AGENT_REGISTRY.items()
                ]
            }
        
        @self.app.post("/mcp/register_agent")
        async def register_agent(payload: Dict[str, Any]):
            """
            register an agent with the global mcp server.
            
            request body:
                {
                    "agent_uri": "agent://tools/salesforce",
                    "org": "tools",
                    "name": "salesforce",
                    "tools": ["query_leads", "update_lead"]
                }
                
            response:
                {"status": "ok", "agent_uri": "..."}
            """
            agent_uri = payload.get("agent_uri")
            if not agent_uri:
                raise HTTPException(status_code=400, detail="agent_uri required")
            
            org = payload.get("org", "unknown")
            name = payload.get("name", "unknown")
            tools = payload.get("tools", [])
            
            # store in registry
            from datetime import datetime
            AGENT_REGISTRY[agent_uri] = {
                "org": org,
                "name": name,
                "tools": tools,
                "registered_at": datetime.utcnow().isoformat() + "Z"
            }
            
            logger.info(f"✅ registered remote agent: {agent_uri} (tools: {len(tools)})")
            
            return {
                "status": "ok",
                "agent_uri": agent_uri,
                "tools_count": len(tools)
            }
        
        @self.app.get("/mcp/tools")
        async def list_mcp_tools():
            """list all available mcp tools."""
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
        
        @self.app.post("/mcp/call_tool")
        async def call_mcp_tool(request: Dict[str, Any]):
            """
            call an mcp tool.
            
            request body:
                {
                    "tool": "tool_name",
                    "arguments": {...},
                    "caller": "agent_name" (optional)
                }
                
            response:
                tool result as json
            """
            tool_name = request.get("tool")
            arguments = request.get("arguments", {})
            caller = request.get("caller", "external")
            
            if not tool_name:
                raise HTTPException(status_code=400, detail="tool name required")
            
            logger.info(f"mcp tool call: {tool_name} (caller={caller})")
            
            try:
                # get tool configuration
                tool_config = get_tool_config(tool_name)
                agent_name = tool_config["agent"]
                task_type = tool_config["task_type"]
                
                # create agent id
                agent_id = AgentId(org="tools", name=agent_name)
                agent_uri = agent_id.to_uri()
                
                # check if agent is registered (in cloud mode)
                if agent_uri not in AGENT_REGISTRY:
                    logger.warning(f"agent not registered: {agent_uri}")
                    # don't fail immediately - agent might be local to this server
                    # but log the warning for debugging
                
                # add metadata
                payload = dict(arguments)
                payload["_mcp_origin"] = {
                    "caller": caller,
                    "tool": tool_name,
                    "mode": "cloud"
                }
                
                # call agent via a2a bridge
                logger.info(f"bridging to a2a: {agent_name}.{task_type}")
                result = await self.a2a_client.send_task_and_wait(
                    agent=agent_id,
                    task_type=task_type,
                    payload=payload,
                    timeout=30.0
                )
                
                logger.info(f"mcp tool result: {tool_name} -> {result.get('status')}")
                return result
            
            except KeyError:
                raise HTTPException(
                    status_code=404,
                    detail=f"tool '{tool_name}' not found"
                )
            
            except Exception as e:
                logger.error(f"mcp tool call failed: {tool_name} - {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"tool execution failed: {str(e)}"
                )
    
    def run_cloud(self, host: str = "0.0.0.0", port: int = 8080):
        """
        run server in cloud mode with http transport.
        
        args:
            host: bind address (defaults to 0.0.0.0 for Fly.io)
            port: bind port (defaults to 8080 for Fly.io)
        """
        logger.info(f"starting global mcp server on {host}:{port}")
        logger.info(f"workspace: {self.workspace_id}")
        logger.info(f"tools available: {len(list_tools())}")
        uvicorn.run(self.app, host=host, port=port, log_level="info")


async def create_cloud_server(
    router: MessageRouter,
    workspace_id: str = "cloud"
) -> GlobalMCPServer:
    """
    factory function to create global mcp server.
    
    args:
        router: message router with registered agents
        workspace_id: workspace identifier
        
    returns:
        GlobalMCPServer instance
    """
    server = GlobalMCPServer(router, workspace_id)
    logger.info("global mcp server created")
    return server


def main():
    """
    main entrypoint for running global mcp server.
    
    usage:
        python -m synqed_mcp.server_cloud
        
    environment variables:
        SYNQ_MCP_HOST: bind address (default: 0.0.0.0)
        SYNQ_MCP_PORT: bind port (default: 8080)
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # get config from env
    host = os.getenv("SYNQ_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("SYNQ_MCP_PORT", "8080"))
    
    # create router
    # note: in production, agents would be registered here
    # or discovered dynamically from a registry
    router = MessageRouter()
    
    # create and run server
    server = GlobalMCPServer(router, workspace_id="cloud")
    
    logger.info("="*60)
    logger.info("SYNQED GLOBAL MCP SERVER")
    logger.info("="*60)
    logger.info(f"listening on {host}:{port}")
    logger.info(f"tools registered: {len(list_tools())}")
    logger.info("="*60)
    
    server.run_cloud(host=host, port=port)


if __name__ == "__main__":
    main()

