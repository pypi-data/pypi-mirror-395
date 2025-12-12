"""
mcp client implementations: local vs remote.

provides unified interface for agents to call mcp tools,
with automatic routing to either in-process or cloud mcp server.

architecture:
- MCPClientBase: abstract interface
- LocalMCPClient: calls in-process mcp server / dispatcher
- RemoteMCPClient: calls cloud mcp server via http
- create_mcp_client(): factory that selects based on env vars
"""

import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import httpx

from synqed import AgentId

logger = logging.getLogger(__name__)


class MCPClientBase(ABC):
    """
    abstract base class for mcp clients.
    
    defines interface for calling mcp tools from agent logic.
    implementations handle local vs remote routing.
    """
    
    def __init__(self, agent_name: str):
        """
        initialize mcp client.
        
        args:
            agent_name: name of the agent using this client
        """
        self.agent_name = agent_name
        logger.debug(f"mcp client initialized for {agent_name}")
    
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        call an mcp tool and return result.
        
        args:
            tool_name: name of tool (e.g., "zoom.create_meeting")
            arguments: tool arguments
            
        returns:
            tool result as dictionary
        """
        pass
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available mcp tools (optional).
        
        Returns:
            List of tool dictionaries with name, description, and input_schema
        """
        return []


class LocalMCPClient(MCPClientBase):
    """
    local mcp client for in-process server.
    
    used in dev/local mode. calls a2a client directly
    to execute target agents without network round-trip.
    """
    
    def __init__(self, agent_name: str, a2a_client: Any, tool_registry: Dict[str, Dict[str, str]]):
        """
        initialize local mcp client.
        
        args:
            agent_name: name of agent using this client
            a2a_client: A2AClient instance for direct execution
            tool_registry: mapping of tool_name -> (agent, task_type)
        """
        super().__init__(agent_name)
        self.a2a_client = a2a_client
        self.tool_registry = tool_registry
        logger.info(f"local mcp client created for {agent_name}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        call mcp tool via local a2a client.
        
        directly executes target agent without network overhead.
        """
        logger.info(f"{self.agent_name} calling local mcp tool: {tool_name}")
        
        # check if tool is registered
        if tool_name not in self.tool_registry:
            logger.error(f"mcp tool not found: {tool_name}")
            return {
                "status": "error",
                "error": f"mcp tool '{tool_name}' not registered",
                "available_tools": list(self.tool_registry.keys())
            }
        
        # get tool config
        tool_config = self.tool_registry[tool_name]
        target_agent_name = tool_config["agent"]
        task_type = tool_config["task_type"]
        
        # create agent id
        target_agent_id = AgentId(org="tools", name=target_agent_name)
        
        # add metadata to prevent infinite loops
        mcp_payload = dict(arguments)
        mcp_payload["_mcp_origin"] = {
            "caller": self.agent_name,
            "tool": tool_name,
            "depth": arguments.get("_mcp_origin", {}).get("depth", 0) + 1
        }
        
        # prevent deep recursion
        if mcp_payload["_mcp_origin"]["depth"] > 2:
            logger.warning(f"mcp call depth limit reached for {tool_name}")
            return {
                "status": "error",
                "error": "mcp call depth limit exceeded",
                "max_depth": 2
            }
        
        try:
            # call via local a2a client
            result = await self.a2a_client.send_task_and_wait(
                agent=target_agent_id,
                task_type=task_type,
                payload=mcp_payload,
                timeout=10.0
            )
            
            logger.info(f"local mcp tool response from {target_agent_name}")
            return result
        
        except Exception as e:
            logger.error(f"local mcp tool call failed: {tool_name} - {e}")
            return {
                "status": "error",
                "error": str(e),
                "tool": tool_name
            }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from local registry.
        
        Returns:
            List of tool dictionaries with name and description
        """
        tools = []
        for tool_name, tool_info in self.tool_registry.items():
            tools.append({
                "name": tool_name,
                "description": tool_info.get("description", ""),
                "handler": tool_info.get("handler")
            })
        return tools


class RemoteMCPClient(MCPClientBase):
    """
    remote mcp client for cloud server.
    
    used in cloud/prod mode. calls global mcp server
    via http to execute tools on any agent.
    """
    
    def __init__(self, agent_name: str, endpoint: str, timeout: float = 30.0):
        """
        initialize remote mcp client.
        
        args:
            agent_name: name of agent using this client
            endpoint: cloud mcp server endpoint (e.g., "https://mcp.synq.cloud")
            timeout: request timeout in seconds
        """
        super().__init__(agent_name)
        self.endpoint = endpoint.rstrip('/')
        self.timeout = timeout
        self._http_client = httpx.AsyncClient(timeout=timeout)
        logger.info(f"remote mcp client created for {agent_name} -> {endpoint}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        call mcp tool via cloud server.
        
        sends http request to global mcp server which
        routes to appropriate agent via a2a.
        """
        logger.info(f"{self.agent_name} calling remote mcp tool: {tool_name}")
        
        # construct request payload
        payload = {
            "tool": tool_name,
            "arguments": arguments,
            "caller": self.agent_name
        }
        
        try:
            # call cloud mcp server
            logger.debug(f"POST {self.endpoint}/call_tool with tool={tool_name}")
            response = await self._http_client.post(
                f"{self.endpoint}/call_tool",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Log response details
            logger.debug(f"response status: {response.status_code}")
            
            if response.status_code != 200:
                error_detail = response.text[:200] if response.text else "no error details"
                logger.error(f"remote mcp server returned {response.status_code}: {error_detail}")
                return {
                    "status": "error",
                    "error": f"server returned {response.status_code}: {error_detail}",
                    "tool": tool_name,
                    "endpoint": self.endpoint
                }
            
            result = response.json()
            logger.info(f"✅ remote mcp tool '{tool_name}' completed successfully")
            return result
        
        except httpx.HTTPStatusError as e:
            error_body = e.response.text[:200] if e.response else "no response body"
            logger.error(f"❌ remote mcp tool call failed: {tool_name}")
            logger.error(f"   status: {e.response.status_code if e.response else 'unknown'}")
            logger.error(f"   body: {error_body}")
            return {
                "status": "error",
                "error": f"http {e.response.status_code if e.response else 'error'}: {error_body}",
                "tool": tool_name,
                "endpoint": self.endpoint
            }
        
        except httpx.HTTPError as e:
            logger.error(f"❌ remote mcp http error for {tool_name}: {e}")
            return {
                "status": "error",
                "error": f"http error: {str(e)}",
                "tool": tool_name,
                "endpoint": self.endpoint
            }
        
        except Exception as e:
            logger.error(f"❌ remote mcp unexpected error for {tool_name}: {e}")
            logger.exception("full traceback:")
            return {
                "status": "error",
                "error": str(e),
                "tool": tool_name
            }
    
    async def close(self):
        """close http client."""
        await self._http_client.aclose()
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from remote server.
        
        Returns:
            List of tool dictionaries with name, description, and input_schema
        """
        try:
            logger.debug(f"Fetching tools list from {self.endpoint}/tools")
            response = await self._http_client.get(
                f"{self.endpoint}/tools",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch tools list: {response.status_code}")
                return []
            
            data = response.json()
            tools = data.get("tools", [])
            logger.debug(f"Fetched {len(tools)} tools from remote MCP server")
            return tools
            
        except Exception as e:
            logger.warning(f"Error fetching tools list from remote server: {e}")
            return []


def create_mcp_client(
    agent_name: str,
    a2a_client: Optional[Any] = None,
    tool_registry: Optional[Dict[str, Dict[str, str]]] = None
) -> MCPClientBase:
    """
    factory function to create appropriate mcp client based on mode.
    
    reads SYNQ_MCP_MODE environment variable:
    - "local" (default): creates LocalMCPClient
    - "cloud": creates RemoteMCPClient
    
    in cloud mode, automatically uses Fly.io endpoint if SYNQ_MCP_ENDPOINT is not set.
    
    args:
        agent_name: name of agent using the client
        a2a_client: A2AClient instance (required for local mode)
        tool_registry: tool registry (required for local mode)
        
    returns:
        MCPClientBase instance (Local or Remote)
        
    environment variables:
        SYNQ_MCP_MODE: "local" or "cloud" (default: "local")
        SYNQ_MCP_ENDPOINT: cloud server url (default: "https://synqed.fly.dev/mcp" in cloud mode)
    """
    mode = os.getenv("SYNQ_MCP_MODE", "local").lower()
    
    if mode == "cloud":
        endpoint = os.getenv("SYNQ_MCP_ENDPOINT")
        if not endpoint:
            # Default to Fly.io deployment
            endpoint = "https://synqed.fly.dev/mcp"
            logger.warning(f"⚠️  SYNQ_MCP_ENDPOINT not set, using default Fly.io: {endpoint}")
        
        # Warn if localhost is used in cloud mode
        if "localhost" in endpoint or "127.0.0.1" in endpoint:
            logger.warning(f"⚠️  WARNING: Cloud mode with localhost endpoint: {endpoint}")
            logger.warning(f"⚠️  For production, set SYNQ_MCP_ENDPOINT to your Fly.io URL")
        
        logger.info(f"creating remote mcp client for {agent_name} (endpoint: {endpoint})")
        return RemoteMCPClient(agent_name, endpoint)
    
    else:  # local mode
        if not a2a_client or not tool_registry:
            raise ValueError("a2a_client and tool_registry required for local mode")
        
        logger.info(f"creating local mcp client for {agent_name}")
        return LocalMCPClient(agent_name, a2a_client, tool_registry)

