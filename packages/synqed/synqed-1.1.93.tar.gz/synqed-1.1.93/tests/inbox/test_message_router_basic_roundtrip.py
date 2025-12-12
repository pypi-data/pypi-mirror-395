"""
Tests for MessageRouter basic roundtrip functionality.
"""

import pytest
from synqed.router import MessageRouter


@pytest.mark.skip(reason="Inbox tests require API updates")
class TestMessageRouterBasicRoundtrip:
    """Tests for MessageRouter basic functionality."""
    
    def test_router_initialization(self):
        """Test creating a new router."""
        router = MessageRouter()
        
        assert router.timeout == 30.0
        assert len(router.list_agents()) == 0
    
    def test_register_agent(self):
        """Test registering an agent."""
        router = MessageRouter()
        
        router.register_agent("Agent1", "http://localhost:8001")
        
        assert "Agent1" in router.list_agents()
        assert len(router.list_agents()) == 1
    
    def test_unregister_agent(self):
        """Test unregistering an agent."""
        router = MessageRouter()
        
        router.register_agent("Agent1", "http://localhost:8001")
        router.register_agent("Agent2", "http://localhost:8002")
        
        assert len(router.list_agents()) == 2
        
        router.unregister_agent("Agent1")
        
        assert "Agent1" not in router.list_agents()
        assert "Agent2" in router.list_agents()
        assert len(router.list_agents()) == 1
    
    def test_register_multiple_agents(self):
        """Test registering multiple agents."""
        router = MessageRouter()
        
        router.register_agent("Agent1", "http://localhost:8001")
        router.register_agent("Agent2", "http://localhost:8002")
        router.register_agent("Agent3", "http://localhost:8003")
        
        agents = router.list_agents()
        assert len(agents) == 3
        assert "Agent1" in agents
        assert "Agent2" in agents
        assert "Agent3" in agents
    
    def test_transcript_management(self):
        """Test transcript recording and retrieval."""
        router = MessageRouter()
        
        # Initially empty
        assert len(router.get_transcript()) == 0
        
        # Manually add to transcript (simulating route_message)
        router._transcript.append({
            "from": "Agent1",
            "to": "Agent2",
            "content": "Test message"
        })
        
        transcript = router.get_transcript()
        assert len(transcript) == 1
        assert transcript[0]["from"] == "Agent1"
        assert transcript[0]["to"] == "Agent2"
        
        # Clear transcript
        router.clear_transcript()
        assert len(router.get_transcript()) == 0
    
    def test_router_repr(self):
        """Test router string representation."""
        router = MessageRouter()
        router.register_agent("Agent1", "http://localhost:8001")
        
        repr_str = repr(router)
        assert "MessageRouter" in repr_str
        assert "agents=1" in repr_str
