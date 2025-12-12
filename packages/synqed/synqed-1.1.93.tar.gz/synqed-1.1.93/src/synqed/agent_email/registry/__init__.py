"""
agent registry package.

provides discovery and resolution of agent addresses to inbox endpoints.
"""

from synqed.agent_email.registry.models import AgentRegistry, AgentRegistryEntry

__all__ = ["AgentRegistry", "AgentRegistryEntry"]

