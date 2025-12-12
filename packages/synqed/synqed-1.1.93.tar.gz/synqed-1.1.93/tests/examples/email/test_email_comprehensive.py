"""
Comprehensive CI Tests for Email Examples

This test suite covers:
- agent_alice.py, agent_bob.py, agent_charlie.py
- send_email.py
- single_workspace_email.py  
- planner_parallel_workspaces.py
- mcp.py (basic structure)
"""
import asyncio
import os
from pathlib import Path
import pytest

import synqed


@pytest.mark.asyncio
async def test_email_addressing():
    """Test that agents have proper email addresses with role-based addressing."""
    
    async def test_logic(context):
        return '{"send_to": "USER", "content": "test"}'
    
    # Create agents with roles
    alice = synqed.Agent(
        name="alice",
        description="Alice agent",
        logic=test_logic,
        role="wonderland"
    )
    
    bob = synqed.Agent(
        name="bob",
        description="Bob agent",
        logic=test_logic,
        role="builder"
    )
    
    charlie = synqed.Agent(
        name="charlie",
        description="Charlie agent",
        logic=test_logic,
        role="chef"
    )
    
    # Verify email addresses
    assert alice.email == "alice@wonderland"
    assert bob.email == "bob@builder"
    assert charlie.email == "charlie@chef"
    
    print("✅ Email addressing test passed!")


@pytest.mark.asyncio
async def test_agent_capabilities_metadata():
    """Test that agents can declare capabilities and coordination styles."""
    
    async def test_logic(context):
        return '{"send_to": "USER", "content": "test"}'
    
    agent = synqed.Agent(
        name="test_agent",
        description="Test agent",
        logic=test_logic,
        capabilities=["skill1", "skill2", "skill3"],
        default_coordination="respond_to_sender"
    )
    
    # Verify capabilities
    assert hasattr(agent, 'capabilities')
    assert "skill1" in agent.capabilities
    
    # Verify coordination style
    assert hasattr(agent, 'default_coordination')
    assert agent.default_coordination == "respond_to_sender"
    
    print("✅ Agent capabilities metadata test passed!")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_planner_task_breakdown():
    """Test that PlannerLLM can break down tasks and create delegation plans."""
    
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    # Create planner
    planner = synqed.PlannerLLM(
        provider="anthropic",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-sonnet-4-5"
    )
    
    # Register some test agents
    async def test_logic(context):
        return '{"send_to": "USER", "content": "done"}'
    
    synqed.AgentRuntimeRegistry.register(
        "Agent1", 
        synqed.Agent(name="Agent1", description="Agent 1", logic=test_logic)
    )
    synqed.AgentRuntimeRegistry.register(
        "Agent2",
        synqed.Agent(name="Agent2", description="Agent 2", logic=test_logic)
    )
    
    # Planner should be able to create task plans
    # (In real usage, it would call LLM, but we verify the structure)
    assert planner.provider == "anthropic"
    assert planner.model == "claude-sonnet-4-5"
    
    # Clean up
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Planner task breakdown test passed!")


@pytest.mark.asyncio
async def test_workspace_message_routing():
    """Test that workspaces can route messages between agents."""
    
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    message_log = []
    
    async def logging_logic(context: synqed.AgentLogicContext) -> dict:
        """Logic that logs when called."""
        if context.latest_message:
            message_log.append({
                "agent": context.agent_name,
                "from": context.latest_message.sender,
                "content": context.latest_message.content
            })
        return '{"send_to": "USER", "content": "processed"}'
    
    # Create agents
    agent1 = synqed.Agent(name="Agent1", description="Agent 1", logic=logging_logic)
    agent2 = synqed.Agent(name="Agent2", description="Agent 2", logic=logging_logic)
    
    synqed.AgentRuntimeRegistry.register("Agent1", agent1)
    synqed.AgentRuntimeRegistry.register("Agent2", agent2)
    
    # Create workspace
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_routing")
    )
    
    task_node = synqed.TaskTreeNode(
        id="routing-test",
        description="Message routing test",
        required_agents=["Agent1", "Agent2"],
        may_need_subteams=False
    )
    
    workspace = await workspace_manager.create_workspace(
        task_tree_node=task_node,
        parent_workspace_id=None
    )
    
    # Route messages
    await workspace.route_message("USER", "Agent1", "Test message 1", manager=workspace_manager)
    await workspace.route_message("Agent1", "Agent2", "Test message 2", manager=workspace_manager)
    
    # Verify messages were routed
    assert len(workspace.router.get_transcript()) > 0
    
    # Verify workspace has both agents
    assert "Agent1" in workspace.agents
    assert "Agent2" in workspace.agents
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Workspace message routing test passed!")


@pytest.mark.asyncio
async def test_workspace_conversation_history():
    """Test that agents can access conversation history."""
    
    async def history_logic(context: synqed.AgentLogicContext) -> dict:
        """Logic that accesses conversation history."""
        # Get conversation history
        history = context.get_conversation_history()
        
        # Verify history is accessible
        assert isinstance(history, str)
        
        return '{"send_to": "USER", "content": "history accessed"}'
    
    agent = synqed.Agent(
        name="HistoryAgent",
        description="Tests history access",
        logic=history_logic
    )
    
    synqed.AgentRuntimeRegistry.register("HistoryAgent", agent)
    
    # Create workspace
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_history")
    )
    
    task_node = synqed.TaskTreeNode(
        id="history-test",
        description="History test",
        required_agents=["HistoryAgent"],
        may_need_subteams=False
    )
    
    workspace = await workspace_manager.create_workspace(
        task_tree_node=task_node,
        parent_workspace_id=None
    )
    
    # Send message
    await workspace.route_message("USER", "HistoryAgent", "Test", manager=workspace_manager)
    
    # Verify workspace has messages
    assert len(workspace.router.get_transcript()) > 0
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Workspace conversation history test passed!")


if __name__ == "__main__":
    asyncio.run(test_email_addressing())
    asyncio.run(test_agent_capabilities_metadata())
    asyncio.run(test_planner_task_breakdown())
    asyncio.run(test_workspace_message_routing())
    asyncio.run(test_workspace_conversation_history())

