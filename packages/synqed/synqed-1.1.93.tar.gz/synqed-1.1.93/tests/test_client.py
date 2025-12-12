"""
Unit tests for the Client class.
"""

import pytest
from synqed.client import Client
from a2a.types import AgentCard


class TestClient:
    """Tests for the Client class."""
    
    def test_client_creation_with_url(self):
        """Test creating client with URL."""
        client = Client(agent_url="http://localhost:8000")
        
        assert client.agent_url == "http://localhost:8000"
        assert client.streaming is True
        assert client.timeout == 30.0
    
    def test_client_creation_with_card(self):
        """Test creating client with agent card."""
        card = AgentCard(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000",
            skills=[],
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            capabilities={}
        )
        
        client = Client(agent_card=card)
        
        assert client._agent_card == card
    
    def test_client_creation_without_url_or_card(self):
        """Test that creating client without URL or card raises error."""
        with pytest.raises(ValueError, match="Either agent_url or agent_card"):
            Client()
    
    def test_client_repr(self):
        """Test client string representation."""
        client = Client(agent_url="http://localhost:8000")
        
        repr_str = repr(client)
        
        assert "Client" in repr_str
        assert "http://localhost:8000" in repr_str
    
    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Test client as async context manager."""
        async with Client(agent_url="http://localhost:8000") as client:
            assert client is not None
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires agent card endpoint implementation")
    async def test_client_send_message(self, simple_server):
        """Test sending a message to an agent."""
        client = Client(agent_url=simple_server.url)
        
        responses = []
        async for response in client.stream("Hello"):
            responses.append(response)
        
        # Should get at least one response
        assert len(responses) > 0
        
        # Response should contain echo
        full_response = "".join(responses)
        assert "Echo" in full_response or "Hello" in full_response
        
        await client.close()
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires agent card endpoint implementation")
    async def test_client_ask(self, simple_server):
        """Test sending message and waiting for complete response."""
        client = Client(agent_url=simple_server.url)
        
        response = await client.ask("Test message")
        
        assert isinstance(response, str)
        assert len(response) > 0
        
        await client.close()
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires agent card endpoint implementation")
    async def test_client_multiple_messages(self, simple_server):
        """Test sending multiple messages."""
        async with Client(agent_url=simple_server.url) as client:
            response1 = await client.ask("First message")
            response2 = await client.ask("Second message")
            
            assert response1 != response2
            assert "First" in response1 or "message" in response1
            assert "Second" in response2 or "message" in response2
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires agent card endpoint implementation")
    async def test_client_with_custom_timeout(self, simple_server):
        """Test client with custom timeout."""
        client = Client(
            agent_url=simple_server.url,
            timeout=10.0
        )
        
        assert client.timeout == 10.0
        
        response = await client.ask("Test")
        assert isinstance(response, str)
        
        await client.close()
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires agent card endpoint implementation")
    async def test_client_streaming_disabled(self, simple_server):
        """Test client with streaming disabled."""
        client = Client(
            agent_url=simple_server.url,
            streaming=False
        )
        
        assert client.streaming is False
        
        response = await client.ask("Test")
        assert isinstance(response, str)
        
        await client.close()

