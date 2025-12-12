"""
AgentServer - FastAPI server running an Agent with inbox endpoints.

This module provides the AgentServer class that serves an Agent
with POST /inbox, GET /inbox, and POST /respond endpoints.
"""

import asyncio
import logging
from typing import Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from synqed.agent import Agent
from synqed.memory import InboxMessage

logger = logging.getLogger(__name__)


# Filter to suppress CancelledError logging during server shutdown
class _CancelledErrorFilter(logging.Filter):
    """Suppresses CancelledError tracebacks that occur during graceful shutdown."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno == logging.ERROR:
            # Check exception info
            if record.exc_info:
                exc_type = record.exc_info[0]
                if exc_type and exc_type.__name__ == "CancelledError":
                    return False
            # Also check if message contains traceback with CancelledError
            msg = str(record.getMessage())
            if "CancelledError" in msg or "asyncio.exceptions.CancelledError" in msg:
                return False
        return True


# Apply the filter to suppress noisy shutdown errors
_cancelled_error_filter = _CancelledErrorFilter()
logging.getLogger("uvicorn.error").addFilter(_cancelled_error_filter)
logging.getLogger("uvicorn").addFilter(_cancelled_error_filter)


class AgentResponse(BaseModel):
    """Structured response from an agent."""
    send_to: str
    content: str


class AgentServer:
    """
    Server for hosting Agents with inbox endpoints.
    
    This server provides:
    - POST /inbox: Receive messages in the agent's inbox
    - GET /inbox: Get all messages in the agent's inbox
    - POST /respond: Process inbox and generate a response
    
    Example:
        ```python
        agent = Agent(
            name="Writer",
            description="Creative writer",
            logic=writer_logic
        )
        
        server = AgentServer(
            agent=agent,
            port=8001
        )
        
        await server.start_background()
        ```
    """
    
    def __init__(
        self,
        agent: Agent,
        port: int,
        host: str = "0.0.0.0",
        path_prefix: str = "",
        enable_cors: bool = True,
    ):
        """
        Initialize the agent server.
        
        Args:
            agent: The Agent instance to serve
            port: Port to bind to
            host: Host to bind to (default: 0.0.0.0)
            path_prefix: Path prefix for endpoints (default: empty string)
            enable_cors: Whether to enable CORS (default: True)
        """
        self.agent = agent
        self.host = host
        self.port = port
        self.path_prefix = path_prefix
        
        # Create FastAPI app
        self.app = FastAPI(title=f"{agent.name} Server")
        
        # Add inbox endpoints
        self._add_inbox_endpoints()
        
        # Add welcome endpoint
        self._add_welcome_endpoint()
        
        # Enable CORS if requested
        if enable_cors:
            self._enable_cors()
        
        # Server process reference
        self._server_task: asyncio.Task | None = None
        self._server_started = False
        self._uvicorn_server: Any | None = None
    
    def _add_inbox_endpoints(self) -> None:
        """Add inbox endpoints to the FastAPI app."""
        
        @self.app.post("/inbox")
        async def post_inbox(message: InboxMessage) -> dict:
            """
            Receive a message in the agent's inbox.
            
            Args:
                message: InboxMessage with from_agent and content
                
            Returns:
                Status confirmation
            """
            self.agent.memory.add_message(
                from_agent=message.from_agent,
                content=message.content
            )
            return {
                "status": "received",
                "agent": self.agent.name,
                "message_count": len(self.agent.memory.messages)
            }
        
        @self.app.get("/inbox")
        async def get_inbox() -> dict:
            """
            Get all messages in the agent's inbox.
            
            Returns:
                Dictionary with agent name, messages, and count
            """
            messages = self.agent.memory.get_messages()
            # Use model_dump() for Pydantic v2, fallback to dict() for v1
            try:
                message_dicts = [msg.model_dump() for msg in messages]
            except AttributeError:
                message_dicts = [msg.dict() for msg in messages]
            return {
                "agent": self.agent.name,
                "messages": message_dicts,
                "count": len(messages)
            }
        
        @self.app.post("/respond")
        async def respond() -> AgentResponse:
            """
            Process inbox and generate a response.
            
            This endpoint:
            1. Calls the agent's logic function
            2. Ensures response is structured JSON
            3. Returns AgentResponse with send_to and content
            
            Returns:
                AgentResponse with structured response
                
            Raises:
                HTTPException: If response generation fails
            """
            try:
                response_dict = await self.agent.process()
                
                # Validate response structure
                if "send_to" not in response_dict or "content" not in response_dict:
                    raise ValueError("Invalid response structure: missing send_to or content")
                
                return AgentResponse(**response_dict)
                
            except Exception as e:
                import traceback
                error_detail = f"Error generating response: {str(e)}\n{traceback.format_exc()}"
                raise HTTPException(status_code=500, detail=error_detail) from e
    
    def _add_welcome_endpoint(self) -> None:
        """Add a welcome GET endpoint at the root."""
        @self.app.get("/")
        async def welcome():
            return {
                "agent": self.agent.name,
                "description": self.agent.description,
                "status": "online",
                "endpoints": {
                    "POST /inbox": "Receive messages",
                    "GET /inbox": "Get all messages",
                    "POST /respond": "Process inbox and generate response"
                }
            }
        
        @self.app.get("/favicon.ico")
        async def favicon():
            """Handle favicon requests to prevent 404 errors."""
            from fastapi.responses import Response
            return Response(status_code=204)
    
    def _enable_cors(self) -> None:
        """Enable CORS for the FastAPI app."""
        try:
            from fastapi.middleware.cors import CORSMiddleware
            
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            logger.info("CORS enabled for agent server")
        except ImportError:
            logger.warning("FastAPI not available, CORS not enabled")
    
    async def start(self) -> None:
        """
        Start the server (blocking).
        
        This will run the server until interrupted.
        """
        try:
            import uvicorn
        except ImportError as e:
            raise ImportError(
                "uvicorn is required to run the server. "
                "Install with: pip install uvicorn"
            ) from e
        
        logger.info(
            f"Starting agent server for '{self.agent.name}' on "
            f"http://{self.host}:{self.port}{self.path_prefix}"
        )
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )
        server = uvicorn.Server(config)
        self._server_started = True
        
        try:
            await server.serve()
        finally:
            self._server_started = False
    
    async def start_background(self) -> None:
        """
        Start the server in the background.
        
        Returns immediately while the server runs in a background task.
        Use stop() to shut down the server.
        """
        if self._server_task is not None:
            logger.warning("Server is already running in background")
            return
        
        self._server_task = asyncio.create_task(self._run_background())
        
        # Wait a bit for server to start
        await asyncio.sleep(1)
        
        logger.info(
            f"Agent server started in background for '{self.agent.name}' on "
            f"http://{self.host}:{self.port}{self.path_prefix}"
        )
    
    async def _run_background(self) -> None:
        """Internal method to run server in background."""
        try:
            import uvicorn
        except ImportError as e:
            raise ImportError(
                "uvicorn is required to run the server. "
                "Install with: pip install uvicorn"
            ) from e
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )
        server = uvicorn.Server(config)
        self._uvicorn_server = server
        self._server_started = True
        
        try:
            await server.serve()
        except asyncio.CancelledError:
            # Expected when server is stopped - suppress the error
            logger.debug(f"Server task cancelled for agent '{self.agent.name}'")
        except Exception as e:
            logger.error(f"Unexpected error in server task for agent '{self.agent.name}': {e}")
            raise
        finally:
            self._server_started = False
            self._server_task = None
            self._uvicorn_server = None
    
    async def stop(self) -> None:
        """Stop the background server."""
        if self._server_task is None:
            logger.warning("Server is not running")
            return
        
        # Shutdown uvicorn gracefully
        if self._uvicorn_server is not None:
            self._uvicorn_server.should_exit = True
            # Give it more time to shutdown gracefully
            await asyncio.sleep(0.5)
        
        # Cancel the server task
        if self._server_task and not self._server_task.done():
            self._server_task.cancel()
            try:
                await self._server_task
            except (asyncio.CancelledError, Exception) as e:
                # Suppress CancelledError and other expected shutdown errors
                if isinstance(e, asyncio.CancelledError):
                    pass  # Expected during shutdown
                else:
                    logger.debug(f"Error during server shutdown: {e}")
        
        logger.info(f"Server stopped for agent '{self.agent.name}'")
        self._server_task = None
        self._server_started = False
        self._uvicorn_server = None
    
    @property
    def is_running(self) -> bool:
        """Check if the server is currently running."""
        return self._server_started
    
    @property
    def url(self) -> str:
        """Get the server URL."""
        client_host = "localhost" if self.host == "0.0.0.0" else self.host
        return f"http://{client_host}:{self.port}{self.path_prefix}"
    
    def __repr__(self) -> str:
        """String representation of the server."""
        status = "running" if self.is_running else "stopped"
        return (
            f"AgentServer(agent='{self.agent.name}', "
            f"url='{self.url}', status='{status}')"
        )
