"""
Client - Simplified interface for interacting with A2A agents.

This module provides a high-level Python client for communicating with agents
that implement the Agent-to-Agent (A2A) protocol. It abstracts away the complexity
of the underlying protocol and provides intuitive methods for common operations.

Key Features
------------
- **Simple API**: Send messages and receive responses with minimal code
- **Two interaction modes**: Stream responses in real-time or wait for completion
- **Automatic agent discovery**: Fetches agent capabilities automatically
- **Context management**: Built-in async context manager for resource cleanup
- **Task management**: Track, query, and cancel ongoing tasks
- **Type-safe**: Full type hints for better IDE support

Core Methods
------------

ask(message: str) -> str
    Send a message and wait for the complete response.
    
    Use this when:
    - You need the full response before proceeding
    - Response time is reasonable (< 30 seconds)
    - You want simpler code without iteration
    
    Example:
        >>> async with Client("http://localhost:8000") as client:
        ...     answer = await client.ask("What's 2+2?")
        ...     print(f"Answer: {answer}")
        Answer: 4

stream(message: str) -> AsyncIterator[str]
    Send a message and stream response chunks as they arrive.
    
    Use this when:
    - You want to show progress to users (like ChatGPT typing effect)
    - The response might be long
    - You want to process data as it arrives
    
    Example:
        >>> async with Client("http://localhost:8000") as client:
        ...     async for chunk in client.stream("Tell me a story"):
        ...         print(chunk, end="", flush=True)
        Once upon a time...
    
    Note: 
    - `end=""` prevents newlines between chunks
    - `flush=True` displays output immediately (creates typing effect)

Understanding Streaming Parameters
----------------------------------
When using `stream()`, you typically use:
    
    async for chunk in client.stream("message"):
        print(chunk, end="", flush=True)

- **chunk**: A piece of the response text as it arrives (e.g., "Hello", " world", "!")
- **end=""**: Prevents `print()` from adding newline (default is '\\n')
- **flush=True**: Forces immediate output instead of buffering (creates real-time effect)

Additional Methods
------------------
- get_task(task_id: str) -> Task
    Retrieve the current state and history of a task
    
- cancel_task(task_id: str) -> Task
    Cancel a running task and get its final state

Basic Usage
-----------
    from synqed import Client
    import asyncio
    
    async def main():
        # Connect to an agent
        async with Client("http://localhost:8000") as client:
            # Simple request-response
            response = await client.ask("Hello!")
            print(response)
            
            # Streaming response
            print("Streaming: ", end="")
            async for chunk in client.stream("Tell me about Python"):
                print(chunk, end="", flush=True)
            print()
    
    asyncio.run(main())

Advanced Usage
--------------
    # Custom configuration
    client = Client(
        agent_url="http://localhost:8000",
        streaming=True,  # Enable streaming support
        timeout=60.0     # Request timeout in seconds
    )
    
    # Manual resource management (use context manager instead when possible)
    try:
        response = await client.ask("Process this")
    finally:
        await client.close()
    
    # Task management
    task_id = "task-123"
    task = await client.get_task(task_id)
    print(f"Status: {task.status}")
    
    # Cancel long-running tasks
    cancelled = await client.cancel_task(task_id)

Connection Methods
------------------
1. By URL (agent card auto-discovery):
    client = Client("http://localhost:8000")
    
2. By pre-loaded agent card:
    card = AgentCard(...)
    client = Client(agent_card=card)

Best Practices
--------------
1. Always use async context manager (`async with`) for automatic cleanup
2. Use `stream()` for user-facing responses to show progress
3. Use `ask()` for programmatic/API calls where you need the full response
4. Set appropriate timeouts for long-running operations
5. Handle task cancellation for better user experience

Error Handling
--------------
    from synqed import Client
    
    async with Client("http://localhost:8000") as client:
        try:
            response = await client.ask("risky operation")
        except asyncio.TimeoutError:
            print("Request timed out")
        except Exception as e:
            print(f"Error: {e}")

See Also
--------
- Agent: For creating your own agents
- Server: For hosting agents
- Delegator: For coordinating multiple agents

"""

import logging
import uuid
from typing import Any, AsyncIterator

import httpx
from a2a.client import Client, ClientConfig, ClientFactory
from a2a.types import AgentCard, Message, Part, Role, Task, TextPart

logger = logging.getLogger(__name__)


