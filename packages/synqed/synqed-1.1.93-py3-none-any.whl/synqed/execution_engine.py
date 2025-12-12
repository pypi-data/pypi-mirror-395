"""
WorkspaceExecutionEngine - Production-hard execution engine for multi-agent workspaces.

This module provides the WorkspaceExecutionEngine class that:
- Executes agents using event-driven scheduling with deterministic message IDs
- Prevents dropped messages through ID-based matching
- Enforces recursion safety (max workspaces, depth limits, per-agent throttling)
- Protects against infinite loops and unbounded execution
- Validates agent outputs strictly
- Maintains complete transcripts for debugging
"""

from __future__ import annotations

import json
import logging
import asyncio
from typing import Any, Optional
from datetime import datetime

from synqed.agent import AgentLogicContext
from synqed.memory import InboxMessage, AgentMemory
from synqed.workspace_manager import Workspace, WorkspaceManager, AgentRuntimeRegistry
from synqed.planner import PlannerLLM
from synqed.planner_agent import PlannerAgent
from synqed.scheduler import EventScheduler, AgentEvent
from synqed.display import MessageDisplay

logger = logging.getLogger(__name__)


def infer_turn_type(message_content: str) -> str:
    """
    Infer the turn type from a message based on heuristics.
    
    This helps classify agent actions into categories:
    - delegation: Agent is delegating work to another agent
    - finalization: Agent is providing a final result
    - proposal: Agent is proposing a solution or idea
    - coordination: Agent is coordinating with others
    - challenge: Agent is challenging another agent's reasoning
    
    Args:
        message_content: The content of the message
        
    Returns:
        Turn type string (delegation, finalization, proposal, coordination, challenge)
    """
    content_lower = message_content.lower()
    
    # Check for challenge keywords (new for Deep Reasoning Protocol)
    if any(word in content_lower for word in ["challenge", "disagree", "question", "concern about", "why do you assume", "what about"]):
        return "challenge"
    
    # Check for delegation keywords
    if any(word in content_lower for word in ["delegate", "please handle", "can you", "could you", "need your help"]):
        return "delegation"
    
    # Check for finalization keywords
    if any(word in content_lower for word in ["final", "complete", "done", "finished", "ready for user", "here is the result"]):
        return "finalization"
    
    # Check for coordination keywords
    if any(word in content_lower for word in ["coordinate", "collaborate", "work together", "let's", "we should"]):
        return "coordination"
    
    # Default to proposal
    return "proposal"


class Context(AgentLogicContext):
    """
    Context object passed to agent logic functions during workspace execution.
    
    Extends AgentLogicContext with workspace-specific information and event details.
    """
    
    def __init__(
        self,
        agent_name: str,
        workspace: Workspace,
        workspace_id: str,
        messages: list[InboxMessage],
        memory: AgentMemory,
        default_target: Optional[str] = None,
        event_trigger: Optional[str] = None,
        event_payload: Optional[dict] = None,
        shared_plan: Optional[str] = None,
    ):
        """Initialize the context."""
        super().__init__(
            memory=memory, 
            default_target=default_target,
            workspace=workspace,
            agent_name=agent_name,
            shared_plan=shared_plan
        )
        self.agent_name = agent_name
        self.workspace = workspace
        self.workspace_id = workspace_id
        self.messages = messages
        self.event_trigger = event_trigger
        self.event_payload = event_payload or {}
    
    def build_response(self, target: str, content: str) -> dict[str, str]:
        """Build a response dictionary. Delegates to parent AgentLogicContext.build_response."""
        return super().build_response(target, content)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Context(agent='{self.agent_name}', workspace='{self.workspace_id}', messages={len(self.messages)})"


