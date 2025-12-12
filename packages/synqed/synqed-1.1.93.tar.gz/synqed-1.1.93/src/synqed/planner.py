"""
PlannerLLM - LLM-powered hierarchical task-tree planning and subteam creation.

This module provides:
- PlannerLLM: Pure planning logic for generating hierarchical task trees
- SubteamApprovalController: Handles user approval workflow for subteam requests
- TaskTreeNode: Recursive tree node structure
- TaskTreePlan: Complete task plan with metadata
"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional, Callable, Awaitable
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)


class TaskTreeNode(BaseModel):
    """
    Represents a node in a hierarchical task tree.
    
    This is a recursive structure where each node can have child nodes,
    creating a tree of tasks and subtasks.
    """
    id: str = Field(description="Unique identifier for this task node")
    description: str = Field(description="Description of what needs to be done")
    required_agents: list[str] = Field(description="List of agent names/types needed for this task")
    may_need_subteams: Optional[bool] = Field(default=None, description="Whether this task may require deeper subteams")
    children: list[TaskTreeNode] = Field(default_factory=list, description="List of child task nodes")
    
    @model_validator(mode="after")
    def set_may_need_subteams(self) -> "TaskTreeNode":
        """Automatically set may_need_subteams based on children if not explicitly provided."""
        # If explicitly provided, keep that value
        if self.may_need_subteams is not None:
            return self
        # Otherwise, set based on whether node has children
        self.may_need_subteams = len(self.children) > 0
        return self
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> TaskTreeNode:
        """Create from JSON string."""
        return cls.model_validate_json(json_str)
    
    def __repr__(self) -> str:
        """String representation."""
        children_count = len(self.children)
        return f"TaskTreeNode(id='{self.id}', agents={self.required_agents}, children={children_count})"


class TaskTreePlan(BaseModel):
    """
    Machine-readable hierarchical task plan with a root node containing nested children.
    
    The structure is recursive: root -> children -> children -> ...
    """
    task_id: str = Field(description="Unique identifier for the overall task")
    original_task: str = Field(description="The original user task string")
    schema_version: int = Field(default=1, description="Schema version for compatibility")
    root: TaskTreeNode = Field(description="Root node of the task tree")
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> TaskTreePlan:
        """Create from JSON string."""
        return cls.model_validate_json(json_str)
    
    def flatten_tree(self) -> list[TaskTreeNode]:
        """
        Flatten the tree into a list of all nodes.
        
        Returns:
            List of all TaskTreeNode objects in depth-first order
        """
        result: list[TaskTreeNode] = []
        
        def traverse(node: TaskTreeNode) -> None:
            result.append(node)
            for child in node.children:
                traverse(child)
        
        traverse(self.root)
        return result
    
    def find_node(self, node_id: str) -> Optional[TaskTreeNode]:
        """
        Find a node by ID in the tree.
        
        Args:
            node_id: ID of the node to find
            
        Returns:
            TaskTreeNode if found, None otherwise
        """
        def search(node: TaskTreeNode) -> Optional[TaskTreeNode]:
            if node.id == node_id:
                return node
            for child in node.children:
                result = search(child)
                if result:
                    return result
            return None
        
        return search(self.root)
    
    def reindex(self) -> "TaskTreePlan":
        """
        Reassign global, deterministic, collision-free IDs across the entire tree.
        
        Deep copies self.root, rebuilds every node ID deterministically
        (root → root.0 → root.0.1 etc.), and assigns it back to self.root.
        
        Returns:
            Self for method chaining
        """
        def assign_ids(node: TaskTreeNode, prefix: str = "root") -> TaskTreeNode:
            """Recursively assign IDs to nodes via DFS."""
            # Set ID for current node
            node.id = prefix
            
            # Recursively assign IDs to children
            for idx, child in enumerate(node.children):
                child_prefix = f"{prefix}.{idx}"
                assign_ids(child, child_prefix)
            
            return node
        
        # Deep copy self.root to avoid mutating during assignment
        import copy
        root_copy = copy.deepcopy(self.root)
        
        # Do a full DFS and rewrite all IDs top-down
        self.root = assign_ids(root_copy, "root")
        
        return self
    
    def attach_subtree(self, parent_id: str, subtree: TaskTreeNode) -> "TaskTreePlan":
        """
        Attach a subtree to a parent node identified by parent_id.
        
        Locates the parent node by ID, appends the subtree, then calls reindex().
        
        Args:
            parent_id: ID of the parent node to attach to
            subtree: The subtree to attach
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If parent node is not found
        """
        def find_and_attach(node: TaskTreeNode) -> TaskTreeNode:
            """Recursively find parent and attach subtree."""
            # Check if this node is the parent
            if node.id == parent_id:
                # Create new node with subtree attached
                new_children = list(node.children)
                new_children.append(subtree)
                return TaskTreeNode(
                    id=node.id,
                    description=node.description,
                    required_agents=node.required_agents,
                    may_need_subteams=node.may_need_subteams,
                    children=new_children
                )
            
            # Recursively search in children
            new_children = []
            for child in node.children:
                new_child = find_and_attach(child)
                new_children.append(new_child)
            
            # Create new node with updated children
            return TaskTreeNode(
                id=node.id,
                description=node.description,
                required_agents=node.required_agents,
                may_need_subteams=node.may_need_subteams,
                children=new_children
            )
        
        # Verify parent exists before attaching
        if self.find_node(parent_id) is None:
            raise ValueError(f"Parent node with ID '{parent_id}' not found in tree")
        
        # Find parent and attach subtree
        self.root = find_and_attach(self.root)
        
        # Globally reindex the entire tree
        self.reindex()
        
        return self
    
    def replace_node(self, target_id: str, new_subtree: TaskTreeNode) -> "TaskTreePlan":
        """
        Replace a node in the tree with a new subtree.
        
        DFS searches for target, replaces target with new_subtree, then calls reindex().
        
        Args:
            target_id: ID of the node to replace
            new_subtree: New subtree to replace the target node with
            
        Returns:
            Self for method chaining
        """
        def replace_recursive(node: TaskTreeNode) -> TaskTreeNode:
            """Recursively search and replace."""
            # Check if this node matches
            if node.id == target_id:
                return new_subtree
            
            # Recursively replace in children
            new_children = []
            for child in node.children:
                new_child = replace_recursive(child)
                new_children.append(new_child)
            
            # Create new node with updated children
            return TaskTreeNode(
                id=node.id,
                description=node.description,
                required_agents=node.required_agents,
                may_need_subteams=node.may_need_subteams,
                children=new_children
            )
        
        # Perform replacement
        self.root = replace_recursive(self.root)
        
        # Globally reindex the entire tree
        self.reindex()
        
        return self
    
    def update_subtree(self, parent_id: str, subtree: TaskTreeNode) -> "TaskTreePlan":
        """
        Shortcut that attaches subtree then reindexes.
        
        Equivalent to: attach_subtree(parent_id, subtree)
        
        Args:
            parent_id: ID of the parent node to attach to
            subtree: The subtree to attach
            
        Returns:
            Self for method chaining
        """
        return self.attach_subtree(parent_id, subtree)
    
    def __repr__(self) -> str:
        """String representation."""
        total_nodes = len(self.flatten_tree())
        return f"TaskTreePlan(task_id='{self.task_id}', total_nodes={total_nodes}, schema_version={self.schema_version})"


class SubteamApprovalController:
    """
    Handles user approval workflow for subteam requests.
    
    This class manages workspace pausing/resuming and user interaction,
    keeping PlannerLLM free of IO concerns.
    """
    
    def __init__(
        self,
        user_prompt_callback: Optional[Callable[[str], Awaitable[str]]] = None,
    ):
        """
        Initialize the approval controller.
        
        Args:
            user_prompt_callback: Optional async callback for user prompts.
                                 If None, uses input() for synchronous prompts.
        """
        self.user_prompt_callback = user_prompt_callback
    
    async def approve(
        self,
        request_json: dict[str, Any],
        workspace: Any,
    ) -> bool:
        """
        Handle approval workflow for a subteam request.
        
        This method:
        1. Pauses the workspace execution
        2. Prompts the human user for approval
        3. Returns True if approved, False if rejected
        4. Resumes workspace execution
        
        Args:
            request_json: Request dictionary containing at least:
                - requesting_agent: Name of the agent making the request
                - reason: Reason for the request
            workspace: Workspace object with pause() and resume() methods
            
        Returns:
            True if approved, False if rejected
        """
        requesting_agent = request_json.get("requesting_agent", "Unknown")
        reason = request_json.get("reason", "")
        
        # Pause workspace execution
        if hasattr(workspace, "pause"):
            await workspace.pause()
            logger.info(f"Paused workspace due to subteam request from {requesting_agent}")
        else:
            logger.warning("Workspace does not have pause() method, continuing without pausing")
        
        # Prompt user for approval
        prompt_message = (
            f"Agent {requesting_agent} requests new subteam.\n"
            f"Reason: {reason}\n"
            f"Approve? (yes/no): "
        )
        
        try:
            if self.user_prompt_callback:
                user_response = await self.user_prompt_callback(prompt_message)
            else:
                # Synchronous fallback
                user_response = input(prompt_message).strip().lower()
            
            approved = user_response in ("yes", "y")
            
            # Resume workspace
            if hasattr(workspace, "resume"):
                await workspace.resume()
                logger.info(f"Resumed workspace (request {'approved' if approved else 'rejected'})")
            
            return approved
                
        except Exception as e:
            # On error, resume workspace
            if hasattr(workspace, "resume"):
                await workspace.resume()
            raise


class PlannerLLM:
    """
    Pure planning logic for generating hierarchical task trees.
    
    This class:
    - Accepts user task strings and breaks them into hierarchical task trees
    - Determines required agents for each node in the tree
    - Generates subtrees for subteam requests
    - Always outputs valid hierarchical JSON
    
    This class does NOT handle:
    - User interaction (use SubteamApprovalController)
    - Workspace pausing/resuming (use SubteamApprovalController)
    - Input/output operations
    
    Example:
        ```python
        import os
        from dotenv import load_dotenv
        
        # Load API key from .env file in your own script
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        planner = PlannerLLM(
            provider="openai",
            api_key=api_key,
            model="gpt-4o"
        )
        
        task_plan = await planner.plan_task("Build a web application with authentication")
        
        # Generate subtree for subteam request
        if request_json.get("action") == "request_subteam":
            subtree_root = await planner.create_subteam_subtree(request_json)
        ```
    """
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the PlannerLLM.
        
        Args:
            provider: LLM provider name ("openai" or "anthropic")
            api_key: API key for the LLM provider (required)
            model: Model name (e.g., "gpt-4o", "claude-sonnet-4-5")
            base_url: Optional base URL for API (useful for proxies)
        
        Raises:
            ValueError: If api_key is not provided
        """
        self.provider = provider.lower()
        
        if not api_key:
            raise ValueError(
                f"api_key is required for provider '{self.provider}'. "
                "Provide it as a parameter. If loading from .env file, do that in your own script."
            )
        
        self.api_key = api_key
        self.model = model or self._get_default_model()
        self.base_url = base_url
        
        # Initialize LLM client
        self._client = self._initialize_client()
    
    def _get_default_model(self) -> str:
        """Get default model based on provider."""
        if self.provider == "openai":
            return "gpt-4o"
        elif self.provider == "anthropic":
            return "claude-sonnet-4-5"
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_client(self) -> Any:
        """Initialize the LLM client based on provider."""
        if self.provider == "openai":
            try:
                from openai import AsyncOpenAI
                return AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError(
                    "openai package is required. Install with: pip install openai"
                )
        elif self.provider == "anthropic":
            try:
                import anthropic
                return anthropic.AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "anthropic package is required. Install with: pip install anthropic"
                )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def plan_task(self, user_task: str, task_id: Optional[str] = None) -> TaskTreePlan:
        """
        Break a user task into a hierarchical task tree with agent assignments.
        
        This method automatically queries the AgentRuntimeRegistry to discover
        available agents and their capabilities, ensuring only registered agents
        are assigned to tasks.
        
        Args:
            user_task: The user's task description
            task_id: Optional unique identifier for the task
            
        Returns:
            TaskTreePlan object with hierarchical root node and nested children
            
        Raises:
            ValueError: If LLM response is not valid JSON or doesn't match schema
        """
        import uuid
        task_id = task_id or str(uuid.uuid4())
        
        # Query AgentRuntimeRegistry to get available agents
        from synqed.workspace_manager import AgentRuntimeRegistry
        
        available_agents = []
        for role in AgentRuntimeRegistry.list_roles():
            agent = AgentRuntimeRegistry.get(role)
            if agent:
                # Get agent capabilities from agent metadata
                caps = agent.capabilities if agent.capabilities else ["general tasks"]
                available_agents.append({
                    "name": role,
                    "description": agent.description,
                    "capabilities": caps
                })
        
        # Build agent roster for system prompt
        if available_agents:
            agent_roster = "\n".join([
                f"  - {a['name']}: {a['description']}\n    Capabilities: {', '.join(a['capabilities'])}"
                for a in available_agents
            ])
            agent_constraint = f"""
AVAILABLE AGENTS (you MUST ONLY use these agents):
{agent_roster}

CRITICAL: Only assign tasks to the agents listed above. Match agent capabilities to task requirements."""
        else:
            agent_constraint = "Note: No agents registered yet. Use generic role names."
        
        system_prompt = f"""You are a hierarchical task planning expert. Break the user's task into a recursive tree structure.

{agent_constraint}

COORDINATOR SELECTION RULES:
The execution engine automatically selects a root coordinator for cross-workspace coordination using this ranking (highest to lowest priority):
1. 'coordinator' (highest priority)
2. 'manager'
3. 'lead'
4. 'director'
5. 'chief'
6. 'head'
7. 'orchestrator' (lowest priority)

When distributing agents, be aware that an agent with the highest-priority coordination keyword will be moved to the root workspace to serve as cross-workspace coordinator. Plan accordingly.

CRITICAL RULES FOR ROOT NODE:
- If you create child nodes, the root node should have ONLY coordination/management agents that don't appear in children
- If you create child nodes, you MUST NOT duplicate agents between root and children
- Each agent can appear in ONLY ONE location (either root OR one child, never both)

Respond with a SINGLE JSON object representing the ROOT TaskTreeNode ONLY:

{{
  "id": "placeholder",
  "description": "overall task description",
  "required_agents": ["agent_name1", "agent_name2"],
  "may_need_subteams": true,
  "children": [
    {{
      "id": "placeholder",
      "description": "subtask A description",
      "required_agents": ["agent_name1", "agent_name2"],
      "may_need_subteams": true,
      "children": [
        {{
          "id": "placeholder",
          "description": "subtask A1 description",
          "required_agents": ["agent_name3", "agent_name4"],
          "may_need_subteams": false,
          "children": []
        }}
      ]
    }},
    {{
      "id": "placeholder",
      "description": "subtask B description",
      "required_agents": ["agent_name5", "agent_name6"],
      "may_need_subteams": false,
      "children": []
    }}
  ]
}}

RULES:
- Output ONLY a single JSON object representing the root node.
- Do NOT include task_id, original_task, wrapper objects, or extra fields.
- Every node MUST have: id, description, required_agents, may_need_subteams (optional), children.
- Children MUST follow the exact same schema recursively.
- ONLY use agent names from the AVAILABLE AGENTS list above.
- Match agent capabilities to task requirements when assigning agents.
- MINIMUM 2 AGENTS per subtask/workspace: Each child node should have at least 2 agents assigned to enable collaboration. Pair agents with complementary capabilities.
- DO NOT DUPLICATE AGENTS: Each agent should appear in ONLY ONE child workspace. Distribute agents efficiently across workspaces.
- If you have N agents, create at most N/2 child workspaces (since each needs minimum 2 agents).
- Group related agents together in the same workspace for efficient collaboration.
- Ignore IDs; placeholder IDs are acceptable, they will be replaced by the system. Focus on correct tree structure.
- Output NOTHING except valid JSON."""
        
        user_prompt = f"""Break down this task into a hierarchical task tree with agent assignments:

Task: {user_task}

Create a recursive tree structure where complex tasks are broken into subtasks, and those subtasks can have their own children.
Assign agents from the available list based on their capabilities.

CRITICAL AGENT ALLOCATION RULES:
1. MINIMUM 2 AGENTS per child workspace for collaboration
2. NO DUPLICATE AGENTS - each agent appears in ONLY ONE child workspace
3. With N available agents, create at most N/2 child workspaces
4. Group related agents together (e.g., put content_curator with speaker_coordinator, put venue_manager with catering_manager)
5. Distribute agents efficiently - don't leave any agents unassigned

Respond with valid JSON only."""
        
        # Make LLM call
        response_text = await self._call_llm(system_prompt, user_prompt)
        
        # Parse and validate response
        try:
            # Extract JSON from response
            json_str = self.extract_json(response_text)
            node_dict = json.loads(json_str)
            
            # Parse root node only (ignore any wrapper fields)
            root_node = TaskTreeNode.model_validate(node_dict)
            
            # Generate stable IDs
            root_node = self.generate_stable_ids(root_node)
            
            # Wrap root into TaskTreePlan
            task_plan = TaskTreePlan(
                task_id=task_id,
                original_task=user_task,
                schema_version=1,
                root=root_node
            )
            
            # Reindex the plan before returning
            task_plan.reindex()
            
            # Validate tree structure
            self.validate_tree_structure(task_plan.root)
            
            return task_plan
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(
                f"Invalid JSON. Received: {response_text[:200]}"
            ) from e
    
    def validate_tree_structure(self, node: TaskTreeNode, visited_ids: Optional[set[str]] = None) -> None:
        """
        Validate the tree structure recursively.
        
        Args:
            node: The node to validate
            visited_ids: Set of already visited node IDs (to detect cycles)
            
        Raises:
            ValueError: If tree structure is invalid
        """
        if visited_ids is None:
            visited_ids = set()
        
        # Check for duplicate IDs
        if node.id in visited_ids:
            raise ValueError(f"Duplicate node ID found: {node.id}")
        visited_ids.add(node.id)
        
        # Validate node fields with strict type checking
        if not isinstance(node.id, str) or not node.id:
            raise ValueError(f"Node ID must be a non-empty string, got: {type(node.id)}")
        if not isinstance(node.description, str) or not node.description:
            raise ValueError(f"Node {node.id} description must be a non-empty string, got: {type(node.description)}")
        if not isinstance(node.required_agents, list):
            raise ValueError(f"Node {node.id} required_agents must be a list, got: {type(node.required_agents)}")
        # Validate required_agents contains only strings
        if not all(isinstance(agent, str) for agent in node.required_agents):
            raise ValueError(f"Node {node.id} required_agents must be list[str]")
        if not isinstance(node.children, list):
            raise ValueError(f"Node {node.id} children must be a list, got: {type(node.children)}")
        # Validate children contains only TaskTreeNode
        if not all(isinstance(child, TaskTreeNode) for child in node.children):
            raise ValueError(f"Node {node.id} children must be list[TaskTreeNode]")
        
        # Recursively validate children
        for child in node.children:
            self.validate_tree_structure(child, visited_ids)
    
    async def create_subteam_subtree(self, request_json: dict[str, Any]) -> TaskTreeNode:
        """
        Create a subtree for a subteam request based on request JSON.
        
        This method extracts relevant fields from request_json and generates
        a subtree using the LLM. All fields from request_json are passed as
        context to the LLM for better understanding.
        
        Args:
            request_json: Request dictionary containing:
                - requesting_agent: Name of the agent requesting the subteam
                - reason: Reason for the subteam request
                - parent_node_id: Optional parent node ID for context
                - Any other fields will be passed as context to the LLM
        
        Returns:
            TaskTreeNode object representing the root of the new subteam tree
            
        Raises:
            ValueError: If required fields are missing or LLM response is invalid
        """
        requesting_agent = request_json.get("requesting_agent")
        reason = request_json.get("reason", "")
        parent_id = request_json.get("parent_node_id")
        
        if not requesting_agent:
            raise ValueError("requesting_agent is required in request_json")
        
        # Extract all other fields as context
        context_fields = {k: v for k, v in request_json.items() 
                         if k not in ("action", "requesting_agent", "reason", "parent_node_id")}
        
        # Generate subtree using LLM
        subtree_root = await self.generate_subtree(
            requesting_agent=requesting_agent,
            reason=reason,
            parent_id=parent_id,
            context_fields=context_fields
        )
        
        return subtree_root
    
    async def generate_subtree(
        self,
        requesting_agent: str,
        reason: str,
        parent_id: Optional[str] = None,
        context_fields: Optional[dict[str, Any]] = None,
    ) -> TaskTreeNode:
        """
        Generate a subtree (TaskTreeNode) for a new subteam using the LLM.
        
        This creates a hierarchical tree structure that can be attached to an existing
        task tree as a child node.
        
        Args:
            requesting_agent: Name of the agent requesting the subteam
            reason: Reason for the subteam request
            parent_id: Optional parent node ID for context
            context_fields: Optional additional context fields to include in prompt
        
        Returns:
            TaskTreeNode object representing the root of the new subteam tree
        """
        system_prompt = """You are a subteam planning expert. When an agent requests a new subteam, you create a hierarchical task tree structure for that subteam.

Respond with a SINGLE JSON object representing the ROOT TaskTreeNode ONLY:

{
  "id": "placeholder",
  "description": "description of what this subteam will do",
  "required_agents": ["AgentType1", "AgentType2"],
  "may_need_subteams": true,
  "children": [
    {
      "id": "placeholder",
      "description": "subtask 1 description",
      "required_agents": ["AgentType3"],
      "may_need_subteams": false,
      "children": []
    }
  ]
}

RULES:
- Output ONLY a single JSON object representing the root node.
- Do NOT include task_id, original_task, wrapper objects, or extra fields.
- Every node MUST have: id, description, required_agents, may_need_subteams (optional), children.
- Children MUST follow the exact same schema recursively.
- Ignore IDs; placeholder IDs are acceptable, they will be replaced by the system. Focus on correct tree structure.
- Output NOTHING except valid JSON."""
        
        # Build context string
        context_parts = []
        if parent_id:
            context_parts.append(f"Parent task ID: {parent_id}")
        else:
            context_parts.append("This is a top-level subteam request")
        
        if context_fields:
            context_parts.append("\nAdditional context:")
            for key, value in context_fields.items():
                context_parts.append(f"  {key}: {value}")
        
        context = "\n".join(context_parts)
        
        user_prompt = f"""Agent {requesting_agent} requests a new subteam.

Reason: {reason}
{context}

Create a hierarchical task tree structure for this subteam. The tree should represent:
1. The overall subteam task (root node)
2. Subtasks that the subteam will handle (children nodes)
3. Required agents for each task

Respond with valid JSON only."""
        
        # Make LLM call
        response_text = await self._call_llm(system_prompt, user_prompt)
        
        # Parse and validate response
        try:
            json_str = self.extract_json(response_text)
            node_dict = json.loads(json_str)
            
            # Validate and create TaskTreeNode
            subtree_root = TaskTreeNode.model_validate(node_dict)
            
            # Generate stable IDs
            subtree_root = self.generate_stable_ids(subtree_root)
            
            # Validate tree structure
            self.validate_tree_structure(subtree_root)
            
            return subtree_root
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(
                f"Invalid JSON. Received: {response_text[:200]}"
            ) from e
    
    def generate_stable_ids(self, root: TaskTreeNode) -> TaskTreeNode:
        """
        Recursively assign deterministic IDs to all nodes in the tree.
        
        IDs follow the pattern:
        - root = "root"
        - root child index 0 = "root.0"
        - root child index 1 = "root.1"
        - child of root.0 with index 2 = "root.0.2"
        
        Args:
            root: The root node to assign IDs to
            
        Returns:
            TaskTreeNode with all nodes having deterministic IDs
        """
        def assign_ids(node: TaskTreeNode, prefix: str = "root") -> TaskTreeNode:
            """Recursively assign IDs to nodes."""
            # Set ID for current node
            node.id = prefix
            
            # Recursively assign IDs to children
            for idx, child in enumerate(node.children):
                child_prefix = f"{prefix}.{idx}"
                assign_ids(child, child_prefix)
            
            return node
        
        # Create a copy to avoid mutating the original
        import copy
        root_copy = copy.deepcopy(root)
        
        # Assign IDs starting from "root"
        return assign_ids(root_copy, "root")
    
    def extract_json(self, text: str) -> str:
        """
        Extract JSON from text, handling markdown fences.
        
        This method is strict: it will raise ValueError if no valid JSON
        object or array is found. It does not attempt to be permissive.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Extracted JSON string
            
        Raises:
            ValueError: If no valid JSON object or array can be extracted
        """
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]  # Remove ```json
        elif text.startswith("```"):
            text = text[3:]  # Remove ```
        
        if text.endswith("```"):
            text = text[:-3]  # Remove closing ```
        
        text = text.strip()
        
        # Try to find JSON array first (for agent specs)
        array_start = text.find("[")
        array_end = text.rfind("]")
        
        # Try to find JSON object
        obj_start = text.find("{")
        obj_end = text.rfind("}")
        
        # Determine which comes first - array or object
        json_str = None
        
        if array_start != -1 and array_end != -1 and array_end > array_start:
            # Check if array comes before object, or if there's no object
            if obj_start == -1 or array_start < obj_start:
                # Extract array
                json_str = text[array_start:array_end + 1]
        
        # If no array found or array extraction failed, try object
        if json_str is None:
            if obj_start != -1 and obj_end != -1 and obj_end > obj_start:
                json_str = text[obj_start:obj_end + 1]
        
        if json_str is None:
            raise ValueError(f"No valid JSON object or array found in text: {text[:200]}")
        
        # Validate it's parseable JSON
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError as e:
            raise ValueError(f"Extracted text is not valid JSON: {json_str[:200]}") from e
    
    async def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Make a call to the LLM API.
        
        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt/message
            
        Returns:
            Response text from the LLM
        """
        if self.provider == "openai":
            # Try to use response_format for JSON mode (available in newer OpenAI API versions)
            try:
                response = await self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1,  # Low temperature for consistent JSON output
                    response_format={"type": "json_object"}
                )
            except TypeError:
                # Fallback if response_format is not supported
                response = await self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1
                )
            return response.choices[0].message.content.strip()
        
        elif self.provider == "anthropic":
            response = await self._client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            return response.content[0].text.strip()
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def create_agents_from_task(
        self,
        user_task: str,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Dynamically create agent specifications based on the user task.
        
        This method analyzes the task and determines what agents are needed,
        then generates agent specifications including name, description, 
        capabilities, and role.
        
        Args:
            user_task: The user's task description
            provider: LLM provider for generated agents ("anthropic" or "openai")
            api_key: API key for the agent LLM (defaults to planner's API key)
            model: Model name for generated agents (defaults to planner's model)
            
        Returns:
            List of agent specifications, each containing:
            {
                "name": str,
                "description": str,
                "capabilities": list[str],
                "role": str,
                "provider": str,
                "api_key": str,
                "model": str
            }
            
        Example:
            ```python
            planner = PlannerLLM(provider="anthropic", api_key="...")
            
            agent_specs = await planner.create_agents_from_task(
                "Plan a wedding with vendors, budget, and timeline"
            )
            
            # agent_specs will contain specifications for agents like:
            # - wedding_planner: coordinates overall planning
            # - vendor_coordinator: manages vendor relationships
            # - budget_manager: tracks expenses and budget
            # - timeline_coordinator: manages schedules and deadlines
            ```
        """
        import uuid
        
        # Use provided credentials or fall back to planner's credentials
        agent_provider = provider
        agent_api_key = api_key or self.api_key
        agent_model = model or self.model
        
        system_prompt = """You are an expert at designing multi-agent systems. Given a task, determine what agents are needed to accomplish it.

For each agent, provide:
- name: snake_case identifier (e.g., "research_specialist")
- description: Clear description of the agent's purpose
- capabilities: List of specific capabilities/skills
- role: A team/domain identifier (e.g., "research_team", "engineering_team")

Output a JSON array of agent specifications:

[
  {
    "name": "agent_name",
    "description": "Agent description",
    "capabilities": ["capability1", "capability2", "capability3"],
    "role": "team_name"
  }
]

RULES:
- Create 2-6 agents depending on task complexity
- Each agent should have a clear, distinct purpose
- Agents should be able to collaborate and delegate work
- Include a coordinator/manager agent to orchestrate the work
- Use descriptive, professional names
- Capabilities should be specific and actionable
- Output ONLY valid JSON, nothing else

IMPORTANT - Coordinator Selection:
The execution engine will automatically select a root coordinator for cross-workspace coordination using this ranking system (highest to lowest priority):
1. 'coordinator' (highest priority)
2. 'manager'
3. 'lead'
4. 'director'
5. 'chief'
6. 'head'
7. 'orchestrator' (lowest priority)

When naming agents, if you want a specific agent to be selected as the cross-workspace coordinator, include one of these keywords in the agent's name (e.g., "project_coordinator", "team_manager", "tech_lead"). Agents with higher-priority keywords will be selected over those with lower-priority keywords. If multiple agents have the same keyword, the first one encountered will be selected."""
        
        user_prompt = f"""Analyze this task and design a multi-agent system to accomplish it:

Task: {user_task}

Create agent specifications that will work together effectively. Include agents with complementary skills.
Respond with valid JSON only."""
        
        # Make LLM call
        response_text = await self._call_llm(system_prompt, user_prompt)
        
        # Parse and validate response
        try:
            # Extract JSON from response
            json_str = self.extract_json(response_text)
            
            # Handle both array and object responses
            parsed = json.loads(json_str)
            
            # If response is wrapped in an object, extract the array
            if isinstance(parsed, dict):
                # Try common wrapper keys
                for key in ["agents", "agent_specs", "specifications", "agent_list"]:
                    if key in parsed and isinstance(parsed[key], list):
                        parsed = parsed[key]
                        break
                else:
                    # If no wrapper found but it's a single agent spec, wrap it
                    if "name" in parsed and "description" in parsed:
                        parsed = [parsed]
                    else:
                        raise ValueError("Response is a dict but doesn't contain agent specifications")
            
            if not isinstance(parsed, list):
                raise ValueError(f"Expected list of agents, got {type(parsed)}")
            
            # Validate and enrich agent specifications
            agent_specs = []
            for i, agent_spec in enumerate(parsed):
                if not isinstance(agent_spec, dict):
                    logger.warning(f"Skipping invalid agent spec at index {i}: not a dict")
                    continue
                
                # Validate required fields
                if "name" not in agent_spec or "description" not in agent_spec:
                    logger.warning(f"Skipping invalid agent spec at index {i}: missing name or description")
                    continue
                
                # Ensure capabilities is a list
                if "capabilities" not in agent_spec:
                    agent_spec["capabilities"] = ["general tasks"]
                elif not isinstance(agent_spec["capabilities"], list):
                    agent_spec["capabilities"] = [str(agent_spec["capabilities"])]
                
                # Ensure role is set
                if "role" not in agent_spec or not agent_spec["role"]:
                    agent_spec["role"] = "team"
                
                # Add LLM credentials
                agent_spec["provider"] = agent_provider
                agent_spec["api_key"] = agent_api_key
                agent_spec["model"] = agent_model
                
                agent_specs.append(agent_spec)
            
            if not agent_specs:
                raise ValueError("No valid agent specifications generated")
            
            logger.info(f"Generated {len(agent_specs)} agent specifications from task")
            return agent_specs
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse agent specifications: {e}")
            raise ValueError(
                f"Invalid agent specification response. Received: {response_text[:200]}"
            ) from e
    
    async def plan_task_and_create_agent_specs(
        self,
        user_task: str,
        task_id: Optional[str] = None,
        agent_provider: str = "anthropic",
        agent_api_key: Optional[str] = None,
        agent_model: Optional[str] = None,
    ) -> tuple[TaskTreePlan, list[dict[str, Any]]]:
        """
        RECOMMENDED APPROACH: Break down task first, THEN create required agent specifications.
        
        This method:
        1. Analyzes the task and creates a hierarchical breakdown
        2. Determines what agent types are needed for each subtask
        3. Creates agent SPECIFICATIONS (not instances) for only the required agents
        4. Returns both the task plan and agent specs
        
        Note: This creates agent SPECIFICATIONS (dictionaries), not actual Agent instances.
        Use create_agents_from_specs() to turn specifications into Agent objects.
        
        This is more efficient than creating agents first and then planning,
        because you only create exactly the agents you need.
        
        Args:
            user_task: The user's task description
            task_id: Optional unique identifier for the task
            agent_provider: LLM provider for generated agents ("anthropic" or "openai")
            agent_api_key: API key for the agent LLM (defaults to planner's API key)
            agent_model: Model name for generated agents (defaults to planner's model)
            
        Returns:
            Tuple of (TaskTreePlan, list of agent specifications)
            
        Example:
            ```python
            planner = PlannerLLM(provider="anthropic", api_key="...")
            
            # Step 1: Create task plan and agent specifications in one call
            task_plan, agent_specs = await planner.plan_task_and_create_agent_specs(
                "Plan a wedding with vendors, budget, and timeline"
            )
            
            # Step 2: Create actual Agent instances from specifications
            agents = synqed.create_agents_from_specs(agent_specs)
            
            # Step 3: Register agents
            for agent in agents:
                synqed.AgentRuntimeRegistry.register(agent.name, agent)
            
            # Step 4: Execute the plan
            await execution_engine.execute_task_plan(task_plan, user_task)
            ```
        """
        import uuid
        task_id = task_id or str(uuid.uuid4())
        
        # Use provided credentials or fall back to planner's credentials
        agent_provider = agent_provider
        agent_api_key = agent_api_key or self.api_key
        agent_model = agent_model or self.model
        
        # STEP 1: Break down the task hierarchically WITHOUT any agents registered
        # The LLM will generate generic agent role names based on what's needed
        system_prompt = """You are a hierarchical task planning expert. Break the user's task into a recursive tree structure.

IMPORTANT: You are creating a task breakdown FIRST, before any agents exist.
For each subtask, specify what TYPES of agents would be needed (e.g., "content_specialist", "logistics_manager", "budget_coordinator").
These are just role names - the actual agents will be created later based on your requirements.

COORDINATOR SELECTION RULES:
The execution engine automatically selects a root coordinator for cross-workspace coordination using this ranking (highest to lowest priority):
1. 'coordinator' (highest priority)
2. 'manager'
3. 'lead'
4. 'director'
5. 'chief'
6. 'head'
7. 'orchestrator' (lowest priority)

Include at least one agent with a coordination keyword in your plan.

Respond with a SINGLE JSON object representing the ROOT TaskTreeNode ONLY:

{
  "id": "placeholder",
  "description": "overall task description",
  "required_agents": ["role_name1", "role_name2"],
  "may_need_subteams": true,
  "children": [
    {
      "id": "placeholder",
      "description": "subtask A description",
      "required_agents": ["role_name3", "role_name4"],
      "may_need_subteams": false,
      "children": []
    }
  ]
}

RULES:
- Output ONLY a single JSON object representing the root node.
- Do NOT include task_id, original_task, wrapper objects, or extra fields.
- Every node MUST have: id, description, required_agents, may_need_subteams (optional), children.
- Children MUST follow the exact same schema recursively.
- Use descriptive role names (e.g., "project_coordinator", "technical_specialist")
- MINIMUM 2 AGENTS per subtask/workspace for collaboration
- DO NOT DUPLICATE AGENTS: Each agent should appear in ONLY ONE location
- Group related agents together
- Ignore IDs; placeholder IDs are acceptable
- Output NOTHING except valid JSON."""
        
        user_prompt = f"""Break down this task into a hierarchical task tree:

Task: {user_task}

For each subtask, specify what TYPES of agents would be needed to accomplish it.
Use descriptive role names like "project_coordinator", "content_curator", "logistics_manager", etc.

CRITICAL RULES:
1. MINIMUM 2 AGENTS per child workspace for collaboration
2. NO DUPLICATE AGENTS - each agent role appears in ONLY ONE place
3. Group related agent roles together
4. Include at least one coordinator/manager role for cross-team coordination

Respond with valid JSON only."""
        
        # Make LLM call for task breakdown
        response_text = await self._call_llm(system_prompt, user_prompt)
        
        # Parse and validate response
        try:
            # Extract JSON from response
            json_str = self.extract_json(response_text)
            node_dict = json.loads(json_str)
            
            # Parse root node only
            root_node = TaskTreeNode.model_validate(node_dict)
            
            # Generate stable IDs
            root_node = self.generate_stable_ids(root_node)
            
            # Wrap root into TaskTreePlan
            task_plan = TaskTreePlan(
                task_id=task_id,
                original_task=user_task,
                schema_version=1,
                root=root_node
            )
            
            # Reindex the plan
            task_plan.reindex()
            
            # Validate tree structure
            self.validate_tree_structure(task_plan.root)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse task breakdown: {e}")
            raise ValueError(
                f"Invalid task breakdown response. Received: {response_text[:200]}"
            ) from e
        
        # STEP 2: Extract all unique agent requirements from the task tree
        def collect_agent_roles(node: TaskTreeNode) -> set[str]:
            """Recursively collect all unique agent role names from the tree."""
            roles = set(node.required_agents)
            for child in node.children:
                roles.update(collect_agent_roles(child))
            return roles
        
        required_roles = collect_agent_roles(task_plan.root)
        logger.info(f"Task breakdown requires {len(required_roles)} unique agent roles: {sorted(required_roles)}")
        
        # STEP 3: Create agent specifications for each required role
        agent_specs_system_prompt = """You are an expert at designing agent specifications. Given a list of agent role names and the overall task context, create detailed specifications for each agent.

For each agent role, provide:
- name: The exact role name provided (do not change it)
- description: Clear description of the agent's purpose and responsibilities
- capabilities: List of specific capabilities/skills this agent needs
- role: A team/domain identifier (e.g., "management_team", "content_team")

Output a JSON array of agent specifications:

[
  {
    "name": "exact_role_name",
    "description": "Agent description with specific responsibilities",
    "capabilities": ["capability1", "capability2", "capability3"],
    "role": "team_name"
  }
]

RULES:
- Use the EXACT role names provided (do not modify them)
- Each agent should have 3-6 specific, actionable capabilities
- Descriptions should be clear and focused
- Group agents into logical teams via the "role" field
- Output ONLY valid JSON, nothing else"""
        
        agent_specs_user_prompt = f"""Create detailed specifications for these agent roles:

Task Context: {user_task}

Required Agent Roles: {', '.join(sorted(required_roles))}

For each role, provide:
1. name: Use the EXACT role name from the list
2. description: What this agent does in the context of this task
3. capabilities: Specific skills needed for this role
4. role: Team/domain this agent belongs to

Respond with valid JSON array only."""
        
        # Make LLM call for agent specifications
        agent_specs_response = await self._call_llm(agent_specs_system_prompt, agent_specs_user_prompt)
        
        # Parse agent specifications
        try:
            json_str = self.extract_json(agent_specs_response)
            parsed = json.loads(json_str)
            
            # Handle both array and object responses
            if isinstance(parsed, dict):
                for key in ["agents", "agent_specs", "specifications", "agent_list"]:
                    if key in parsed and isinstance(parsed[key], list):
                        parsed = parsed[key]
                        break
                else:
                    if "name" in parsed and "description" in parsed:
                        parsed = [parsed]
                    else:
                        raise ValueError("Response is a dict but doesn't contain agent specifications")
            
            if not isinstance(parsed, list):
                raise ValueError(f"Expected list of agent specifications, got {type(parsed)}")
            
            # Validate and normalize each agent spec
            agent_specs = []
            for i, agent_spec in enumerate(parsed):
                if not isinstance(agent_spec, dict):
                    logger.warning(f"Skipping invalid agent spec at index {i}: not a dict")
                    continue
                
                if "name" not in agent_spec or "description" not in agent_spec:
                    logger.warning(f"Skipping invalid agent spec at index {i}: missing name or description")
                    continue
                
                # Ensure capabilities is a list
                if "capabilities" not in agent_spec:
                    agent_spec["capabilities"] = ["general tasks"]
                elif not isinstance(agent_spec["capabilities"], list):
                    agent_spec["capabilities"] = [str(agent_spec["capabilities"])]
                
                # Ensure role is set
                if "role" not in agent_spec or not agent_spec["role"]:
                    agent_spec["role"] = "team"
                
                # Add LLM credentials
                agent_spec["provider"] = agent_provider
                agent_spec["api_key"] = agent_api_key
                agent_spec["model"] = agent_model
                
                agent_specs.append(agent_spec)
            
            if not agent_specs:
                raise ValueError("No valid agent specifications generated")
            
            logger.info(f"Generated {len(agent_specs)} agent specifications")
            
            return task_plan, agent_specs
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse agent specifications: {e}")
            raise ValueError(
                f"Invalid agent specification response. Received: {agent_specs_response[:200]}"
            ) from e
    
    # Backward compatibility alias
    async def plan_task_and_create_agents(
        self,
        user_task: str,
        task_id: Optional[str] = None,
        agent_provider: str = "anthropic",
        agent_api_key: Optional[str] = None,
        agent_model: Optional[str] = None,
    ) -> tuple[TaskTreePlan, list[dict[str, Any]]]:
        """
        Deprecated: Use plan_task_and_create_agent_specs() instead.
        
        This is an alias for backward compatibility.
        """
        return await self.plan_task_and_create_agent_specs(
            user_task=user_task,
            task_id=task_id,
            agent_provider=agent_provider,
            agent_api_key=agent_api_key,
            agent_model=agent_model,
        )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"PlannerLLM(provider='{self.provider}', model='{self.model}')"
