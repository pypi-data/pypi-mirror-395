"""
Synqed - Inbox-based multi-agent communication system.

This module provides high-level abstractions for creating, managing,
and coordinating AI agents using an inbox-based messaging architecture.

Architecture:
- Agents run as microservices with inbox endpoints (POST /inbox, GET /inbox, POST /respond)
- Agents maintain their own internal conversation memory
- MessageRouter routes messages between agents one at a time
- Agents respond with structured JSON: {"send_to": "AgentName", "content": "text"}
- True agent-to-agent communication via structured actions
"""

import asyncio
import aiohttp

from synqed.agent import (
    Agent, 
    AgentLogicContext, 
    ResponseBuilder,
    parse_llm_response,
    extract_partial_json_content,
    get_team_roster,
    get_interaction_protocol,
)
from synqed.server import AgentServer
from synqed.memory import AgentMemory, InboxMessage
from synqed.router import MessageRouter
from synqed.planner import PlannerLLM, TaskTreePlan, TaskTreeNode
from synqed.planner_agent import PlannerAgent
from synqed.display import MessageDisplay
from synqed.execution_engine import WorkspaceExecutionEngine
from synqed.workspace_manager import Workspace, WorkspaceManager, AgentRuntimeRegistry
from synqed.a2a_remote_agent import RemoteA2AAgent
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
from synqed.agent_factory import (
    create_generic_agent_logic,
    create_agent_from_spec,
    create_agents_from_specs,
    validate_deep_reasoning,
    enforce_structured_output,
    format_content_with_reasoning,
)
from synqed.llm_utils import (
    extract_json_from_llm_output,
    validate_visible_reasoning,
    create_fallback_response,
)

# MDAP/MAKER framework
from synqed.mdap import (
    # types
    StepInput,
    StepOutput,
    StepSpec,
    ModelConfig,
    MdapConfig,
    VotingStats,
    # red flagging
    RedFlagger,
    # voting
    Voter,
    VotingResult,
    # calibration
    CalibrationReport,
    estimate_p_and_cost,
    choose_k_for_target_success,
    compute_expected_cost,
    # execution
    MdapExecutor,
    # step runner
    StepRunnerInterface,
    SynqedStepRunner,
)

__version__ = "1.1.93"

__all__ = [
    # === Core Agent Components ===
    "Agent",
    "AgentLogicContext",
    "ResponseBuilder",
    "AgentServer",
    
    # === Remote A2A Integration ===
    "RemoteA2AAgent",
    
    # === Agent Email Layer ===
    "AgentId",
    "AgentRegistry",
    "AgentRegistryEntry",
    "LocalAgentRuntime",
    "A2AInboxRequest",
    "A2AInboxResponse",
    "register_agent_runtime",
    "get_agent_runtime",
    "AutoWorkspaceManager",
    "AutoWorkspaceConfig",
    "get_auto_workspace_manager",
    "set_auto_workspace_manager",
    
    # === Memory ===
    "AgentMemory",
    "InboxMessage",
    
    # === Routing ===
    "MessageRouter",
    
    # === Workspace Management ===
    "Workspace",
    "WorkspaceManager",
    "AgentRuntimeRegistry",
    
    # === Planning ===
    "PlannerLLM",
    "PlannerAgent",
    "TaskTreePlan",
    "TaskTreeNode",
    
    # === Execution ===
    "WorkspaceExecutionEngine",
    "MessageDisplay",
    
    # === Agent Factory ===
    "create_generic_agent_logic",
    "create_agent_from_spec",
    "create_agents_from_specs",
    "validate_deep_reasoning",
    "enforce_structured_output",
    "format_content_with_reasoning",
    
    # === LLM Utils ===
    "extract_json_from_llm_output",
    "validate_visible_reasoning",
    "create_fallback_response",
    
    # === Response Parsing Utils ===
    "parse_llm_response",
    "extract_partial_json_content",
    
    # === Team Coordination Utils ===
    "get_team_roster",
    "get_interaction_protocol",
    
    # === MDAP/MAKER Framework ===
    # types
    "StepInput",
    "StepOutput",
    "StepSpec",
    "ModelConfig",
    "MdapConfig",
    "VotingStats",
    # red flagging
    "RedFlagger",
    # voting
    "Voter",
    "VotingResult",
    # calibration
    "CalibrationReport",
    "estimate_p_and_cost",
    "choose_k_for_target_success",
    "compute_expected_cost",
    # execution
    "MdapExecutor",
    # step runner
    "StepRunnerInterface",
    "SynqedStepRunner",
    
    # === Utils ===
    "asyncio",
    "aiohttp",
]
