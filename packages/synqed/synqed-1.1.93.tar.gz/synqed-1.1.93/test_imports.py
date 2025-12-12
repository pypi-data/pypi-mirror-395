"""
Quick test to check if MCP imports work
"""
import sys
sys.path.insert(0, '/Users/dorsa/Desktop/PROJECTS/synq_2/synqed-python/src')

print("Testing imports...")
print(f"Python path: {sys.path[:3]}")
print()

try:
    print("1. Importing synqed...")
    from synqed import MessageRouter
    print("   ✅ synqed.MessageRouter imported")
except Exception as e:
    print(f"   ❌ Failed: {e}")

try:
    print("2. Importing synqed_mcp.a2a.client...")
    from synqed_mcp.a2a.client import A2AClient
    print("   ✅ A2AClient imported")
except Exception as e:
    print(f"   ❌ Failed: {e}")

try:
    print("3. Importing synqed_mcp.registry...")
    from synqed_mcp.registry import get_tool_config, get_tool_registry, list_tools
    print("   ✅ Registry functions imported")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()
print("If all imports succeed, MCP should work!")

