"""
Unit tests for the Agent class.
"""

import pytest
from synqed import Agent


class TestAgent:
    """Tests for the Agent class."""
    
    def test_agent_creation_with_simple_capabilities(self):
        """Test creating an agent with simple string capabilities."""
        agent = Agent(
            name="Test Agent",
            description="A test agent",
            capabilities=["skill1", "skill2", "skill3"]
        )
        
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert len(agent.capabilities) == 3
    
    def test_agent_creation_with_logic(self):
        """Test creating an agent with custom logic."""
        async def custom_logic(context):
            return "custom response"
        
        agent = Agent(
            name="Logic Agent",
            description="Has custom logic",
            logic=custom_logic
        )
        
        assert agent.name == "Logic Agent"
        assert agent.logic == custom_logic
    
    def test_agent_creation_with_default_target(self):
        """Test creating an agent with a default target."""
        agent = Agent(
            name="Test Agent",
            description="Test description",
            default_target="OtherAgent"
        )
        
        assert agent.name == "Test Agent"
        assert agent.default_target == "OtherAgent"
    
    def test_agent_with_role(self):
        """Test creating an agent with a role for email capabilities."""
        agent = Agent(
            name="alice",
            description="Alice's agent",
            role="wonderland"
        )
        
        assert agent.name == "alice"
        assert agent.role == "wonderland"
        assert agent.email == "alice@wonderland"
        assert agent.agent_id == "agent://wonderland/alice"
    
    def test_agent_with_memory(self):
        """Test that agent has memory."""
        agent = Agent(
            name="Memory Agent",
            description="Has memory"
        )
        
        assert agent.memory is not None
        assert agent.memory.agent_name == "Memory Agent"
    
    def test_agent_with_capabilities(self):
        """Test agent with custom capabilities."""
        agent = Agent(
            name="Advanced Agent",
            description="Has capabilities",
            capabilities=["analysis", "reporting"]
        )
        
        assert agent.capabilities is not None
        assert len(agent.capabilities) == 2
    
    def test_agent_with_custom_coordination(self):
        """Test agent with custom coordination style."""
        agent = Agent(
            name="Coordinator",
            description="Custom coordinator",
            default_coordination="broadcast"
        )
        
        assert agent.default_coordination == "broadcast"
    
    def test_agent_repr(self):
        """Test agent string representation."""
        agent = Agent(
            name="Test Agent",
            description="Test description",
            capabilities=["test"]
        )
        
        repr_str = repr(agent)
        assert "Agent" in repr_str or "Test Agent" in repr_str
    
    @pytest.mark.asyncio
    async def test_agent_logic_callable(self):
        """Test that agent logic is assigned correctly."""
        call_count = [0]
        
        async def counting_logic(context):
            call_count[0] += 1
            return "response"
        
        agent = Agent(
            name="Test Agent",
            description="Test",
            logic=counting_logic
        )
        
        # Logic should be assigned
        assert agent.logic == counting_logic
    
    def test_agent_without_logic_has_default(self):
        """Test that agent without logic gets a default no-op logic."""
        agent = Agent(
            name="Default Agent",
            description="Uses default logic"
        )
        
        assert agent.logic is not None
    
    def test_agent_logic_must_be_async(self):
        """Test that non-async logic raises an error."""
        def sync_logic(context):
            return "sync"
        
        with pytest.raises(ValueError, match="async function"):
            Agent(
                name="Bad Agent",
                description="Has sync logic",
                logic=sync_logic
            )
