"""
demo script for mcp wrapper around a2a in synqed.

demonstrates:
1. creating a2a agents (salesforce, zoom, content_creator)
2. registering agents in synqed workspace
3. starting mcp server
4. sending tasks via mcp tools
5. receiving and displaying results

usage:
    # run demo with stdio transport (default)
    python demo.py
    
    # run with sse transport
    python demo.py --transport sse --port 8080
    
    # run with custom agents
    python demo.py --setup-agents
"""

import asyncio
import json
import logging
from typing import Optional

from synqed import (
    Agent,
    AgentLogicContext,
    MessageRouter,
    Workspace,
    WorkspaceManager,
    AgentRuntimeRegistry,
)
from synqed_mcp.server import MCPServer
from synqed_mcp.a2a.client import A2AClient

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# agent logic functions
# ============================================================

async def salesforce_agent_logic(context: AgentLogicContext) -> dict:
    """
    salesforce agent logic.
    
    handles soql queries and returns lead data.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[salesforce agent ready]")
    
    try:
        # parse task message
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "query_leads":
            query = payload.get("query", "")
            logger.info(f"salesforce: executing query: {query[:100]}...")
            
            # simulate salesforce query
            results = [
                {"Id": "001", "Name": "John Doe", "Email": "john@example.com", "Status": "New"},
                {"Id": "002", "Name": "Jane Smith", "Email": "jane@example.com", "Status": "Qualified"},
                {"Id": "003", "Name": "Bob Johnson", "Email": "bob@example.com", "Status": "New"},
            ]
            
            response = {
                "status": "success",
                "data": results,
                "count": len(results),
                "query": query
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except json.JSONDecodeError:
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": "invalid json in task message"
        }))
    except Exception as e:
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


async def zoom_agent_logic(context: AgentLogicContext) -> dict:
    """
    zoom agent logic.
    
    handles meeting creation requests.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[zoom agent ready]")
    
    try:
        # parse task message
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "create_meeting":
            topic = payload.get("topic", "Meeting")
            start_time = payload.get("start_time", "")
            duration = payload.get("duration", 60)
            
            logger.info(f"zoom: creating meeting: {topic} at {start_time}")
            
            # simulate zoom meeting creation
            meeting_id = f"12345678{len(topic)}"
            join_url = f"https://zoom.us/j/{meeting_id}"
            password = "abc123"
            
            response = {
                "status": "success",
                "join_url": join_url,
                "meeting_id": meeting_id,
                "password": password,
                "topic": topic,
                "start_time": start_time,
                "duration": duration
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except Exception as e:
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


async def content_creator_agent_logic(context: AgentLogicContext) -> dict:
    """
    content creator agent logic.
    
    handles content generation requests.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[content creator agent ready]")
    
    try:
        # parse task message
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "generate_content":
            prompt = payload.get("prompt", "")
            tone = payload.get("tone", "professional")
            format_type = payload.get("format", "markdown")
            max_length = payload.get("max_length", 1000)
            
            logger.info(f"content_creator: generating content with tone={tone}")
            
            # simulate content generation
            content = f"""
# Generated Content

Based on your prompt: "{prompt[:50]}..."

This is {tone} content in {format_type} format.

## Key Points

- Content generated with specified tone and style
- Following A2A protocol standards
- Integrated via Synqed infrastructure
- Exposed through MCP wrapper

## Summary

This demonstrates the MCP wrapper successfully routing tasks
through A2A agents in the Synqed ecosystem.

---
*Generated by ContentCreator Agent*
"""
            
            response = {
                "status": "success",
                "content": content,
                "prompt": prompt,
                "tone": tone,
                "format": format_type,
                "word_count": len(content.split())
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except Exception as e:
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


# ============================================================
# setup functions
# ============================================================

def create_agents():
    """create and register a2a agents."""
    
    logger.info("creating agents...")
    
    # create salesforce agent
    salesforce_agent = Agent(
        name="salesforce",
        description="Salesforce integration agent for querying leads",
        logic=salesforce_agent_logic,
        role="tools"
    )
    
    # create zoom agent
    zoom_agent = Agent(
        name="zoom",
        description="Zoom integration agent for creating meetings",
        logic=zoom_agent_logic,
        role="tools"
    )
    
    # create content creator agent
    content_creator_agent = Agent(
        name="content_creator",
        description="Content generation agent",
        logic=content_creator_agent_logic,
        role="tools"
    )
    
    # register agents in runtime registry
    AgentRuntimeRegistry.register("salesforce", salesforce_agent)
    AgentRuntimeRegistry.register("zoom", zoom_agent)
    AgentRuntimeRegistry.register("content_creator", content_creator_agent)
    
    logger.info("agents registered successfully")
    
    return {
        "salesforce": salesforce_agent,
        "zoom": zoom_agent,
        "content_creator": content_creator_agent
    }


async def test_tools(a2a_client: A2AClient):
    """test the mcp tools by sending tasks directly."""
    
    logger.info("\n" + "="*60)
    logger.info("testing mcp tools via a2a client")
    logger.info("="*60)
    
    from synqed import AgentId
    
    # test salesforce tool
    logger.info("\n1. testing salesforce query...")
    result = await a2a_client.send_task(
        agent=AgentId.from_email_like("salesforce@tools"),
        task_type="query_leads",
        payload={"query": "SELECT Id, Name, Email FROM Lead WHERE Status='New'"}
    )
    logger.info(f"result: {json.dumps(result, indent=2)}")
    
    # test zoom tool
    logger.info("\n2. testing zoom meeting creation...")
    result = await a2a_client.send_task(
        agent=AgentId.from_email_like("zoom@tools"),
        task_type="create_meeting",
        payload={
            "topic": "MCP Demo Meeting",
            "start_time": "2025-11-23T10:00:00Z",
            "duration": 60
        }
    )
    logger.info(f"result: {json.dumps(result, indent=2)}")
    
    # test content creator tool
    logger.info("\n3. testing content generation...")
    result = await a2a_client.send_task(
        agent=AgentId.from_email_like("content_creator@tools"),
        task_type="generate_content",
        payload={
            "prompt": "Write about the future of AI agents",
            "tone": "informative",
            "format": "markdown"
        }
    )
    logger.info(f"result: {json.dumps(result, indent=2)}")
    
    logger.info("\n" + "="*60)
    logger.info("all tests completed successfully!")
    logger.info("="*60 + "\n")


# ============================================================
# main demo
# ============================================================

async def main(
    transport: str = "stdio",
    host: str = "localhost",
    port: int = 8080,
    test_mode: bool = True
):
    """
    main demo function.
    
    args:
        transport: mcp transport mode ("stdio" or "sse")
        host: server host for sse mode
        port: server port for sse mode
        test_mode: if true, run tool tests before starting server
    """
    logger.info("="*60)
    logger.info("mcp wrapper for a2a in synqed - demo")
    logger.info("="*60)
    
    # step 1: create agents
    logger.info("\nstep 1: creating a2a agents")
    agents = create_agents()
    logger.info(f"created {len(agents)} agents: {list(agents.keys())}")
    
    # step 2: setup message router
    logger.info("\nstep 2: setting up message router")
    router = MessageRouter()
    for name, agent in agents.items():
        router.register_agent(name, agent)
    logger.info("message router configured with agents")
    
    # step 3: create a2a client
    logger.info("\nstep 3: creating a2a client")
    a2a_client = A2AClient(router)
    logger.info("a2a client initialized")
    
    # step 4: test tools (optional)
    if test_mode:
        logger.info("\nstep 4: testing tools")
        await test_tools(a2a_client)
    
    # step 5: create and configure mcp server
    logger.info("\nstep 5: creating mcp server")
    server = MCPServer(
        name="synqed-a2a-mcp",
        host=host,
        port=port
    )
    server.set_router(router)
    logger.info(f"mcp server configured: transport={transport}")
    
    # step 6: return configured server (will be started by caller)
    logger.info("\nstep 6: mcp server ready")
    logger.info("="*60)
    
    if transport == "sse":
        logger.info(f"\nmcp server will start at: http://{host}:{port}/sse")
        logger.info("connect your mcp client to this endpoint")
    else:
        logger.info("\nmcp server will start on stdio")
        logger.info("use this with claude desktop or other mcp clients")
    
    logger.info("\navailable tools:")
    logger.info("  1. salesforce_query_leads - Query Salesforce leads")
    logger.info("  2. zoom_create_meeting - Create Zoom meetings")
    logger.info("  3. content_creator_generate - Generate content")
    logger.info("="*60 + "\n")
    
    return server, transport


if __name__ == "__main__":
    import sys
    
    # parse args
    transport = "stdio"
    host = "localhost"
    port = 8080
    test_mode = True
    
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]
    
    if "--host" in sys.argv:
        idx = sys.argv.index("--host")
        if idx + 1 < len(sys.argv):
            host = sys.argv[idx + 1]
    
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    
    if "--no-test" in sys.argv:
        test_mode = False
    
    # run setup and get configured server
    server, transport = asyncio.run(main(
        transport=transport,
        host=host,
        port=port,
        test_mode=test_mode
    ))
    
    # start mcp server (this will create its own event loop)
    logger.info("starting mcp server: transport={}".format(transport))
    server.run(transport=transport)

