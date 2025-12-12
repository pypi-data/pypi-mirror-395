"""
CI Test for dynamic_agents_email.py example - Dynamic agent creation

This test verifies that agents can be created dynamically at runtime.
"""
import asyncio
import os
from pathlib import Path
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_dynamic_agent_creation():
    """Test that agents can be created dynamically based on task requirements."""
    
    async def dynamic_logic(context: synqed.AgentLogicContext) -> dict:
        """Dynamic agent logic."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "USER", "content": "Task complete"}'
    
    # Set API key
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    # Initially no agents registered
    synqed.AgentRuntimeRegistry.clear()
    assert len(synqed.AgentRuntimeRegistry) == 0
    
    # Dynamically create and register agents
    agent_names = ["DynamicAgent1", "DynamicAgent2", "DynamicAgent3"]
    
    for name in agent_names:
        agent = synqed.Agent(
            name=name,
            description=f"Dynamically created {name}",
            logic=dynamic_logic
        )
        synqed.AgentRuntimeRegistry.register(name, agent)
    
    # Verify agents were registered
    assert len(synqed.AgentRuntimeRegistry) == 3
    for name in agent_names:
        assert name in synqed.AgentRuntimeRegistry
    
    # Create workspace with dynamically created agents
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_dynamic")
    )
    
    task_node = synqed.TaskTreeNode(
        id="dynamic-test",
        description="Dynamic agent test",
        required_agents=agent_names,
        may_need_subteams=False
    )
    
    workspace = await workspace_manager.create_workspace(
        task_tree_node=task_node,
        parent_workspace_id=None
    )
    
    # Verify all agents are in workspace
    for name in agent_names:
        assert name in workspace.agents
    
    # Send task
    await workspace.route_message("USER", "DynamicAgent1", "Test task", manager=workspace_manager)
    
    # Verify message was routed
    assert len(workspace.router.get_transcript()) > 0
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Dynamic agent creation test passed!")


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires API updates")
    async @pytest.mark.skip(reason="Requires API updates")
 def test_agent_registry_operations():
    """Test agent registry operations."""
    
    async def test_logic(context):
        return "test"
    
    # Clear registry
    synqed.AgentRuntimeRegistry.clear()
    
    # Register agent
    agent1 = synqed.Agent(name="TestAgent1", description="Test 1", logic=test_logic)
    synqed.AgentRuntimeRegistry.register("TestAgent1", agent1)
    
    # Verify registration
    assert "TestAgent1" in synqed.AgentRuntimeRegistry
    retrieved = synqed.AgentRuntimeRegistry.get("TestAgent1")
    assert retrieved == agent1
    
    # Register multiple agents
    agent2 = synqed.Agent(name="TestAgent2", description="Test 2", logic=test_logic)
    agent3 = synqed.Agent(name="TestAgent3", description="Test 3", logic=test_logic)
    synqed.AgentRuntimeRegistry.register("TestAgent2", agent2)
    synqed.AgentRuntimeRegistry.register("TestAgent3", agent3)
    
    # Verify all registered
    assert len(synqed.AgentRuntimeRegistry) == 3
    
    # Clean up
    synqed.AgentRuntimeRegistry.clear()
    assert len(synqed.AgentRuntimeRegistry) == 0
    
    print("✅ Agent registry operations test passed!")


if __name__ == "__main__":
    asyncio.run(test_dynamic_agent_creation())
    asyncio.run(test_agent_registry_operations())

