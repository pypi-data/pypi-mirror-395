"""
Tests for Agent response generation.
"""

import pytest
from synqed.agent import Agent, AgentLogicContext, ResponseBuilder
from synqed.memory import AgentMemory


@pytest.mark.skip(reason="Inbox tests require API updates")
class TestAgentResponse:
    """Tests for Agent response generation."""
    
    @pytest.mark.asyncio
    async def test_agent_with_dict_response(self):
        """Test agent that returns a dict response."""
        async def simple_logic(context: AgentLogicContext) -> dict:
            return context.build_response("Target", "Hello!")
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=simple_logic
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "Target"
        assert response["content"] == "Hello!"
    
    @pytest.mark.asyncio
    async def test_agent_with_string_response(self):
        """Test agent that returns a string (should be wrapped)."""
        async def string_logic(context: AgentLogicContext) -> str:
            return "Just a string"
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=string_logic,
            default_target="DefaultTarget"
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "DefaultTarget"
        assert response["content"] == "Just a string"
    
    @pytest.mark.asyncio
    async def test_agent_with_memory_access(self):
        """Test agent accessing its memory."""
        memory = AgentMemory(agent_name="TestAgent")
        memory.add_message(from_agent="Sender", content="Hello!")
        
        async def memory_logic(context: AgentLogicContext) -> dict:
            latest = context.latest_message
            if latest:
                return context.build_response("Sender", f"Received: {latest.content}")
            return context.build_response("Unknown", "No messages")
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=memory_logic,
            memory=memory
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "Sender"
        assert "Received: Hello!" in response["content"]
    
    @pytest.mark.asyncio
    async def test_agent_with_response_builder(self):
        """Test agent using ResponseBuilder."""
        async def builder_logic(context: AgentLogicContext) -> dict:
            return context.response.send_to("Target").content("Built response").build()
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=builder_logic
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "Target"
        assert response["content"] == "Built response"
    
    @pytest.mark.asyncio
    async def test_agent_with_invalid_json_string(self):
        """Test agent returning invalid JSON string."""
        async def invalid_logic(context: AgentLogicContext) -> str:
            return "Not JSON at all"
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=invalid_logic,
            default_target="Default"
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "Default"
        assert response["content"] == "Not JSON at all"
    
    @pytest.mark.asyncio
    async def test_agent_with_partial_dict(self):
        """Test agent returning dict missing required fields."""
        async def partial_logic(context: AgentLogicContext) -> dict:
            return {"content": "Missing send_to"}
        
        agent = Agent(
            name="TestAgent",
            description="Test",
            logic=partial_logic,
            default_target="Default"
        )
        
        response = await agent.process()
        
        assert response["send_to"] == "Default"
        assert "content" in response


@pytest.mark.skip(reason="Inbox tests require API updates")
class TestResponseBuilder:
    """Tests for ResponseBuilder helper class."""
    
    def test_builder_chaining(self):
        """Test method chaining on ResponseBuilder."""
        builder = ResponseBuilder()
        result = builder.send_to("Target").content("Message").build()
        
        assert result["send_to"] == "Target"
        assert result["content"] == "Message"
    
    def test_builder_to_json(self):
        """Test converting builder to JSON."""
        builder = ResponseBuilder()
        json_str = builder.send_to("Target").content("Message").to_json()
        
        import json
        parsed = json.loads(json_str)
        assert parsed["send_to"] == "Target"
        assert parsed["content"] == "Message"
    
    def test_builder_missing_send_to(self):
        """Test builder error when send_to is missing."""
        builder = ResponseBuilder()
        builder.content("Message")
        
        with pytest.raises(ValueError, match="send_to"):
            builder.build()
    
    def test_builder_missing_content(self):
        """Test builder error when content is missing."""
        builder = ResponseBuilder()
        builder.send_to("Target")
        
        with pytest.raises(ValueError, match="content"):
            builder.build()
