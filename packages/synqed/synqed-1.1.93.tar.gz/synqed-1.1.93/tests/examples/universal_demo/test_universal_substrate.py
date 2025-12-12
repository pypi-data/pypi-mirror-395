"""
CI Test for universal_substrate_demo.py and client_a2a_agent.py examples

This test verifies the universal substrate integration and A2A agent capabilities.
"""
import asyncio
import os
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_universal_substrate_agent_creation():
    """Test that agents can be created with universal substrate compatibility."""
    
    async def substrate_logic(context: synqed.AgentLogicContext) -> dict:
        """Agent logic compatible with universal substrate."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        
        user_input = context.get_user_input()
        return f'{{"send_to": "USER", "content": "Processed: {user_input}"}}'
    
    # Create agent
    agent = synqed.Agent(
        name="UniversalAgent",
        description="Agent compatible with universal substrate",
        logic=substrate_logic,
        capabilities=["universal", "substrate", "a2a"]
    )
    
    # Verify agent properties
    assert agent.name == "UniversalAgent"
    assert "universal" in agent.skills
    assert "substrate" in agent.skills
    assert "a2a" in agent.skills
    
    print("✅ Universal substrate agent creation test passed!")


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_a2a_protocol_compatibility():
    """Test that agents are compatible with A2A protocol."""
    
    async def a2a_logic(context: synqed.AgentLogicContext) -> dict:
        """Agent logic that follows A2A protocol."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        
        # A2A-compatible response structure
        return {
            "send_to": "USER",
            "content": "Response following A2A protocol"
        }
    
    # Create A2A-compatible agent
    agent = synqed.Agent(
        name="A2AAgent",
        description="Agent following A2A protocol",
        logic=a2a_logic,
        version="1.0.0"
    )
    
    # Verify agent structure
    assert agent.name == "A2AAgent"
    assert agent.description == "Agent following A2A protocol"
    assert agent.version == "1.0.0"
    
    # Create mock context
    from a2a.server.agent_execution import RequestContext
    mock_request = type('obj', (object,), {'message': 'test'})()
    context = RequestContext(mock_request)
    
    # Call agent logic
    result = await agent.executor(context)
    
    # Verify result structure
    assert isinstance(result, (dict, str))
    
    print("✅ A2A protocol compatibility test passed!")


@pytest.mark.asyncio
async def test_client_a2a_agent_server():
    """Test that A2A agents can be served via AgentServer."""
    
    async def server_logic(context):
        """Simple server logic."""
        return "Server response"
    
    # Create agent
    agent = synqed.Agent(
        name="ServerAgent",
        description="Agent for server testing",
        logic=server_logic,
        capabilities=["server", "a2a"]
    )
    
    # Create server (don't start to avoid port binding)
    server = synqed.AgentServer(agent, port=9998)
    
    # Verify server properties
    assert server.agent == agent
    assert server.port == 9998
    
    print("✅ Client A2A agent server test passed!")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_universal_mcp_integration_structure():
    """Test that universal MCP integration structure is correct."""
    
    # This test verifies the structure without actually connecting to MCP
    # Real MCP tests are in the MCP examples
    
    async def mcp_aware_logic(context: synqed.AgentLogicContext) -> dict:
        """Logic that could potentially use MCP tools."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        
        # In real usage, agent would access MCP tools via context
        # For testing, we just verify the structure
        return '{"send_to": "USER", "content": "MCP-aware agent responding"}'
    
    agent = synqed.Agent(
        name="MCPAwareAgent",
        description="Agent that could use MCP tools",
        logic=mcp_aware_logic,
        capabilities=["mcp_tools"]
    )
    
    # Verify agent has capabilities
    assert hasattr(agent, 'capabilities')
    assert "mcp_tools" in agent.capabilities
    
    print("✅ Universal MCP integration structure test passed!")


if __name__ == "__main__":
    asyncio.run(test_universal_substrate_agent_creation())
    asyncio.run(test_a2a_protocol_compatibility())
    asyncio.run(test_client_a2a_agent_server())
    asyncio.run(test_universal_mcp_integration_structure())

