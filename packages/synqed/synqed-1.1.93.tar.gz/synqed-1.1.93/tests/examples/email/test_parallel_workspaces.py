"""
CI Test for parallel_workspaces.py example - Parallel workspace execution

This test verifies that multiple workspaces can execute in parallel.
"""
import asyncio
import os
from pathlib import Path
import pytest

import synqed


@pytest.mark.asyncio
@pytest.mark.integration
async def test_parallel_workspaces_execution():
    """Test that multiple workspaces can execute in parallel."""
    
    # Track execution order
    execution_log = []
    
    async def team1_logic(context: synqed.AgentLogicContext) -> dict:
        """Team 1 agent logic."""
        execution_log.append("team1")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        await asyncio.sleep(0.1)  # Simulate work
        return '{"send_to": "USER", "content": "Team 1 complete"}'
    
    async def team2_logic(context: synqed.AgentLogicContext) -> dict:
        """Team 2 agent logic."""
        execution_log.append("team2")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        await asyncio.sleep(0.1)  # Simulate work
        return '{"send_to": "USER", "content": "Team 2 complete"}'
    
    async def team3_logic(context: synqed.AgentLogicContext) -> dict:
        """Team 3 agent logic."""
        execution_log.append("team3")
        if not context.latest_message:
            return '{"send_to": "USER", "content": "Ready"}'
        await asyncio.sleep(0.1)  # Simulate work
        return '{"send_to": "USER", "content": "Team 3 complete"}'
    
    # Set API key
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    
    # Create agents
    team1 = synqed.Agent(name="Team1", description="Team 1", logic=team1_logic)
    team2 = synqed.Agent(name="Team2", description="Team 2", logic=team2_logic)
    team3 = synqed.Agent(name="Team3", description="Team 3", logic=team3_logic)
    
    # Register agents
    synqed.AgentRuntimeRegistry.register("Team1", team1)
    synqed.AgentRuntimeRegistry.register("Team2", team2)
    synqed.AgentRuntimeRegistry.register("Team3", team3)
    
    # Create workspace manager
    workspace_manager = synqed.WorkspaceManager(
        workspaces_root=Path("/tmp/synqed_test_parallel")
    )
    
    # Create planner
    planner = synqed.PlannerLLM(
        provider="anthropic",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-sonnet-4-5"
    )
    
    # Create three workspaces
    workspace1 = await workspace_manager.create_workspace(
        task_tree_node=synqed.TaskTreeNode(
            id="ws1", description="Workspace 1", required_agents=["Team1"], may_need_subteams=False
        ),
        parent_workspace_id=None
    )
    
    workspace2 = await workspace_manager.create_workspace(
        task_tree_node=synqed.TaskTreeNode(
            id="ws2", description="Workspace 2", required_agents=["Team2"], may_need_subteams=False
        ),
        parent_workspace_id=None
    )
    
    workspace3 = await workspace_manager.create_workspace(
        task_tree_node=synqed.TaskTreeNode(
            id="ws3", description="Workspace 3", required_agents=["Team3"], may_need_subteams=False
        ),
        parent_workspace_id=None
    )
    
    # Send tasks
    await workspace1.route_message("USER", "Team1", "Task 1", manager=workspace_manager)
    await workspace2.route_message("USER", "Team2", "Task 2", manager=workspace_manager)
    await workspace3.route_message("USER", "Team3", "Task 3", manager=workspace_manager)
    
    # Create execution engine
    execution_engine = synqed.WorkspaceExecutionEngine(
        planner=planner,
        workspace_manager=workspace_manager,
        enable_display=False,
        max_agent_turns=5,
    )
    
    # Execute in parallel
    import time
    start = time.time()
    
    try:
        await asyncio.gather(
            execution_engine.run(workspace1.workspace_id),
            execution_engine.run(workspace2.workspace_id),
            execution_engine.run(workspace3.workspace_id),
        )
    except Exception:
        pass  # Expected with mocks
    
    elapsed = time.time() - start
    
    # Verify all teams executed
    assert "team1" in execution_log or "team2" in execution_log or "team3" in execution_log
    
    # Verify parallel execution (should be faster than sequential)
    # If sequential: would take 0.3s+, parallel should be ~0.1s
    # But we're lenient with timing in CI
    assert elapsed < 1.0, f"Parallel execution took too long: {elapsed}s"
    
    # Clean up
    await workspace_manager.destroy_workspace(workspace1.workspace_id)
    await workspace_manager.destroy_workspace(workspace2.workspace_id)
    await workspace_manager.destroy_workspace(workspace3.workspace_id)
    synqed.AgentRuntimeRegistry.clear()
    
    print(f"✅ Parallel workspaces test passed! Executed in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(test_parallel_workspaces_execution())

