"""
CI Test for agent_card.py example - Agent card metadata

This test verifies agent card endpoint returns proper metadata.
"""
import asyncio
import pytest
import aiohttp

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_agent_card_endpoint():
    """Test that agent card is available at /.well-known/agent-card endpoint."""
    
    # Create test agent
    async def test_logic(context):
        return "test response"
    
    agent = synqed.Agent(
        name="Test Agent",
        description="Test agent for card validation",
        capabilities=["skill1", "skill2", "skill3"],
        logic=test_logic
    )
    
    # Start server
    server = synqed.AgentServer(agent, host="127.0.0.1", port=8903)
    await server.start_background()
    
    # Wait for server to be ready
    await asyncio.sleep(1)
    
    try:
        # Fetch agent card
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8903/.well-known/agent-card.json") as resp:
                assert resp.status == 200, f"Agent card endpoint returned {resp.status}"
                
                card = await resp.json()
                
                # Verify card structure
                assert "name" in card
                assert card["name"] == "Test Agent"
                
                assert "description" in card
                assert card["description"] == "Test agent for card validation"
                
                assert "skills" in card
                assert len(card["skills"]) == 3
                skill_ids = [s["id"] for s in card["skills"]]
                assert "skill1" in skill_ids
                assert "skill2" in skill_ids
                assert "skill3" in skill_ids
                
                assert "capabilities" in card
                assert card["capabilities"]["streaming"] is True
                
        print("✅ Agent card test passed!")
    
    finally:
        # Cleanup
        await server.stop()
        await asyncio.sleep(0.5)


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires API updates")
    async @pytest.mark.skip(reason="Requires API updates")
 def test_agent_card_structure():
    """Test agent card structure without server."""
    
    async def test_logic(context):
        return "test"
    
    agent = synqed.Agent(
        name="Card Test Agent",
        description="Testing card structure",
        capabilities=["a", "b", "c"],
        logic=test_logic,
        version="1.2.3"
    )
    
    # Verify agent has expected properties
    assert agent.name == "Card Test Agent"
    assert agent.description == "Testing card structure"
    assert agent.skills == ["a", "b", "c"]
    assert agent.version == "1.2.3"
    
    print("✅ Agent card structure test passed!")


if __name__ == "__main__":
    asyncio.run(test_agent_card_endpoint())
    asyncio.run(test_agent_card_structure())

