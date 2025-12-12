"""
Tests for AgentMemory class.
"""

import pytest
from synqed.memory import AgentMemory, InboxMessage


@pytest.mark.skip(reason="Inbox tests require API updates")
class TestAgentMemory:
    """Tests for the AgentMemory class."""
    
    def test_memory_initialization(self):
        """Test creating a new memory instance."""
        memory = AgentMemory(agent_name="TestAgent")
        
        assert memory.agent_name == "TestAgent"
        assert len(memory.messages) == 0
    
    def test_add_message(self):
        """Test adding a message to memory."""
        memory = AgentMemory(agent_name="TestAgent")
        
        memory.add_message(from_agent="Sender", content="Hello!")
        
        assert len(memory.messages) == 1
        assert memory.messages[0].from_agent == "Sender"
        assert memory.messages[0].content == "Hello!"
        assert memory.messages[0].timestamp is not None
    
    def test_get_messages(self):
        """Test retrieving all messages."""
        memory = AgentMemory(agent_name="TestAgent")
        
        memory.add_message(from_agent="Agent1", content="Message 1")
        memory.add_message(from_agent="Agent2", content="Message 2")
        
        messages = memory.get_messages()
        assert len(messages) == 2
        assert messages[0].content == "Message 1"
        assert messages[1].content == "Message 2"
        
        # Verify it returns a copy
        messages.append(InboxMessage(from_agent="Test", content="Test"))
        assert len(memory.messages) == 2  # Original unchanged
    
    def test_get_latest_message(self):
        """Test retrieving the latest message."""
        memory = AgentMemory(agent_name="TestAgent")
        
        # No messages
        assert memory.get_latest_message() is None
        
        # Add messages
        memory.add_message(from_agent="Agent1", content="First")
        memory.add_message(from_agent="Agent2", content="Second")
        
        latest = memory.get_latest_message()
        assert latest is not None
        assert latest.content == "Second"
        assert latest.from_agent == "Agent2"
    
    def test_clear(self):
        """Test clearing all messages."""
        memory = AgentMemory(agent_name="TestAgent")
        
        memory.add_message(from_agent="Agent1", content="Message 1")
        memory.add_message(from_agent="Agent2", content="Message 2")
        
        assert len(memory.messages) == 2
        
        memory.clear()
        
        assert len(memory.messages) == 0
        assert memory.get_latest_message() is None