class WorkspaceExecutionEngine:
    """
    Production-hard execution engine for multi-agent workspaces.
    
    Features:
    - Deterministic message processing with unique IDs
    - Zero dropped messages through ID-based matching
    - Recursion safety (max workspaces, depth limits, throttling)
    - Event loop protection (max events per workspace/cycle)
    - Infinite loop detection and prevention
    - Strict agent output validation
    - Complete transcript tracking
    """
    
    def __init__(
        self,
        planner: PlannerLLM,
        workspace_manager: WorkspaceManager,
        enable_display: bool = True,
        max_cycles: int = 20,
        max_events_per_cycle: int = 50,
        max_events_per_workspace: int = 2000,
        max_agent_turns: Optional[int] = None,
        max_total_workspaces: int = 50,
        max_workspace_depth: int = 8,
        max_subteam_requests_per_agent: int = 3,
        fatal_cycle_threshold: int = 5,
        mcp_middleware: Optional[Any] = None,
        on_deliverable: Optional[Any] = None,
    ):
        """
        Initialize the workspace execution engine.
        
        Args:
            planner: PlannerLLM instance for creating subteam subtrees
            workspace_manager: WorkspaceManager instance for workspace operations
            enable_display: Whether to enable real-time message display (default: True)
            max_cycles: Maximum number of event processing cycles per workspace (default: 20)
            max_events_per_cycle: Maximum events to process in a single cycle (default: 50)
            max_events_per_workspace: Maximum total events per workspace (default: 2000)
            max_agent_turns: Maximum number of agent responses/turns before stopping (default: None = unlimited)
            max_total_workspaces: Maximum total workspaces that can be created (default: 50)
            max_workspace_depth: Maximum nesting depth for workspaces (default: 8)
            max_subteam_requests_per_agent: Maximum subteam requests per agent (default: 3)
            fatal_cycle_threshold: Cycles with no output before killing workspace (default: 5)
            mcp_middleware: Optional MCP middleware to attach to all workspace agents (default: None)
            on_deliverable: Optional callback for when a deliverable is produced.
                           Called with (workspace_id, title, content, agent_name)
        """
        self.planner = planner
        self.workspace_manager = workspace_manager
        self.mcp_middleware = mcp_middleware
        self._workspace_schedulers: dict[str, EventScheduler] = {}  # Track schedulers for all workspaces
        self._total_workspaces_created = 0
        
        # Configurable execution limits
        self.max_cycles = max_cycles
        self.max_events_per_cycle = max_events_per_cycle
        self.max_events_per_workspace = max_events_per_workspace
        self.max_agent_turns = max_agent_turns
        self.max_total_workspaces = max_total_workspaces
        self.max_workspace_depth = max_workspace_depth
        self.max_subteam_requests_per_agent = max_subteam_requests_per_agent
        self.fatal_cycle_threshold = fatal_cycle_threshold
        
        # Global workspace execution queue for asynchronous hierarchical execution
        self.global_workspace_queue: asyncio.Queue[str] = asyncio.Queue()
        # Track which workspaces are currently executing to prevent re-entry
        self._running_workspaces: set[str] = set()
        # Track which workspaces are queued to prevent duplicate scheduling
        self._queued_workspaces: set[str] = set()
        # Track which agent requested each child workspace (child_id -> requesting_agent_name)
        self._subteam_requesters: dict[str, str] = {}
        # Real-time message display
        self.display = MessageDisplay() if enable_display else None
        # Track active agent for display
        self._active_agent: Optional[str] = None
        # Deliverable callback - called when PlannerLLM produces a deliberate deliverable
        self._on_deliverable = on_deliverable
    
    def _attach_mcp_to_workspace(self, workspace: Any) -> None:
        """
        Attach MCP middleware to all agents in a workspace.
        
        This is called after workspace creation to ensure all agent instances
        (which are deep copied) have MCP capabilities attached.
        
        Args:
            workspace: Workspace instance containing agents
        """
        if not self.mcp_middleware:
            return
        
        # Attach MCP to all agents in the workspace
        for agent_name, agent in workspace.agents.items():
            try:
                self.mcp_middleware.attach(agent)
            except Exception as e:
                logger.error(f"Failed to attach MCP middleware to {agent_name}: {e}")
    
    def schedule_workspace(self, workspace_id: str) -> None:
        """
        Schedule a workspace for execution in the global queue.
        
        This method enqueues a workspace ID for later execution. Workspaces
        cannot be enqueued if they are already running OR already in the queue.
        
        Args:
            workspace_id: ID of workspace to schedule
        """
        workspace = self.workspace_manager.get_workspace(workspace_id)
        
        # Prevent re-entry: skip if already running
        if workspace.is_running or workspace_id in self._running_workspaces:
            logger.debug(f"Workspace {workspace_id} is already running, skipping enqueue")
            return
        
        # FIX: Check if workspace is already in the queue to prevent duplicate scheduling
        # This prevents the same workspace from being queued multiple times before execution
        if workspace_id in self._queued_workspaces:
            logger.debug(f"Workspace {workspace_id} is already queued, skipping duplicate enqueue")
            return
        
        # Enqueue for execution
        self._queued_workspaces.add(workspace_id)
        self.global_workspace_queue.put_nowait(workspace_id)
        logger.debug(f"Scheduled workspace {workspace_id} for execution")
    
    async def run_global_scheduler(self) -> None:
        """
        Process all workspaces in the global execution queue IN PARALLEL.
        
        This method continuously processes workspaces from the queue until
        the queue is empty. Workspaces run concurrently using asyncio.gather,
        allowing true parallel execution. Workspaces may schedule child workspaces
        during execution, which will be processed in subsequent iterations.
        """
        # Continue processing until queue is empty
        # New workspaces may be scheduled during execution
        processed_count = 0
        max_iterations = 1000  # Safety limit to prevent infinite loops
        
        for iteration in range(max_iterations):
            if self.global_workspace_queue.empty():
                break
            
            # Collect all workspaces currently in queue
            batch_size = self.global_workspace_queue.qsize()
            workspace_ids = []
            for _ in range(batch_size):
                try:
                    workspace_id = self.global_workspace_queue.get_nowait()
                    workspace_ids.append(workspace_id)
                except asyncio.QueueEmpty:
                    break
            
            if workspace_ids:
                logger.debug(f"Running {len(workspace_ids)} workspaces in parallel: {workspace_ids}")
                
                # FIX: Remove workspaces from queued set before running
                # This allows them to be re-queued later if needed
                for wid in workspace_ids:
                    self._queued_workspaces.discard(wid)
                
                # Run all workspaces in this batch CONCURRENTLY
                tasks = [self.run_workspace(workspace_id=wid) for wid in workspace_ids]
                try:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    processed_count += len(workspace_ids)
                except Exception as e:
                    logger.error(f"Error in parallel workspace execution: {e}")
    
    async def distribute_task_to_workspaces(
        self,
        task_plan: Any,  # TaskTreePlan
        user_task: str,
        root_workspace_id: str,
        use_planner_agent: bool = True,
    ) -> None:
        """
        Automatically distribute the user task to agents in workspaces based on task plan.
        
        When use_planner_agent=True, tasks are sent from "planner" (the PlannerAgent/CEO).
        Execution agents respond to "planner", NOT "USER".
        
        This method handles the initial task distribution:
        - If there are child workspaces, sends subtasks to the first agent in each
        - If no child workspaces, sends the full task to the first agent in root workspace
        
        Args:
            task_plan: TaskTreePlan with workspace hierarchy
            user_task: The original user task description
            root_workspace_id: ID of the root workspace
            use_planner_agent: If True, send tasks from "planner" instead of "USER" (default: True)
        """
        root_workspace = self.workspace_manager.get_workspace(root_workspace_id)
        
        # Check if there are child workspaces with subtasks
        if task_plan.root.children and root_workspace.children:
            # Distribute subtasks to child workspaces
            for child_id in root_workspace.children:
                try:
                    child_workspace = self.workspace_manager.get_workspace(child_id)
                    
                    # Find the corresponding subtask from task plan
                    subtask = None
                    for child_node in task_plan.root.children:
                        # Match by agents (child workspace agents should match subtask required_agents)
                        if set(child_node.required_agents) == set(child_workspace.agents.keys()):
                            subtask = child_node
                            break
                    
                    if not subtask:
                        # Fallback: use first unmatched subtask
                        subtask = task_plan.root.children[0]
                    
                    # Send subtask to first agent in workspace
                    agent_names = list(child_workspace.agents.keys())
                    if agent_names:
                        first_agent = agent_names[0]
                        other_agents = agent_names[1:] if len(agent_names) > 1 else []
                        
                        # Get root workspace coordinator for cross-workspace communication
                        root_workspace = self.workspace_manager.get_workspace(root_workspace_id)
                        root_agents = list(root_workspace.agents.keys())
                        root_coordinator = root_agents[0] if root_agents else None
                        
                        # Build collaborative task message
                        team_info = ""
                        if other_agents:
                            team_info = f"\n\nYour direct teammate(s) in this workspace: {', '.join(other_agents)}\nCoordinate with them on your specific subtask."
                        
                        cross_workspace_info = ""
                        if root_coordinator:
                            cross_workspace_info = (
                                f"\n\nFor cross-team coordination: Contact {root_coordinator} (root coordinator) "
                                f"to communicate with agents in other workspaces. {root_coordinator} will relay messages between teams."
                            )
                        
                        subtask_message = (
                            f"{user_task}\n\n"
                            f"Your team's focus: {subtask.description}"
                            f"{team_info}"
                            f"{cross_workspace_info}\n\n"
                            f"Start by discussing the approach with your direct teammate(s), divide the work, "
                            f"and use the root coordinator for any cross-team dependencies."
                        )
                        
                        # Send from "planner" (PlannerAgent) instead of "USER"
                        # The PlannerAgent is the CEO - execution agents report to it
                        sender = "planner" if use_planner_agent else "USER"
                        await child_workspace.route_message(
                            sender,
                            first_agent,
                            subtask_message,
                            manager=self.workspace_manager
                        )
                        logger.info(f"Distributed subtask to {first_agent} in workspace {child_id}")
                
                except Exception as e:
                    logger.error(f"Error distributing task to child workspace {child_id}: {e}")
        else:
            # No child workspaces, send full task to root workspace
            # Use "planner" as sender when PlannerAgent is enabled
            agent_names = list(root_workspace.agents.keys())
            if agent_names:
                first_agent = agent_names[0]
                sender = "planner" if use_planner_agent else "USER"
                await root_workspace.route_message(
                    sender,
                    first_agent,
                    user_task,
                    manager=self.workspace_manager
                )
                logger.info(f"Distributed task to {first_agent} in root workspace (sender: {sender})")
    
    async def execute_task_plan(
        self,
        task_plan: Any,  # TaskTreePlan
        user_task: str,
        use_planner_agent: bool = True,
    ) -> tuple[Any, list[Any]]:  # Returns (root_workspace, child_workspaces)
        """
        High-level method to execute a complete task plan automatically.
        
        This method handles:
        1. Creating root workspace with PlannerAgent as sole coordinator
        2. Creating child workspaces for each subtask (execution agents only)
        3. Distributing initial tasks to agents
        4. Scheduling and executing all workspaces
        
        The root workspace contains ONLY the PlannerAgent (CEO):
        - It is the only agent the user interacts with
        - It coordinates all child workspace execution agents
        - It synthesizes results and delivers final output
        
        Child workspaces contain ONLY execution agents that:
        - Do NOT perform planning or delegation
        - Execute the specific subtask assigned to them
        - Return deliverables to the PlannerAgent
        
        Args:
            task_plan: TaskTreePlan with workspace hierarchy
            user_task: The original user task description
            use_planner_agent: If True, use PlannerAgent as sole root agent (default: True)
            
        Returns:
            Tuple of (root_workspace, list of child_workspaces)
            
        Example:
            ```python
            # Create task plan
            task_plan = await planner.plan_task(user_task)
            
            # Execute everything automatically with PlannerAgent as CEO
            root_ws, child_ws = await engine.execute_task_plan(task_plan, user_task)
            ```
        """
        # ================================================================
        # ROOT WORKSPACE = PLANNER AGENT ONLY
        # ================================================================
        # The root workspace contains exactly one agent: the PlannerAgent
        # All execution agents are distributed to child workspaces only
        # ================================================================
        
        if task_plan.root.children and use_planner_agent:
            # Collect all agents from task plan - ALL go to child workspaces
            all_child_agents = set()
            for child in task_plan.root.children:
                all_child_agents.update(child.required_agents)
            
            # Any agents originally in root should be redistributed to children
            # to ensure they're used as execution agents, not coordinators
            orphaned_agents = list(task_plan.root.required_agents)
            
            # Fix single-agent workspaces by assigning orphaned agents
            for child in task_plan.root.children:
                if len(child.required_agents) == 1 and orphaned_agents:
                    # Assign an orphaned agent to this workspace
                    orphaned_agent = orphaned_agents.pop(0)
                    if orphaned_agent not in child.required_agents:
                        child.required_agents.append(orphaned_agent)
                        logger.info(
                            f"Fixed single-agent workspace: added {orphaned_agent} to "
                            f"pair with {child.required_agents[0]}"
                        )
            
            # Distribute any remaining orphaned agents to child workspaces
            for i, orphaned_agent in enumerate(orphaned_agents):
                child_idx = i % len(task_plan.root.children)
                if orphaned_agent not in task_plan.root.children[child_idx].required_agents:
                    task_plan.root.children[child_idx].required_agents.append(orphaned_agent)
                    logger.info(f"Distributed orphaned agent {orphaned_agent} to child workspace {child_idx}")
            
            # Create PlannerAgent as the sole root workspace agent
            # Get child workspace descriptions for the PlannerAgent
            child_descriptions = [child.description for child in task_plan.root.children]
            
            planner_agent = PlannerAgent(
                planner_llm=self.planner,
                child_workspace_count=len(task_plan.root.children),
                child_descriptions=child_descriptions,
                name="planner",
                description="CEO/Planner that coordinates all execution teams and synthesizes results",
            )
            
            # Register the PlannerAgent in the registry
            AgentRuntimeRegistry.register("planner", planner_agent)
            
            # Set root to have ONLY the planner agent
            task_plan.root.required_agents = ["planner"]
            
            # Count total execution agents across child workspaces
            total_child_agents = sum(len(child.required_agents) for child in task_plan.root.children)
            
            logger.info(
                f"Root workspace: PlannerAgent (CEO) only | "
                f"Child workspaces: {len(task_plan.root.children)} teams with {total_child_agents} execution agents"
            )
        
        # Create root workspace
        root_workspace = await self.workspace_manager.create_workspace(
            task_tree_node=task_plan.root,
            parent_workspace_id=None
        )
        
        # Attach MCP middleware to all agents in root workspace
        self._attach_mcp_to_workspace(root_workspace)
        
        logger.info(f"Created root workspace: {root_workspace.workspace_id}")
        
        # Create child workspaces for each subtask
        child_workspaces = []
        if task_plan.root.children:
            for i, subtask in enumerate(task_plan.root.children, 1):
                child_ws = await self.workspace_manager.create_workspace(
                    task_tree_node=subtask,
                    parent_workspace_id=root_workspace.workspace_id
                )
                # Attach MCP middleware to all agents in child workspace
                self._attach_mcp_to_workspace(child_ws)
                child_workspaces.append(child_ws)
                logger.info(f"Created child workspace {i}: {child_ws.workspace_id}")
        
        # Send task to PlannerAgent (CEO) from the real user
        # The PlannerAgent IS the user-facing agent - it receives tasks from the real human user
        if root_workspace.agents:
            root_agent = list(root_workspace.agents.keys())[0]
            
            # Check if this is a PlannerAgent (CEO) or a legacy execution agent coordinator
            is_planner_agent = root_agent == "planner" and use_planner_agent
            
            if is_planner_agent:
                # PlannerAgent receives task from the real user
                # Note: Real user messages come in labeled as "USER" to the PlannerAgent
                # But the PlannerAgent then sends to execution agents as "planner"
                task_message = (
                    f"Task: {user_task}\n\n"
                    f"You are coordinating {len(child_workspaces)} specialized teams:\n"
                )
                for i, subtask in enumerate(task_plan.root.children, 1):
                    task_message += f"  Team {i}: {', '.join(subtask.required_agents)} - {subtask.description}\n"
                
                task_message += (
                    f"\nTeams are now executing their subtasks in parallel. "
                    f"You will receive [subteam_result] messages as they complete."
                )
            else:
                # Legacy mode: send detailed instructions to execution agent acting as coordinator
                task_message = (
                    f"{user_task}\n\n"
                    f"Your role: You are the ROOT COORDINATOR for this multi-team project.\n\n"
                    f"Your responsibilities:\n"
                    f"1. Coordinate between {len(child_workspaces)} specialized teams working in parallel\n"
                    f"2. Relay messages between teams when they need to communicate across workspaces\n"
                    f"3. Monitor progress from all teams\n"
                    f"4. Aggregate final results from all teams\n"
                    f"5. Send final comprehensive report to USER when all teams complete their work\n\n"
                    f"The teams are:\n"
                )
                for i, subtask in enumerate(task_plan.root.children, 1):
                    task_message += f"  Team {i}: {', '.join(subtask.required_agents)} - {subtask.description}\n"
                
                task_message += (
                    f"\nWait for teams to report their progress, coordinate any cross-team dependencies, "
                    f"and aggregate their final outputs into a comprehensive conference plan for USER."
                )
            
            # Real user sends to PlannerAgent
            await root_workspace.route_message(
                "USER",
                root_agent,
                task_message,
                manager=self.workspace_manager
            )
            logger.info(f"Sent task to root agent: {root_agent} (PlannerAgent: {is_planner_agent})")
        
        # Distribute initial tasks to agents
        # Tasks are sent from "planner" when PlannerAgent is enabled
        await self.distribute_task_to_workspaces(
            task_plan=task_plan,
            user_task=user_task,
            root_workspace_id=root_workspace.workspace_id,
            use_planner_agent=use_planner_agent,
        )
        
        # Schedule workspaces for execution
        if child_workspaces:
            # Schedule root workspace (for coordinator to process messages)
            if root_workspace.agents:
                self.schedule_workspace(root_workspace.workspace_id)
            
            # Schedule all child workspaces
            for child_ws in child_workspaces:
                self.schedule_workspace(child_ws.workspace_id)
            
            # Run global scheduler to execute all workspaces in parallel
            await self.run_global_scheduler()
        else:
            # Execute root workspace only
            await self.run_workspace(root_workspace.workspace_id)
        
        return root_workspace, child_workspaces
    
    async def run(self, root_workspace_id: str) -> None:
        """
        Top-level entrypoint for executing a root workspace and all its children.
        
        This method schedules the root workspace and then runs the global scheduler
        to process all workspaces (including children) asynchronously.
        
        Args:
            root_workspace_id: ID of the root workspace to execute
        """
        # Display initial message placement if display is enabled
        if self.display:
            workspace = self.workspace_manager.get_workspace(root_workspace_id)
            # Check if there are any initial messages
            for agent_name, agent in workspace.agents.items():
                messages = agent.memory.get_messages()
                if messages:
                    # Display initial for the first agent with a message
                    self.display.display_initial("user task", agent_name)
                    break
        
        self.schedule_workspace(root_workspace_id)
        await self.run_global_scheduler()
    
    async def run_workspace(
        self,
        workspace_id: str,
        max_cycles: Optional[int] = None,
    ) -> None:
        """
        Execute a workspace's agents using event-driven scheduling.
        
        This method executes a workspace independently without recursion.
        When a workspace completes, it sends subteam_result messages to its
        parent workspace if it has one.
        
        Args:
            workspace_id: ID of workspace to execute
            max_cycles: Maximum number of event processing cycles (default: uses engine's max_cycles)
        """
        # Use instance max_cycles if not provided
        if max_cycles is None:
            max_cycles = self.max_cycles
        workspace = self.workspace_manager.get_workspace(workspace_id)
        
        # Prevent re-entry
        if workspace.is_running or workspace_id in self._running_workspaces:
            logger.warning(f"Workspace {workspace_id} is already running, skipping execution")
            return
        
        # Mark as running
        workspace.is_running = True
        self._running_workspaces.add(workspace_id)
        
        try:
            # Get or create shared event scheduler for this workspace
            if workspace_id not in self._workspace_schedulers:
                self._workspace_schedulers[workspace_id] = EventScheduler()
            scheduler = self._workspace_schedulers[workspace_id]
        
            # Schedule startup events for all agents (only on first execution)
            # FIX: Skip agents that already have unprocessed messages (e.g., initial USER message)
            # FIX: Only send startup to root workspace (child workspaces activate on-demand via messages)
            # The unprocessed messages section below will schedule events for them
            if not workspace.has_started:
                # Only root workspace agents get startup events
                # Child workspace agents activate only when messaged
                if workspace.depth == 0:
                    for agent_name, agent in workspace.agents.items():
                        # Check if agent already has unprocessed messages
                        unprocessed = agent.memory.get_unprocessed_messages()
                        if unprocessed:
                            # Agent already has work to do, skip startup event
                            # The unprocessed messages loop below will schedule events for these
                            logger.debug(f"Skipping startup event for {agent_name} - already has {len(unprocessed)} unprocessed messages")
                            continue
                        
                        # Route a system startup message via workspace
                        msg_id = await workspace.route_message(
                            sender="SYSTEM",
                            recipient=agent_name,
                            content="[startup]",
                            manager=self.workspace_manager,
                        )
                        
                        # Schedule startup event carrying that message_id
                        scheduler.schedule_event_dedup(AgentEvent(
                            agent_name=agent_name,
                            trigger="startup",
                            payload={"message_id": msg_id},
                        ))
                workspace.has_started = True
            
            # Check for unprocessed messages (e.g., subteam_result from child workspaces)
            # and schedule message events for them
            for agent_name, agent in workspace.agents.items():
                unprocessed_messages = agent.memory.get_unprocessed_messages()
                for message in unprocessed_messages:
                    # ROUTING ENFORCEMENT: Only schedule event if message is targeted to this agent
                    # target should always be set by router, but check just in case
                    message_target = getattr(message, 'target', None)
                    
                    # If target is set and doesn't match this agent, skip
                    if message_target is not None and message_target != agent_name:
                        logger.debug(f"Skipping message {message.message_id} for {agent_name} - targeted to {message_target}")
                        continue
                    
                    # If target is not set, this is a legacy message or system message
                    # Only allow for the first agent (backwards compatibility) or if content suggests it's for this agent
                    if message_target is None:
                        # For None targets, only schedule if this is a system message or workspace-level broadcast
                        # Most messages should have targets, so log a warning
                        logger.warning(f"Message {message.message_id} has no target, scheduling for {agent_name}")
                    
                    # Determine trigger type based on message content
                    trigger = "message"
                    if message.content.startswith("[subteam_result]"):
                        trigger = "subteam_result"
                    
                    # Schedule event for unprocessed messages
                    scheduler.schedule_event_dedup(AgentEvent(
                        agent_name=agent_name,
                        trigger=trigger,
                        payload={"message_id": message.message_id},
                    ))
            
            cycle = 0
            consecutive_no_output_cycles = 0
            total_events_processed = 0
            agent_turns = 0  # Count of actual agent responses
            task_complete = False  # Flag to stop execution when USER receives a message
            
            while scheduler.has_pending_events() and cycle < max_cycles and not task_complete:
                # Event loop protection: max events per workspace
                if total_events_processed >= self.max_events_per_workspace:
                    if self.display:
                        self.display.display_error(
                            "max_events_exceeded",
                            f"Workspace stopped after {total_events_processed} events"
                        )
                    # Add error transcript entry
                    self._add_error_transcript_entry(
                        workspace, workspace_id, "max_events_exceeded",
                        f"Stopped after {total_events_processed} events"
                    )
                    break
                
                cycle += 1
                
                cycle_had_output = False
                events_processed_this_cycle = 0
                
                # Process events with per-cycle throttle
                while (scheduler.has_pending_events() and 
                       events_processed_this_cycle < self.max_events_per_cycle):
                    
                    event = scheduler.pop_next_event()
                    if event is None:
                        break
                    
                    events_processed_this_cycle += 1
                    total_events_processed += 1
                    agent_name = event.agent_name
                    
                    # NOTE: Display processing message AFTER we confirm agent produces output
                    # (moved below to avoid showing "processing" for filtered messages)
                    
                    # Strict validation for event.trigger
                    valid_triggers = {"startup", "message", "subteam_result"}
                    if event.trigger not in valid_triggers:
                        logger.error(
                            f"Invalid event trigger '{event.trigger}' for agent '{agent_name}' "
                            f"in workspace {workspace_id}. Valid triggers: {valid_triggers}. Skipping."
                        )
                        continue
                    
                    # Verify agent exists
                    if agent_name not in workspace.agents:
                        logger.warning(f"Event for unknown agent '{agent_name}' in workspace {workspace_id}")
                        continue
                    
                    agent = workspace.agents[agent_name]
                    
                    # Message-like events must always carry a message_id that matches AgentMemory
                    message_like_triggers = {"startup", "message", "subteam_result"}
                    message_id: Optional[str] = None
                    
                    if event.trigger in message_like_triggers:
                        message_id = event.payload.get("message_id")
                        if not message_id:
                            logger.warning(
                                f"{event.trigger} event missing message_id for agent {agent_name} "
                                f"in workspace {workspace_id}"
                            )
                            continue
                        
                        # Fetch exact message by id
                        message = agent.memory.get_message_by_id(message_id)
                        if message is None:
                            logger.debug(
                                f"message {message_id} not found for agent {agent_name} in workspace {workspace_id}, skipping"
                            )
                            continue
                        
                        # Check if already processed
                        if agent.memory.is_message_processed(message_id):
                            logger.debug(
                                f"message {message_id} already processed for agent {agent_name} in workspace {workspace_id}, skipping"
                            )
                            continue
                    
                    # Get messages for context
                    messages = agent.memory.get_messages()
                    
                    # Create context with event trigger, payload, and shared_plan
                    context = Context(
                        agent_name=agent_name,
                        workspace=workspace,
                        workspace_id=workspace_id,
                        messages=messages[-10:] if messages else [],
                        memory=agent.memory,
                        default_target=agent.default_target,
                        event_trigger=event.trigger,
                        event_payload=event.payload,
                        shared_plan=workspace.shared_plan,
                    )
                    
                    try:
                        # ExecutionEngine is the only component allowed to route messages;
                        # agent logic may not use routers. All routing must go through workspace.route_message.
                        # Agent.process enforces router isolation and structured return format.
                        
                        # Check if this is a local agent or remote A2A agent
                        if hasattr(agent, 'process'):
                            # Local agent built with Synqed - call process() with context
                            result = await agent.process(context)
                            
                            # Mark message as processed after successful logic execution
                            if message_id:
                                agent.memory.mark_message_processed(message_id)
                            
                            # Check if agent returned None (agent chose not to respond)
                            if result is None:
                                logger.debug(f"Agent {agent_name} returned None - skipping (no response needed)")
                                continue
                        else:
                            # Remote A2A agent - call get_response() (messages already buffered)
                            result = await agent.get_response()
                            # No memory to mark - remote agent manages its own state
                            
                            # Check if agent returned None (e.g., for startup messages that should be skipped)
                            if result is None:
                                logger.debug(f"Agent {agent_name} returned None - skipping (no response needed)")
                                continue
                        
                        # Display processing message NOW (agent produced output)
                        if self.display and agent_name != self._active_agent:
                            self._active_agent = agent_name
                            self.display.display_processing(agent_name)
                        
                        # Hardened agent output validation (supports broadcast)
                        agent_response = self._validate_and_normalize_response(
                            result, agent_name, workspace
                        )
                        
                        if agent_response is None:
                            continue  # Invalid response, skip
                        
                        # Handle BROADCAST: convert single dict to list for uniform processing
                        responses_to_process = [agent_response] if isinstance(agent_response, dict) else agent_response
                        
                        # BROADCAST DISPLAY: Show broadcast message only ONCE with "ALL"
                        # instead of showing each individual recipient
                        is_broadcast = isinstance(agent_response, list) and len(agent_response) > 1
                        broadcast_displayed = False
                        
                        # Process each response (single or broadcast)
                        for single_response in responses_to_process:
                            # Infer turn type for this response
                            turn_type = infer_turn_type(single_response.get("content", ""))
                            logger.debug(f"Agent {agent_name} turn type: {turn_type}")
                            
                            # Optionally update shared plan based on turn type
                            # (For now, we just log it; agents can update shared_plan organically)
                            
                            # Check if this is a DELIBERATE DELIVERABLE from PlannerLLM
                            # Deliverables have type="deliverable" and include deliverable_title/content
                            is_deliverable = single_response.get("type") == "deliverable"
                            
                            logger.info(f"🔍 Agent {agent_name} response type: {single_response.get('type')}, is_deliverable: {is_deliverable}")
                            if single_response.get("type"):
                                logger.info(f"   Response keys: {list(single_response.keys())}")
                            
                            if is_deliverable:
                                # Extract deliverable info
                                deliverable_title = single_response.get("deliverable_title", "Task Deliverable")
                                deliverable_content = single_response.get("deliverable_content", "")
                                
                                logger.info(f"🎯 DELIVERABLE DETECTED!")
                                logger.info(f"   Title: {deliverable_title}")
                                logger.info(f"   Content length: {len(deliverable_content)} chars")
                                logger.info(f"   Callback registered: {self._on_deliverable is not None}")
                                
                                # Invoke the deliverable callback if registered
                                if self._on_deliverable and deliverable_content:
                                    logger.info(f"   Invoking callback...")
                                    try:
                                        self._on_deliverable(
                                            workspace_id=workspace_id,
                                            title=deliverable_title,
                                            content=deliverable_content,
                                            agent_name=agent_name,
                                        )
                                        logger.info(
                                            f"📦 Deliverable emitted: '{deliverable_title[:50]}...' "
                                            f"from {agent_name} in workspace {workspace_id[:20]}..."
                                        )
                                    except Exception as e:
                                        logger.error(f"Error invoking deliverable callback: {e}")
                                else:
                                    logger.warning(f"   ⚠️ Callback not invoked! callback={self._on_deliverable is not None}, content={len(deliverable_content) if deliverable_content else 0}")
                                
                                # The "content" field contains the short notification for chat
                                # (deliverable_content is stored separately, not in chat)
                            
                            # Handle messages to USER or planner (CEO/coordinator)
                            # - Execution agents in child workspaces send to "planner"
                            # - PlannerAgent in root workspace sends to "USER" (the real human)
                            send_to = single_response["send_to"]
                            is_final_recipient = send_to in ("USER", "planner")
                            
                            if is_final_recipient:
                                # Display the message (the short notification, not the full deliverable)
                                if self.display:
                                    self.display.display_message(
                                        sender=agent_name,
                                        recipient=send_to,
                                        content=single_response["content"]
                                    )
                                
                                await workspace.route_message(
                                    sender=agent_name,
                                    recipient=send_to,
                                    content=single_response["content"],
                                    manager=self.workspace_manager,
                                )
                                
                                # CHATGPT-STYLE PERSISTENT CONVERSATIONS:
                                # DO NOT auto-complete the workspace when sending to USER.
                                # The user should be able to continue the conversation indefinitely.
                                # Workspaces only end when:
                                # - max_cycles is reached
                                # - no more pending events after waiting for user input
                                # - explicitly terminated
                                
                                is_root_planner = (workspace.depth == 0 and len(workspace.children) > 0)
                                
                                if send_to == "USER":
                                    # Message to USER - conversation continues, do NOT end workspace
                                    logger.info(
                                        f"Agent {agent_name} sent message to USER - "
                                        f"conversation continues (ChatGPT-style persistent)"
                                    )
                                    cycle_had_output = True
                                    # Continue processing - user may respond and agents should be ready
                                    continue
                                elif is_root_planner:
                                    # Root PlannerAgent sending to something other than USER (rare)
                                    # Continue coordinating
                                    logger.info(
                                        f"PlannerAgent {agent_name} sent update to {send_to} - "
                                        f"continuing to coordinate {len(workspace.children)} child workspaces"
                                    )
                                    cycle_had_output = True
                                    continue
                                else:
                                    # Child workspace - sending to planner means this workspace's subtask is complete
                                    # But the overall conversation continues via the root workspace
                                    logger.info(f"Agent {agent_name} sent to {send_to} - child workspace subtask complete")
                                    task_complete = True
                                    # Clear remaining events for THIS workspace
                                    while scheduler.has_pending_events():
                                        scheduler.pop_next_event()
                                    break  # Exit this workspace's event loop (parent continues)
                            
                            # Check for subteam request
                            subteam_handled = await self._handle_subteam_request(
                                workspace=workspace,
                                workspace_id=workspace_id,
                                agent_name=agent_name,
                                response=single_response,
                                scheduler=scheduler,  # Only used for error cases
                            )
                            
                            if subteam_handled:
                                cycle_had_output = True
                                continue
                            
                            # Check for infinite self-message loops
                            if self._is_self_message_loop(
                                agent, single_response["send_to"], agent_name, single_response["content"]
                            ):
                                logger.warning(
                                    f"Blocked self-message loop for agent {agent_name} in workspace {workspace_id}"
                                )
                                self._add_error_transcript_entry(
                                    workspace, workspace_id, "self_message_loop_blocked",
                                    f"Agent {agent_name} attempted self-message loop"
                                )
                                continue
                            
                            # Recipient validation already done in _validate_and_normalize_response
                            # No need to check again here
                            
                            # Display the message (only once for broadcasts)
                            if self.display and not (is_broadcast and broadcast_displayed):
                                display_recipient = "ALL" if is_broadcast else single_response["send_to"]
                                self.display.display_message(
                                    sender=agent_name,
                                    recipient=display_recipient,
                                    content=single_response["content"]
                                )
                                if is_broadcast:
                                    broadcast_displayed = True
                            
                            # Route message with deterministic ID
                            message_id = await workspace.route_message(
                                sender=agent_name,
                                recipient=single_response["send_to"],
                                content=single_response["content"],
                                manager=self.workspace_manager,
                            )
                            
                            if message_id:
                                # Determine which workspace the recipient is in
                                recipient_workspace_id = None
                                if single_response["send_to"] in workspace.agents:
                                    # Recipient is in current workspace
                                    recipient_workspace_id = workspace_id
                                elif self.workspace_manager:
                                    # Check child workspaces
                                    for child_id in workspace.children:
                                        try:
                                            child_workspace = self.workspace_manager.get_workspace(child_id)
                                            if single_response["send_to"] in child_workspace.agents:
                                                recipient_workspace_id = child_id
                                                break
                                        except:
                                            pass
                                    
                                    # Check parent workspace
                                    if not recipient_workspace_id and workspace.parent_id:
                                        try:
                                            parent_workspace = self.workspace_manager.get_workspace(workspace.parent_id)
                                            if single_response["send_to"] in parent_workspace.agents:
                                                recipient_workspace_id = workspace.parent_id
                                        except:
                                            pass
                                
                                # Schedule event in the appropriate workspace's scheduler
                                if recipient_workspace_id:
                                    # Get or create scheduler for the target workspace
                                    if recipient_workspace_id not in self._workspace_schedulers:
                                        self._workspace_schedulers[recipient_workspace_id] = EventScheduler()
                                    
                                    target_scheduler = self._workspace_schedulers[recipient_workspace_id]
                                    target_scheduler.schedule_event_dedup(AgentEvent(
                                        agent_name=single_response["send_to"],
                                        trigger="message",
                                        payload={"message_id": message_id}
                                    ))
                                    
                                    # For cross-workspace messages, schedule the target workspace for execution
                                    if recipient_workspace_id != workspace_id:
                                        self.schedule_workspace(recipient_workspace_id)
                                        logger.debug(
                                            f"Cross-workspace message: {agent_name} → {single_response['send_to']} "
                                            f"(workspace {workspace_id} → {recipient_workspace_id}), "
                                            f"scheduled target workspace for execution"
                                        )
                                
                                cycle_had_output = True
                        
                        # Increment agent turns counter AFTER processing all broadcast responses
                        agent_turns += 1
                        
                        # 🔧 FIX: Force early action - inject reminder at turn 5 if no concrete actions yet
                        # Check max_agent_turns limit
                        if self.max_agent_turns is not None and agent_turns >= self.max_agent_turns:
                            if self.display:
                                self.display.display_error(
                                    "max_agent_turns_exceeded",
                                    f"Stopped after {agent_turns} agent responses (task incomplete)"
                                )
                            logger.info(f"Max agent turns ({self.max_agent_turns}) reached, stopping workspace")
                            task_complete = True
                            # Clear remaining events
                            while scheduler.has_pending_events():
                                scheduler.pop_next_event()
                            break
                    
                    except Exception as e:
                        logger.error(f"Error executing agent {agent_name} in workspace {workspace_id}: {e}")
                        continue
                
                # Fatal-cycle detection: no output for N cycles with non-empty queue
                if cycle_had_output:
                    consecutive_no_output_cycles = 0
                else:
                    consecutive_no_output_cycles += 1
                    if (consecutive_no_output_cycles >= self.fatal_cycle_threshold and 
                        scheduler.has_pending_events()):
                        if self.display:
                            self.display.display_error(
                                "fatal_cycle_detected",
                                f"Workspace stuck (no output for {consecutive_no_output_cycles} cycles)"
                            )
                        self._add_error_transcript_entry(
                            workspace, workspace_id, "fatal_cycle_detected",
                            f"Killed after {consecutive_no_output_cycles} cycles with no output"
                        )
                        break
            
            # Display completion
            if self.display and workspace.depth == 0:
                self.display.display_completion(workspace_id, cycle)
            
            # If this workspace has a parent, send subteam_result message
            # Note: We don't have access to parent's scheduler here, so we'll route the message
            # and schedule the parent workspace. The parent will pick up the message when it runs.
            if workspace.parent_id:
                await self._send_subteam_result_to_parent(workspace, workspace_id)
        finally:
            # Mark as not running
            workspace.is_running = False
            self._running_workspaces.discard(workspace_id)
    
    async def _send_subteam_result_to_parent(
        self,
        child_workspace: Workspace,
        child_workspace_id: str,
    ) -> None:
        """
        Send subteam_result message to parent workspace when child completes.
        
        This method is called when a child workspace finishes execution.
        It creates a subteam_result message and routes it to the requesting
        agent in the parent workspace via normal message routing. The parent
        workspace will pick up this message when it runs next and schedule
        a subteam_result event automatically (via unprocessed message detection).
        
        Args:
            child_workspace: The child workspace that just completed
            child_workspace_id: ID of the child workspace
        """
        if not child_workspace.parent_id:
            return
        
        try:
            parent_workspace = self.workspace_manager.get_workspace(child_workspace.parent_id)
            
            # Find which agent in parent requested this subteam
            requesting_agent = self._subteam_requesters.get(child_workspace_id)
            
            if not requesting_agent:
                # Fallback: try to find agent with subteam requests
                for agent_name, count in parent_workspace.subteam_requests.items():
                    if count > 0:
                        requesting_agent = agent_name
                        break
                
                if not requesting_agent:
                    # Final fallback: send to first agent in parent
                    if parent_workspace.agents:
                        requesting_agent = list(parent_workspace.agents.keys())[0]
                    else:
                        logger.warning(f"No agent found in parent workspace {child_workspace.parent_id} for subteam_result")
                        return
            
            # Fetch final transcript from child workspace
            child_transcript = child_workspace.router.get_transcript()
            result_message = ""
            
            if child_transcript:
                # Only include the last message
                last_entry = child_transcript[-1]
                result_message = last_entry.get("content", "")[:500]  # Truncate
            else:
                result_message = f"Subteam {child_workspace_id} completed"
            
            # Build a canonical payload for the result
            payload = {
                "child_workspace_id": child_workspace_id,
                "result_message": result_message,
            }
            
            # Create a system message to the requesting agent with the subteam result
            # The message content starts with [subteam_result] so it will be detected
            # as a subteam_result trigger when the parent workspace processes unprocessed messages
            msg_id = await parent_workspace.route_message(
                sender="SYSTEM",
                recipient=requesting_agent,
                content=f"[subteam_result]{json.dumps(payload, sort_keys=True)}",
                manager=self.workspace_manager,
            )
            
            # Schedule parent workspace to process the subteam_result message
            # When parent runs, it will detect the unprocessed [subteam_result] message
            # and schedule a subteam_result event automatically
            self.schedule_workspace(child_workspace.parent_id)
        
        except Exception as e:
            logger.error(f"Error sending subteam_result to parent: {e}")
    
    def _all_children_completed(self, workspace: Workspace) -> bool:
        """
        Check if all child workspaces have reported back with subteam_result.
        
        This is used to determine when a root coordinator can finish execution.
        
        Args:
            workspace: The workspace to check
            
        Returns:
            True if all children have completed and reported back, False otherwise
        """
        if not workspace.children:
            # No children means this check is not applicable
            return False
        
        # Count how many subteam_result messages have been received by agents in this workspace
        subteam_results_received = 0
        for agent_name, agent in workspace.agents.items():
            messages = agent.memory.get_messages()
            for msg in messages:
                if msg.content.startswith("[subteam_result]"):
                    subteam_results_received += 1
        
        # All children completed if we've received as many subteam_result messages as we have children
        all_completed = subteam_results_received >= len(workspace.children)
        
        if all_completed:
            logger.info(
                f"All {len(workspace.children)} child workspaces have completed "
                f"({subteam_results_received} subteam_result messages received)"
            )
        
        return all_completed
    
    def _validate_and_normalize_response(
        self,
        result: dict[str, str],
        agent_name: str,
        workspace: Workspace,
    ) -> Optional[dict[str, str] | list[dict[str, str]]]:
        """
        Validate and normalize agent response with broadcast support.
        
        Supports both single and broadcast responses:
        - Single: {"send_to": "Agent", "content": "..."}
        - Broadcast: {"send_to": ["Agent1", "Agent2", "Agent3"], "content": "..."}
        
        Args:
            result: dict from Agent.process() with "send_to" (str or list) and "content"
            agent_name: Name of the agent for logging
            workspace: Workspace instance for agent validation
            
        Returns:
            dict[str, str] if single recipient
            list[dict[str, str]] if broadcast to multiple recipients
            None if invalid
        """
        # Validate required fields exist
        if "send_to" not in result:
            logger.warning(f"Agent {agent_name} returned invalid response structure (missing send_to)")
            return None
        
        # Support both "content" and "message" fields (LLMs sometimes use "message")
        if "content" not in result and "message" not in result:
            logger.warning(f"Agent {agent_name} returned invalid response structure (missing content or message)")
            return None
        
        send_to = result["send_to"]
        content = result.get("content") or result.get("message", "")
        
        # BROADCAST SUPPORT: Handle "ALL" keyword - broadcast to all agents in workspace
        if send_to == "ALL":
            all_agent_names = list(workspace.agents.keys())
            if not all_agent_names:
                logger.warning(f"Agent {agent_name} tried to broadcast to ALL but no agents in workspace")
                return None
            
            # Exclude self from broadcast
            broadcast_recipients = [name for name in all_agent_names if name != agent_name]
            if not broadcast_recipients:
                logger.warning(f"Agent {agent_name} tried to broadcast to ALL but no other agents")
                return None
            
            logger.info(f"Agent {agent_name} broadcasting to ALL ({len(broadcast_recipients)} agents): {broadcast_recipients}")
            send_to = broadcast_recipients  # Convert to list for processing below
        
        # BROADCAST SUPPORT: Handle list of recipients
        if isinstance(send_to, list):
            if not send_to:
                logger.warning(f"Agent {agent_name} returned empty recipient list")
                return None
            
            logger.info(f"Agent {agent_name} broadcasting to {len(send_to)} recipients: {send_to}")
            
            # Validate and normalize each recipient
            normalized_responses = []
            for recipient in send_to:
                if not isinstance(recipient, str):
                    logger.warning(f"Agent {agent_name} returned non-string recipient in list: {recipient}")
                    continue
                
                # Validate this recipient exists (using same logic as single recipient)
                validated_recipient = self._validate_single_recipient(recipient.strip(), workspace, agent_name)
                if validated_recipient:
                    # Preserve all fields from original response (including type, deliverable_*, etc.)
                    normalized = dict(result)
                    normalized["send_to"] = validated_recipient
                    normalized["content"] = content
                    normalized_responses.append(normalized)
            
            if not normalized_responses:
                logger.warning(f"Agent {agent_name} broadcast had no valid recipients")
                return None
            
            return normalized_responses
        
        # SINGLE RECIPIENT: Use validation helper
        if not isinstance(send_to, str):
            logger.warning(f"Agent {agent_name} returned non-string send_to: {type(send_to)}")
            return None
        
        # Validate recipient
        send_to = self._validate_single_recipient(send_to.strip(), workspace, agent_name)
        if not send_to:
            return None
        
        # Truncate content if too long
        if len(content) > 10000:
            logger.warning(f"Agent {agent_name} response content truncated from {len(content)} to 10000 chars")
            content = content[:10000]
        
        # Ignore empty content
        if not content.strip():
            logger.debug(f"Agent {agent_name} returned empty content, ignoring")
            return None
        
        # Preserve all fields from original response (including type, deliverable_*, etc.)
        normalized = dict(result)
        normalized["send_to"] = send_to
        normalized["content"] = content
        return normalized
    
    def _validate_single_recipient(
        self,
        send_to: str,
        workspace: Workspace,
        agent_name: str
    ) -> Optional[str]:
        """
        Validate a single recipient exists in workspace hierarchy.
        
        Returns the validated recipient name, or None if invalid.
        "planner" and "USER" are always valid recipients.
        """
        if not send_to:
            return None
        
        # Handle nonexistent send_to by checking workspace hierarchy
        recipient_exists = False
        # "USER" and "planner" are always valid - planner is the CEO/coordinator
        if send_to in ("USER", "planner"):
            recipient_exists = True
        elif send_to in workspace.agents:
            recipient_exists = True
        elif self.workspace_manager:
            # Check child workspaces
            for child_id in workspace.children:
                try:
                    child_workspace = self.workspace_manager.get_workspace(child_id)
                    if send_to in child_workspace.agents:
                        recipient_exists = True
                        logger.debug(f"Found recipient '{send_to}' in child workspace {child_id}")
                        break
                except Exception as e:
                    logger.debug(f"Error checking child workspace {child_id}: {e}")
            
            # Check parent workspace if not found in children
            if not recipient_exists and workspace.parent_id:
                try:
                    parent_workspace = self.workspace_manager.get_workspace(workspace.parent_id)
                    if send_to in parent_workspace.agents:
                        recipient_exists = True
                        logger.debug(f"Found recipient '{send_to}' in parent workspace {workspace.parent_id}")
                except Exception as e:
                    logger.debug(f"Error checking parent workspace {workspace.parent_id}: {e}")
        
        if not recipient_exists:
            # 🔧 FIX: Reject nonexistent agents instead of silently converting to USER
            error_msg = (
                f"Agent {agent_name} tried to send message to nonexistent agent '{send_to}'. "
                f"Available agents in workspace {workspace.workspace_id}: {list(workspace.agents.keys())}. "
                f"Checked: current workspace, {len(workspace.children)} children, parent: {workspace.parent_id}"
            )
            logger.error(error_msg)
            
            # Return None to indicate invalid recipient (will be caught by validation)
            # This forces the agent to use correct names instead of silent fallback
            return None
        
        return send_to
    
    def _is_self_message_loop(
        self,
        agent: Any,
        send_to: str,
        agent_name: str,
        content: str,
    ) -> bool:
        """
        Detect infinite self-message loops.
        
        Returns True if:
        - send_to == sender AND
        - last 3 messages were self-targeted with same content
        """
        if send_to != agent_name:
            return False
        
        messages = agent.memory.get_last_n_messages(3)
        if len(messages) < 3:
            return False
        
        # Check if last 3 messages were self-targeted with same content
        self_targeted_same_content = sum(
            1 for msg in messages 
            if msg.from_agent == agent_name and msg.content == content
        )
        
        return self_targeted_same_content >= 3
    
    def _add_error_transcript_entry(
        self,
        workspace: Workspace,
        workspace_id: str,
        error_type: str,
        message: str,
    ) -> None:
        """Add an error entry to workspace transcript."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "workspace_id": workspace_id,
            "from": "SYSTEM",
            "to": "ERROR",
            "message_id": f"error-{datetime.now().isoformat()}",
            "content": f"[{error_type}] {message}",
        }
        workspace.router.add_transcript_entry(entry)
    
    async def _handle_subteam_request(
        self,
        workspace: Workspace,
        workspace_id: str,
        agent_name: str,
        response: dict[str, str],
        scheduler: EventScheduler,
    ) -> bool:
        """
        Handle a subteam request with recursion safety checks.
        
        The scheduler parameter is only used for error cases. The success path
        does not schedule any events - subteam results are handled later in
        _send_subteam_result_to_parent.
        
        Returns:
            True if subteam request was handled, False otherwise
        """
        # Parse request JSON from response content
        try:
            request_json = json.loads(response["content"])
        except (json.JSONDecodeError, TypeError, KeyError):
            return False
        
        if not isinstance(request_json, dict):
            return False
        
        if request_json.get("action") != "request_subteam":
            return False
        
        # Recursion safety checks
        # 1. Global workspace limit
        if self._total_workspaces_created >= self.max_total_workspaces:
            logger.error(
                f"Subteam creation denied: max total workspaces ({self.max_total_workspaces}) exceeded"
            )
            await self._schedule_subteam_error_result(
                workspace, scheduler, agent_name, "max_workspaces_exceeded"
            )
            return True
        
        # 2. Depth limit
        if workspace.depth >= self.max_workspace_depth:
            logger.error(
                f"Subteam creation denied: max depth ({self.max_workspace_depth}) reached "
                f"for workspace {workspace_id}"
            )
            await self._schedule_subteam_error_result(
                workspace, scheduler, agent_name, "max_depth_exceeded"
            )
            return True
        
        # 3. Per-agent throttling
        agent_request_count = workspace.subteam_requests.get(agent_name, 0)
        if agent_request_count >= self.max_subteam_requests_per_agent:
            logger.error(
                f"Subteam creation denied: agent {agent_name} exceeded max requests "
                f"({self.max_subteam_requests_per_agent})"
            )
            await self._schedule_subteam_error_result(
                workspace, scheduler, agent_name, "max_requests_per_agent_exceeded"
            )
            return True
        
        try:
            # Ensure requesting_agent is set
            if "requesting_agent" not in request_json:
                request_json["requesting_agent"] = agent_name
            
            # Create subtree
            subtree_root = await self.planner.create_subteam_subtree(request_json)
            
            # Create child workspace
            child_workspace = await self.workspace_manager.create_workspace(
                task_tree_node=subtree_root,
                parent_workspace_id=workspace_id,
            )
            
            # Attach MCP middleware to all agents in child workspace
            self._attach_mcp_to_workspace(child_workspace)
            
            self._total_workspaces_created += 1
            
            # Link subteam
            self.workspace_manager.link_subteam(
                parent_workspace_id=workspace_id,
                subteam_workspace_id=child_workspace.workspace_id,
            )
            
            # Increment agent request count
            workspace.subteam_requests[agent_name] = agent_request_count + 1
            
            # Track which agent requested this child workspace
            self._subteam_requesters[child_workspace.workspace_id] = agent_name
            
            # Schedule child workspace for asynchronous execution (no recursion)
            # The child will send subteam_result to parent when it completes
            self.schedule_workspace(child_workspace.workspace_id)
            
            # Return immediately - parent continues execution
            # Child workspace will send subteam_result message to parent when it finishes
            return True
            
        except Exception as e:
            logger.error(f"Error handling subteam request from {agent_name}: {e}")
            await self._schedule_subteam_error_result(
                workspace, scheduler, agent_name, f"error: {str(e)}"
            )
            return True
    
    async def _schedule_subteam_error_result(
        self,
        workspace: Workspace,
        scheduler: EventScheduler,
        agent_name: str,
        error_reason: str,
    ) -> None:
        """
        Schedule a subteam_result event pointing to an error message in memory.
        """
        payload = {
            "error": "subteam_limit_reached",
            "reason": error_reason,
        }
        
        # Create error message in agent memory via workspace.route_message
        msg_id = await workspace.route_message(
            sender="SYSTEM",
            recipient=agent_name,
            content=f"[subteam_result]{json.dumps(payload, sort_keys=True)}",
            manager=self.workspace_manager,
        )
        
        # Schedule the event with payload={"message_id": msg_id}
        scheduler.schedule_event_dedup(AgentEvent(
            agent_name=agent_name,
            trigger="subteam_result",
            payload={"message_id": msg_id},
        ))
