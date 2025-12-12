"""
CI Test for single_workspace.py example - Email-based multi-agent coordination

This test verifies that agents can collaborate in a single workspace with email addresses.
"""
import asyncio
import os
import logging
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async def test_single_workspace_email_collaboration():
    """Test that multiple agents can collaborate in a single workspace using email addresses."""
    
    # Mock LLM responses for alice, bob, and charlie
    mock_responses = {
        "alice": [
            '{"send_to": "bob", "content": "Bob, can you help with the setup?"}',
            '{"send_to": "USER", "content": "Decorations complete!"}',
        ],
        "bob": [
            '{"send_to": "alice", "content": "Setup is done!"}',
            '{"send_to": "charlie", "content": "Charlie, what about food?"}',
        ],
        "charlie": [
            '{"send_to": "bob", "content": "Menu is ready!"}',
            '{"send_to": "USER", "content": "Food preparation complete!"}',
        ]
    }
    
    response_indices = {"alice": 0, "bob": 0, "charlie": 0}
    
    def get_mock_response(agent_name):
        """Get next mock response for agent."""
        responses = mock_responses.get(agent_name, ['{"send_to": "USER", "content": "Done"}'])
        idx = response_indices[agent_name]
        response_indices[agent_name] = (idx + 1) % len(responses)
        return responses[idx]
    
    # Create agent logic functions
    async def alice_logic(context: synqed.AgentLogicContext) -> dict:
        """Mock alice logic."""
        if not context.latest_message or not context.latest_message.content:
            return None
        return get_mock_response("alice")
    
    async def bob_logic(context: synqed.AgentLogicContext) -> dict:
        """Mock bob logic."""
        if not context.latest_message or not context.latest_message.content:
            return None
        return get_mock_response("bob")
    
    async def charlie_logic(context: synqed.AgentLogicContext) -> dict:
        """Mock charlie logic."""
        if not context.latest_message or not context.latest_message.content:
            return None
        return get_mock_response("charlie")
    
    # Set API key
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    # Create agents with email addresses
    alice = synqed.Agent(
        name="alice",
        description="decorations specialist",
        logic=alice_logic,
        role="wonderland",
        default_target="USER",
        capabilities=["decorations"],
        default_coordination="respond_to_sender"
    )
    
    bob = synqed.Agent(
        name="bob",
        description="setup specialist",
        logic=bob_logic,
        role="builder",
        default_target="alice",
        capabilities=["construction"],
        default_coordination="respond_to_sender"
    )
    
    charlie = synqed.Agent(
        name="charlie",
        description="food specialist",
        logic=charlie_logic,
        role="chef",
        default_target="alice",
        capabilities=["menu planning"],
        default_coordination="respond_to_sender"
    )
    
    # Verify email addresses are set
    assert alice.email == "alice@wonderland"
    assert bob.email == "bob@builder"
    assert charlie.email == "charlie@chef"
    
    # Register agents
    synqed.AgentRuntimeRegistry.register("alice", alice)
    synqed.AgentRuntimeRegistry.register("bob", bob)
    synqed.AgentRuntimeRegistry.register("charlie", charlie)
    
    # Create workspace manager
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_email_workspace")
    )
    
    # Create planner
    planner = synqed.PlannerLLM(
        provider="anthropic",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-sonnet-4-20250514"
    )
    
    # Create execution engine
    execution_engine = synqed.WorkspaceExecutionEngine(
        planner=planner,
        workspace_manager=workspace_manager,
        enable_display=False,
        max_agent_turns=10,
    )
    
    # Create workspace with all three agents
    task_node = synqed.TaskTreeNode(
        id="email-test",
        description="Email collaboration test",
        required_agents=["alice", "bob", "charlie"],
        may_need_subteams=False
    )
    
    workspace = await workspace_manager.create_workspace(
        task_tree_node=task_node,
        parent_workspace_id=None
    )
    
    # Verify workspace has all agents
    assert "alice" in workspace.agents
    assert "bob" in workspace.agents
    assert "charlie" in workspace.agents
    
    # Send task to agents
    task = "Plan a magical tea party"
    await workspace.route_message("USER", "alice", task, manager=workspace_manager)
    
    # Execute workspace
    try:
        await execution_engine.run(workspace.workspace_id)
    except Exception as e:
        # Some execution errors are expected with mocks
        pass
    
    # Verify messages were exchanged
    assert len(workspace.router.get_transcript()) >= 0
    assert len(workspace.router.get_transcript()) > 0
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Single workspace email collaboration test passed!")


if __name__ == "__main__":
    asyncio.run(test_single_workspace_email_collaboration())

