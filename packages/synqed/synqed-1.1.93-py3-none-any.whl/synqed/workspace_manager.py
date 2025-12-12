"""
WorkspaceManager - Manages hierarchical workspaces for multi-agent execution.

This module provides:
- Workspace: Logical routing domain for agents
- WorkspaceManager: Creates and manages workspace hierarchies
- AgentRuntimeRegistry: Registry for agent runtime instances

Workspaces are logical routing domains that route messages between agents.
They do not own or spawn HTTP servers - agents are provided via AgentRuntimeRegistry.
"""

from __future__ import annotations

import copy
import logging
import uuid
from pathlib import Path
from typing import Optional, Callable, Awaitable, Any
from pydantic import BaseModel, Field

from synqed.agent import Agent
from synqed.router import MessageRouter

logger = logging.getLogger(__name__)


class AgentRuntimeRegistry:
    """
    Universal registry for agent roles - supports both local and remote A2A agents.
    
    This registry stores:
    - Local agent prototypes (templates) built with Synqed
    - Remote A2A agent endpoints (any agent implementing A2A protocol)
    
    When creating workspaces, use create_instance() to get fresh, independent
    Agent instances cloned from local prototypes, or RemoteA2AAgent instances
    for remote endpoints.
    
    Each workspace gets its own Agent instances - no Agent instance is shared
    between workspaces. This prevents shared mutable state issues.
    
    UNIVERSAL SUBSTRATE:
    Any agent that implements the A2A protocol can be registered here.
    The agent just needs to provide:
    - Endpoint URL
    - AgentCard schema (/.well-known/agent-card.json)
    - Authentication details (optional)
    
    Synqed will handle routing messages to it.
    """
    
    _local_prototypes: dict[str, Agent] = {}  # role -> local prototype Agent
    _remote_agents: dict[str, Any] = {}  # role -> RemoteA2AAgent config
    
    @classmethod
    def register(cls, role: str, agent: Agent) -> None:
        """
        Register a local agent prototype for a role.
        
        Args:
            role: Agent role name (e.g., "Writer", "Editor")
            agent: Local Agent prototype instance
        """
        cls._local_prototypes[role] = agent
        logger.debug(f"Registered local agent prototype for role '{role}'")
    
    @classmethod
    def register_remote(
        cls,
        role: str,
        url: str,
        name: Optional[str] = None,
        auth_token: Optional[str] = None,
        transport: str = "JSONRPC",
        description: Optional[str] = None
    ) -> None:
        """
        Register a remote A2A-compliant agent.
        
        This allows ANY agent from ANY ecosystem to participate in Synqed workspaces,
        as long as it implements the A2A protocol.
        
        The agent just needs to say:
        - Here is my endpoint URL
        - Here is my schema (A2A AgentCard at /.well-known/agent-card.json)
        - Here is my auth (optional)
        
        And Synqed will route messages to it.
        
        Args:
            role: Agent role name (e.g., "ExternalSpecialist")
            url: A2A endpoint URL (e.g., "https://my-agent.example.com")
            name: Optional agent name (fetched from AgentCard if not provided)
            auth_token: Optional authentication token
            transport: Transport protocol (JSONRPC, GRPC, or HTTP+JSON)
            description: Optional description (fetched from AgentCard if not provided)
            
        Example:
            ```python
            # Register a remote A2A agent from any source
            AgentRuntimeRegistry.register_remote(
                role="CodeReviewAgent",
                url="https://code-review-agent.example.com",
                auth_token="secret-key"
            )
            
            # Now it can be used in any workspace
            ```
        """
        cls._remote_agents[role] = {
            "url": url,
            "name": name,
            "auth_token": auth_token,
            "transport": transport,
            "description": description
        }
        logger.info(f"Registered remote A2A agent for role '{role}' at {url}")
    
    @classmethod
    def get(cls, role: str) -> Optional[Agent]:
        """
        Get the local agent prototype for a role (for introspection only).
        
        NOTE: This returns the prototype, not a workspace-specific instance.
        Use create_instance() whenever attaching an Agent to a Workspace.
        
        Args:
            role: Agent role name
            
        Returns:
            Agent prototype if found, None otherwise
        """
        return cls._local_prototypes.get(role)
    
    @classmethod
    def create_instance(cls, role: str, workspace_id: Optional[str] = None) -> Optional[Any]:
        """
        Create a fresh agent instance for a workspace.
        
        This method:
        - For local agents: deep copies the prototype
        - For remote A2A agents: creates a new RemoteA2AAgent client
        
        Each workspace gets its own independent instance.
        
        Args:
            role: Agent role name
            workspace_id: Optional workspace ID for debugging annotation
            
        Returns:
            Agent instance (local Agent or RemoteA2AAgent) if found, None otherwise
        """
        # Check for local agent prototype
        local_prototype = cls._local_prototypes.get(role)
        if local_prototype is not None:
            # Deep copy the prototype
            cloned_agent = copy.deepcopy(local_prototype)
            
            # Annotate with workspace_id for debugging
            if workspace_id is not None:
                cloned_agent.workspace_id = workspace_id  # type: ignore
            
            logger.debug(f"Created local agent instance for role '{role}' (workspace: {workspace_id})")
            return cloned_agent
        
        # Check for remote A2A agent
        remote_config = cls._remote_agents.get(role)
        if remote_config is not None:
            # Import here to avoid circular dependency
            from synqed.a2a_remote_agent import RemoteA2AAgent
            
            # Create new RemoteA2AAgent instance
            # IMPORTANT: Use role as the name for routing consistency
            # Workspace.add_agent() keys agents by agent.name, so we must use the role name
            # to ensure routing works correctly (agents send messages using role names)
            remote_agent = RemoteA2AAgent(
                url=remote_config["url"],
                name=role,  # Use role as name for routing consistency
                auth_token=remote_config.get("auth_token"),
                transport=remote_config.get("transport", "JSONRPC"),
                description=remote_config.get("description")
            )
            
            logger.debug(f"Created remote A2A agent instance for role '{role}' (workspace: {workspace_id})")
            return remote_agent
        
        return None
    
    @classmethod
    def has(cls, role: str) -> bool:
        """
        Check if a role is registered (local or remote).
        
        Args:
            role: Agent role name
            
        Returns:
            True if role is registered
        """
        return role in cls._local_prototypes or role in cls._remote_agents
    
    @classmethod
    def list_roles(cls) -> list[str]:
        """
        List all registered roles (local and remote).
        
        Returns:
            List of role names
        """
        return list(set(cls._local_prototypes.keys()) | set(cls._remote_agents.keys()))
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered agents (local and remote)."""
        cls._local_prototypes.clear()
        cls._remote_agents.clear()


class Workspace(BaseModel):
    """
    Logical routing domain for multi-agent execution.
    
    A workspace is a lightweight object that:
    - Routes messages between agents within the workspace
    - Maintains parent/child relationships with other workspaces
    - Supports message callbacks for monitoring
    - Does NOT own or spawn HTTP servers
    - Does NOT run its own event loop
    
    Each Workspace contains independent Agent instances cloned from global role
    prototypes via AgentRuntimeRegistry.create_instance(). AgentRuntimeRegistry
    is a prototype registry, not a shared runtime. No Agent instance is shared
    between workspaces - each workspace gets its own cloned agents.
    
    All routing happens immediately within the global asyncio event loop.
    """
    
    workspace_id: str = Field(description="Unique identifier for this workspace")
    parent_id: Optional[str] = Field(default=None, description="ID of parent workspace")
    subtask_id: Optional[str] = Field(default=None, description="Link to TaskTreeNode ID")
    directory: Path = Field(description="Directory path for metadata/log storage")
    children: list[str] = Field(default_factory=list, description="List of child workspace IDs")
    router: MessageRouter = Field(default_factory=MessageRouter, description="Message router for this workspace")
    agents: dict[str, Agent] = Field(default_factory=dict, description="Agent name -> Agent instance mapping")
    depth: int = Field(default=0, description="Workspace depth in hierarchy (0 = root)")
    subteam_requests: dict[str, int] = Field(default_factory=dict, description="Agent name -> count of subteam requests")
    user_message_counter: int = Field(default=0, exclude=True, description="Counter for USER messages")
    message_callbacks: list[Callable[[str, str, str], Awaitable[None]]] = Field(
        default_factory=list,
        exclude=True,
        description="Callbacks for message routing events"
    )
    is_running: bool = Field(default=False, exclude=True, description="Flag indicating if workspace is currently executing")
    has_started: bool = Field(default=False, exclude=True, description="Flag indicating if workspace has received startup events")
    shared_plan: str = Field(default="", exclude=True, description="Shared plan document that all agents can read and update")
    workspace_name: str = Field(default="", description="Human-readable name for this workspace")
    workspace_description: str = Field(default="", description="Description of workspace's purpose")
    created_at: Optional[str] = Field(default=None, description="ISO timestamp when workspace was created")
    blocking_requirements: dict = Field(default_factory=dict, description="Consolidated blocking requirements from agents")
    waiting_for_user_input: bool = Field(default=False, description="Flag indicating workspace is blocked waiting for user")
    
    model_config = {"arbitrary_types_allowed": True}
    
    async def route_message(
        self,
        sender: str,
        recipient: str,
        content: str,
        manager: Optional[Any] = None,  # WorkspaceManager, avoid circular import
        message_id: Optional[str] = None,
    ) -> str:
        """
        Route a message within this workspace, assigning a deterministic message id.
        
        This is the single source of truth for message creation in a workspace.
        All messages (agent-to-agent, system-to-agent, USER) flow through here.
        
        - if recipient is an agent in this workspace:
            - use recipient's AgentMemory to add the message
            - generate a deterministic message_id if not provided
        - if recipient is "USER":
            - do not touch any AgentMemory, but still write a transcript entry
            - generate a synthetic message_id like "msg-{workspace_id}-USER-{counter}" using a workspace-local counter
        - record everything in router via router.add_transcript_entry(...)
        - return the message_id actually used
        
        Args:
            sender: Name of sending agent
            recipient: Name of target agent or "USER"
            content: Message content
            manager: Optional WorkspaceManager for parent/child routing
            message_id: Optional pre-generated message ID
            
        Returns:
            The message_id of the routed message
        """
        from datetime import datetime
        
        # Generate message ID if not provided
        if message_id is None:
            if recipient in self.agents:
                # Use recipient's memory to generate ID
                recipient_agent = self.agents[recipient]
                message_id = recipient_agent.memory.generate_message_id()
            elif recipient == "USER":
                # Generate USER message ID using workspace counter
                self.user_message_counter += 1
                message_id = f"msg-{self.workspace_id}-USER-{self.user_message_counter}"
            else:
                # Fallback: generate ID using workspace and sender
                message_id = f"msg-{self.workspace_id}-{sender}-{uuid.uuid4().hex[:8]}"
        
        # Route to agent in this workspace
        if recipient in self.agents:
            try:
                # route via unified MessageRouter (all routing goes through route_message)
                routed_message_id = await self.router.route_message(
                    workspace_id=self.workspace_id,
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    message_id=message_id,
                )
                
                # Call callbacks after successful routing
                for callback in self.message_callbacks:
                    try:
                        await callback(sender, recipient, content)
                    except Exception as e:
                        logger.error(f"Error in message callback: {e}")
                
                logger.debug(f"Routed message {routed_message_id} from {sender} to {recipient} in workspace {self.workspace_id}")
                return routed_message_id
            except ValueError:
                # Recipient not found locally, continue to parent/child routing
                pass
        
        # Handle USER recipient (no agent memory, just transcript)
        elif recipient == "USER":
            # Create transcript entry only
            transcript_entry = {
                "timestamp": datetime.now().isoformat(),
                "workspace_id": self.workspace_id,
                "from": sender,
                "to": recipient,
                "message_id": message_id,
                "content": content[:1000] if len(content) > 1000 else content,
            }
            self.router.add_transcript_entry(transcript_entry)
            logger.debug(f"Routed message {message_id} from {sender} to USER in workspace {self.workspace_id}")
            return message_id
        
        # Try routing to parent workspace
        if manager and self.parent_id:
            try:
                parent_workspace = manager.get_workspace(self.parent_id)
                routed_id = await parent_workspace.route_message(
                    sender, recipient, content, manager, message_id=message_id
                )
                if routed_id:
                    # Create transcript entry for parent routing
                    transcript_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "workspace_id": self.workspace_id,
                        "from": sender,
                        "to": recipient,
                        "message_id": routed_id,
                        "content": content[:1000] if len(content) > 1000 else content,
                    }
                    self.router.add_transcript_entry(transcript_entry)
                logger.debug(f"Routed message from {sender} to {recipient} via parent workspace {self.parent_id}")
                return routed_id
            except Exception as e:
                logger.debug(f"Could not route via parent: {e}")
        
        # Try routing to child workspaces
        if manager and self.children:
            for child_id in self.children:
                try:
                    child_workspace = manager.get_workspace(child_id)
                    if recipient in child_workspace.agents:
                        routed_id = await child_workspace.route_message(
                            sender, recipient, content, manager, message_id=message_id
                        )
                        if routed_id:
                            # Create transcript entry for child routing
                            transcript_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "workspace_id": self.workspace_id,
                                "from": sender,
                                "to": recipient,
                                "message_id": routed_id,
                                "content": content[:1000] if len(content) > 1000 else content,
                            }
                            self.router.add_transcript_entry(transcript_entry)
                        logger.debug(f"Routed message from {sender} to {recipient} via child workspace {child_id}")
                        return routed_id
                except Exception as e:
                    logger.debug(f"Could not route via child {child_id}: {e}")
        
        # Recipient not found
        logger.warning(f"Recipient '{recipient}' not found in workspace {self.workspace_id} or parent/children")
        # Still return message_id for transcript consistency
        return message_id
    
    async def broadcast(
        self,
        sender: str,
        content: str,
        manager: Optional[Any] = None,
    ) -> None:
        """
        Broadcast a message to all agents in this workspace.
        
        Args:
            sender: Name of sending agent
            content: Message content
            manager: Optional WorkspaceManager for parent/child routing
        """
        for agent_name in self.agents.keys():
            await self.route_message(sender, agent_name, content, manager)
    
    def add_agent(self, agent: Any) -> None:
        """
        Add an agent to this workspace.
        
        Supports both:
        - Local agents (built with Synqed)
        - Remote A2A agents (any agent implementing A2A protocol)
        
        Args:
            agent: Agent instance (local Agent or RemoteA2AAgent)
        """
        self.agents[agent.name] = agent
        
        # Register agent with router
        # Router will handle both local and remote agents
        self.router.register_agent(agent.name, agent)
        
        logger.debug(f"Added agent '{agent.name}' to workspace {self.workspace_id}")
    
    def add_child(self, workspace_id: str) -> None:
        """
        Add a child workspace ID to this workspace.
        
        Args:
            workspace_id: ID of child workspace
        """
        if workspace_id not in self.children:
            self.children.append(workspace_id)
            logger.debug(f"Added child workspace {workspace_id} to workspace {self.workspace_id}")
    
    def on_message(self, callback: Callable[[str, str, str], Awaitable[None]]) -> None:
        """
        Register a callback to be called when messages are routed.
        
        Args:
            callback: Async function(sender, recipient, content) -> None
        """
        self.message_callbacks.append(callback)
    
    def append_to_shared_plan(self, agent_name: str, content: str) -> None:
        """
        Append content to the shared plan document.
        
        This allows agents to organically update the shared plan as they work.
        
        Args:
            agent_name: Name of the agent updating the plan
            content: Content to append to the shared plan
        """
        if self.shared_plan:
            self.shared_plan += f"\n\n[{agent_name}] {content}"
        else:
            self.shared_plan = f"[{agent_name}] {content}"
    
    def add_blocking_requirement(self, agent_name: str, required_fields: list[str]) -> None:
        """
        Add blocking requirements when an agent needs user input.
        
        This consolidates all user input requests so the UI can show one
        combined prompt instead of multiple redundant requests.
        
        Args:
            agent_name: Name of the agent requesting input
            required_fields: List of field names needed (e.g., ["customer_name", "industry"])
        """
        # Track which agents are waiting
        if "agents_waiting" not in self.blocking_requirements:
            self.blocking_requirements["agents_waiting"] = []
        
        if agent_name not in self.blocking_requirements["agents_waiting"]:
            self.blocking_requirements["agents_waiting"].append(agent_name)
        
        # Consolidate required fields (dedupe)
        if "required_fields" not in self.blocking_requirements:
            self.blocking_requirements["required_fields"] = []
        
        for field in required_fields:
            if field not in self.blocking_requirements["required_fields"]:
                self.blocking_requirements["required_fields"].append(field)
        
        self.waiting_for_user_input = True
    
    def clear_blocking_requirements(self) -> None:
        """Clear blocking requirements after user provides input."""
        self.blocking_requirements = {}
        self.waiting_for_user_input = False
    
    def get_blocking_summary(self) -> Optional[dict]:
        """
        Get consolidated blocking requirements summary for UI display.
        
        Returns:
            Dict with 'agents_waiting' and 'required_fields' if blocked, None if not
        """
        if not self.waiting_for_user_input:
            return None
        
        return {
            "agents_waiting": self.blocking_requirements.get("agents_waiting", []),
            "required_fields": self.blocking_requirements.get("required_fields", []),
            "workspace_id": self.workspace_id,
        }
    
    def log_routed_message(
        self,
        sender: str,
        recipient: str,
        message_id: str,
        content: str,
    ) -> None:
        """
        Log a routed message to the transcript.
        
        Args:
            sender: Name of sending agent
            recipient: Name of recipient agent
            message_id: Message ID
            content: Message content
        """
        from datetime import datetime
        transcript_entry = {
            "timestamp": datetime.now().isoformat(),
            "workspace_id": self.workspace_id,
            "from": sender,
            "to": recipient,
            "message_id": message_id,
            "content": content[:1000] if len(content) > 1000 else content,
        }
        self.router.add_transcript_entry(transcript_entry)
    
    def display_transcript(
        self,
        include_system_messages: bool = False,
        parse_json_content: bool = True,
        title: Optional[str] = None
    ) -> None:
        """
        Display the complete conversation transcript in a readable format.
        
        This utility method displays the transcript with automatic JSON parsing
        and formatting, making it easy to review agent conversations.
        
        Args:
            include_system_messages: Whether to include system messages like [startup]
            parse_json_content: Whether to parse JSON content and extract "content" field
            title: Optional title to display above the transcript
        """
        import json
        
        if title:
            print("\n" + "="*80)
            print(f"  {title}")
            print("="*80 + "\n")
        
        transcript = self.router.get_transcript()
        message_num = 0
        
        for entry in transcript:
            sender = entry.get("from", "?")
            recipient = entry.get("to", "?")
            content = entry.get("content", "")
            
            # Skip system messages unless requested
            if not include_system_messages:
                if content == "[startup]" or content.startswith("[subteam_result]"):
                    continue
            
            message_num += 1
            
            # Clean format: agent name and email only (no arrows)
            print(f"[Message {message_num}]")
            print(f"  From: {sender}")
            print(f"  To: {recipient}")
            print("-" * 80)
            
            # Parse and display content
            display_content = content
            if parse_json_content:
                try:
                    parsed = json.loads(content)
                    if isinstance(parsed, dict) and "send_to" in parsed and "content" in parsed:
                        # It's a structured message, show the actual content
                        display_content = parsed["content"]
                except (json.JSONDecodeError, TypeError):
                    # Not JSON, show as-is
                    pass
            
            print(display_content)
            print()
        
        if message_num == 0:
            print("(No messages in transcript)")
            print()
    
    def get_completion_status(self) -> dict:
        """
        Analyze the transcript to determine task completion status.
        
        This utility method checks if:
        - Any message was successfully sent to USER (task completed)
        - Any attempted messages to USER (malformed/truncated)
        
        Returns:
            Dictionary with completion status information:
            {
                "completed": bool,  # True if message successfully sent to USER
                "attempted": int,   # Number of attempted USER messages (malformed)
                "total_messages": int,  # Total non-system messages
                "status_message": str  # Human-readable status
            }
        """
        transcript = self.router.get_transcript()
        
        # Check if task completed (any message to USER)
        task_completed = any(
            entry.get("to") == "USER" 
            for entry in transcript
            if entry.get("content", "") not in ["[startup]", ""] 
            and not entry.get("content", "").startswith("[subteam_result]")
        )
        
        # Count malformed attempts to send to USER or planner (coordinator)
        # Agents should respond to "planner" (not "USER") - planner is the CEO
        attempted_user_messages = 0
        for entry in transcript:
            content = entry.get("content", "")
            to_field = entry.get("to", "")
            # Only count non-routed attempts
            if to_field not in ["USER", "planner"]:
                if ('"send_to": "USER"' in content or '"send_to":"USER"' in content or
                    '"send_to": "planner"' in content or '"send_to":"planner"' in content):
                    attempted_user_messages += 1
        
        # Count total non-system messages
        total_messages = sum(
            1 for entry in transcript
            if entry.get("content", "") not in ["[startup]", ""]
            and not entry.get("content", "").startswith("[subteam_result]")
        )
        
        # Build status message
        if task_completed:
            status_message = "✅ Task completed successfully (message sent to planner/USER)"
        elif attempted_user_messages > 0:
            status_message = (
                f"⚠️  Task incomplete ({attempted_user_messages} attempt(s) to send to planner/USER, "
                f"but JSON was malformed/truncated)\n"
                f"    Suggestion: Increase max_tokens to allow complete responses"
            )
        else:
            status_message = "⚠️  Task incomplete (no message sent to USER)"
        
        return {
            "completed": task_completed,
            "attempted": attempted_user_messages,
            "total_messages": total_messages,
            "status_message": status_message
        }
    
    def print_summary(self) -> None:
        """
        Print a summary of the workspace execution.
        
        This displays:
        - Total message count
        - Completion status
        - Any relevant warnings or suggestions
        """
        status = self.get_completion_status()
        
        print("="*80)
        print("  SUMMARY")
        print("="*80)
        print(f"Workspace: {self.workspace_id}")
        print(f"Total messages: {status['total_messages']}")
        print(f"Status: {status['status_message']}")
        print()
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Workspace(id='{self.workspace_id}', "
            f"agents={len(self.agents)}, children={len(self.children)}, "
            f"parent_id={self.parent_id})"
        )


class WorkspaceManager:
    """
    Manages hierarchical workspaces for multi-agent execution.
    
    This class is responsible for:
    - Creating workspaces from TaskTreeNode specifications
    - Storing and retrieving workspaces
    - Linking parent-child workspace relationships
    - Destroying workspaces
    
    It is NOT responsible for:
    - Planning (use PlannerLLM)
    - Agent logic (use Agent class)
    - Agent runtime management (use AgentRuntimeRegistry)
    - HTTP server management (handled elsewhere)
    
    Example:
        ```python
        manager = WorkspaceManager(workspaces_root=Path("/tmp/workspaces"))
        
        # Register agent runtimes
        AgentRuntimeRegistry.register("Writer", writer_agent)
        AgentRuntimeRegistry.register("Editor", editor_agent)
        
        # Create root workspace
        root_workspace = await manager.create_workspace(
            task_tree_node=root_node,
            parent_workspace_id=None
        )
        
        # Create child workspace
        child_workspace = await manager.create_workspace(
            task_tree_node=child_node,
            parent_workspace_id=root_workspace.workspace_id
        )
        ```
    """
    
    def __init__(
        self,
        workspaces_root: Optional[Path] = None,
    ):
        """
        Initialize the workspace manager.
        
        Args:
            workspaces_root: Optional root directory for workspace metadata/logs
        """
        self.workspaces_root = workspaces_root or Path("/tmp/synqed_workspaces")
        self.workspaces: dict[str, Workspace] = {}
        
        # Ensure workspaces root exists
        self.workspaces_root.mkdir(parents=True, exist_ok=True)
    
    def _generate_workspace_id(self) -> str:
        """
        Generate a deterministic workspace ID.
        
        Returns:
            Unique workspace ID string
        """
        return f"ws-{uuid.uuid4().hex[:12]}"
    
    async def create_workspace(
        self,
        task_tree_node: Any,  # TaskTreeNode from planner module
        parent_workspace_id: Optional[str] = None,
    ) -> Workspace:
        """
        Create a new workspace from a TaskTreeNode specification.
        
        This method:
        - Generates a workspace_id
        - Creates a directory for metadata/logs (if workspaces_root is set)
        - Extracts required agent roles from TaskTreeNode.required_agents
        - Requests agent instances from AgentRuntimeRegistry
        - Creates a MessageRouter
        - Registers the workspace in self.workspaces
        - Links to parent workspace if provided
        
        Args:
            task_tree_node: TaskTreeNode specifying the workspace requirements
            parent_workspace_id: Optional ID of parent workspace
            
        Returns:
            Created Workspace instance
            
        Raises:
            ValueError: If parent workspace is not found or required agents are missing
        """
        # Generate workspace ID
        workspace_id = self._generate_workspace_id()
        
        # Create workspace directory for metadata/logs
        workspace_dir = self.workspaces_root / workspace_id
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract required agents from TaskTreeNode
        required_agents = getattr(task_tree_node, "required_agents", [])
        if not isinstance(required_agents, list):
            raise ValueError("TaskTreeNode.required_agents must be a list")
        
        # Get fresh agent instances from registry (cloned per workspace)
        agents: dict[str, Agent] = {}
        missing_agents = []
        
        for agent_role in required_agents:
            agent = AgentRuntimeRegistry.create_instance(agent_role, workspace_id)
            if agent is None:
                missing_agents.append(agent_role)
            else:
                # Key by role name (workspace provides scoping, key remains logical role)
                agents[agent_role] = agent
        
        if missing_agents:
            raise ValueError(
                f"Missing agent runtimes for roles: {missing_agents}. "
                f"Register them with AgentRuntimeRegistry.register()"
            )
        
        # Determine workspace depth
        depth = 0
        if parent_workspace_id:
            parent_workspace = self.workspaces.get(parent_workspace_id)
            if parent_workspace:
                depth = parent_workspace.depth + 1
        
        # Create message router
        router = MessageRouter()
        
        # Extract workspace metadata from TaskTreeNode
        from datetime import datetime
        workspace_name = getattr(task_tree_node, "id", workspace_id)
        workspace_description = getattr(task_tree_node, "description", "")
        created_at = datetime.utcnow().isoformat() + "Z"
        
        # Create workspace
        workspace = Workspace(
            workspace_id=workspace_id,
            parent_id=parent_workspace_id,
            subtask_id=getattr(task_tree_node, "id", None),
            directory=workspace_dir,
            router=router,
            agents={},  # Will be populated by add_agent calls
            children=[],
            depth=depth,
            subteam_requests={},
            workspace_name=workspace_name,
            workspace_description=workspace_description,
            created_at=created_at,
        )
        
        # Initialize agent memory with workspace_id and register agents
        for agent_role, agent in agents.items():
            # Initialize memory with workspace_id (only for local agents)
            if hasattr(agent, 'memory'):
                agent.memory.workspace_id = workspace_id
            workspace.add_agent(agent)
        
        # Register workspace
        self.workspaces[workspace_id] = workspace
        
        # Link to parent if provided
        if parent_workspace_id:
            if parent_workspace_id not in self.workspaces:
                raise ValueError(f"Parent workspace '{parent_workspace_id}' not found")
            self.workspaces[parent_workspace_id].add_child(workspace_id)
        
        logger.info(
            f"Created workspace {workspace_id} with {len(agents)} agents "
            f"(parent: {parent_workspace_id})"
        )
        
        return workspace
    
    async def destroy_workspace(self, workspace_id: str) -> None:
        """
        Destroy a workspace and clean up resources.
        
        This method:
        - Removes workspace from parent's children list
        - Recursively destroys child workspaces
        - Removes workspace directory (if exists)
        - Removes workspace from workspaces dictionary
        
        Args:
            workspace_id: ID of workspace to destroy
            
        Raises:
            ValueError: If workspace is not found
        """
        if workspace_id not in self.workspaces:
            raise ValueError(f"Workspace '{workspace_id}' not found")
        
        workspace = self.workspaces[workspace_id]
        
        # Remove from parent's children
        if workspace.parent_id and workspace.parent_id in self.workspaces:
            parent = self.workspaces[workspace.parent_id]
            if workspace_id in parent.children:
                parent.children.remove(workspace_id)
        
        # Recursively destroy children
        for child_id in list(workspace.children):
            await self.destroy_workspace(child_id)
        
        # Remove workspace directory
        try:
            import shutil
            workspace_dir = self.workspaces_root / workspace_id
            if workspace_dir.exists():
                shutil.rmtree(workspace_dir)
        except Exception as e:
            logger.warning(f"Error removing workspace directory: {e}")
        
        # Remove from workspaces
        del self.workspaces[workspace_id]
        
        logger.info(f"Destroyed workspace {workspace_id}")
    
    def get_workspace(self, workspace_id: str) -> Workspace:
        """
        Get a workspace by ID.
        
        Args:
            workspace_id: ID of workspace to retrieve
            
        Returns:
            Workspace instance
            
        Raises:
            ValueError: If workspace is not found
        """
        if workspace_id not in self.workspaces:
            raise ValueError(f"Workspace '{workspace_id}' not found")
        
        return self.workspaces[workspace_id]
    
    def get_workspace_tree(self, root_workspace_id: Optional[str] = None) -> dict:
        """
        Get hierarchical tree of all workspaces or starting from a specific root.
        
        Args:
            root_workspace_id: Optional root workspace ID. If None, returns all root workspaces.
            
        Returns:
            Dictionary containing workspace tree with metadata
        """
        def build_tree_node(workspace: Workspace) -> dict:
            """Recursively build tree node for a workspace"""
            agent_list = []
            for agent_name, agent in workspace.agents.items():
                email = getattr(agent, 'email', None) or f"{agent_name}@{workspace.workspace_id}"
                agent_list.append({
                    "name": agent_name,
                    "email": email,
                    "role": getattr(agent, 'role', None) or agent_name,
                    "description": getattr(agent, 'description', ''),
                })
            
            children_nodes = []
            for child_id in workspace.children:
                if child_id in self.workspaces:
                    child_workspace = self.workspaces[child_id]
                    children_nodes.append(build_tree_node(child_workspace))
            
            return {
                "workspace_id": workspace.workspace_id,
                "workspace_name": workspace.workspace_name,
                "description": workspace.workspace_description,
                "depth": workspace.depth,
                "parent_id": workspace.parent_id,
                "agents": agent_list,
                "children": children_nodes,
                "is_running": workspace.is_running,
                "created_at": workspace.created_at,
                "message_count": len(workspace.router.get_transcript()),
            }
        
        if root_workspace_id:
            # Return tree starting from specific root
            if root_workspace_id not in self.workspaces:
                raise ValueError(f"Workspace '{root_workspace_id}' not found")
            root_workspace = self.workspaces[root_workspace_id]
            return build_tree_node(root_workspace)
        else:
            # Return all root workspaces (depth=0)
            root_workspaces = [
                ws for ws in self.workspaces.values() if ws.depth == 0
            ]
            return {
                "roots": [build_tree_node(ws) for ws in root_workspaces],
                "total_workspaces": len(self.workspaces),
            }
    
    def link_subteam(
        self,
        parent_workspace_id: str,
        subteam_workspace_id: str,
    ) -> None:
        """
        Link a subteam workspace to its parent workspace.
        
        This updates the parent's children list and the subteam's parent_id.
        
        Args:
            parent_workspace_id: ID of parent workspace
            subteam_workspace_id: ID of subteam workspace
            
        Raises:
            ValueError: If either workspace is not found
        """
        if parent_workspace_id not in self.workspaces:
            raise ValueError(f"Parent workspace '{parent_workspace_id}' not found")
        
        if subteam_workspace_id not in self.workspaces:
            raise ValueError(f"Subteam workspace '{subteam_workspace_id}' not found")
        
        parent = self.workspaces[parent_workspace_id]
        subteam = self.workspaces[subteam_workspace_id]
        
        # Update parent's children
        parent.add_child(subteam_workspace_id)
        
        # Update subteam's parent_id
        subteam.parent_id = parent_workspace_id
        
        logger.info(f"Linked subteam {subteam_workspace_id} to parent {parent_workspace_id}")
    
    def list_workspaces(self) -> list[str]:
        """
        List all workspace IDs.
        
        Returns:
            List of workspace IDs
        """
        return list(self.workspaces.keys())
    
    def get_root_workspaces(self) -> list[Workspace]:
        """
        Get all root workspaces (workspaces with no parent).
        
        Returns:
            List of root Workspace instances
        """
        return [
            workspace
            for workspace in self.workspaces.values()
            if workspace.parent_id is None
        ]
    
    def __repr__(self) -> str:
        """String representation."""
        return f"WorkspaceManager(workspaces={len(self.workspaces)}, root={self.workspaces_root})"


# ============================================================================
# Usage Example
# ============================================================================
"""
Example usage demonstrating independent Agent instances per workspace:

