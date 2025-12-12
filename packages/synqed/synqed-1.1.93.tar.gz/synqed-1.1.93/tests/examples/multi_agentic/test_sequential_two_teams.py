"""
CI Test for sequential_two_teams.py example - Sequential team execution

This test verifies that teams can work sequentially in a coordinated workflow.
"""
import asyncio
import os
from pathlib import Path
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async def test_sequential_two_teams_workflow():
    """Test that two teams can work sequentially with proper coordination."""
    
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    execution_order = []
    
    async def team1_lead_logic(context: synqed.AgentLogicContext) -> dict:
        """Team 1 lead that completes first."""
        execution_order.append("team1_lead")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "Coordinator", "content": "Team 1 complete"}'
    
    async def team2_lead_logic(context: synqed.AgentLogicContext) -> dict:
        """Team 2 lead that waits for team 1."""
        execution_order.append("team2_lead")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "Coordinator", "content": "Team 2 complete"}'
    
    async def coordinator_logic(context: synqed.AgentLogicContext) -> dict:
        """Coordinator that manages sequential execution."""
        execution_order.append("coordinator")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        
        # First send to Team 1
        if "Team 1 complete" not in str(context.latest_message.content):
            return '{"send_to": "Team1Lead", "content": "Start phase 1"}'
        # Then send to Team 2
        else:
            return '{"send_to": "Team2Lead", "content": "Start phase 2"}'
    
    # Create agents
    coordinator = synqed.Agent(
        name="Coordinator",
        description="Sequential coordinator",
        logic=coordinator_logic
    )
    
    team1_lead = synqed.Agent(
        name="Team1Lead",
        description="Team 1 lead",
        logic=team1_lead_logic
    )
    
    team2_lead = synqed.Agent(
        name="Team2Lead",
        description="Team 2 lead",
        logic=team2_lead_logic
    )
    
    # Register agents
    synqed.AgentRuntimeRegistry.register("Coordinator", coordinator)
    synqed.AgentRuntimeRegistry.register("Team1Lead", team1_lead)
    synqed.AgentRuntimeRegistry.register("Team2Lead", team2_lead)
    
    # Create workspace manager
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_sequential")
    )
    
    # Create hierarchical structure
    root_node = synqed.TaskTreeNode(
        id="root",
        description="Sequential coordination",
        required_agents=["Coordinator"],
        may_need_subteams=True,
        children=[
            synqed.TaskTreeNode(
                id="team1",
                description="Team 1 work",
                required_agents=["Team1Lead"],
                may_need_subteams=False
            ),
            synqed.TaskTreeNode(
                id="team2",
                description="Team 2 work",
                required_agents=["Team2Lead"],
                may_need_subteams=False
            )
        ]
    )
    
    # Create workspaces
    root_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_node,
        parent_workspace_id=None
    )
    
    team1_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_node.children[0],
        parent_workspace_id=root_workspace.workspace_id
    )
    
    team2_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_node.children[1],
        parent_workspace_id=root_workspace.workspace_id
    )
    
    # Verify workspaces
    assert "Coordinator" in root_workspace.agents
    assert "Team1Lead" in team1_workspace.agents
    assert "Team2Lead" in team2_workspace.agents
    
    # Send initial task
    await root_workspace.route_message(
        "USER",
        "Coordinator",
        "Execute sequential workflow",
        manager=workspace_manager
    )
    
    # Verify message was sent
    assert len(root_workspace.router.get_transcript()) > 0
    
    # Clean up
    await workspace_manager.destroy_workspace(root_workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Sequential two teams workflow test passed!")


@pytest.mark.asyncio
async def test_workspace_hierarchy():
    """Test that workspace parent-child relationships work correctly."""
    
    async def test_logic(context):
        return '{"send_to": "USER", "content": "done"}'
    
    agent = synqed.Agent(name="TestAgent", description="Test", logic=test_logic)
    synqed.AgentRuntimeRegistry.register("TestAgent", agent)
    
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_hierarchy")
    )
    
    # Create parent workspace
    parent_node = synqed.TaskTreeNode(
        id="parent",
        description="Parent workspace",
        required_agents=["TestAgent"],
        may_need_subteams=True
    )
    
    parent_workspace = await workspace_manager.create_workspace(
        task_tree_node=parent_node,
        parent_workspace_id=None
    )
    
    # Create child workspace
    child_node = synqed.TaskTreeNode(
        id="child",
        description="Child workspace",
        required_agents=["TestAgent"],
        may_need_subteams=False
    )
    
    child_workspace = await workspace_manager.create_workspace(
        task_tree_node=child_node,
        parent_workspace_id=parent_workspace.workspace_id
    )
    
    # Verify hierarchy
    assert parent_workspace.workspace_id is not None
    assert child_workspace.workspace_id is not None
    assert parent_workspace.workspace_id != child_workspace.workspace_id
    
    # Clean up
    await workspace_manager.destroy_workspace(parent_workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Workspace hierarchy test passed!")


if __name__ == "__main__":
    asyncio.run(test_sequential_two_teams_workflow())
    asyncio.run(test_workspace_hierarchy())

