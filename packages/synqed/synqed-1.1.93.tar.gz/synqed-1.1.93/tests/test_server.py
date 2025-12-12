"""
Unit tests for the AgentServer class.
"""

import pytest
import asyncio
from synqed import Agent, AgentServer


@pytest.mark.skip(reason="Server API has changed")
class TestAgentServer:
    """Tests for the AgentServer class."""
    
    def test_server_creation(self, simple_agent):
        """Test creating a server."""
        server = AgentServer(simple_agent, host="127.0.0.1", port=8200)
        
        assert server.agent == simple_agent
        assert server.host == "127.0.0.1"
        assert server.port == 8200
        assert server.is_running is False
    
    def test_server_url_property(self, simple_agent):
        """Test server URL property."""
        server = AgentServer(simple_agent, host="127.0.0.1", port=8201)
        
        assert server.url == "http://127.0.0.1:8201"
    
    def test_server_updates_agent_url(self, simple_agent):
        """Test that server updates the agent's URL."""
        original_url = simple_agent.url
        
        server = AgentServer(simple_agent, host="127.0.0.1", port=8202)
        
        # Agent URL should be updated to match server
        assert simple_agent.url != original_url
        assert simple_agent.url == "http://127.0.0.1:8202"
    
    def test_server_get_card(self, simple_agent):
        """Test getting agent card from server."""
        server = AgentServer(simple_agent, host="127.0.0.1", port=8203)
        
        card = server.get_card()
        
        assert card.name == simple_agent.name
        assert card.url == server.url
    
    @pytest.mark.asyncio
    async def test_server_start_background(self, simple_agent, port_generator):
        """Test starting server in background."""
        port = port_generator()
        server = AgentServer(simple_agent, host="127.0.0.1", port=port)
        
        assert server.is_running is False
        
        await server.start_background()
        
        # Give server time to start
        await asyncio.sleep(1)
        
        assert server.is_running is True
        
        # Cleanup
        await server.stop()
        assert server.is_running is False
    
    @pytest.mark.asyncio
    async def test_server_stop(self, simple_agent, port_generator):
        """Test stopping the server."""
        port = port_generator()
        server = AgentServer(simple_agent, host="127.0.0.1", port=port)
        
        await server.start_background()
        await asyncio.sleep(1)
        
        assert server.is_running is True
        
        await server.stop()
        
        assert server.is_running is False
    
    @pytest.mark.asyncio
    async def test_server_double_start_warning(self, simple_agent, port_generator):
        """Test that starting server twice shows warning."""
        port = port_generator()
        server = AgentServer(simple_agent, host="127.0.0.1", port=port)
        
        await server.start_background()
        await asyncio.sleep(1)
        
        # Try to start again - should log warning but not fail
        await server.start_background()
        
        await server.stop()
    
    @pytest.mark.asyncio
    async def test_server_stop_when_not_running(self, simple_agent):
        """Test stopping server that's not running."""
        server = AgentServer(simple_agent, host="127.0.0.1", port=8204)
        
        # Should not raise error
        await server.stop()
    
    def test_server_repr(self, simple_agent):
        """Test server string representation."""
        server = AgentServer(simple_agent, host="127.0.0.1", port=8205)
        
        repr_str = repr(server)
        
        assert "AgentServer" in repr_str
        assert simple_agent.name in repr_str
        assert "stopped" in repr_str
    
    @pytest.mark.asyncio
    async def test_server_custom_path_prefix(self, simple_agent, port_generator):
        """Test server with custom path prefix."""
        port = port_generator()
        server = AgentServer(
            simple_agent,
            host="127.0.0.1",
            port=port,
            path_prefix="/api"
        )
        
        assert server.url == f"http://127.0.0.1:{port}/api"
        assert simple_agent.url == server.url

