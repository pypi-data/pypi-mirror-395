"""
mcp server for a2a tool endpoints.

provides model context protocol server exposing salesforce, zoom,
and content creator tools via a2a protocol using synqed infrastructure.

this server:
- registers 3 tool endpoints (salesforce, zoom, content_creator)
- translates mcp tool calls into a2a tasks
- routes tasks via synqed's message router
- returns structured responses

usage:
    # stdio mode (for claude desktop / clients)
    python -m mcp.server --transport stdio
    
    # sse mode (for web/http clients)
    python -m mcp.server --transport sse --host localhost --port 8080
"""

import logging
import json
from typing import Optional

from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger

from synqed import MessageRouter
from synqed_mcp.a2a.client import A2AClient
from synqed_mcp.tools import salesforce, zoom, content_creator

logger = get_logger(__name__)


class MCPServer:
    """
    mcp server for a2a tools.
    
    wraps synqed's a2a infrastructure with mcp protocol,
    exposing remote agent capabilities as mcp tools.
    """
    
    def __init__(
        self,
        name: str = "synqed-a2a-mcp",
        host: str = "localhost",
        port: int = 8080
    ):
        """
        initialize mcp server.
        
        args:
            name: server name
            host: server host (for sse mode)
            port: server port (for sse mode)
        """
        self.name = name
        self.host = host
        self.port = port
        
        # initialize fastmcp
        self.mcp = FastMCP(name, host=host, port=port)
        
        # initialize a2a client (router will be set during run)
        self.router: Optional[MessageRouter] = None
        self.a2a_client: Optional[A2AClient] = None
        
        # register tools
        self._register_tools()
        
        logger.info(f"mcp server initialized: {name}")
    
    def set_router(self, router: MessageRouter):
        """
        set message router for a2a communication.
        
        args:
            router: synqed message router
        """
        self.router = router
        self.a2a_client = A2AClient(router)
        logger.info("message router configured")
    
    def _register_tools(self):
        """register all mcp tools."""
        
        # salesforce tool
        @self.mcp.tool(
            name="salesforce_query_leads",
            description=salesforce.TOOL_SCHEMA["description"]
        )
        async def salesforce_query_leads(query: str) -> str:
            """
            query salesforce leads using soql.
            
            args:
                query: soql query string
                
            returns:
                json string with query results
            """
            if not self.a2a_client:
                return json.dumps({
                    "error": "a2a client not initialized",
                    "status": "error"
                })
            
            result = await salesforce.query_leads(self.a2a_client, query)
            return json.dumps(result, indent=2)
        
        # zoom tool
        @self.mcp.tool(
            name="zoom_create_meeting",
            description=zoom.TOOL_SCHEMA["description"]
        )
        async def zoom_create_meeting(
            topic: str,
            start_time: str,
            duration: int = 60,
            agenda: Optional[str] = None
        ) -> str:
            """
            create a zoom meeting.
            
            args:
                topic: meeting topic/title
                start_time: start time in iso 8601 format
                duration: duration in minutes (default: 60)
                agenda: optional meeting agenda
                
            returns:
                json string with meeting details
            """
            if not self.a2a_client:
                return json.dumps({
                    "error": "a2a client not initialized",
                    "status": "error"
                })
            
            result = await zoom.create_meeting(
                self.a2a_client,
                topic,
                start_time,
                duration,
                agenda
            )
            return json.dumps(result, indent=2)
        
        # content creator tool
        @self.mcp.tool(
            name="content_creator_generate",
            description=content_creator.TOOL_SCHEMA["description"]
        )
        async def content_creator_generate(
            prompt: str,
            tone: str = "professional",
            format: str = "markdown",
            max_length: int = 1000
        ) -> str:
            """
            generate content based on a prompt.
            
            args:
                prompt: content generation prompt
                tone: desired tone (default: "professional")
                format: output format (default: "markdown")
                max_length: max length in characters (default: 1000)
                
            returns:
                json string with generated content
            """
            if not self.a2a_client:
                return json.dumps({
                    "error": "a2a client not initialized",
                    "status": "error"
                })
            
            result = await content_creator.generate_content(
                self.a2a_client,
                prompt,
                tone,
                format,
                max_length
            )
            return json.dumps(result, indent=2)
        
        logger.info("registered 3 mcp tools")
    
    def run(self, transport: str = "stdio"):
        """
        run the mcp server.
        
        args:
            transport: transport mode ("stdio" or "sse")
        """
        logger.info(f"starting mcp server: transport={transport}")
        
        if transport == "sse":
            logger.info(f"mcp server listening at http://{self.host}:{self.port}/sse")
        
        self.mcp.run(transport=transport)


def serve(
    host: str = "localhost",
    port: int = 8080,
    transport: str = "stdio"
):
    """
    serve the mcp server.
    
    args:
        host: server host (for sse mode)
        port: server port (for sse mode)
        transport: transport mode ("stdio" or "sse")
    """
    server = MCPServer(host=host, port=port)
    
    # in production, router would be injected from workspace
    # for now, create a standalone router
    router = MessageRouter()
    server.set_router(router)
    
    # run server
    server.run(transport=transport)


if __name__ == "__main__":
    import sys
    
    # parse command line args
    transport = "stdio"
    host = "localhost"
    port = 8080
    
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]
    
    if "--host" in sys.argv:
        idx = sys.argv.index("--host")
        if idx + 1 < len(sys.argv):
            host = sys.argv[idx + 1]
    
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    
    # serve
    serve(host=host, port=port, transport=transport)

