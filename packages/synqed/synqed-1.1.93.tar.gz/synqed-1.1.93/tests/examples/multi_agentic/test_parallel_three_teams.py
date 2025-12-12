"""
CI Test for parallel_three_teams.py example - Parallel team execution

This test verifies that multiple teams can work in parallel with hierarchical workspaces.
"""
import asyncio
import os
from pathlib import Path
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async @pytest.mark.skip(reason="Requires API updates")
 def test_parallel_three_teams_structure():
    """Test that parallel team structure can be created with coordinator and sub-teams."""
    
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    # Create mock logic for different roles
    async def coordinator_logic(context: synqed.AgentLogicContext) -> dict:
        """Coordinator that broadcasts to team leads."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        # Broadcast to all team leads
        return '{"send_to": ["AILead", "ClimateLead", "SpaceLead"], "content": "Research your topic"}'
    
    async def lead_logic(context: synqed.AgentLogicContext) -> dict:
        """Lead that delegates to senior."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "USER", "content": "Research complete"}'
    
    async def senior_logic(context: synqed.AgentLogicContext) -> dict:
        """Senior that collaborates with junior."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "USER", "content": "Senior work done"}'
    
    async def junior_logic(context: synqed.AgentLogicContext) -> dict:
        """Junior that assists senior."""
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        return '{"send_to": "USER", "content": "Junior work done"}'
    
    # Create coordinator
    coordinator = synqed.Agent(
        name="Coordinator",
        description="Research coordinator",
        logic=coordinator_logic
    )
    
    # Create AI Team (3 agents)
    ai_lead = synqed.Agent(
        name="AILead",
        description="AI research lead",
        logic=lead_logic
    )
    ai_senior = synqed.Agent(
        name="AISenior",
        description="AI senior researcher",
        logic=senior_logic
    )
    ai_junior = synqed.Agent(
        name="AIJunior",
        description="AI junior researcher",
        logic=junior_logic
    )
    
    # Create Climate Team (3 agents)
    climate_lead = synqed.Agent(
        name="ClimateLead",
        description="Climate research lead",
        logic=lead_logic
    )
    climate_senior = synqed.Agent(
        name="ClimateSenior",
        description="Climate senior researcher",
        logic=senior_logic
    )
    climate_junior = synqed.Agent(
        name="ClimateJunior",
        description="Climate junior researcher",
        logic=junior_logic
    )
    
    # Create Space Team (3 agents)
    space_lead = synqed.Agent(
        name="SpaceLead",
        description="Space research lead",
        logic=lead_logic
    )
    space_senior = synqed.Agent(
        name="SpaceSenior",
        description="Space senior researcher",
        logic=senior_logic
    )
    space_junior = synqed.Agent(
        name="SpaceJunior",
        description="Space junior researcher",
        logic=junior_logic
    )
    
    # Register all 10 agents
    agents = [
        coordinator,
        ai_lead, ai_senior, ai_junior,
        climate_lead, climate_senior, climate_junior,
        space_lead, space_senior, space_junior
    ]
    
    for agent in agents:
        synqed.AgentRuntimeRegistry.register(agent.name, agent)
    
    # Verify all agents registered
    assert len(synqed.AgentRuntimeRegistry) == 10
    
    # Create workspace manager
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_parallel_teams")
    )
    
    # Create hierarchical task structure
    root_task_node = synqed.TaskTreeNode(
        id="root",
        description="Coordinate research",
        required_agents=["Coordinator"],
        may_need_subteams=True,
        children=[
            synqed.TaskTreeNode(
                id="ai-team",
                description="AI research",
                required_agents=["AILead", "AISenior", "AIJunior"],
                may_need_subteams=False
            ),
            synqed.TaskTreeNode(
                id="climate-team",
                description="Climate research",
                required_agents=["ClimateLead", "ClimateSenior", "ClimateJunior"],
                may_need_subteams=False
            ),
            synqed.TaskTreeNode(
                id="space-team",
                description="Space research",
                required_agents=["SpaceLead", "SpaceSenior", "SpaceJunior"],
                may_need_subteams=False
            )
        ]
    )
    
    # Create root workspace
    root_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_task_node,
        parent_workspace_id=None
    )
    
    # Verify root workspace
    assert "Coordinator" in root_workspace.agents
    assert root_workspace.workspace_id is not None
    
    # Create child workspaces
    ai_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_task_node.children[0],
        parent_workspace_id=root_workspace.workspace_id
    )
    
    climate_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_task_node.children[1],
        parent_workspace_id=root_workspace.workspace_id
    )
    
    space_workspace = await workspace_manager.create_workspace(
        task_tree_node=root_task_node.children[2],
        parent_workspace_id=root_workspace.workspace_id
    )
    
    # Verify all workspaces created
    assert ai_workspace.workspace_id is not None
    assert climate_workspace.workspace_id is not None
    assert space_workspace.workspace_id is not None
    
    # Verify agents in each workspace
    assert "AILead" in ai_workspace.agents
    assert "ClimateLead" in climate_workspace.agents
    assert "SpaceLead" in space_workspace.agents
    
    # Clean up
    await workspace_manager.destroy_workspace(root_workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Parallel three teams structure test passed!")


@pytest.mark.asyncio
async def test_broadcast_delegation():
    """Test that coordinator can broadcast to multiple agents."""
    
    received_messages = []
    
    async def receiver_logic(context: synqed.AgentLogicContext) -> dict:
        """Logic that records received messages."""
        if context.latest_message:
            received_messages.append({
                "agent": context.agent_name,
                "from": context.latest_message.sender,
                "content": context.latest_message.content
            })
        return '{"send_to": "USER", "content": "received"}'
    
    # Create agents
    agent1 = synqed.Agent(name="Agent1", description="Agent 1", logic=receiver_logic)
    agent2 = synqed.Agent(name="Agent2", description="Agent 2", logic=receiver_logic)
    agent3 = synqed.Agent(name="Agent3", description="Agent 3", logic=receiver_logic)
    
    synqed.AgentRuntimeRegistry.register("Agent1", agent1)
    synqed.AgentRuntimeRegistry.register("Agent2", agent2)
    synqed.AgentRuntimeRegistry.register("Agent3", agent3)
    
    # Create workspace
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_broadcast")
    )
    
    task_node = synqed.TaskTreeNode(
        id="broadcast-test",
        description="Broadcast test",
        required_agents=["Agent1", "Agent2", "Agent3"],
        may_need_subteams=False
    )
    
    workspace = await workspace_manager.create_workspace(
        task_tree_node=task_node,
        parent_workspace_id=None
    )
    
    # Send broadcast message (to all agents)
    for agent_name in ["Agent1", "Agent2", "Agent3"]:
        await workspace.route_message(
            "Coordinator",
            agent_name,
            "Broadcast message",
            manager=workspace_manager
        )
    
    # Verify messages were routed
    assert len(workspace.router.get_transcript()) >= 3
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print("✅ Broadcast delegation test passed!")


if __name__ == "__main__":
    asyncio.run(test_parallel_three_teams_structure())
    asyncio.run(test_broadcast_delegation())