class Client:
    """
    Simplified client for interacting with A2A agents.
    
    This class provides an easy-to-use interface for sending messages to agents
    and receiving responses, without needing to understand A2A protocol details.
    
    Example:
        ```python
        client = Client("http://localhost:8000/a2a/v1")
        
        # Stream a response
        async for response in client.stream("Hello, agent!"):
            print(response)
        
        # Or get the complete response
        result = await client.ask("Tell me a joke")
        print(result)
        ```
    """
    
    def __init__(
        self,
        agent_url: str | None = None,
        agent_card: AgentCard | None = None,
        streaming: bool = True,
        timeout: float = 30.0,
    ):
        """
        Initialize the client.
        
        Args:
            agent_url: URL of the agent (or URL to fetch the agent card from)
            agent_card: Pre-loaded agent card (optional)
            streaming: Whether to use streaming responses (default: True)
            timeout: Request timeout in seconds (default: 30.0)
        """
        if agent_url is None and agent_card is None:
            raise ValueError("Either agent_url or agent_card must be provided")
        
        self.agent_url = agent_url
        self._agent_card = agent_card
        self.streaming = streaming
        self.timeout = timeout
        
        # HTTP client for requests
        self._http_client = httpx.AsyncClient(timeout=timeout)
        
        # A2A client (created lazily)
        self._a2a_client: Client | None = None
        self._client_config = ClientConfig(
            streaming=streaming,
            httpx_client=self._http_client,
        )
    
    async def _get_client(self) -> Client:
        """Get or create the A2A client."""
        if self._a2a_client is None:
            # Get the agent card if not already loaded
            if self._agent_card is None:
                self._agent_card = await self._fetch_card()
            
            # Create the A2A client factory and then the client
            factory = ClientFactory(config=self._client_config)
            self._a2a_client = factory.create(card=self._agent_card)
        
        return self._a2a_client
    
    async def _fetch_card(self) -> AgentCard:
        """Fetch the agent card from the server."""
        if self.agent_url is None:
            raise ValueError("Cannot fetch card without agent_url")
        
        logger.info(f"Fetching agent card from {self.agent_url}")
        
        # Agents should serve their card at /.well-known/agent-card.json
        card_url = self.agent_url.rstrip("/")
        if not card_url.endswith("/.well-known/agent-card.json"):
            # Try common card locations
            base_url = card_url
            card_url = f"{base_url}/.well-known/agent-card.json"
        
        try:
            response = await self._http_client.get(card_url)
            response.raise_for_status()
            card_data = response.json()
            return AgentCard(**card_data)
        except Exception as e:
            logger.error(f"Failed to fetch agent card: {e}")
            raise ValueError(f"Could not fetch agent card from {card_url}: {e}") from e
    
    async def stream(
        self,
        message: str | Message,
        task_id: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Send a message to the agent and stream responses.
        
        Args:
            message: Text message or Message object to send
            task_id: Optional task ID to continue an existing conversation
            
        Yields:
            Response text chunks from the agent
        """
        client = await self._get_client()
        
        # Create message object if needed
        if isinstance(message, str):
            msg = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text=message))],
                message_id=str(uuid.uuid4()),
                task_id=task_id,
            )
        else:
            msg = message
        
        # Send the message
        async for event in client.send_message(msg):
            # Handle different event types
            if isinstance(event, tuple):
                # (Task, Update) pair - ClientEvent
                task, update = event
                # Extract text from the latest message in task history
                if task and task.history:
                    # Get the latest message from the agent
                    for msg in reversed(task.history):
                        if msg.role == Role.agent:
                            text = self._extract_text(msg)
                            if text:
                                yield text
                            break
            elif isinstance(event, Message):
                # Direct message response
                text = self._extract_text(event)
                if text:
                    yield text
    
    async def ask(
        self,
        message: str | Message,
        task_id: str | None = None,
    ) -> str:
        """
        Send a message and wait for the complete response.
        
        Args:
            message: Text message or Message object to send
            task_id: Optional task ID to continue an existing conversation
            
        Returns:
            Complete response text from the agent
        """
        response_parts = []
        async for chunk in self.stream(message, task_id):
            response_parts.append(chunk)
        
        return "".join(response_parts)
    
    async def get_task(self, task_id: str) -> Task:
        """
        Get the current state of a task.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task object with current state and history
        """
        client = await self._get_client()
        from a2a.types import TaskQueryParams
        
        return await client.get_task(TaskQueryParams(id=task_id))
    
    async def cancel_task(self, task_id: str) -> Task:
        """
        Cancel a running task.
        
        Args:
            task_id: ID of the task to cancel
            
        Returns:
            Task object with final state
        """
        client = await self._get_client()
        from a2a.types import TaskIdParams
        
        return await client.cancel_task(TaskIdParams(id=task_id))
    
    def _extract_text(self, message: Message) -> str:
        """Extract text content from a message."""
        text_parts = []
        for part in message.parts:
            # Part has a root attribute that can be TextPart
            if hasattr(part, "root") and isinstance(part.root, TextPart):
                text_parts.append(part.root.text)
        return "".join(text_parts)
    
    async def close(self) -> None:
        """Close the client and cleanup resources."""
        await self._http_client.aclose()
        logger.info("Client closed")
    
    async def __aenter__(self) -> "Client":
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"Client(agent_url='{self.agent_url}', streaming={self.streaming})"

