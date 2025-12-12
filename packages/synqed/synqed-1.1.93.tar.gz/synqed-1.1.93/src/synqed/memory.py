"""
Agent Memory - Server-side message storage for inbox-based agents.

This module provides the AgentMemory abstraction that stores messages
with deterministic IDs and supports message tracking.
"""

from datetime import datetime
from typing import List, Optional, Dict, Set
from pydantic import BaseModel


class InboxMessage(BaseModel):
    """Message structure for inbox with deterministic ID."""
    message_id: str
    from_agent: str
    content: str
    target: Optional[str] = None  # Explicit target recipient for filtering
    timestamp: Optional[str] = None


class AgentMemory:
    """
    Server-side memory storage for each agent with deterministic message IDs.
    
    This class provides a simple in-memory storage for messages received
    by an agent. Messages are assigned deterministic IDs and tracking prevents
    duplicate processing.
    
    Example:
        ```python
        memory = AgentMemory(agent_name="Writer", workspace_id="ws-123")
        message_id = memory.add_message(from_agent="Editor", content="Great work!")
        message = memory.get_message_by_id(message_id)
        ```
    """
    
    def __init__(self, agent_name: str, workspace_id: Optional[str] = None):
        """
        Initialize memory for an agent.
        
        Args:
            agent_name: Name of the agent this memory belongs to
            workspace_id: Optional workspace ID for message ID generation
        """
        self.agent_name = agent_name
        self.workspace_id = workspace_id or "unknown"
        self.messages: List[InboxMessage] = []
        self._message_counter: int = 0
        self._messages_by_id: Dict[str, InboxMessage] = {}
        self.processed_ids: Set[str] = set()
    
    def _generate_message_id(self) -> str:
        """
        Generate a deterministic message ID.
        
        Format: "msg-{workspace_id}-{agent_name}-{counter}"
        
        Returns:
            Unique message ID string
        """
        self._message_counter += 1
        return f"msg-{self.workspace_id}-{self.agent_name}-{self._message_counter}"
    
    def generate_message_id(self) -> str:
        """
        Public API to generate a deterministic message ID.
        
        Returns:
            Unique message ID string
        """
        return self._generate_message_id()
    
    def add_message(self, from_agent: str, content: str, message_id: Optional[str] = None, target: Optional[str] = None) -> str:
        """
        Add a message to the agent's memory.
        
        Args:
            from_agent: Name of the agent that sent the message
            content: Message content
            message_id: Optional pre-generated message ID (if None, generates one)
            target: Optional explicit target recipient (defaults to this agent)
            
        Returns:
            The message_id of the added message
        """
        if message_id is None:
            message_id = self._generate_message_id()
        
        # Check if message ID already exists
        if message_id in self._messages_by_id:
            return message_id
        
        # Default target to this agent if not specified
        if target is None:
            target = self.agent_name
        
        message = InboxMessage(
            message_id=message_id,
            from_agent=from_agent,
            content=content,
            target=target,
            timestamp=datetime.now().isoformat()
        )
        
        self.messages.append(message)
        self._messages_by_id[message_id] = message
        
        return message_id
    
    def get_message_by_id(self, message_id: str) -> Optional[InboxMessage]:
        """
        Get a message by its ID.
        
        Args:
            message_id: The message ID to look up
            
        Returns:
            InboxMessage if found, None otherwise
        """
        return self._messages_by_id.get(message_id)
    
    def has_message(self, message_id: str) -> bool:
        """
        Check if a message with the given ID exists.
        
        Args:
            message_id: The message ID to check
            
        Returns:
            True if message exists, False otherwise
        """
        return message_id in self._messages_by_id
    
    def is_message_processed(self, message_id: str) -> bool:
        """
        Check if a message has been processed.
        
        Args:
            message_id: The message ID to check
            
        Returns:
            True if message has been processed (in processed_ids set)
        """
        return message_id in self.processed_ids
    
    def mark_message_processed(self, message_id: str) -> None:
        """
        Mark a message as processed.
        
        Args:
            message_id: The message ID to mark as processed
        """
        if message_id in self._messages_by_id:
            self.processed_ids.add(message_id)
    
    def get_messages(self) -> List[InboxMessage]:
        """
        Get all messages in the agent's memory.
        
        Returns:
            List of all messages (copy to prevent external modification)
        """
        return self.messages.copy()
    
    def get_unprocessed_messages(self) -> List[InboxMessage]:
        """
        Get all unprocessed messages.
        
        Returns:
            List of messages that haven't been processed yet
        """
        return [msg for msg in self.messages if msg.message_id not in self.processed_ids]
    
    def get_latest_message(self) -> Optional[InboxMessage]:
        """
        Get the most recent message.
        
        Returns:
            Latest message, or None if no messages exist
        """
        return self.messages[-1] if self.messages else None
    
    def get_last_n_messages(self, n: int) -> List[InboxMessage]:
        """
        Get the last N messages.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of last N messages
        """
        return self.messages[-n:] if len(self.messages) >= n else self.messages.copy()
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages.clear()
        self._messages_by_id.clear()
        self._message_counter = 0
        self.processed_ids.clear()
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AgentMemory(agent_name='{self.agent_name}', "
            f"messages={len(self.messages)}, "
            f"processed={len(self.processed_ids)})"
        )
