"""
redis streams-based message queue for guaranteed delivery.

provides:
- async message queuing with redis streams
- automatic retry with exponential backoff
- dead letter queue for failed messages
- consumer groups for scalable processing
"""

import asyncio
import json
import logging
import time
from typing import Any, Callable, Dict, Optional
from datetime import datetime

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


logger = logging.getLogger(__name__)


# configuration
MAX_RETRIES = 5
INITIAL_BACKOFF_MS = 100
MAX_BACKOFF_MS = 30000
BACKOFF_MULTIPLIER = 2


class QueueError(Exception):
    """raised when queue operations fail."""
    pass


class MessageQueue:
    """
    redis streams-based message queue.
    
    uses redis streams for durable message storage and consumer groups
    for distributed processing with automatic retry and dlq support.
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        group_name: str = "inbox_workers",
        consumer_name: Optional[str] = None,
    ):
        """
        initialize message queue.
        
        args:
            redis_url: redis connection url
            group_name: consumer group name for distributed processing
            consumer_name: unique consumer identifier (auto-generated if None)
        """
        if not REDIS_AVAILABLE:
            raise QueueError(
                "redis library not available - install with: pip install redis"
            )
        
        self.redis_url = redis_url
        self.group_name = group_name
        self.consumer_name = consumer_name or f"consumer-{id(self)}"
        self._redis: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """establish redis connection."""
        if self._redis is None:
            self._redis = await redis.from_url(
                self.redis_url,
                decode_responses=True,
            )
    
    async def close(self) -> None:
        """close redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    def _get_stream_key(self, agent_id: str) -> str:
        """get redis stream key for agent."""
        return f"agent_inbox:{agent_id}"
    
    def _get_dlq_key(self, agent_id: str) -> str:
        """get dead letter queue key for agent."""
        return f"agent_inbox_dlq:{agent_id}"
    
    async def _ensure_consumer_group(self, stream_key: str) -> None:
        """ensure consumer group exists for stream."""
        if not self._redis:
            raise QueueError("not connected to redis")
        
        try:
            # try to create group (fails if exists)
            await self._redis.xgroup_create(
                stream_key,
                self.group_name,
                id="0",
                mkstream=True,
            )
            logger.info(f"created consumer group {self.group_name} for {stream_key}")
        except redis.ResponseError as e:
            # ignore "BUSYGROUP" error (group already exists)
            if "BUSYGROUP" not in str(e):
                raise
    
    async def push(
        self,
        agent_id: str,
        envelope: Dict[str, Any],
        message_id: str,
    ) -> str:
        """
        push message to agent's inbox queue.
        
        args:
            agent_id: recipient agent canonical uri
            envelope: complete message envelope
            message_id: unique message identifier
            
        returns:
            redis stream message id
            
        raises:
            QueueError: if push fails
        """
        if not self._redis:
            raise QueueError("not connected to redis")
        
        stream_key = self._get_stream_key(agent_id)
        
        # ensure consumer group exists
        await self._ensure_consumer_group(stream_key)
        
        # prepare message data
        message_data = {
            "message_id": message_id,
            "agent_id": agent_id,
            "envelope": json.dumps(envelope),
            "retry_count": "0",
            "queued_at": str(time.time()),
        }
        
        # add to stream
        try:
            stream_id = await self._redis.xadd(stream_key, message_data)
            logger.info(f"queued message {message_id} to {stream_key}: {stream_id}")
            return stream_id
        except Exception as e:
            raise QueueError(f"failed to push message: {e}") from e
    
    async def consume(
        self,
        agent_id: str,
        callback: Callable[[Dict[str, Any]], Any],
        block_ms: int = 5000,
    ) -> None:
        """
        consume messages from agent's inbox queue.
        
        processes messages with automatic retry and dlq handling.
        
        args:
            agent_id: agent canonical uri to consume for
            callback: async function to process envelope
            block_ms: how long to block waiting for messages
            
        raises:
            QueueError: if consumption fails
        """
        if not self._redis:
            raise QueueError("not connected to redis")
        
        stream_key = self._get_stream_key(agent_id)
        dlq_key = self._get_dlq_key(agent_id)
        
        # ensure consumer group exists
        await self._ensure_consumer_group(stream_key)
        
        logger.info(
            f"starting consumer {self.consumer_name} for {stream_key}"
        )
        
        while True:
            try:
                # read from stream
                messages = await self._redis.xreadgroup(
                    self.group_name,
                    self.consumer_name,
                    {stream_key: ">"},
                    count=1,
                    block=block_ms,
                )
                
                if not messages:
                    continue
                
                # process each message
                for stream, message_list in messages:
                    for message_id, message_data in message_list:
                        await self._process_message(
                            stream_key,
                            dlq_key,
                            message_id,
                            message_data,
                            callback,
                        )
            
            except asyncio.CancelledError:
                logger.info(f"consumer {self.consumer_name} cancelled")
                break
            
            except Exception as e:
                logger.error(f"consumer error: {e}", exc_info=True)
                await asyncio.sleep(1)
    
    async def _process_message(
        self,
        stream_key: str,
        dlq_key: str,
        message_id: str,
        message_data: Dict[str, str],
        callback: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """process single message with retry logic."""
        if not self._redis:
            return
        
        try:
            # parse envelope
            envelope = json.loads(message_data["envelope"])
            retry_count = int(message_data.get("retry_count", "0"))
            
            logger.info(
                f"processing message {message_data['message_id']} "
                f"(retry {retry_count}/{MAX_RETRIES})"
            )
            
            # call handler
            await callback(envelope)
            
            # success - acknowledge message
            await self._redis.xack(stream_key, self.group_name, message_id)
            await self._redis.xdel(stream_key, message_id)
            
            logger.info(f"successfully processed message {message_data['message_id']}")
        
        except Exception as e:
            retry_count = int(message_data.get("retry_count", "0"))
            
            if retry_count >= MAX_RETRIES:
                # max retries exceeded - move to dlq
                logger.error(
                    f"max retries exceeded for message {message_data['message_id']}, "
                    f"moving to DLQ: {e}"
                )
                
                # add to dlq
                dlq_data = {
                    **message_data,
                    "failed_at": str(time.time()),
                    "error": str(e),
                }
                await self._redis.xadd(dlq_key, dlq_data)
                
                # acknowledge and remove from main stream
                await self._redis.xack(stream_key, self.group_name, message_id)
                await self._redis.xdel(stream_key, message_id)
            
            else:
                # retry with exponential backoff
                backoff_ms = min(
                    INITIAL_BACKOFF_MS * (BACKOFF_MULTIPLIER ** retry_count),
                    MAX_BACKOFF_MS,
                )
                
                logger.warning(
                    f"message {message_data['message_id']} failed (retry {retry_count}), "
                    f"will retry in {backoff_ms}ms: {e}"
                )
                
                # update retry count
                new_data = {
                    **message_data,
                    "retry_count": str(retry_count + 1),
                    "last_error": str(e),
                    "last_retry_at": str(time.time()),
                }
                
                # re-add to stream after backoff
                await asyncio.sleep(backoff_ms / 1000)
                await self._redis.xadd(stream_key, new_data)
                
                # acknowledge old message
                await self._redis.xack(stream_key, self.group_name, message_id)
                await self._redis.xdel(stream_key, message_id)
    
    async def get_queue_length(self, agent_id: str) -> int:
        """
        get number of pending messages in queue.
        
        args:
            agent_id: agent canonical uri
            
        returns:
            number of pending messages
        """
        if not self._redis:
            raise QueueError("not connected to redis")
        
        stream_key = self._get_stream_key(agent_id)
        return await self._redis.xlen(stream_key)
    
    async def get_dlq_length(self, agent_id: str) -> int:
        """
        get number of messages in dead letter queue.
        
        args:
            agent_id: agent canonical uri
            
        returns:
            number of dlq messages
        """
        if not self._redis:
            raise QueueError("not connected to redis")
        
        dlq_key = self._get_dlq_key(agent_id)
        return await self._redis.xlen(dlq_key)


# global queue instance
_message_queue: Optional[MessageQueue] = None


def get_message_queue(redis_url: str = "redis://localhost:6379") -> MessageQueue:
    """
    get or create global message queue instance.
    
    args:
        redis_url: redis connection url
        
    returns:
        message queue instance
    """
    global _message_queue
    if _message_queue is None:
        _message_queue = MessageQueue(redis_url=redis_url)
    return _message_queue


async def initialize_queue(redis_url: str = "redis://localhost:6379") -> None:
    """
    initialize and connect message queue.
    
    args:
        redis_url: redis connection url
    """
    queue = get_message_queue(redis_url)
    await queue.connect()


async def shutdown_queue() -> None:
    """shutdown message queue."""
    global _message_queue
    if _message_queue:
        await _message_queue.close()
        _message_queue = None

