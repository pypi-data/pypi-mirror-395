"""
worker for async message processing.

consumes messages from redis queue and dispatches to local runtime or remote inbox.
handles retries, error classification, and dlq routing.

automatic workspace creation:
when both sender and recipient have local runtimes, automatically creates
a workspace to manage their conversation.
"""

import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

from synqed.agent_email.inbox.api import (
    A2AInboxRequest,
    A2AInboxResponse,
    LocalAgentRuntime,
    get_agent_runtime,
)
from synqed.agent_email.inbox.queue import MessageQueue, get_message_queue
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.auto_workspace import get_auto_workspace_manager


logger = logging.getLogger(__name__)


class MessageWorker:
    """
    worker for processing queued messages.
    
    consumes messages from redis streams and dispatches to:
    1. local runtime (if available)
    2. remote inbox_url (if no local runtime)
    
    handles automatic retry with exponential backoff.
    """
    
    def __init__(
        self,
        queue: MessageQueue,
        http_timeout: float = 30.0,
    ):
        """
        initialize worker.
        
        args:
            queue: message queue instance
            http_timeout: timeout for remote http requests
        """
        self.queue = queue
        self.http_timeout = http_timeout
        self._tasks: Dict[str, asyncio.Task] = {}
    
    async def process_envelope(self, envelope: Dict[str, Any]) -> None:
        """
        process single message envelope.
        
        tries automatic workspace routing first (if both agents are local),
        then local runtime, then remote forwarding.
        
        args:
            envelope: complete envelope dict with sender, recipient, message, etc.
            
        raises:
            Exception: if processing fails (for retry handling)
        """
        sender = envelope["sender"]
        recipient = envelope["recipient"]
        message = envelope["message"]
        message_id = envelope.get("message_id", "unknown")
        
        logger.info(f"processing envelope {message_id}: {sender} -> {recipient}")
        
        # lookup recipient in registry
        registry = get_registry()
        try:
            recipient_entry = registry.get_by_uri(recipient)
        except KeyError:
            logger.error(f"recipient not found in registry: {recipient}")
            raise ValueError(f"recipient not found: {recipient}")
        
        # check if both sender and recipient have local runtimes
        sender_runtime = get_agent_runtime(sender)
        recipient_runtime = get_agent_runtime(recipient)
        
        # AUTO-WORKSPACE ROUTING: If both agents are local, use workspace routing
        if sender_runtime is not None and recipient_runtime is not None:
            logger.info(
                f"both agents are local - routing via auto-workspace: {sender} ↔ {recipient}"
            )
            try:
                # Get auto-workspace manager
                auto_ws_manager = get_auto_workspace_manager()
                
                # Route message via auto-created workspace
                response_envelope = await auto_ws_manager.route_message_via_workspace(
                    sender=sender,
                    recipient=recipient,
                    envelope=message,
                )
                
                logger.info(
                    f"successfully processed {message_id} via auto-workspace"
                )
                return
            
            except Exception as e:
                logger.error(
                    f"auto-workspace routing error for {message_id}: {e}",
                    exc_info=True,
                )
                # Fall back to direct local runtime call
                logger.warning("falling back to direct local runtime call")
        
        # DIRECT LOCAL RUNTIME: If only recipient is local
        if recipient_runtime is not None:
            logger.info(f"dispatching to local runtime: {recipient}")
            try:
                response_envelope = await recipient_runtime.handle_a2a_envelope(
                    sender=sender,
                    recipient=recipient,
                    envelope=message,
                )
                logger.info(
                    f"successfully processed {message_id} via local runtime"
                )
                return
            
            except Exception as e:
                logger.error(
                    f"local runtime error for {message_id}: {e}",
                    exc_info=True,
                )
                # raise for retry
                raise
        
        # REMOTE FORWARDING: No local runtime - forward to remote inbox
        if recipient_entry.inbox_url:
            logger.info(
                f"forwarding to remote inbox: {recipient_entry.inbox_url}"
            )
            try:
                await self._forward_to_remote(
                    inbox_url=str(recipient_entry.inbox_url),
                    envelope=envelope,
                )
                logger.info(
                    f"successfully forwarded {message_id} to remote inbox"
                )
                return
            
            except Exception as e:
                logger.error(
                    f"remote forwarding error for {message_id}: {e}",
                    exc_info=True,
                )
                # raise for retry
                raise
        
        # no runtime and no inbox_url
        logger.error(
            f"no delivery method for {recipient}: "
            f"no local runtime or remote inbox_url"
        )
        raise ValueError(f"no delivery method for {recipient}")
    
    async def _forward_to_remote(
        self,
        inbox_url: str,
        envelope: Dict[str, Any],
    ) -> None:
        """
        forward envelope to remote inbox via http.
        
        args:
            inbox_url: remote inbox endpoint url
            envelope: complete envelope dict
            
        raises:
            httpx.HTTPError: on network/http errors (for retry)
        """
        async with httpx.AsyncClient(timeout=self.http_timeout) as client:
            try:
                response = await client.post(
                    inbox_url,
                    json=envelope,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                
                # parse response
                response_data = response.json()
                
                # check if remote accepted the message
                if response_data.get("status") == "error":
                    # check if retryable
                    if not response_data.get("retryable", False):
                        # non-retryable error from remote
                        logger.error(
                            f"remote inbox returned non-retryable error: "
                            f"{response_data.get('error')}"
                        )
                        # don't raise - this should go to dlq immediately
                        # but for now, treat as retriable
                        raise ValueError(
                            f"remote error: {response_data.get('error')}"
                        )
                    else:
                        # retryable error from remote
                        raise ValueError(
                            f"remote retryable error: {response_data.get('error')}"
                        )
            
            except httpx.TimeoutException as e:
                # timeout is retryable
                logger.warning(f"timeout forwarding to {inbox_url}")
                raise
            
            except httpx.HTTPStatusError as e:
                # classify by status code
                if 500 <= e.response.status_code < 600:
                    # 5xx errors are retryable
                    logger.warning(
                        f"remote server error {e.response.status_code}: {e.response.text}"
                    )
                    raise
                else:
                    # 4xx errors are not retryable
                    logger.error(
                        f"remote client error {e.response.status_code}: {e.response.text}"
                    )
                    # still raise for now, but in production might want to skip retry
                    raise
            
            except httpx.RequestError as e:
                # connection errors are retryable
                logger.warning(f"connection error forwarding to {inbox_url}: {e}")
                raise
    
    async def start_consumer(self, agent_id: str) -> None:
        """
        start consuming messages for an agent.
        
        args:
            agent_id: agent canonical uri to consume for
        """
        if agent_id in self._tasks:
            logger.warning(f"consumer already running for {agent_id}")
            return
        
        # create consumer task
        task = asyncio.create_task(
            self.queue.consume(
                agent_id=agent_id,
                callback=self.process_envelope,
            )
        )
        
        self._tasks[agent_id] = task
        logger.info(f"started consumer for {agent_id}")
    
    async def stop_consumer(self, agent_id: str) -> None:
        """
        stop consuming messages for an agent.
        
        args:
            agent_id: agent canonical uri
        """
        if agent_id not in self._tasks:
            logger.warning(f"no consumer running for {agent_id}")
            return
        
        task = self._tasks.pop(agent_id)
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        logger.info(f"stopped consumer for {agent_id}")
    
    async def stop_all(self) -> None:
        """stop all consumers."""
        agent_ids = list(self._tasks.keys())
        for agent_id in agent_ids:
            await self.stop_consumer(agent_id)


# global worker instance
_message_worker: Optional[MessageWorker] = None


def get_message_worker(redis_url: str = "redis://localhost:6379") -> MessageWorker:
    """
    get or create global message worker instance.
    
    args:
        redis_url: redis connection url
        
    returns:
        message worker instance
    """
    global _message_worker
    if _message_worker is None:
        queue = get_message_queue(redis_url)
        _message_worker = MessageWorker(queue=queue)
    return _message_worker


async def start_workers_for_all_agents(redis_url: str = "redis://localhost:6379") -> None:
    """
    start worker consumers for all registered agents.
    
    this should be called on application startup.
    
    args:
        redis_url: redis connection url
    """
    from synqed.agent_email.inbox.queue import initialize_queue
    
    # ensure queue is connected
    await initialize_queue(redis_url)
    
    # get worker
    worker = get_message_worker(redis_url)
    
    # start consumers for all registered agents
    registry = get_registry()
    for entry in registry.list_all():
        await worker.start_consumer(entry.agent_id)
    
    logger.info("started workers for all registered agents")


async def shutdown_workers() -> None:
    """shutdown all workers."""
    global _message_worker
    if _message_worker:
        await _message_worker.stop_all()
        _message_worker = None
    
    from synqed.agent_email.inbox.queue import shutdown_queue
    await shutdown_queue()

