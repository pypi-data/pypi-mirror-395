"""
CI Test for synqed_client.py example - Client connection to agent

This test verifies client can connect and communicate with an agent.
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_client_ask():
    """Test client.ask() method for complete responses."""
    
    # Create mock agent
    async def test_logic(context):
        message = context.get_user_input()
        return f"Response to: {message}"
    
    agent = synqed.Agent(
        name="Test Agent",
        description="Test agent",
        capabilities=["test"],
        logic=test_logic
    )
    
    # Start server in background
    server = synqed.AgentServer(agent, host="127.0.0.1", port=8901)
    await server.start_background()
    
    # Wait for server to be ready
    await asyncio.sleep(1)
    
    try:
        # Test client connection and ask()
        async with synqed.Client("http://127.0.0.1:8901") as client:
            response = await client.ask("What are 3 best practices?")
            
            # Verify response
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
            
        print("✅ Client ask() test passed!")
    
    finally:
        # Cleanup
        await server.stop()
        await asyncio.sleep(0.5)


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_client_stream():
    """Test client.stream() method for streaming responses."""
    
    # Create mock agent that returns multi-part response
    async def stream_logic(context):
        message = context.get_user_input()
        return f"Streaming response to: {message}"
    
    agent = synqed.Agent(
        name="Stream Agent",
        description="Streaming test agent",
        capabilities=["streaming"],
        logic=stream_logic
    )
    
    # Start server in background
    server = synqed.AgentServer(agent, host="127.0.0.1", port=8902)
    await server.start_background()
    
    # Wait for server to be ready
    await asyncio.sleep(1)
    
    try:
        # Test client streaming
        async with synqed.Client("http://127.0.0.1:8902") as client:
            chunks = []
            async for chunk in client.stream("Tell me a story"):
                chunks.append(chunk)
            
            # Verify we got chunks
            assert len(chunks) > 0
            
            # Verify chunks combine to full response
            full_response = "".join(chunks)
            assert len(full_response) > 0
            
        print("✅ Client stream() test passed!")
    
    finally:
        # Cleanup
        await server.stop()
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(test_client_ask())
    asyncio.run(test_client_stream())

