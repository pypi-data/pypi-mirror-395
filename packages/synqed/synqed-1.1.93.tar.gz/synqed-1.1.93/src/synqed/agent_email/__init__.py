"""
agent email layer - email-like addressing for agents.

provides:
- global agent addressing (agent://org/name or name@org)
- agent discovery via registry api
- standard a2a inbox http api

architecture:
    ┌─────────────────────────────────────┐
    │         agent addressing            │
    │   agent://org/name ⟷ name@org      │
    └─────────────────────────────────────┘
                    │
    ┌───────────────┴────────────────────┐
    │                                    │
    ▼                                    ▼
┌─────────────────┐          ┌─────────────────┐
│  registry api   │          │   inbox api     │
│  /v1/agents     │          │  /v1/a2a/inbox  │
└─────────────────┘          └─────────────────┘
"""

from synqed.agent_email.addressing import AgentId
from synqed.agent_email.registry.models import AgentRegistry, AgentRegistryEntry
from synqed.agent_email.inbox.api import (
    LocalAgentRuntime,
    A2AInboxRequest,
    A2AInboxResponse,
    register_agent_runtime,
    get_agent_runtime,
)
from synqed.agent_email.auto_workspace import (
    AutoWorkspaceManager,
    AutoWorkspaceConfig,
    get_auto_workspace_manager,
    set_auto_workspace_manager,
)

__all__ = [
    # addressing
    "AgentId",
    # registry
    "AgentRegistry",
    "AgentRegistryEntry",
    # inbox
    "LocalAgentRuntime",
    "A2AInboxRequest",
    "A2AInboxResponse",
    "register_agent_runtime",
    "get_agent_runtime",
    # auto workspace
    "AutoWorkspaceManager",
    "AutoWorkspaceConfig",
    "get_auto_workspace_manager",
    "set_auto_workspace_manager",
]

