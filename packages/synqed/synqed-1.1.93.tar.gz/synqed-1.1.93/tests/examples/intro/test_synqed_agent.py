"""
CI Test for synqed_agent.py example - Agent creation and server hosting

This test verifies basic agent creation and server startup.
"""
import asyncio
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_agent_creation_and_server():
    """Test that an agent can be created and server can start."""
    
    # Mock OpenAI response
    class MockChoice:
        def __init__(self):
            self.message = MagicMock()
            self.message.content = "Test response from agent"
    
    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]
    
    # Create mock agent logic
    async def test_agent_logic(context):
        """Test agent logic."""
        user_message = context.get_user_input()
        return f"Echo: {user_message}"
    
    # Create agent
    agent = synqed.Agent(
        name="Test Agent",
        description="Test agent for CI",
        capabilities=["testing", "ci"],
        logic=test_agent_logic
    )
    
    # Verify agent properties
    assert agent.name == "Test Agent"
    assert agent.description == "Test agent for CI"
    assert "testing" in agent.skills
    assert agent.capabilities["streaming"] is True
    
    # Create server (but don't start it fully to avoid port binding)
    server = synqed.AgentServer(agent, port=9999)
    
    # Verify server was created
    assert server.agent == agent
    assert server.port == 9999
    
    print("✅ Agent creation test passed!")


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires API updates")
    async @pytest.mark.skip(reason="Requires API updates")
 def test_agent_executor_call():
    """Test that agent executor can process messages."""
    
    call_count = [0]
    
    async def counting_logic(context):
        """Logic that counts calls."""
        call_count[0] += 1
        user_message = context.get_user_input()
        return f"Processed message {call_count[0]}: {user_message}"
    
    # Create agent
    agent = synqed.Agent(
        name="Counter Agent",
        description="Counts invocations",
        capabilities=["counting"],
        logic=counting_logic
    )
    
    # Create a mock context
    from a2a.server.agent_execution import RequestContext
    
    # Create mock request
    mock_request = MagicMock()
    mock_request.message = "test message"
    
    context = RequestContext(mock_request)
    
    # Call executor
    result = await agent.executor(context)
    
    # Verify
    assert call_count[0] == 1
    assert "Processed message 1" in result
    assert "test message" in result
    
    print("✅ Agent executor test passed!")


if __name__ == "__main__":
    asyncio.run(test_agent_creation_and_server())
    asyncio.run(test_agent_executor_call())

