"""
synqed_mcp - model context protocol wrapper for a2a in synqed.

provides mcp server exposing remote a2a agent capabilities as mcp tools.

this package bridges:
- mcp protocol (used by claude desktop and other ai assistants)
- a2a protocol (google's agent-to-agent communication)
- synqed infrastructure (workspace-based agent coordination)

architecture:
    mcp client → mcp server → a2a client → message router → a2a agents
    
usage:
    # start mcp server (stdio mode - requires fastmcp)
    python -m synqed_mcp --transport stdio
    
    # start cloud mcp server (http mode - no fastmcp required)
    python -m synqed_mcp --host 0.0.0.0 --port 8080
    
    # or use in code
    from synqed_mcp.server import MCPServer  # requires fastmcp
    from synqed_mcp.server_cloud import GlobalMCPServer  # no fastmcp needed
    from synqed import MessageRouter
    
    server = GlobalMCPServer(MessageRouter())
    server.run_cloud()
"""

# Only import A2AClient by default (no fastmcp dependency)
# Other imports should be done explicitly to avoid requiring fastmcp
from synqed_mcp.a2a import A2AClient

__all__ = ["A2AClient"]

# Note: MCPServer and serve require fastmcp and should be imported explicitly:
# from synqed_mcp.server import MCPServer, serve

