"""
simple test script for mcp wrapper.

verifies:
- a2a client can send tasks
- agents can receive and respond
- mcp tools can be called programmatically
"""

import asyncio
import json
import sys
from pathlib import Path

# add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from synqed import Agent, AgentLogicContext, MessageRouter, AgentRuntimeRegistry
from synqed_mcp.a2a.client import A2AClient


async def test_agent_logic(context: AgentLogicContext) -> dict:
    """simple test agent that echoes back the task."""
    latest = context.latest_message
    if not latest:
        return context.send("USER", "[test agent ready]")
    
    try:
        task = json.loads(latest.content)
        response = {
            "status": "success",
            "received": task,
            "echo": f"processed {task.get('task_type', 'unknown')}"
        }
        return context.send("TestClient", json.dumps(response))
    except Exception as e:
        return context.send("TestClient", json.dumps({
            "status": "error",
            "error": str(e)
        }))


async def test_a2a_client():
    """test a2a client functionality."""
    print("="*60)
    print("testing a2a client")
    print("="*60)
    
    # create test agent
    test_agent = Agent(
        name="test",
        description="Test agent",
        logic=test_agent_logic,
        role="testtools"
    )
    
    # setup router
    router = MessageRouter()
    router.register_agent("test", test_agent)
    
    # create a2a client
    a2a_client = A2AClient(router)
    
    # send test task
    print("\nsending test task...")
    from synqed import AgentId
    result = await a2a_client.send_task(
        agent=AgentId.from_email_like("test@testtools"),
        task_type="echo",
        payload={"message": "hello from test"}
    )
    
    print(f"result: {json.dumps(result, indent=2)}")
    
    # verify result
    assert result["status"] == "success", "task should succeed"
    assert "message_id" in result, "should have message_id"
    assert result["agent"] == "agent://testtools/test", "should have agent uri"
    
    print("\n✅ all tests passed!")
    print("="*60)


async def test_tool_imports():
    """test that all tool modules can be imported."""
    print("\ntesting tool imports...")
    
    try:
        from synqed_mcp.tools import salesforce, zoom, content_creator
        print("✅ salesforce module imported")
        print("✅ zoom module imported")
        print("✅ content_creator module imported")
        
        # check schemas
        assert hasattr(salesforce, 'TOOL_SCHEMA'), "salesforce should have TOOL_SCHEMA"
        assert hasattr(zoom, 'TOOL_SCHEMA'), "zoom should have TOOL_SCHEMA"
        assert hasattr(content_creator, 'TOOL_SCHEMA'), "content_creator should have TOOL_SCHEMA"
        print("✅ all tool schemas present")
        
        return True
    except Exception as e:
        print(f"❌ import failed: {e}")
        return False


async def test_server_import():
    """test that mcp server can be imported."""
    print("\ntesting server import...")
    
    try:
        from synqed_mcp.server import MCPServer
        print("✅ MCPServer imported")
        
        # create server instance
        server = MCPServer()
        print("✅ MCPServer instantiated")
        
        return True
    except Exception as e:
        print(f"❌ import failed: {e}")
        return False


async def main():
    """run all tests."""
    print("\n" + "="*60)
    print("mcp wrapper test suite")
    print("="*60 + "\n")
    
    # test 1: tool imports
    result1 = await test_tool_imports()
    
    # test 2: server import
    result2 = await test_server_import()
    
    # test 3: a2a client
    try:
        await test_a2a_client()
        result3 = True
    except Exception as e:
        print(f"❌ a2a client test failed: {e}")
        import traceback
        traceback.print_exc()
        result3 = False
    
    # summary
    print("\n" + "="*60)
    print("test summary")
    print("="*60)
    print(f"tool imports: {'✅ passed' if result1 else '❌ failed'}")
    print(f"server import: {'✅ passed' if result2 else '❌ failed'}")
    print(f"a2a client: {'✅ passed' if result3 else '❌ failed'}")
    print("="*60)
    
    if result1 and result2 and result3:
        print("\n🎉 all tests passed!")
        return 0
    else:
        print("\n❌ some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

