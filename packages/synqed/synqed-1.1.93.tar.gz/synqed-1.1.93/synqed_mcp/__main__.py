"""
entrypoint for running synqed mcp server as module.

usage:
    python -m synqed_mcp
"""

from synqed_mcp.server_cloud import main

if __name__ == "__main__":
    main()
