"""
MessageRouter - unified message routing for local and remote agents.

this module provides the MessageRouter class that handles all message routing
between agents using a single canonical async path. both sync and async callers
use the same underlying routing logic.

architecture:
- route_message() is the SINGLE source of truth for all routing
- send_message() is a sync wrapper that calls route_message() via asyncio
- route_local_message() is a backward-compatible async wrapper
- all transcript logic is centralized in route_message()
- local + remote agents follow identical routing semantics
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from synqed.agent import Agent

logger = logging.getLogger(__name__)

# maximum transcript size before removing oldest entries
MAX_TRANSCRIPT_SIZE = 20000


class MessageRouter:
    """
    unified message router for local and remote agents.
    
    all routing passes through one canonical async method: route_message().
    this ensures:
    - identical transcript entries for sync + async callers
    - consistent message_id generation
    - single deduplication logic
    - deterministic ordering
    
    example:
        ```python
        router = MessageRouter()
        
        router.register_agent("Writer", writer_agent)
        router.register_agent("Editor", editor_agent)
        
        # async routing (preferred)
        msg_id = await router.route_message(
            workspace_id="ws_123",
            sender="Writer",
            recipient="Editor",
            content="Draft ready"
        )
        
        # sync routing (for worker initial execution)
        msg_id = router.send_message(
            from_agent="Writer",
            to_agent="Editor",
            content="Draft ready"
        )
        ```
    """
    
    def __init__(self):
        """initialize the message router."""
        self._agents: Dict[str, Any] = {}  # agent_name -> Agent instance (local or remote)
        self._transcript: List[Dict[str, Any]] = []
        self._transcripted_message_ids: set[str] = set()  # for deduplication
        self._message_counter: int = 0  # for deterministic message_id generation
    
    def register_agent(self, agent_name: str, agent: Any) -> None:
        """
        register an agent for routing.
        
        supports both:
        - local agents (built with synqed) - routed in-memory
        - remote a2a agents (any a2a-compliant agent) - routed via http/grpc
        
        args:
            agent_name: name of the agent (must match send_to values)
            agent: agent instance (local Agent or RemoteA2AAgent)
        """
        self._agents[agent_name] = agent
        logger.debug(f"router: registered agent '{agent_name}'")
    
    def unregister_agent(self, agent_name: str) -> None:
        """
        unregister an agent.
        
        args:
            agent_name: name of the agent to unregister
        """
        if agent_name in self._agents:
            del self._agents[agent_name]
            logger.debug(f"router: unregistered agent '{agent_name}'")
    
    def _generate_message_id(self, workspace_id: str, recipient: str) -> str:
        """
        generate a deterministic message id.
        
        uses a counter for ordering guarantee + uuid suffix for uniqueness.
        """
        self._message_counter += 1
        short_uuid = uuid.uuid4().hex[:8]
        return f"msg-{self._message_counter:06d}-{workspace_id[:8] if workspace_id else 'ws'}-{recipient[:8]}-{short_uuid}"
    
    # =========================================================================
    # canonical async routing - all routing logic lives here
    # =========================================================================
    
    async def route_message(
        self,
        workspace_id: str,
        sender: str,
        recipient: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> str:
        """
        canonical async entrypoint for routing messages between agents.
        
        ALL routing (local + remote, sync + async) must pass through here.
        this is the single source of truth for:
        - agent validation
        - message delivery (memory injection or remote buffering)
        - message_id generation
        - transcript entry creation
        - deduplication
        
        args:
            workspace_id: workspace identifier (required for transcript)
            sender: name of the sending agent
            recipient: name of the target agent
            content: message content
            message_id: optional pre-generated message id
            
        returns:
            the message_id string of the routed message
            
        raises:
            ValueError: if recipient is not registered
        """
        logger.debug(f"router: routing message {sender} -> {recipient}")
        
        # validate recipient exists
        if recipient not in self._agents:
            logger.warning(f"router: recipient '{recipient}' not registered")
            raise ValueError(f"Agent '{recipient}' is not registered")
        
        agent = self._agents[recipient]
        
        # generate message_id if not provided
        msg_id = message_id or self._generate_message_id(workspace_id, recipient)
        logger.debug(f"router: message_id={msg_id}")
        
        # determine routing path and deliver message
        if hasattr(agent, 'memory'):
            # local agent - direct memory injection
            logger.debug(f"router: using local path for '{recipient}'")
            agent.memory.add_message(
                from_agent=sender,
                content=content,
                message_id=msg_id,
                target=recipient
            )
        else:
            # remote a2a agent - buffer message for next get_response() call
            logger.debug(f"router: using remote path for '{recipient}'")
            try:
                from synqed.memory import InboxMessage
                inbox_msg = InboxMessage(
                    from_agent=sender,
                    content=content,
                    target=recipient,
                    message_id=msg_id,
                )
                await agent.send_message(inbox_msg)
            except ImportError:
                logger.warning(f"router: InboxMessage not available, skipping remote send")
            except Exception as e:
                logger.error(f"router: remote send failed for '{recipient}': {e}")
                # still record in transcript even if remote send fails
        
        # create transcript entry (shared by all paths)
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "workspace_id": workspace_id,
            "from": sender,
            "to": recipient,
            "message_id": msg_id,
            "content": content
        }
        self._add_transcript_entry(entry)
        
        logger.debug(f"router: message routed successfully, msg_id={msg_id}")
        return msg_id
    
    # =========================================================================
    # sync wrapper - calls async route_message() under the hood
    # =========================================================================
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_id: Optional[str] = None,
        workspace_id: str = "",
    ) -> str:
        """
        synchronous wrapper for route_message().
        
        this method is used by worker.py during initial task distribution
        where async context may not be available. it NEVER implements its own
        routing logic - all routing goes through route_message().
        
        args:
            from_agent: name of the sending agent
            to_agent: name of the target agent  
            content: message content
            message_id: optional pre-generated message id
            workspace_id: workspace identifier (optional, defaults to empty)
            
        returns:
            the message_id string of the routed message
            
        raises:
            ValueError: if recipient is not registered
        """
        logger.debug(f"router: send_message (sync) {from_agent} -> {to_agent}")
        
        async def _route():
            return await self.route_message(
                workspace_id=workspace_id,
                sender=from_agent,
                recipient=to_agent,
                content=content,
                message_id=message_id,
            )
        
        # detect if we're in an async context
        try:
            loop = asyncio.get_running_loop()
            # we're inside an async context - need to schedule and wait
            logger.debug(f"router: sync wrapper running inside existing event loop")
            
            # create a new thread to run the coroutine to avoid blocking
            # this handles the case where send_message is called from sync code
            # that's running inside an async context (like worker.py)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(asyncio.run, _route())
                return future.result()
                
        except RuntimeError:
            # no running loop - create one and run
            logger.debug(f"router: sync wrapper creating new event loop")
            return asyncio.run(_route())
    
    # =========================================================================
    # backward-compatible async wrapper
    # =========================================================================
    
    async def route_local_message(
        self,
        workspace_id: str,
        sender: str,
        recipient: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> str:
        """
        backward-compatible async wrapper for route_message().
        
        this method exists for backward compatibility with existing code
        that calls route_local_message(). new code should use route_message()
        directly.
        
        args:
            workspace_id: workspace identifier (required)
            sender: name of the sending agent
            recipient: name of the target agent
            content: message content
            message_id: optional pre-generated message id
            
        returns:
            the message_id string of the routed message
        """
        return await self.route_message(
            workspace_id=workspace_id,
            sender=sender,
            recipient=recipient,
            content=content,
            message_id=message_id,
        )
    
    # =========================================================================
    # transcript management
    # =========================================================================
    
    def _add_transcript_entry(self, entry: Dict[str, Any]) -> None:
        """
        add an entry to the transcript with validation and deduplication.
        
        internal method - all callers should go through route_message().
        
        this method enforces strict validation, fifo ordering, size limits,
        and deduplication. invalid entries are logged and ignored.
        
        args:
            entry: dictionary containing transcript entry fields
        """
        # validate required keys
        required_keys = {"timestamp", "workspace_id", "from", "to", "message_id", "content"}
        if not isinstance(entry, dict):
            logger.warning(f"router: invalid transcript entry: not a dictionary, ignoring")
            return
        
        missing_keys = required_keys - set(entry.keys())
        if missing_keys:
            logger.warning(f"router: invalid transcript entry: missing keys {missing_keys}, ignoring")
            return
        
        # deduplication check
        msg_id = entry.get("message_id")
        if msg_id in self._transcripted_message_ids:
            logger.debug(f"router: duplicate transcript entry '{msg_id}', ignoring")
            return
        
        # add to transcript (fifo ordering - append only, no reordering)
        self._transcript.append(entry)
        self._transcripted_message_ids.add(msg_id)
        
        # enforce size limit: remove oldest entries if over limit
        if len(self._transcript) > MAX_TRANSCRIPT_SIZE:
            excess_count = len(self._transcript) - MAX_TRANSCRIPT_SIZE
            removed_entries = self._transcript[:excess_count]
            self._transcript = self._transcript[excess_count:]
            
            # remove message_ids from deduplication set
            for removed_entry in removed_entries:
                removed_msg_id = removed_entry.get("message_id")
                if removed_msg_id:
                    self._transcripted_message_ids.discard(removed_msg_id)
            
            logger.debug(f"router: transcript size limit exceeded, removed {excess_count} oldest entries")
    
    def add_transcript_entry(self, entry: Dict[str, Any]) -> None:
        """
        public method to add transcript entry (for external callers).
        
        delegates to internal _add_transcript_entry().
        """
        self._add_transcript_entry(entry)
    
    def get_transcript(self) -> List[Dict[str, Any]]:
        """
        get the conversation transcript.
        
        returns:
            list of message dictionaries
        """
        return self._transcript.copy()
    
    def clear_transcript(self) -> None:
        """clear the conversation transcript and deduplication set."""
        self._transcript = []
        self._transcripted_message_ids.clear()
        self._message_counter = 0
        logger.debug(f"router: transcript cleared")
    
    # =========================================================================
    # utility methods
    # =========================================================================
    
    def list_local_agents(self) -> List[str]:
        """
        list all registered agent names (local and remote).
        
        returns:
            list of registered agent names
        """
        return list(self._agents.keys())
    
    def has_agent(self, agent_name: str) -> bool:
        """
        check if an agent is registered.
        
        args:
            agent_name: name of the agent to check
            
        returns:
            True if agent is registered
        """
        return agent_name in self._agents
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """
        get a registered agent by name.
        
        args:
            agent_name: name of the agent
            
        returns:
            agent instance or None if not found
        """
        return self._agents.get(agent_name)
    
    def __repr__(self) -> str:
        """string representation."""
        return (
            f"MessageRouter(agents={len(self._agents)}, "
            f"transcript_length={len(self._transcript)}, "
            f"unique_message_ids={len(self._transcripted_message_ids)})"
        )
