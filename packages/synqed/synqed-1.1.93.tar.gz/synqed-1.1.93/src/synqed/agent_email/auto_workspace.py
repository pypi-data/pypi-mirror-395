"""
Automatic Workspace Creation for Cloud-Based Agent Communication

This module enables seamless agent-to-agent communication via email addresses
by automatically creating and managing workspaces in the background.

When an agent sends a message to another agent via cloud/email:
1. The message arrives at the inbox
2. This module detects that both agents are registered
3. Automatically creates a workspace (if not exists) for their conversation
4. Routes the message through the workspace
5. The receiving agent's logic processes the message
6. Any response is automatically sent back via cloud

This eliminates the need for users to manually create workspaces for
cloud-based agent communication.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

from synqed.workspace_manager import Workspace, WorkspaceManager, AgentRuntimeRegistry
from synqed.router import MessageRouter
from synqed.agent_email.inbox.api import get_agent_runtime

logger = logging.getLogger(__name__)


@dataclass
class AutoWorkspaceConfig:
    """Configuration for automatic workspace management."""
    
    workspaces_root: Path = Path("/tmp/synqed_auto_workspaces")
    workspace_ttl_seconds: int = 3600  # 1 hour default
    max_workspaces: int = 1000


class AutoWorkspaceManager:
    """
    Manages automatic workspace creation for cloud-based agent communication.
    
    When agents communicate via email addresses (cloud messaging), this manager
    automatically creates workspaces in the background to handle the conversation.
    
    Each conversation thread gets its own workspace, which is automatically
    cleaned up after a period of inactivity.
    
    Example flow:
        alice@wonderland sends message to bob@builder
        → AutoWorkspaceManager creates workspace "alice_bob_thread123"
        → Message is routed through the workspace
        → bob's logic function processes the message
        → bob's response is automatically sent back to alice via cloud
    """
    
    def __init__(self, config: Optional[AutoWorkspaceConfig] = None):
        """
        Initialize the automatic workspace manager.
        
        Args:
            config: Optional configuration for workspace management
        """
        self.config = config or AutoWorkspaceConfig()
        self.workspace_manager = WorkspaceManager(
            workspaces_root=self.config.workspaces_root
        )
        
        # Track workspaces by thread_id
        self._thread_to_workspace: Dict[str, str] = {}
        
        # Ensure root directory exists
        self.config.workspaces_root.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"AutoWorkspaceManager initialized: {self.config.workspaces_root}")
    
    def _extract_agent_names(self, agent_id: str) -> tuple[str, str]:
        """
        Extract agent name and role from agent_id.
        
        Args:
            agent_id: Canonical agent URI (e.g., "agent://wonderland/alice")
            
        Returns:
            Tuple of (name, role)
        """
        # agent://role/name
        if agent_id.startswith("agent://"):
            agent_id = agent_id[8:]  # Remove "agent://"
        
        parts = agent_id.split("/")
        if len(parts) >= 2:
            role = parts[0]
            name = parts[1]
            return name, role
        
        return agent_id, "unknown"
    
    def _generate_workspace_id(self, sender: str, recipient: str, thread_id: str) -> str:
        """
        Generate a deterministic workspace ID for a conversation.
        
        Args:
            sender: Sender agent_id
            recipient: Recipient agent_id
            thread_id: Conversation thread ID
            
        Returns:
            Workspace ID string
        """
        sender_name, _ = self._extract_agent_names(sender)
        recipient_name, _ = self._extract_agent_names(recipient)
        
        # Create deterministic ID from thread_id
        # Use first 8 chars of thread_id for brevity
        thread_short = thread_id[:8] if len(thread_id) > 8 else thread_id
        
        return f"auto_{sender_name}_{recipient_name}_{thread_short}"
    
    async def get_or_create_workspace(
        self,
        sender: str,
        recipient: str,
        thread_id: str,
    ) -> Optional[Workspace]:
        """
        Get existing workspace or create a new one for this conversation.
        
        Args:
            sender: Sender agent_id (canonical URI)
            recipient: Recipient agent_id (canonical URI)
            thread_id: Conversation thread ID
            
        Returns:
            Workspace instance if successful, None if agents not found
        """
        # Check if workspace already exists for this thread
        if thread_id in self._thread_to_workspace:
            workspace_id = self._thread_to_workspace[thread_id]
            workspace = self.workspace_manager.workspaces.get(workspace_id)
            if workspace:
                logger.debug(f"Using existing workspace: {workspace_id}")
                return workspace
        
        # Get agent runtimes (these are the actual Agent instances)
        sender_runtime = get_agent_runtime(sender)
        recipient_runtime = get_agent_runtime(recipient)
        
        if not sender_runtime or not recipient_runtime:
            logger.warning(
                f"Cannot create workspace: missing agent runtimes "
                f"(sender={sender_runtime is not None}, recipient={recipient_runtime is not None})"
            )
            return None
        
        # Generate workspace ID
        workspace_id = self._generate_workspace_id(sender, recipient, thread_id)
        
        # Create workspace
        workspace_dir = self.config.workspaces_root / workspace_id
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract agent names
        sender_name, _ = self._extract_agent_names(sender)
        recipient_name, _ = self._extract_agent_names(recipient)
        
        # Create router
        router = MessageRouter()
        
        # Create workspace
        workspace = Workspace(
            workspace_id=workspace_id,
            directory=workspace_dir,
            router=router,
            agents={},
            depth=0,
        )
        
        # Add agents to workspace
        # Note: The runtimes from get_agent_runtime are already Agent instances
        workspace.add_agent(recipient_runtime)
        
        # Only add sender if it's also a local agent
        if hasattr(sender_runtime, 'memory'):
            workspace.add_agent(sender_runtime)
        
        # Register workspace
        self.workspace_manager.workspaces[workspace_id] = workspace
        self._thread_to_workspace[thread_id] = workspace_id
        
        logger.info(
            f"Created auto-workspace: {workspace_id} "
            f"for {sender_name} → {recipient_name} (thread: {thread_id})"
        )
        
        return workspace
    
    async def route_message_via_workspace(
        self,
        sender: str,
        recipient: str,
        envelope: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Route a message through an auto-created workspace.
        
        This method:
        1. Gets or creates a workspace for the conversation
        2. Routes the message through the workspace
        3. Processes the message using the recipient's logic
        4. Returns any response from the recipient
        
        Args:
            sender: Sender agent_id (canonical URI)
            recipient: Recipient agent_id (canonical URI)
            envelope: A2A message envelope
            
        Returns:
            Optional response envelope from recipient
        """
        thread_id = envelope.get("thread_id", "default")
        content = envelope.get("content", "")
        
        # Get or create workspace
        workspace = await self.get_or_create_workspace(sender, recipient, thread_id)
        
        if not workspace:
            logger.error(f"Failed to create workspace for {sender} → {recipient}")
            return None
        
        # Extract agent names
        sender_name, _ = self._extract_agent_names(sender)
        recipient_name, _ = self._extract_agent_names(recipient)
        
        # Route message through workspace
        try:
            await workspace.route_message(
                sender=sender_name,
                recipient=recipient_name,
                content=content,
            )
            
            logger.info(
                f"Routed message via workspace {workspace.workspace_id}: "
                f"{sender_name} → {recipient_name}"
            )
            
            # Get recipient agent
            recipient_agent = workspace.agents.get(recipient_name)
            if not recipient_agent:
                logger.error(f"Recipient agent not found in workspace: {recipient_name}")
                return None
            
            # Process the message using recipient's logic
            from synqed.agent import AgentLogicContext
            
            context = AgentLogicContext(
                memory=recipient_agent.memory,
                default_target=sender_name,  # Default response goes back to sender
                workspace=workspace,
                agent_name=recipient_name,
            )
            
            # Call recipient's logic function
            result = await recipient_agent.process(context)
            
            if result is None:
                logger.debug(f"Agent {recipient_name} returned no response")
                return None
            
            # If agent wants to send a response, prepare response envelope
            if result and "content" in result:
                response_content = result["content"]
                
                # Create response envelope
                response_envelope = {
                    "thread_id": thread_id,
                    "role": "assistant",
                    "content": response_content,
                }
                
                logger.info(
                    f"Agent {recipient_name} generated response to {sender_name}"
                )
                
                # Note: In production, the response would be sent back via cloud
                # automatically by the inbox worker. For now, we just return it.
                # The caller can decide whether to send it back via cloud.
                
                return response_envelope
            
            return None
            
        except Exception as e:
            logger.error(
                f"Error routing message via workspace: {e}",
                exc_info=True,
            )
            return None
    
    def _agent_id_to_email(self, agent_id: str) -> str:
        """
        Convert agent_id to email format.
        
        Args:
            agent_id: Canonical agent URI (e.g., "agent://wonderland/alice")
            
        Returns:
            Email format (e.g., "alice@wonderland")
        """
        name, role = self._extract_agent_names(agent_id)
        return f"{name}@{role}"
    
    async def cleanup_workspace(self, workspace_id: str) -> None:
        """
        Clean up a workspace and its resources.
        
        Args:
            workspace_id: ID of workspace to clean up
        """
        workspace = self.workspace_manager.workspaces.get(workspace_id)
        if workspace:
            # Remove from tracking
            thread_to_remove = None
            for thread_id, ws_id in self._thread_to_workspace.items():
                if ws_id == workspace_id:
                    thread_to_remove = thread_id
                    break
            
            if thread_to_remove:
                del self._thread_to_workspace[thread_to_remove]
            
            # Remove from manager
            del self.workspace_manager.workspaces[workspace_id]
            
            logger.info(f"Cleaned up workspace: {workspace_id}")
    
    def get_workspace_count(self) -> int:
        """Get the current number of active workspaces."""
        return len(self.workspace_manager.workspaces)


# Global instance
_auto_workspace_manager: Optional[AutoWorkspaceManager] = None


def get_auto_workspace_manager(
    config: Optional[AutoWorkspaceConfig] = None
) -> AutoWorkspaceManager:
    """
    Get the global AutoWorkspaceManager instance.
    
    Args:
        config: Optional configuration (only used on first call)
        
    Returns:
        AutoWorkspaceManager instance
    """
    global _auto_workspace_manager
    
    if _auto_workspace_manager is None:
        _auto_workspace_manager = AutoWorkspaceManager(config)
    
    return _auto_workspace_manager


def set_auto_workspace_manager(manager: AutoWorkspaceManager) -> None:
    """
    Set the global AutoWorkspaceManager instance (useful for testing).
    
    Args:
        manager: AutoWorkspaceManager instance
    """
    global _auto_workspace_manager
    _auto_workspace_manager = manager

