"""
mcp injection middleware for synqed agents.

automatically wraps all agents to provide context.mcp capability
supporting both local and cloud modes.

architecture:
- MCPInjectionMiddleware.attach(agent) wraps agent.logic once
- creates AgentLogicContext with context.mcp injected automatically
- context.mcp routes to either local or cloud mcp server based on mode
- production-ready, scalable, concurrency-safe
"""

import asyncio
import logging
import os
from typing import Any, Callable, Dict, List, Optional, Set

from synqed import Agent, AgentId, AgentLogicContext, MessageRouter
from synqed_mcp.client import MCPClientBase, create_mcp_client
from synqed_mcp.registry import get_tool_registry, list_tools_by_agent

logger = logging.getLogger(__name__)

# import httpx for cloud registration (optional dependency)
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False
    logger.warning("httpx not installed - cloud mode registration unavailable")


class MCPInjectionMiddleware:
    """
    centralized mcp injection middleware.
    
    wraps agent logic functions to automatically provide context.mcp
    with support for local and cloud modes.
    
    usage:
        middleware = MCPInjectionMiddleware(router, a2a_client)
        middleware.attach(salesforce_agent)
        middleware.attach(zoom_agent)
        # all agents now have context.mcp automatically
    """
    
    def __init__(
        self,
        router: Optional[MessageRouter] = None,
        a2a_client: Optional[Any] = None,
        mode: Optional[str] = None,
        endpoint: Optional[str] = None
    ):
        """
        initialize middleware.
        
        args:
            router: message router for a2a communication (required for local mode, ignored in cloud)
            a2a_client: A2AClient instance (required for local mode, ignored in cloud)
            mode: "local" or "cloud" (if None, reads from env)
            endpoint: cloud MCP server endpoint (only used in cloud mode)
        """
        self.router = router
        self.a2a_client = a2a_client
        self.mode = mode or os.getenv("SYNQ_MCP_MODE", "local").lower()
        self._attached_agents: Set[int] = set()  # Track by id(agent), not name
        self._attached_agent_names: Set[str] = set()  # Track names for reporting
        self._exported_tools: Dict[str, List[str]] = {}  # agent_name -> [tool_names]
        
        # In cloud mode: no local tool registry
        if self.mode == "local":
            self.tool_registry = get_tool_registry()
        else:
            self.tool_registry = None
        
        # determine cloud endpoint
        self.cloud_endpoint = endpoint or os.getenv("SYNQ_MCP_ENDPOINT")
        if self.mode == "cloud" and not self.cloud_endpoint:
            # default to Fly.io deployment if no endpoint specified
            self.cloud_endpoint = "https://synqed.fly.dev/mcp"
            logger.warning(f"⚠️  SYNQ_MCP_ENDPOINT not set, using default Fly.io: {self.cloud_endpoint}")
        
        # warn if localhost is used in cloud mode
        if self.mode == "cloud" and self.cloud_endpoint and ("localhost" in self.cloud_endpoint or "127.0.0.1" in self.cloud_endpoint):
            logger.warning(f"⚠️  WARNING: Cloud mode with localhost endpoint: {self.cloud_endpoint}")
            logger.warning(f"⚠️  For production, set SYNQ_MCP_ENDPOINT to your Fly.io URL")
        
        logger.info(f"mcp injection middleware initialized (mode={self.mode}, endpoint={self.cloud_endpoint if self.mode == 'cloud' else 'N/A'})")
    
    async def register_with_cloud(self, agent: Agent) -> bool:
        """
        register agent with cloud mcp server.
        
        IN CLOUD MODE: This is a NO-OP. Agents don't register themselves.
        The cloud MCP server manages its own agent registry.
        
        args:
            agent: agent to register
            
        returns:
            Always returns True (no registration needed)
        """
        # In cloud mode, agents don't self-register
        # The cloud MCP server has its own agent registry
        logger.debug(f"[cloud] skipping agent registration for {agent.name} - managed by cloud server")
        return True
    
    def attach(self, agent: Agent) -> None:
        """
        attach mcp capability to an agent.
        
        wraps agent.logic to inject context.mcp automatically.
        in cloud mode, also registers the agent with the cloud server.
        idempotent - can be called multiple times safely.
        
        args:
            agent: agent to attach mcp capability to
        """
        agent_name = agent.name
        agent_id = id(agent)
        
        # check if THIS SPECIFIC INSTANCE is already attached (by object identity)
        if agent_id in self._attached_agents:
            logger.debug(f"MCP already attached to {agent_name}, skipping")
            return
        
        # store original logic
        original_logic = agent.logic
        
        # create wrapped logic
        async def mcp_enabled_logic(context: AgentLogicContext) -> Dict[str, Any]:
            """
            wrapped logic with context.mcp injected.
            
            creates appropriate mcp client (local or cloud) based on mode
            and injects it into context.
            """
            # create mcp client for this agent
            if self.mode == "cloud":
                # Cloud mode: use RemoteMCPClient pointing to Fly.io
                from synqed_mcp.client import RemoteMCPClient
                mcp_client = RemoteMCPClient(
                    agent_name=agent_name,
                    endpoint=self.cloud_endpoint
                )
            else:
                # Local mode: use LocalMCPClient with local A2A
                mcp_client = create_mcp_client(
                    agent_name=agent_name,
                    a2a_client=self.a2a_client,
                    tool_registry=self.tool_registry
                )
            
            # inject into context
            context.mcp = mcp_client
            
            # call original logic
            return await original_logic(context)
        
        # replace agent's logic with wrapped version
        agent.logic = mcp_enabled_logic
        
        # mark as attached (track by instance identity, not name)
        self._attached_agents.add(agent_id)
        self._attached_agent_names.add(agent_name)
        
        logger.debug(f"MCP capability attached to {agent_name} (mode={self.mode})")
    
    def attach_all(self, agents: Dict[str, Agent]) -> None:
        """
        attach mcp capability to all agents in a dictionary.
        
        args:
            agents: dictionary of agent_name → agent
        """
        for agent_name, agent in agents.items():
            self.attach(agent)
        
        logger.info(f"✅ mcp capability attached to {len(agents)} agents")
    
    def is_attached(self, agent_name: str) -> bool:
        """check if mcp is attached to an agent (by name)."""
        return agent_name in self._attached_agent_names
    
    def get_attached_agents(self) -> Set[str]:
        """get set of agent names with mcp attached."""
        return self._attached_agent_names.copy()
    
    def get_exported_tools(self, agent_name: str) -> List[str]:
        """get list of tools exported by an agent."""
        return self._exported_tools.get(agent_name, [])


