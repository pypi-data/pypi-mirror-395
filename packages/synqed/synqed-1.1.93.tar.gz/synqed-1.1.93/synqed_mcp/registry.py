"""
global mcp tool registry.

centralizes mapping from mcp tool names to agent tasks.
used by both local and cloud mcp servers.

this is the single source of truth for all mcp tools
exposed by synqed agents.
"""

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


# global tool registry
# maps tool_name -> (agent_name, task_type)
GLOBAL_TOOL_REGISTRY: Dict[str, Dict[str, str]] = {
    # salesforce agent tools
    "salesforce.query_leads": {
        "agent": "salesforce",
        "task_type": "query_leads",
        "description": "query salesforce leads with soql"
    },
    "salesforce.update_lead": {
        "agent": "salesforce",
        "task_type": "update_lead",
        "description": "update a salesforce lead"
    },
    
    # zoom agent tools
    "zoom.create_meeting": {
        "agent": "zoom",
        "task_type": "create_meeting",
        "description": "create a zoom meeting"
    },
    "zoom.list_meetings": {
        "agent": "zoom",
        "task_type": "list_meetings",
        "description": "list zoom meetings"
    },
    
    # content creator agent tools
    "content_creator.generate": {
        "agent": "content_creator",
        "task_type": "generate",
        "description": "generate content"
    },
    "content_creator.edit": {
        "agent": "content_creator",
        "task_type": "edit",
        "description": "edit content"
    }
}


def get_tool_registry() -> Dict[str, Dict[str, str]]:
    """
    get the global tool registry.
    
    returns:
        dictionary mapping tool names to agent/task config
    """
    return GLOBAL_TOOL_REGISTRY.copy()


def get_tool_config(tool_name: str) -> Dict[str, str]:
    """
    get configuration for a specific tool.
    
    args:
        tool_name: name of the tool
        
    returns:
        tool configuration dict
        
    raises:
        KeyError: if tool not found
    """
    if tool_name not in GLOBAL_TOOL_REGISTRY:
        raise KeyError(f"tool '{tool_name}' not found in registry")
    
    return GLOBAL_TOOL_REGISTRY[tool_name].copy()


def list_tools() -> List[str]:
    """
    list all available tool names.
    
    returns:
        list of tool names
    """
    return list(GLOBAL_TOOL_REGISTRY.keys())


def list_tools_by_agent(agent_name: str) -> List[str]:
    """
    list tools for a specific agent.
    
    args:
        agent_name: name of agent
        
    returns:
        list of tool names for that agent
    """
    return [
        tool_name
        for tool_name, config in GLOBAL_TOOL_REGISTRY.items()
        if config["agent"] == agent_name
    ]


def register_tool(
    tool_name: str,
    agent_name: str,
    task_type: str,
    description: str = ""
) -> None:
    """
    register a new tool dynamically.
    
    args:
        tool_name: unique tool name (e.g., "myagent.mytask")
        agent_name: target agent name
        task_type: a2a task type
        description: tool description
    """
    if tool_name in GLOBAL_TOOL_REGISTRY:
        logger.warning(f"tool '{tool_name}' already registered, overwriting")
    
    GLOBAL_TOOL_REGISTRY[tool_name] = {
        "agent": agent_name,
        "task_type": task_type,
        "description": description or f"execute {task_type} on {agent_name}"
    }
    
    logger.info(f"registered tool: {tool_name} -> {agent_name}.{task_type}")


def unregister_tool(tool_name: str) -> None:
    """
    unregister a tool.
    
    args:
        tool_name: tool name to remove
    """
    if tool_name in GLOBAL_TOOL_REGISTRY:
        del GLOBAL_TOOL_REGISTRY[tool_name]
        logger.info(f"unregistered tool: {tool_name}")
    else:
        logger.warning(f"tool '{tool_name}' not found for unregistration")


def get_registry_stats() -> Dict[str, any]:
    """
    get statistics about the tool registry.
    
    returns:
        dictionary with registry statistics
    """
    agents = set(config["agent"] for config in GLOBAL_TOOL_REGISTRY.values())
    
    return {
        "total_tools": len(GLOBAL_TOOL_REGISTRY),
        "agents": list(agents),
        "agent_count": len(agents),
        "tools_by_agent": {
            agent: len(list_tools_by_agent(agent))
            for agent in agents
        }
    }


# log registry initialization
logger.info(f"global tool registry initialized with {len(GLOBAL_TOOL_REGISTRY)} tools")