```python
from synqed.workspace_manager import WorkspaceManager, AgentRuntimeRegistry
from synqed.agent import Agent
from synqed.memory import AgentMemory

# Create agent prototypes
async def writer_logic(context):
    return context.build_response("Editor", "Draft ready")

async def editor_logic(context):
    return context.build_response("Writer", "Review complete")

writer_prototype = Agent(
    name="Writer",
    description="Writer agent",
    logic=writer_logic,
    default_target="Editor"
)

editor_prototype = Agent(
    name="Editor",
    description="Editor agent",
    logic=editor_logic,
    default_target="Writer"
)

# Register prototypes (not instances)
AgentRuntimeRegistry.register("Writer", writer_prototype)
AgentRuntimeRegistry.register("Editor", editor_prototype)

# Create workspace manager
manager = WorkspaceManager(workspaces_root=Path("/tmp/workspaces"))

# Create first workspace
class TaskNode1:
    required_agents = ["Writer", "Editor"]
    id = "task1"

workspace1 = await manager.create_workspace(
    task_tree_node=TaskNode1(),
    parent_workspace_id=None
)

# Create second workspace with same roles
class TaskNode2:
    required_agents = ["Writer", "Editor"]
    id = "task2"

workspace2 = await manager.create_workspace(
    task_tree_node=TaskNode2(),
    parent_workspace_id=None
)

# Even though both workspaces use "Writer" and "Editor" roles,
# each workspace gets its own independent Agent instances.
# Modifying one workspace's agent memory does not affect the other:

# Send message to Writer in workspace1
await workspace1.route_message("USER", "Writer", "Write story 1")
# workspace1.agents["Writer"].memory now has 1 message

# Send message to Writer in workspace2
await workspace2.route_message("USER", "Writer", "Write story 2")
# workspace2.agents["Writer"].memory now has 1 message (independent)

# The agents are cloned instances - they share the same logic function
# but have separate memory and state.
```
"""