def create_mcp_middleware(
    router: Optional[MessageRouter] = None,
    a2a_client: Optional[Any] = None,
    mode: Optional[str] = None,
    endpoint: Optional[str] = None
) -> MCPInjectionMiddleware:
    """
    factory function to create mcp injection middleware.
    
    automatically selects local vs cloud mode based on:
    1. explicit mode parameter
    2. SYNQ_MCP_MODE environment variable
    3. default: "local"
    
    in cloud mode:
    - router and a2a_client are ignored (not used)
    - all calls go to remote MCP server at endpoint
    - automatically uses Fly.io endpoint if SYNQ_MCP_ENDPOINT is not set
    
    args:
        router: message router (required for local mode, ignored in cloud)
        a2a_client: A2AClient instance (required for local mode, ignored in cloud)
        mode: explicit mode override ("local" or "cloud")
        endpoint: cloud MCP server URL (only used in cloud mode)
        
    returns:
        configured MCPInjectionMiddleware instance
        
    environment variables:
        SYNQ_MCP_MODE: "local" or "cloud" (default: "local")
        SYNQ_MCP_ENDPOINT: cloud server url (default: "https://synqed.fly.dev/mcp" in cloud mode)
        
    example:
        # local mode
        middleware = create_mcp_middleware(
            router=router,
            a2a_client=a2a_client,
            mode="local"
        )
        
        # cloud mode with Fly.io
        middleware = create_mcp_middleware(
            mode="cloud",
            endpoint="https://synqed.fly.dev/mcp"
        )
    """
    import os
    
    # determine mode
    effective_mode = mode or os.getenv("SYNQ_MCP_MODE", "local").lower()
    
    # validate requirements for local mode
    if effective_mode == "local":
        if not a2a_client or not router:
            raise ValueError("router and a2a_client required for local mode")
    
    logger.info(f"creating mcp middleware (mode={effective_mode})")
    
    return MCPInjectionMiddleware(
        router=router,
        a2a_client=a2a_client,
        mode=effective_mode,
        endpoint=endpoint
    )
