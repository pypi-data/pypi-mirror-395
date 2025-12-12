"""
RemoteA2AAgent - Represents an agent accessible via the A2A protocol.

This module allows Synqed workspaces to route messages to any A2A-compliant agent,
regardless of where it's hosted or what framework it was built with.

The agent just needs to say:
- Here is my endpoint URL
- Here is my schema (A2A AgentCard)
- Here is my auth
- Here is how you call me

And Synqed can route to it.
"""

import logging
from typing import Optional, Dict, Any
import json

from synqed.memory import InboxMessage

logger = logging.getLogger(__name__)


class RemoteA2AAgent:
    """
    Represents a remote agent that implements the A2A protocol.
    
    This is NOT a wrapper that tries to adapt external agents into Synqed's model.
    This is a lightweight client that knows how to talk to A2A endpoints.
    
    Any agent built with ANY framework (not just Synqed) can participate in
    Synqed workspaces as long as it implements the A2A protocol.
    
    Example:
        ```python
        # Register a remote A2A agent
        remote_agent = RemoteA2AAgent(
            url="https://my-agent.example.com",
            auth_token="secret-key"  # Optional
        )
        
        # Discover capabilities
        card = await remote_agent.get_agent_card()
        print(f"Agent: {card['name']}")
        print(f"Skills: {[s['name'] for s in card['skills']]}")
        
        # Register in Synqed workspace
        AgentRuntimeRegistry.register_remote(
            role="ExternalSpecialist",
            agent=remote_agent
        )
        ```
    """
    
    def __init__(
        self,
        url: str,
        name: Optional[str] = None,
        auth_token: Optional[str] = None,
        transport: str = "JSONRPC",
        description: Optional[str] = None,
    ):
        """
        Initialize a remote A2A agent client.
        
        Args:
            url: The A2A endpoint URL for the agent
            name: Optional agent name (will be fetched from AgentCard if not provided)
            auth_token: Optional authentication token
            transport: Transport protocol (JSONRPC, GRPC, or HTTP+JSON)
            description: Optional description (will be fetched from AgentCard if not provided)
        """
        from synqed.memory import AgentMemory
        
        self.url = url
        self._name = name
        self.auth_token = auth_token
        self.transport = transport
        self._description = description
        self._agent_card: Optional[Dict[str, Any]] = None
        self._current_context_id: Optional[str] = None
        self._inbox: list[InboxMessage] = []
        
        # Add attributes for consistency with local Agent interface
        # This allows RemoteA2AAgent to work seamlessly with Synqed's execution engine
        self.memory = AgentMemory(agent_name=name or "RemoteAgent")
        self.default_target: Optional[str] = None  # Remote agents don't have default targets
    
    @property
    def name(self) -> str:
        """Get the agent's name."""
        if self._name:
            return self._name
        if self._agent_card:
            return self._agent_card.get("name", "RemoteAgent")
        return "RemoteAgent"
    
    @property
    def description(self) -> str:
        """Get the agent's description."""
        if self._description:
            return self._description
        if self._agent_card:
            return self._agent_card.get("description", "A remote A2A agent")
        return "A remote A2A agent"
    
    async def get_agent_card(self) -> Dict[str, Any]:
        """
        Fetch the agent's AgentCard from /.well-known/agent-card.json
        
        This discovers the agent's capabilities, skills, authentication requirements,
        and supported transports.
        
        Returns:
            AgentCard dictionary containing agent metadata
        """
        if self._agent_card:
            return self._agent_card
        
        try:
            # Try to import aiohttp
            import aiohttp
        except ImportError:
            raise ImportError(
                "aiohttp is required for remote A2A agents. "
                "Install with: pip install aiohttp"
            )
        
        # Fetch AgentCard
        card_url = f"{self.url.rstrip('/')}/.well-known/agent-card.json"
        
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(card_url, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(
                        f"Failed to fetch AgentCard from {card_url}: "
                        f"HTTP {response.status}"
                    )
                
                self._agent_card = await response.json()
                logger.info(f"Fetched AgentCard for '{self.name}' from {card_url}")
                return self._agent_card
    
    async def send_message(self, message: InboxMessage) -> None:
        """
        Add a message to the agent's inbox (local buffer).
        
        Messages are buffered locally until get_response() is called.
        Also adds to memory for Synqed's internal tracking.
        
        Args:
            message: InboxMessage to add to the inbox
        """
        self._inbox.append(message)
        
        # Add to memory for tracking (Synqed's internal state)
        self.memory.add_message(
            from_agent=message.from_agent,
            content=message.content
        )
        
        logger.debug(f"Added message to inbox for {self.name}: {message.content[:100]}")
    
    async def get_response(self) -> Optional[Dict[str, str]]:
        """
        Send buffered messages to the remote A2A agent and get a response.
        
        This method:
        1. Builds an A2A Message from the inbox
        2. Calls the agent's /v1/message:send endpoint (or JSONRPC equivalent)
        3. Waits for the Task to complete
        4. Extracts the response and structures it as {"send_to": "...", "content": "..."}
        
        Returns:
            Structured response dict with "send_to" and "content"
        """
        if not self._inbox:
            # No messages buffered - check memory for latest unprocessed message
            latest = self.memory.get_latest_message()
            if not latest:
                # Truly no messages - this shouldn't happen in normal flow
                # Return empty response that won't trigger routing
                logger.warning(f"{self.name} called with no messages")
                return {
                    "send_to": "planner", 
                    "content": f"[{self.name} ready]"
                }
            # Use the latest message from memory
            self._inbox.append(latest)
        
        # Skip system messages like [startup] - don't send to remote agent
        if self._inbox:
            latest_message = self._inbox[-1]
            if latest_message.content == "[startup]":
                logger.info(f"RemoteA2AAgent {self.name} - Skipping system [startup] message")
                self._inbox.clear()
                # Return None to indicate no response needed (execution engine will skip this)
                return None
        
        
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "aiohttp is required for remote A2A agents. "
                "Install with: pip install aiohttp"
            )
        
        # Build A2A message from inbox
        latest_message = self._inbox[-1]
        content_text = latest_message.content
        
        logger.info(f"RemoteA2AAgent {self.name} - Sending message to {self.url}")
        logger.info(f"  From: {latest_message.from_agent}")
        logger.info(f"  Content (first 500 chars): {content_text[:500]}")
        logger.info(f"  Content length: {len(content_text)}")
        
        # Build A2A Message structure
        # Note: A2A SDK expects lowercase role without "ROLE_" prefix
        a2a_message = {
            "message_id": f"msg-{id(latest_message)}",
            "context_id": self._current_context_id,
            "role": "user",  # A2A SDK expects "user" or "agent", not "ROLE_USER"
            "parts": [{"text": content_text}]
        }
        
        # Build JSON-RPC request (default transport)
        if self.transport == "JSONRPC":
            request_payload = {
                "jsonrpc": "2.0",
                "method": "message/send",
                "params": {
                    "message": a2a_message,
                    "configuration": {
                        "blocking": True
                    }
                },
                "id": 1
            }
        else:
            raise NotImplementedError(f"Transport '{self.transport}' not yet implemented")
        
        # Send request to remote agent
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                json=request_payload,
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(
                        f"A2A agent request failed: HTTP {response.status}: {error_text}"
                    )
                
                response_data = await response.json()
                
                logger.info(f"RemoteA2AAgent {self.name} - Received response")
                logger.info(f"  Full response: {json.dumps(response_data, indent=2)}")
                logger.info(f"  Response keys: {list(response_data.keys())}")
                
                # Parse JSON-RPC response
                if "error" in response_data:
                    error = response_data["error"]
                    logger.error(f"  Error in response: {error}")
                    raise ValueError(
                        f"A2A agent error: {error.get('message', 'Unknown error')}"
                    )
                
                result = response_data.get("result", {})
                
                logger.info(f"  Result keys: {list(result.keys())}")
                
                # The A2A SDK may wrap the response in a "task" or "message" key
                # Check for wrapped response first
                task = None
                message_response = None
                
                if "task" in result:
                    # Unwrap: {"result": {"task": {...}}}
                    task = result["task"]
                    logger.info(f"  Found wrapped task, keys: {list(task.keys())}")
                elif "message" in result:
                    # Unwrap: {"result": {"message": {...}}}
                    message_response = result["message"]
                    logger.info(f"  Found wrapped message, keys: {list(message_response.keys())}")
                else:
                    # Result might BE the task or message directly (unwrapped)
                    # Check both snake_case and camelCase field names
                    logger.info(f"  Checking if result is task or message directly...")
                    logger.info(f"  Has 'task_id': {'task_id' in result}")
                    logger.info(f"  Has 'taskId': {'taskId' in result}")
                    logger.info(f"  Has 'status': {'status' in result}")
                    logger.info(f"  Has 'artifacts': {'artifacts' in result}")
                    logger.info(f"  Has 'message_id': {'message_id' in result}")
                    logger.info(f"  Has 'messageId': {'messageId' in result}")
                    logger.info(f"  Has 'parts': {'parts' in result}")
                    
                    is_task = (
                        "task_id" in result or "taskId" in result or
                        "status" in result or "artifacts" in result
                    )
                    is_message = (
                        ("message_id" in result or "messageId" in result) and 
                        "parts" in result
                    )
                    
                    logger.info(f"  Looks like Task (direct): {is_task}")
                    logger.info(f"  Looks like Message (direct): {is_message}")
                    
                    task = result if is_task else None
                    message_response = result if is_message else None
                
                logger.info(f"  Treating as task: {task is not None}")
                logger.info(f"  Treating as message: {message_response is not None}")
                
                if task:
                    logger.info(f"  Task keys: {list(task.keys())}")
                    # Extract response from task artifacts or status message
                    artifacts = task.get("artifacts", [])
                    logger.info(f"  Number of artifacts: {len(artifacts)}")
                    if artifacts:
                        # Get content from first artifact
                        logger.info(f"  Artifact 0 keys: {list(artifacts[0].keys())}")
                        parts = artifacts[0].get("parts", [])
                        logger.info(f"  Artifact 0 has {len(parts)} parts")
                        content = self._extract_text_from_parts(parts)
                        logger.info(f"  Extracted content from artifacts (first 200 chars): {content[:200]}")
                    else:
                        # Get content from status message
                        status = task.get("status", {})
                        logger.info(f"  Status keys: {list(status.keys())}")
                        status_message = status.get("message", {})
                        parts = status_message.get("parts", [])
                        logger.info(f"  Status message has {len(parts)} parts")
                        content = self._extract_text_from_parts(parts)
                        logger.info(f"  Extracted content from status (first 200 chars): {content[:200]}")
                    
                    # Update context_id for future messages (handle both snake_case and camelCase)
                    self._current_context_id = task.get("context_id") or task.get("contextId")
                elif message_response:
                    # Direct message response
                    logger.info(f"  Message response keys: {list(message_response.keys())}")
                    parts = message_response.get("parts", [])
                    logger.info(f"  Message has {len(parts)} parts")
                    content = self._extract_text_from_parts(parts)
                    logger.info(f"  Extracted content from message (first 200 chars): {content[:200]}")
                    
                    # Update context_id (handle both snake_case and camelCase)
                    self._current_context_id = message_response.get("context_id") or message_response.get("contextId")
                else:
                    logger.warning("  No task or message in result!")
                    content = "No response from agent"
                
                # Clear inbox after processing
                self._inbox.clear()
                
                logger.info(f"  Final content (first 500 chars): {content[:500]}")
                
                # Parse structured response if possible
                # Try to extract "send_to" from content
                logger.info(f"  Attempting to parse structured response...")
                logger.info(f"  Content preview (first 300 chars): {content[:300]}")
                structured = self._try_parse_structured_response(content)
                if structured:
                    logger.info(f"  ✅ Parsed structured response: send_to={structured['send_to']}, content_len={len(structured['content'])}")
                    return structured
                else:
                    logger.info(f"  ❌ Could not parse structured response")
                
                # Default: return to planner (CEO/coordinator)
                logger.info(f"  Returning unstructured response to planner")
                return {
                    "send_to": "planner",
                    "content": content
                }
    
    def _extract_text_from_parts(self, parts: list) -> str:
        """Extract text content from A2A message parts."""
        texts = []
        for part in parts:
            if "text" in part:
                texts.append(part["text"])
            elif "data" in part:
                # Structured data - convert to JSON string
                texts.append(json.dumps(part["data"]))
        
        return "\n".join(texts) if texts else ""
    
    def _try_parse_structured_response(self, content: str) -> Optional[Dict[str, str]]:
        """
        Try to parse structured response with "send_to" field.
        
        If the A2A agent returns content like:
        {"send_to": "AgentName", "content": "..."}
        
        or wrapped in markdown code fences like:
        ```json
        {"send_to": "AgentName", "content": "..."}
        ```
        
        We extract and return it directly.
        """
        # Strip markdown code fences if present
        content_stripped = content.strip()
        
        logger.info(f"  _try_parse: Original content length: {len(content_stripped)}")
        logger.info(f"  _try_parse: Starts with backticks: {content_stripped.startswith('```')}")
        
        # Check for markdown code fence: ```json ... ``` or ``` ... ```
        if content_stripped.startswith("```"):
            logger.info(f"  _try_parse: Detected markdown code fence, stripping...")
            lines = content_stripped.split("\n")
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line if it's just ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content_stripped = "\n".join(lines).strip()
            logger.info(f"  _try_parse: After stripping, content: {content_stripped[:200]}")
        
        try:
            parsed = json.loads(content_stripped)
            logger.info(f"  _try_parse: Successfully parsed JSON")
            logger.info(f"  _try_parse: Parsed keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'not a dict'}")
            
            if isinstance(parsed, dict) and "send_to" in parsed and "content" in parsed:
                logger.info(f"  _try_parse: ✅ Found send_to and content fields!")
                return {
                    "send_to": parsed["send_to"],
                    "content": parsed["content"]
                }
            else:
                logger.info(f"  _try_parse: ❌ Missing send_to or content fields")
        except (json.JSONDecodeError, TypeError) as e:
            logger.info(f"  _try_parse: ❌ JSON parsing failed: {e}")
        
        return None
    
    def __repr__(self) -> str:
        """String representation."""
        return f"RemoteA2AAgent(name='{self.name}', url='{self.url}')"

