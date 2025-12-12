"""
agent exporter for mcp tools.

automatically exports a2a agents as mcp tools,
making them callable from external mcp clients.

usage:
    exporter = AgentExporter(mcp_server, router)
    exporter.export_agent("salesforce", ["query_leads", "update_lead"])
    
    # now external mcp clients can call:
    # - salesforce.query_leads
    # - salesforce.update_lead
"""

import logging
from typing import List, Dict, Any, Optional, Callable
import json
import inspect

logger = logging.getLogger(__name__)


class AgentExporter:
    """
    exports a2a agents as mcp tools.
    
    automatically creates mcp tool wrappers that route to a2a agents,
    making every agent's capabilities available to external mcp clients.
    """
    
    def __init__(self, mcp_server: Any, router: Any):
        """
        initialize agent exporter.
        
        args:
            mcp_server: mcp server instance (FastMCP)
            router: message router for a2a communication
        """
        self.mcp_server = mcp_server
        self.router = router
        self.exported_tools: Dict[str, Dict[str, Any]] = {}
    
    def export_agent(
        self,
        agent_name: str,
        task_types: List[str],
        descriptions: Optional[Dict[str, str]] = None,
        schemas: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> None:
        """
        export an agent's capabilities as mcp tools.
        
        args:
            agent_name: name of the agent to export
            task_types: list of task types the agent supports
            descriptions: optional descriptions for each task type
            schemas: optional input schemas for each task type
            
        example:
            exporter.export_agent(
                "salesforce",
                ["query_leads", "update_lead"],
                descriptions={
                    "query_leads": "Query Salesforce leads using SOQL",
                    "update_lead": "Update a lead record"
                }
            )
        """
        descriptions = descriptions or {}
        schemas = schemas or {}
        
        for task_type in task_types:
            tool_name = f"{agent_name}.{task_type}"
            description = descriptions.get(task_type, f"{agent_name} - {task_type}")
            schema = schemas.get(task_type, {"type": "object"})
            
            # create tool wrapper
            self._create_tool_wrapper(
                tool_name,
                agent_name,
                task_type,
                description,
                schema
            )
            
            logger.info(f"exported agent task as mcp tool: {tool_name}")
    
    def _create_tool_wrapper(
        self,
        tool_name: str,
        agent_name: str,
        task_type: str,
        description: str,
        schema: Dict[str, Any]
    ) -> None:
        """
        create an mcp tool wrapper for an agent task.
        
        the wrapper routes mcp tool calls to a2a tasks.
        """
        # create the tool function with explicit payload parameter
        # (fastmcp doesn't support **kwargs)
        async def tool_handler(payload: dict = {}) -> str:
            """
            dynamically created mcp tool handler.
            
            args:
                payload: task arguments as dictionary
            """
            logger.info(f"mcp tool called: {tool_name}")
            
            # construct a2a task
            task_message = {
                "task_type": task_type,
                "payload": payload,
                "mcp_origin": True
            }
            
            try:
                # route to agent via unified router api
                message_id = await self.router.route_message(
                    workspace_id="mcp_workspace",
                    sender="MCPServer",
                    recipient=agent_name,
                    content=json.dumps(task_message)
                )
                
                result = {
                    "status": "success",
                    "message_id": message_id,
                    "agent": agent_name,
                    "task_type": task_type
                }
                
                return json.dumps(result, indent=2)
            
            except Exception as e:
                logger.error(f"mcp tool error: {tool_name} - {e}")
                return json.dumps({
                    "status": "error",
                    "error": str(e),
                    "tool": tool_name
                })
        
        # register with mcp server
        # note: FastMCP uses decorators, so we use the underlying method
        if hasattr(self.mcp_server, 'mcp'):
            # get the FastMCP instance
            mcp = self.mcp_server.mcp
            
            # register tool
            mcp.tool(name=tool_name, description=description)(tool_handler)
        else:
            # direct FastMCP instance
            self.mcp_server.tool(name=tool_name, description=description)(tool_handler)
        
        # track exported tool
        self.exported_tools[tool_name] = {
            "agent": agent_name,
            "task_type": task_type,
            "description": description,
            "schema": schema
        }


def export_agent_as_tool(
    mcp_server: Any,
    router: Any,
    agent_name: str,
    task_types: List[str],
    descriptions: Optional[Dict[str, str]] = None
) -> None:
    """
    convenience function to export an agent as mcp tools.
    
    args:
        mcp_server: mcp server instance
        router: message router
        agent_name: agent to export
        task_types: task types to export
        descriptions: optional descriptions
        
    example:
        export_agent_as_tool(
            server,
            router,
            "salesforce",
            ["query_leads", "update_lead"]
        )
    """
    exporter = AgentExporter(mcp_server, router)
    exporter.export_agent(agent_name, task_types, descriptions)


def auto_export_all_agents(
    mcp_server: Any,
    router: Any,
    agent_registry: Dict[str, Any]
) -> None:
    """
    automatically export all registered agents as mcp tools.
    
    introspects each agent to discover its capabilities
    and exports them as mcp tools.
    
    args:
        mcp_server: mcp server instance
        router: message router
        agent_registry: dictionary of agent_name -> agent instance
        
    example:
        auto_export_all_agents(server, router, workspace.agents)
    """
    exporter = AgentExporter(mcp_server, router)
    
    for agent_name, agent in agent_registry.items():
        # try to introspect agent capabilities
        # for now, export with generic task types
        # in production, this would inspect agent logic signature
        
        task_types = ["execute", "query", "action"]
        
        logger.info(f"auto-exporting agent: {agent_name}")
        exporter.export_agent(
            agent_name,
            task_types,
            descriptions={
                "execute": f"Execute a task on {agent_name}",
                "query": f"Query {agent_name} for information",
                "action": f"Perform an action via {agent_name}"
            }
        )
    
    logger.info(f"auto-exported {len(agent_registry)} agents as mcp tools")

