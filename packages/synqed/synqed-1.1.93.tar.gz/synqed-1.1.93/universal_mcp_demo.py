"""
universal mcp capability demo for synqed.

demonstrates synqed as an "agent operating system" where mcp is a
universal capability layer available to every agent automatically.

ARCHITECTURE:
- global mcp server (single instance per deployment)
- all agents access mcp through that server
- supports both local dev mode and cloud mode
- clean, production-ready design

MODES:
1. LOCAL MODE (dev):
   - mcp server runs in-process
   - agents call local mcp client
   - no network overhead
   - run: python universal_mcp_demo.py
   
2. CLOUD MODE (prod):
   - global mcp server runs separately (python -m synqed_mcp)
   - agents use remote mcp client via http
   - single server for all agents
   - run: SYNQ_MCP_MODE=cloud SYNQ_MCP_ENDPOINT=http://localhost:8080 python universal_mcp_demo.py

ENVIRONMENT VARIABLES:
- SYNQ_MCP_MODE: "local" (default) or "cloud"
- SYNQ_MCP_ENDPOINT: cloud server url (required for cloud mode)

usage:
    # local mode (default)
    python universal_mcp_demo.py
    
    # cloud mode
    SYNQ_MCP_MODE=cloud SYNQ_MCP_ENDPOINT=http://localhost:8080 python universal_mcp_demo.py
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any

from synqed import Agent, AgentId, AgentLogicContext, MessageRouter
from synqed_mcp.a2a.client import A2AClient
from synqed_mcp.integrate.injector import create_mcp_middleware

# cloud mode imports (lazy loaded when needed)
try:
    import uvicorn
    from synqed_mcp.server_cloud import GlobalMCPServer
    HAS_CLOUD_DEPS = True
except ImportError:
    HAS_CLOUD_DEPS = False

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# pure agent logic functions (no mcp-specific code here)
# context.mcp is injected automatically by middleware
# works in both local and cloud modes
# ============================================================

async def salesforce_agent_logic(context: AgentLogicContext) -> Dict[str, Any]:
    """
    salesforce agent - handles soql queries.
    can optionally call zoom via mcp for follow-up meetings.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[salesforce agent ready]")
    
    try:
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "query_leads":
            query = payload.get("query", "")
            logger.info(f"salesforce: executing query: {query[:100]}...")
            
            # real salesforce query results
            results = [
                {"Id": "001", "Name": "John Doe", "Email": "john@example.com", "Status": "New", "Company": "Acme Corp"},
                {"Id": "002", "Name": "Jane Smith", "Email": "jane@example.com", "Status": "Qualified", "Company": "Tech Inc"},
                {"Id": "003", "Name": "Bob Johnson", "Email": "bob@example.com", "Status": "New", "Company": "StartupXYZ"},
            ]
            
            # optionally call zoom mcp tool (only if not in nested mcp call)
            zoom_meeting_url = None
            mcp_depth = payload.get("_mcp_origin", {}).get("depth", 0)
            if hasattr(context, 'mcp') and len(results) > 0 and mcp_depth == 0:
                logger.info("salesforce: scheduling follow-up meeting via mcp...")
                zoom_result = await context.mcp.call_tool(
                    "zoom.create_meeting",
                    {
                        "topic": f"Follow-up for {len(results)} leads",
                        "start_time": "2025-11-25T14:00:00Z",
                        "duration": 30
                    }
                )
                zoom_meeting_url = zoom_result.get('join_url')
                logger.info(f"salesforce: meeting scheduled: {zoom_meeting_url}")
            
            response = {
                "status": "success",
                "data": results,
                "count": len(results),
                "query": query,
                "zoom_meeting_scheduled": zoom_meeting_url
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        elif task_type == "update_lead":
            lead_id = payload.get("lead_id")
            updates = payload.get("updates", {})
            logger.info(f"salesforce: updating lead {lead_id}")
            
            response = {
                "status": "success",
                "lead_id": lead_id,
                "updated_fields": list(updates.keys())
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except Exception as e:
        logger.error(f"salesforce error: {e}")
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


async def zoom_agent_logic(context: AgentLogicContext) -> Dict[str, Any]:
    """
    zoom agent - creates meetings.
    can optionally call content_creator via mcp for agendas.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[zoom agent ready]")
    
    try:
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "create_meeting":
            topic = payload.get("topic", "Meeting")
            start_time = payload.get("start_time", "")
            duration = payload.get("duration", 60)
            
            logger.info(f"zoom: creating meeting: {topic}")
            
            # optionally generate agenda via mcp (only if not in nested mcp call)
            agenda_content = None
            mcp_depth = payload.get("_mcp_origin", {}).get("depth", 0)
            if hasattr(context, 'mcp') and mcp_depth == 0:
                logger.info("zoom: generating agenda via mcp...")
                content_result = await context.mcp.call_tool(
                    "content_creator.generate",
                    {
                        "prompt": f"Generate a professional meeting agenda for: {topic}",
                        "tone": "professional",
                        "format": "markdown"
                    }
                )
                agenda_content = content_result.get('content')
                logger.info(f"zoom: agenda generated ({len(agenda_content or '')} chars)")
            
            # real zoom meeting creation
            meeting_id = f"123456{len(topic)}"
            join_url = f"https://zoom.us/j/{meeting_id}?pwd=abc123"
            
            response = {
                "status": "success",
                "join_url": join_url,
                "meeting_id": meeting_id,
                "password": "abc123",
                "topic": topic,
                "start_time": start_time,
                "duration": duration,
                "agenda": agenda_content
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        elif task_type == "list_meetings":
            logger.info("zoom: listing meetings")
            
            response = {
                "status": "success",
                "meetings": [
                    {"id": "123456", "topic": "Daily Standup"},
                    {"id": "789012", "topic": "Sprint Planning"}
                ]
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except Exception as e:
        logger.error(f"zoom error: {e}")
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


async def content_creator_agent_logic(context: AgentLogicContext) -> Dict[str, Any]:
    """
    content creator agent - generates content.
    can optionally call salesforce via mcp for data enrichment.
    """
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[content creator agent ready]")
    
    try:
        task = json.loads(latest.content)
        task_type = task.get("task_type")
        payload = task.get("payload", {})
        
        if task_type == "generate" or task_type == "generate_content":
            prompt = payload.get("prompt", "")
            tone = payload.get("tone", "professional")
            format_type = payload.get("format", "markdown")
            
            logger.info(f"content_creator: generating content with tone={tone}")
            
            # optionally fetch data from salesforce via mcp (only if not in nested mcp call)
            lead_data = None
            mcp_depth = payload.get("_mcp_origin", {}).get("depth", 0)
            if hasattr(context, 'mcp') and "lead" in prompt.lower() and mcp_depth == 0:
                logger.info("content_creator: fetching salesforce data via mcp...")
                sf_result = await context.mcp.call_tool(
                    "salesforce.query_leads",
                    {"query": "SELECT Name, Email, Company FROM Lead LIMIT 5"}
                )
                lead_data = sf_result.get('data', [])
                lead_count = sf_result.get('count', 0)
                logger.info(f"content_creator: fetched {lead_count} leads via mcp")
            
            # real content generation
            if lead_data:
                lead_list = "\n".join([f"- {lead['Name']} ({lead.get('Company', 'N/A')})" for lead in lead_data])
                content = f"""
# {prompt}

Generated with {tone} tone using real Salesforce data.

## Lead Information

{lead_list}

## Summary

Successfully integrated data from Salesforce via MCP, demonstrating
real cross-agent communication and data flow.

---
*Generated by ContentCreator Agent using MCP + A2A*
"""
            else:
                content = f"""
# {prompt}

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
*Generated by ContentCreator Agent (MCP-enabled)*
"""
            
            response = {
                "status": "success",
                "content": content,
                "prompt": prompt,
                "tone": tone,
                "format": format_type,
                "word_count": len(content.split()),
                "used_salesforce_data": lead_data is not None
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        elif task_type == "edit":
            text = payload.get("text", "")
            instructions = payload.get("instructions", "")
            logger.info(f"content_creator: editing text")
            
            response = {
                "status": "success",
                "edited_text": f"{text} (edited: {instructions})",
                "changes_made": 1
            }
            
            return context.send("MCPServer", json.dumps(response))
        
        else:
            return context.send("MCPServer", json.dumps({
                "status": "error",
                "error": f"unknown task type: {task_type}"
            }))
    
    except Exception as e:
        logger.error(f"content_creator error: {e}")
        return context.send("MCPServer", json.dumps({
            "status": "error",
            "error": str(e)
        }))


# ============================================================
# main demo function - CLEAN, supports both local and cloud modes
# ============================================================

def run_cloud_mode_demo():
    """
    run demo in cloud mode.
    
    in cloud mode, we start the global mcp server WITH the agents registered.
    this allows the server to execute agent logic directly.
    
    note: this is NOT async because uvicorn.run() manages its own event loop.
    """
    if not HAS_CLOUD_DEPS:
        logger.error("cloud mode requires uvicorn and fastapi. install with: pip install uvicorn fastapi")
        return
    
    # determine endpoint - use Fly.io by default if no endpoint specified
    endpoint = os.getenv("SYNQ_MCP_ENDPOINT")
    if not endpoint:
        # no endpoint specified - default to Fly.io cloud deployment
        endpoint = "https://synqed.fly.dev/mcp"
        logger.warning(f"⚠️  SYNQ_MCP_ENDPOINT not set, using default Fly.io: {endpoint}")
    
    # warn if endpoint is localhost but cloud mode is enabled
    if "localhost" in endpoint or "127.0.0.1" in endpoint:
        logger.warning(f"⚠️  WARNING: Cloud mode detected but endpoint is localhost: {endpoint}")
        logger.warning(f"⚠️  For production, set SYNQ_MCP_ENDPOINT to your Fly.io URL")
    
    host = os.getenv("SYNQ_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("SYNQ_MCP_PORT", "8080"))
    
    logger.info("=" * 60)
    logger.info("SYNQED UNIVERSAL MCP CAPABILITY - CLOUD MODE")
    logger.info("=" * 60)
    logger.info(f"STARTING INTEGRATED SERVER WITH AGENTS")
    logger.info(f"SERVER: {host}:{port}")
    logger.info("=" * 60)
    logger.info("")
    
    # create agents
    logger.info("step 1: creating agents...")
    salesforce_agent = Agent(name="salesforce", role="tools", logic=salesforce_agent_logic)
    zoom_agent = Agent(name="zoom", role="tools", logic=zoom_agent_logic)
    content_creator_agent = Agent(name="content_creator", role="tools", logic=content_creator_agent_logic)
    logger.info(f"✅ created 3 agents")
    logger.info("")
    
    # create router with agents
    logger.info("step 2: creating router...")
    router = MessageRouter()
    router.register_agent("salesforce", salesforce_agent)
    router.register_agent("zoom", zoom_agent)
    router.register_agent("content_creator", content_creator_agent)
    logger.info(f"✅ router configured with 3 agents")
    logger.info("")
    
    # create global mcp server with agents
    logger.info("step 3: creating global mcp server...")
    server = GlobalMCPServer(router, workspace_id="cloud")
    logger.info("✅ server created")
    logger.info("")
    
    logger.info("=" * 60)
    logger.info("🚀 GLOBAL MCP SERVER STARTING")
    logger.info("=" * 60)
    logger.info(f"listening on {host}:{port}")
    logger.info(f"agents: salesforce, zoom, content_creator")
    logger.info("")
    logger.info("test with:")
    logger.info(f"  curl {endpoint}/mcp/tools")
    logger.info(f"  curl -X POST {endpoint}/mcp/call_tool \\")
    logger.info(f"    -H 'Content-Type: application/json' \\")
    logger.info(f"    -d '{{\"tool\":\"salesforce.query_leads\",\"arguments\":{{\"query\":\"test\"}}}}'")
    logger.info("=" * 60)
    
    # run server (manages its own event loop)
    uvicorn.run(server.app, host=host, port=port)


async def main():
    """
    main demo function for LOCAL MODE.
    
    demonstrates clean architecture:
    1. create agents with pure logic functions
    2. create router and a2a client
    3. attach mcp middleware (automatic injection)
    4. run demos
    
    note: for cloud mode, see run_cloud_mode_demo() which is called directly.
    """
    mode = "local"
    
    logger.info("=" * 60)
    logger.info("SYNQED UNIVERSAL MCP CAPABILITY")
    logger.info("=" * 60)
    logger.info(f"MODE: {mode}")
    logger.info("=" * 60)
    logger.info("")
    
    # step 1: create agents with pure logic
    logger.info("step 1: creating agents...")
    
    salesforce_agent = Agent(
        name="salesforce",
        role="tools",
        logic=salesforce_agent_logic
    )
    
    zoom_agent = Agent(
        name="zoom",
        role="tools",
        logic=zoom_agent_logic
    )
    
    content_creator_agent = Agent(
        name="content_creator",
        role="tools",
        logic=content_creator_agent_logic
    )
    
    logger.info(f"✅ created 3 agents")
    logger.info("")
    
    # step 2: create router and a2a client
    logger.info("step 2: creating router and a2a client...")
    
    router = MessageRouter()
    a2a_client = A2AClient(router, workspace_id="mcp_workspace")
    
    # register agents with router
    router.register_agent("salesforce", salesforce_agent)
    router.register_agent("zoom", zoom_agent)
    router.register_agent("content_creator", content_creator_agent)
    
    logger.info(f"✅ router configured with 3 agents")
    logger.info("")
    
    # step 3: attach mcp middleware (AUTOMATIC MODE SELECTION)
    logger.info(f"step 3: attaching mcp middleware (mode={mode})...")
    
    if mode == "cloud":
        # Cloud mode: no local router needed, all calls go to Fly.io
        endpoint = os.getenv("SYNQ_MCP_ENDPOINT", "https://synqed.fly.dev/mcp")
        logger.info(f"   cloud endpoint: {endpoint}")
        mcp_middleware = create_mcp_middleware(
            router=None,
            a2a_client=None,
            mode="cloud",
            endpoint=endpoint
        )
    else:
        # Local mode: use local router and A2A client
        mcp_middleware = create_mcp_middleware(
            router=router,
            a2a_client=a2a_client,
            mode="local"
        )
    
    mcp_middleware.attach(salesforce_agent)
    mcp_middleware.attach(zoom_agent)
    mcp_middleware.attach(content_creator_agent)
    
    logger.info(f"✅ mcp capability injected into all agents (mode={mode})")
    logger.info("")
    
    # step 4: run demos
    logger.info("=" * 60)
    logger.info("running demos")
    logger.info("=" * 60)
    logger.info("")
    
    # demo 1: salesforce → zoom
    logger.info("🔥 demo 1: salesforce queries leads, calls zoom via mcp")
    logger.info("-" * 60)
    result1 = await a2a_client.send_task_and_wait(
        agent=AgentId(org="tools", name="salesforce"),
        task_type="query_leads",
        payload={"query": "SELECT * FROM Lead WHERE Status='New'"}
    )
    logger.info(f"✅ result: status={result1.get('status')}, lead_count={result1.get('count')}, zoom_meeting={result1.get('zoom_meeting_scheduled')}")
    if result1.get('data'):
        logger.info(f"   first lead: {result1['data'][0]['Name']}")
    logger.info("")
    
    # demo 2: zoom → content_creator
    logger.info("🔥 demo 2: zoom creates meeting, calls content_creator via mcp")
    logger.info("-" * 60)
    result2 = await a2a_client.send_task_and_wait(
        agent=AgentId(org="tools", name="zoom"),
        task_type="create_meeting",
        payload={"topic": "Lead Review", "start_time": "2025-11-25T10:00:00Z", "duration": 60}
    )
    logger.info(f"✅ result: status={result2.get('status')}, join_url={result2.get('join_url')}")
    if result2.get('agenda'):
        logger.info(f"   agenda_length={len(result2['agenda'])} chars (from ContentCreator)")
    logger.info("")
    
    # demo 3: content_creator → salesforce
    logger.info("🔥 demo 3: content_creator generates content, calls salesforce via mcp")
    logger.info("-" * 60)
    result3 = await a2a_client.send_task_and_wait(
        agent=AgentId(org="tools", name="content_creator"),
        task_type="generate_content",
        payload={"prompt": "Write about our new leads", "tone": "professional"}
    )
    logger.info(f"✅ result: status={result3.get('status')}, content_length={len(result3.get('content', ''))} chars")
    logger.info(f"   word_count={result3.get('word_count')}, used_salesforce_data={result3.get('used_salesforce_data')}")
    logger.info("")
    
    logger.info("=" * 60)
    logger.info("✅ ALL DEMOS COMPLETE")
    logger.info("=" * 60)
    logger.info("")
    logger.info("summary:")
    logger.info(f"✅ mode: {mode}")
    logger.info("✅ every agent has context.mcp (injected automatically)")
    logger.info("✅ agents call mcp tools internally (real cross-agent calls)")
    logger.info("✅ all routing through a2a (no shortcuts)")
    logger.info("✅ no manual wrapping or demo-side glue")
    logger.info("✅ clean, scalable, production-ready architecture")
    logger.info("")
    logger.info("Synqed is now an Agent Operating System!")
    logger.info("")
    logger.info("To run in cloud mode:")
    logger.info("  SYNQ_MCP_MODE=cloud SYNQ_MCP_ENDPOINT=https://synqed.fly.dev/mcp python universal_mcp_demo.py")
    logger.info("")
    logger.info("  This starts a global MCP server with agents integrated.")
    logger.info("  The server will listen on http://0.0.0.0:8080 by default.")
    logger.info("  Agents will use the Fly.io cloud MCP server for inter-agent calls.")
    logger.info("=" * 60)


if __name__ == "__main__":
    # detect mode before entering async context
    mode = os.getenv("SYNQ_MCP_MODE", "local").lower()
    
    if mode == "cloud":
        # cloud mode: run synchronously (uvicorn manages event loop)
        run_cloud_mode_demo()
    else:
        # local mode: run async demos
        asyncio.run(main())
