"""
test script to verify cloud mode agent registration.

this script tests the global agent registration flow:
1. checks if cloud server is running
2. creates agents and registers them
3. verifies registration succeeded

usage:
    # terminal 1: start cloud server
    python -m synqed_mcp
    
    # terminal 2: run this test
    SYNQ_MCP_MODE=cloud SYNQ_MCP_ENDPOINT=http://localhost:8080 python test_cloud_registration.py
"""

import asyncio
import logging
import os
import sys

import httpx

from synqed import Agent, AgentId, MessageRouter
from synqed_mcp.a2a.client import A2AClient
from synqed_mcp.integrate.injector import create_mcp_middleware

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def simple_agent_logic(context):
    """simple test agent logic."""
    return context.send("test", "ok")


async def test_cloud_server_running(endpoint: str) -> bool:
    """check if cloud server is running."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ cloud server running: {data}")
                return True
            else:
                logger.error(f"cloud server returned status {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"failed to connect to cloud server: {e}")
        return False


async def test_agent_registration():
    """test agent registration with cloud server."""
    
    # check environment
    mode = os.getenv("SYNQ_MCP_MODE", "local")
    endpoint = os.getenv("SYNQ_MCP_ENDPOINT")
    
    logger.info("=" * 60)
    logger.info("CLOUD AGENT REGISTRATION TEST")
    logger.info("=" * 60)
    logger.info(f"MODE: {mode}")
    logger.info(f"ENDPOINT: {endpoint}")
    logger.info("=" * 60)
    logger.info("")
    
    if mode != "cloud":
        logger.error("SYNQ_MCP_MODE must be set to 'cloud'")
        return False
    
    if not endpoint:
        logger.error("SYNQ_MCP_ENDPOINT must be set")
        return False
    
    # check if server is running
    logger.info("step 1: checking if cloud server is running...")
    if not await test_cloud_server_running(endpoint):
        logger.error("cloud server not running. start it with: python -m synqed_mcp")
        return False
    logger.info("")
    
    # create test agents
    logger.info("step 2: creating test agents...")
    test_agent_1 = Agent(name="test_agent_1", role="tools", logic=simple_agent_logic)
    test_agent_2 = Agent(name="test_agent_2", role="tools", logic=simple_agent_logic)
    logger.info("✅ created 2 test agents")
    logger.info("")
    
    # create router and a2a client
    logger.info("step 3: creating router...")
    router = MessageRouter()
    a2a_client = A2AClient(router, workspace_id="test_workspace")
    router.register_agent("test_agent_1", test_agent_1)
    router.register_agent("test_agent_2", test_agent_2)
    logger.info("✅ router configured")
    logger.info("")
    
    # attach mcp middleware (this should trigger cloud registration)
    logger.info("step 4: attaching mcp middleware (cloud mode)...")
    mcp_middleware = create_mcp_middleware(router, a2a_client, mode="cloud")
    mcp_middleware.attach(test_agent_1)
    mcp_middleware.attach(test_agent_2)
    logger.info("✅ mcp capability attached")
    logger.info("")
    
    # wait for registration to complete
    logger.info("step 5: waiting for cloud registration...")
    await asyncio.sleep(3)
    logger.info("")
    
    # verify registration
    logger.info("step 6: verifying registration...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{endpoint}/mcp/agents", timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            registered_agents = {agent["name"] for agent in data.get("agents", [])}
            logger.info(f"registered agents on server: {registered_agents}")
            
            if "test_agent_1" in registered_agents and "test_agent_2" in registered_agents:
                logger.info("✅ both agents registered successfully!")
                
                # show details
                for agent in data.get("agents", []):
                    if agent["name"].startswith("test_agent"):
                        logger.info(f"  - {agent['agent_uri']}: {len(agent['tools'])} tools")
                
                logger.info("")
                logger.info("=" * 60)
                logger.info("✅ CLOUD REGISTRATION TEST PASSED")
                logger.info("=" * 60)
                return True
            else:
                logger.error(f"agents not found. expected: {{test_agent_1, test_agent_2}}, got: {registered_agents}")
                return False
    
    except Exception as e:
        logger.error(f"failed to verify registration: {e}")
        return False


async def main():
    """main test runner."""
    success = await test_agent_registration()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

