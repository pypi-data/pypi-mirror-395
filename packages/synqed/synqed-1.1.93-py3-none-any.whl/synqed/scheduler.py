"""
EventScheduler - Event-driven scheduling for agent execution.

This module provides:
- AgentEvent: Represents an event that triggers agent execution
- EventScheduler: Manages an event queue for agent execution

The scheduler replaces naive turn-based loops with event-driven execution,
where agents only run when they have scheduled events.
"""

from __future__ import annotations

import json
import logging
from collections import deque
from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AgentEvent:
    """
    Represents an event that triggers agent execution.
    
    Attributes:
        agent_name: Name of the agent this event is for
        trigger: Type of trigger ("message", "startup", "subteam_result")
        payload: Event-specific data (messages, subteam results, etc.)
        timestamp: When the event was created
    """
    
    agent_name: str
    trigger: str  # "message", "startup", "subteam_result"
    payload: dict[str, Any]
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AgentEvent(agent='{self.agent_name}', "
            f"trigger='{self.trigger}', payload_keys={list(self.payload.keys())})"
        )


class EventScheduler:
    """
    Event-driven scheduler for agent execution.
    
    This scheduler maintains a queue of AgentEvents and provides methods
    to schedule, retrieve, and check for pending events. Agents only execute
    when they have events scheduled for them.
    
    Events are processed in FIFO order (first-in, first-out).
    
    Example:
        ```python
        scheduler = EventScheduler()
        
        # Schedule a startup event
        scheduler.schedule_event(AgentEvent(
            agent_name="Writer",
            trigger="startup",
            payload={}
        ))
        
        # Schedule a message event
        scheduler.schedule_event(AgentEvent(
            agent_name="Editor",
            trigger="message",
            payload={"from_agent": "Writer", "content": "Draft ready"}
        ))
        
        # Process events
        while scheduler.has_pending_events():
            event = scheduler.pop_next_event()
            # Execute agent with event
        ```
    """
    
    def __init__(self):
        """Initialize the event scheduler with an empty queue."""
        self._event_queue: deque[AgentEvent] = deque()
        self._pending_signatures: set[tuple[str, str, str]] = set()
        self._total_scheduled = 0
        self._total_processed = 0
    
    def schedule_event(self, event: AgentEvent) -> None:
        """
        Schedule an event for agent execution.
        
        Args:
            event: AgentEvent to add to the queue
        """
        self._event_queue.append(event)
        self._total_scheduled += 1
        logger.debug(f"Scheduled event: {event}")
    
    def schedule_event_dedup(self, event: AgentEvent) -> None:
        """
        Schedule an event with deduplication based on message_id.
        
        For message-like events (message, startup, subteam_result), deduplication
        is based on message_id only if present.
        For other events, deduplication uses (agent_name, trigger, canonicalized payload).
        
        Args:
            event: AgentEvent to add to the queue (if not duplicate)
        """
        # For message-like events, use message_id for deduplication
        message_like_triggers = {"message", "startup", "subteam_result"}
        if event.trigger in message_like_triggers:
            message_id = event.payload.get("message_id")
            if message_id:
                signature = (event.agent_name, event.trigger, message_id)
                if signature in self._pending_signatures:
                    logger.debug(f"Skipping duplicate {event.trigger} event: {event} (message_id: {message_id})")
                    return
            else:
                # Fallback to full payload deduplication if no message_id
                try:
                    payload_json = json.dumps(event.payload, sort_keys=True)
                except (TypeError, ValueError):
                    payload_json = str(event.payload)
                signature = (event.agent_name, event.trigger, payload_json)
        else:
            # For non-message events, use canonicalized payload
            try:
                payload_json = json.dumps(event.payload, sort_keys=True)
            except (TypeError, ValueError) as e:
                logger.warning(f"Could not serialize event payload for dedup: {e}")
                payload_json = str(event.payload)
            signature = (event.agent_name, event.trigger, payload_json)
        
        if signature in self._pending_signatures:
            logger.debug(f"Skipping duplicate event: {event}")
            return
        
        # Add to queue and track signature
        self._event_queue.append(event)
        self._pending_signatures.add(signature)
        self._total_scheduled += 1
        logger.debug(f"Scheduled event (dedup): {event}")
    
    def pop_next_event(self) -> Optional[AgentEvent]:
        """
        Get and remove the next event from the queue.
        
        Returns:
            Next AgentEvent if available, None if queue is empty
        """
        if not self._event_queue:
            return None
        
        event = self._event_queue.popleft()
        
        # Remove signature from pending set
        message_like_triggers = {"message", "startup", "subteam_result"}
        if event.trigger in message_like_triggers:
            message_id = event.payload.get("message_id")
            if message_id:
                signature = (event.agent_name, event.trigger, message_id)
            else:
                try:
                    payload_json = json.dumps(event.payload, sort_keys=True)
                except (TypeError, ValueError):
                    payload_json = str(event.payload)
                signature = (event.agent_name, event.trigger, payload_json)
        else:
            try:
                payload_json = json.dumps(event.payload, sort_keys=True)
            except (TypeError, ValueError):
                payload_json = str(event.payload)
            signature = (event.agent_name, event.trigger, payload_json)
        
        self._pending_signatures.discard(signature)
        
        self._total_processed += 1
        logger.debug(f"Popped event: {event}")
        return event
    
    def has_pending_events(self) -> bool:
        """
        Check if there are pending events in the queue.
        
        Returns:
            True if there are events waiting, False otherwise
        """
        return len(self._event_queue) > 0
    
    def peek_next_event(self) -> Optional[AgentEvent]:
        """
        Peek at the next event without removing it.
        
        Returns:
            Next AgentEvent if available, None if queue is empty
        """
        if not self._event_queue:
            return None
        return self._event_queue[0]
    
    def clear(self) -> None:
        """Clear all pending events from the queue and signature set."""
        count = len(self._event_queue)
        self._event_queue.clear()
        self._pending_signatures.clear()
        logger.debug(f"Cleared {count} pending events")
    
    def get_queue_size(self) -> int:
        """
        Get the current number of pending events.
        
        Returns:
            Number of events in the queue
        """
        return len(self._event_queue)
    
    def get_pending_signatures_count(self) -> int:
        """
        Get the number of pending event signatures.
        
        Returns:
            Number of unique event signatures pending
        """
        return len(self._pending_signatures)
    
    def get_stats(self) -> dict[str, int]:
        """
        Get scheduler statistics.
        
        Returns:
            Dictionary with scheduler statistics
        """
        return {
            "pending_events": len(self._event_queue),
            "pending_signatures": len(self._pending_signatures),
            "total_scheduled": self._total_scheduled,
            "total_processed": self._total_processed,
        }
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"EventScheduler(pending={len(self._event_queue)}, "
            f"scheduled={self._total_scheduled}, processed={self._total_processed})"
        )

