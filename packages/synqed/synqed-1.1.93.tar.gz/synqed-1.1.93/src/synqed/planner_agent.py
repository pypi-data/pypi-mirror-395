"""
PlannerAgent - The CEO agent that sits in the root workspace.

This module provides the PlannerAgent class that:
- Is the ONLY agent in the root workspace
- Is the ONLY agent the user interacts with
- Coordinates all child workspace execution agents
- Synthesizes results from child workspaces
- Delivers final consolidated output to the user
- Controls ALL user input requests (explicit structured protocol)

The PlannerAgent wraps PlannerLLM and implements the Agent interface,
allowing it to participate in the workspace execution system.

USER INPUT REQUEST PROTOCOL:
- Agents NEVER ask the user for input directly
- When an agent needs user input, it sends an internal [need_user_input] message to Planner
- Planner evaluates the request and may emit a structured user_input_request
- Planner controls when and how the user is asked for input
- User responses are routed back through Planner to the requesting agent

Child workspaces contain ONLY execution agents that:
- Do NOT perform planning, delegation, or task decomposition
- Execute the specific subtask assigned by the PlannerAgent
- Return deliverables back to the PlannerAgent
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Optional, List, Dict
from dataclasses import dataclass, asdict

from synqed.agent import Agent, AgentLogicContext
from synqed.memory import AgentMemory
from synqed.planner import PlannerLLM

logger = logging.getLogger(__name__)


# ============================================================
# User Input Request Protocol - Structured Messages
# ============================================================

@dataclass
class AgentInputNeed:
    """
    Internal message from agent to Planner indicating user input is needed.
    Agents send this to Planner; Planner decides whether to ask user.
    """
    agent_name: str
    reason: str  # Why input is needed
    what_is_needed: str  # What information is required
    suggested_question: Optional[str] = None  # Optional suggested question for user


def parse_agent_input_need(content: str, sender: str) -> Optional[AgentInputNeed]:
    """
    Parse an internal [need_user_input] message from an agent.
    Returns None if the message is not a user input request.
    """
    if not content.startswith("[need_user_input]"):
        return None
    
    try:
        # Parse the JSON payload after the prefix
        payload_str = content[len("[need_user_input]"):]
        payload = json.loads(payload_str)
        
        return AgentInputNeed(
            agent_name=payload.get("agent_name", sender),
            reason=payload.get("reason", "Agent needs additional information"),
            what_is_needed=payload.get("what_is_needed", "user input"),
            suggested_question=payload.get("suggested_question"),
        )
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Failed to parse [need_user_input] message: {e}")
        return None


def parse_user_input_response(content: str) -> Optional[Dict[str, Any]]:
    """
    Parse a [user_input_response] message containing user's response.
    Returns the parsed data or None if not a response message.
    """
    if not content.startswith("[user_input_response]"):
        return None
    
    # Parse the structured response
    lines = content.split("\n")
    result = {
        "requesting_agent": None,
        "content": "",
    }
    
    content_started = False
    content_lines = []
    
    for line in lines[1:]:  # Skip the first line (the marker)
        if line.startswith("Original request by:"):
            result["requesting_agent"] = line.split(":", 1)[1].strip()
        elif line.startswith("User response:"):
            content_started = True
        elif content_started:
            content_lines.append(line)
    
    result["content"] = "\n".join(content_lines).strip()
    return result


# System prompt for the Planner Agent's coordination role
PLANNER_AGENT_SYSTEM_PROMPT = """
═══════════════════════════════════════════════════════════════════════════════
PLANNER AGENT (CEO) - ROOT WORKSPACE COORDINATOR
═══════════════════════════════════════════════════════════════════════════════

You are the PLANNER AGENT, the CEO of this multi-agent system. You are the ONLY
agent the user interacts with directly.

YOUR RESPONSIBILITIES:
1. Receive the user's task and understand their requirements
2. Coordinate work across specialized execution teams in child workspaces
3. Monitor progress from all teams
4. Synthesize results from child workspaces into coherent deliverables
5. Deliver the final consolidated output to the user

CRITICAL RULES:
- You do NOT execute tasks yourself - you coordinate execution agents
- You receive [subteam_result] messages when child workspaces complete their work
- You must synthesize ALL results before delivering to USER
- Your final response to USER must be comprehensive and actionable

WHEN YOU RECEIVE A TASK FROM USER:
- Acknowledge the task structure and teams working on it
- Explain how you will coordinate the work
- Let the user know you're orchestrating the execution

WHEN YOU RECEIVE [subteam_result] MESSAGES:
- Parse the results from each child workspace
- Track which teams have completed their work
- When ALL teams have reported, synthesize their outputs
- Deliver the consolidated result to USER

RESPONSE FORMAT:
{
  "send_to": "<USER or team_name>",
  "visible_reasoning": "<your coordination thinking>",
  "collaboration": "<cross-team coordination notes>",
  "content": "<the actual message/deliverable>"
}

═══════════════════════════════════════════════════════════════════════════════
"""


async def create_planner_agent_logic(
    planner_llm: PlannerLLM,
    child_workspace_count: int = 0,
    child_descriptions: Optional[List[str]] = None,
):
    """
    Create the logic function for the PlannerAgent.
    
    This returns an async function that implements the coordination logic
    for the root workspace.
    
    Args:
        planner_llm: The PlannerLLM instance for LLM calls
        child_workspace_count: Number of child workspaces to coordinate
        child_descriptions: Descriptions of each child workspace's task
        
    Returns:
        Async logic function for the PlannerAgent
    """
    # Track received results from child workspaces
    received_results: Dict[str, str] = {}
    
    async def planner_logic(context: AgentLogicContext) -> Optional[dict]:
        """
        The PlannerAgent's core logic function.
        
        Handles:
        1. Initial task from USER -> acknowledge and coordinate
        2. [subteam_result] messages -> collect and synthesize
        3. Deliver final consolidated output when all teams complete
        """
        nonlocal received_results
        
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        content = latest.content
        sender = latest.from_agent or "SYSTEM"
        
        # Skip system startup messages
        if content == "[startup]":
            return None
        
        # Handle subteam_result messages from child workspaces
        if content.startswith("[subteam_result]"):
            try:
                # Parse the result payload
                payload_str = content[len("[subteam_result]"):]
                payload = json.loads(payload_str)
                
                child_workspace_id = payload.get("child_workspace_id", "unknown")
                result_message = payload.get("result_message", "")
                
                # Store the result
                received_results[child_workspace_id] = result_message
                
                logger.info(
                    f"PlannerAgent received result from workspace {child_workspace_id}. "
                    f"Progress: {len(received_results)}/{child_workspace_count}"
                )
                
                # Check if all child workspaces have completed
                if len(received_results) >= child_workspace_count and child_workspace_count > 0:
                    # All teams have reported - synthesize and deliver final output
                    return await _synthesize_final_output(
                        planner_llm=planner_llm,
                        results=received_results,
                        child_descriptions=child_descriptions or [],
                        context=context,
                    )
                else:
                    # Still waiting for more teams
                    return {
                        "send_to": "USER",
                        "visible_reasoning": (
                            f"Received results from team. "
                            f"Progress: {len(received_results)}/{child_workspace_count} teams completed. "
                            f"Waiting for remaining teams to finish their work."
                        ),
                        "collaboration": "",
                        "content": (
                            f"📊 **Progress Update**: {len(received_results)}/{child_workspace_count} "
                            f"teams have completed their work. Waiting for remaining teams..."
                        ),
                    }
                    
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse subteam_result: {e}")
                return None
        
        # Handle initial task from USER
        if sender.upper() == "USER":
            # Acknowledge the task and explain coordination approach
            team_info = ""
            if child_descriptions:
                team_info = "\n".join([
                    f"  • Team {i+1}: {desc}"
                    for i, desc in enumerate(child_descriptions)
                ])
            else:
                team_info = f"  • {child_workspace_count} specialized teams"
            
            return {
                "send_to": "USER",
                "visible_reasoning": (
                    f"I have received the user's task. As the CEO/Planner, I am now coordinating "
                    f"{child_workspace_count} specialized teams to execute different aspects of this task. "
                    f"Each team will work on their assigned subtask in parallel. "
                    f"I will synthesize all results when teams complete their work."
                ),
                "collaboration": "",
                "content": (
                    f"🎯 **Task Received**\n\n"
                    f"I'm coordinating {child_workspace_count} specialized teams to work on your task:\n\n"
                    f"{team_info}\n\n"
                    f"I'll synthesize their outputs and deliver a comprehensive result once all teams complete."
                ),
            }
        
        # Handle other messages (relay or respond)
        return {
            "send_to": "USER",
            "visible_reasoning": f"Received message from {sender}. Forwarding coordination update to user.",
            "collaboration": "",
            "content": f"📬 Update from {sender}: {content[:500]}...",
        }
    
    return planner_logic


async def _synthesize_final_output(
    planner_llm: PlannerLLM,
    results: Dict[str, str],
    child_descriptions: List[str],
    context: AgentLogicContext,
) -> dict:
    """
    Synthesize results from all child workspaces into a final deliverable.
    
    Uses the PlannerLLM to intelligently combine outputs from all teams
    into a coherent, comprehensive response for the user.
    
    IMPORTANT: This returns a DELIVERABLE type response. The execution engine
    should store the full content as a deliverable and only send the short
    notification message to the chat.
    
    Args:
        planner_llm: The PlannerLLM instance for synthesis
        results: Dictionary of workspace_id -> result content
        child_descriptions: List of child workspace task descriptions
        context: The agent logic context
        
    Returns:
        Deliverable response with type="deliverable"
    """
    # Build a summary of all results
    results_summary = "\n\n".join([
        f"=== Team {i+1} Result ===\n{result}"
        for i, (workspace_id, result) in enumerate(results.items())
    ])
    
    # Use LLM to synthesize (if available)
    try:
        synthesis_prompt = f"""You are synthesizing results from multiple teams into a final deliverable.

TEAM RESULTS:
{results_summary}

Create a comprehensive, well-organized final output that:
1. Integrates all team contributions coherently
2. Highlights key deliverables and outcomes
3. Provides actionable next steps if applicable
4. Is formatted for easy reading (use headers, bullet points, etc.)

Respond with the synthesized content only - no meta-commentary."""

        # Make LLM call for synthesis
        synthesis = await planner_llm._call_llm(
            system_prompt="You are an expert at synthesizing multi-team outputs into cohesive deliverables.",
            user_prompt=synthesis_prompt,
        )
        
        final_content = synthesis
        
    except Exception as e:
        logger.warning(f"LLM synthesis failed, using manual concatenation: {e}")
        # Fallback: concatenate results
        final_content = (
            "# Final Deliverable\n\n"
            "The following is a compilation of work from all teams:\n\n"
            + results_summary
        )
    
    # Generate a title for the deliverable
    deliverable_title = "Task Deliverable - All Teams Complete"
    
    # Return a DELIVERABLE type response
    # The execution engine will:
    # 1. Store the full content as a deliverable
    # 2. Only send the short notification to chat
    return {
        "type": "deliverable",  # <-- DELIBERATE deliverable marker
        "send_to": "USER",
        "visible_reasoning": (
            f"All {len(results)} teams have completed their work. "
            f"I have synthesized their outputs into a comprehensive final deliverable. "
            f"This represents the consolidated effort of all specialized teams."
        ),
        "collaboration": "",
        # Short notification for chat
        "content": (
            f"✅ **All Teams Complete**\n\n"
            f"Your deliverable is ready! View the full document in the **Deliverables** tab.\n\n"
            f"📄 *{deliverable_title}*"
        ),
        # Full deliverable content (stored separately, not in chat)
        "deliverable_title": deliverable_title,
        "deliverable_content": final_content,
    }


class PlannerAgent(Agent):
    """
    The CEO agent that coordinates all work in the multi-agent system.
    
    This agent:
    - Is the ONLY agent in the root workspace
    - Is the ONLY agent the user interacts with directly
    - Does NOT execute tasks - it coordinates execution agents
    - Synthesizes results from child workspaces
    - Delivers final consolidated output to the user
    - CONTROLS all user input requests (explicit structured protocol)
    
    USER INPUT REQUEST PROTOCOL:
    - Agents send [need_user_input] messages to Planner
    - Planner evaluates and may emit a user_input_request
    - User responds; Planner routes response to requesting agent
    - No heuristics, no regex - only explicit structured messages
    
    The PlannerAgent wraps a PlannerLLM and uses it for:
    - LLM calls for synthesis and coordination
    - (Task planning is done BEFORE workspace creation, not by this agent)
    
    Example:
        ```python
        # Create PlannerLLM
        planner_llm = PlannerLLM(provider="anthropic", api_key="...")
        
        # Create PlannerAgent for root workspace
        planner_agent = PlannerAgent(
            planner_llm=planner_llm,
            child_workspace_count=3,
            child_descriptions=["Team 1 task", "Team 2 task", "Team 3 task"],
        )
        
        # Register as the only agent in root workspace
        AgentRuntimeRegistry.register("planner", planner_agent)
        ```
    """
    
    def __init__(
        self,
        planner_llm: PlannerLLM,
        child_workspace_count: int = 0,
        child_descriptions: Optional[List[str]] = None,
        name: str = "planner",
        description: str = "CEO/Planner agent that coordinates all execution teams",
        user_input_callback: Optional[callable] = None,
    ):
        """
        Initialize the PlannerAgent.
        
        Args:
            planner_llm: The PlannerLLM instance for LLM calls
            child_workspace_count: Number of child workspaces to coordinate
            child_descriptions: Optional list of child workspace task descriptions
            name: Agent name (default: "planner")
            description: Agent description
            user_input_callback: Callback to create user input requests
        """
        self.planner_llm = planner_llm
        self.child_workspace_count = child_workspace_count
        self.child_descriptions = child_descriptions or []
        self._received_results: Dict[str, str] = {}
        
        # User input request tracking
        self._pending_input_requests: Dict[str, AgentInputNeed] = {}  # request_id -> need
        self._user_input_callback = user_input_callback  # callback to emit requests
        
        # Create the logic function
        async def planner_logic(context: AgentLogicContext) -> Optional[dict]:
            return await self._process_message(context)
        
        # Initialize parent Agent class
        super().__init__(
            name=name,
            description=description,
            logic=planner_logic,
            default_target="USER",
            capabilities=["coordination", "synthesis", "planning", "orchestration", "user_input_control"],
        )
    
    async def _process_message(self, context: AgentLogicContext) -> Optional[dict]:
        """
        Process incoming messages to the PlannerAgent.
        
        Handles:
        1. Initial task from USER
        2. [subteam_result] messages from child workspaces
        3. [need_user_input] messages from agents - emit structured requests
        4. [user_input_response] messages - route to requesting agent
        5. Synthesis and final delivery when all teams complete
        """
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        content = latest.content
        sender = latest.from_agent or "SYSTEM"
        
        # Skip system startup messages
        if content == "[startup]":
            return None
        
        # Handle subteam_result messages from child workspaces
        if content.startswith("[subteam_result]"):
            return await self._handle_subteam_result(content, context)
        
        # Handle agent request for user input
        agent_input_need = parse_agent_input_need(content, sender)
        if agent_input_need:
            return await self._handle_agent_input_need(agent_input_need, context)
        
        # Handle user input response (routed from frontend)
        user_response = parse_user_input_response(content)
        if user_response:
            return await self._handle_user_input_response(user_response, context)
        
        # Handle initial task from USER
        if sender.upper() == "USER":
            return self._handle_user_task(content, context)
        
        # Handle other messages
        return {
            "send_to": "USER",
            "visible_reasoning": f"Received coordination update from {sender}.",
            "collaboration": "",
            "content": f"📬 Update from {sender}: {content[:500]}",
        }
    
    async def _handle_agent_input_need(
        self,
        need: AgentInputNeed,
        context: AgentLogicContext,
    ) -> Optional[dict]:
        """
        Handle an agent's request for user input.
        
        Planner evaluates the request and emits a structured user_input_request.
        This is the ONLY way user input requests are created - no heuristics.
        """
        logger.info(f"📋 Agent {need.agent_name} needs user input: {need.what_is_needed}")
        
        # Generate a request ID
        request_id = str(uuid.uuid4())
        
        # Store the pending request for later routing
        self._pending_input_requests[request_id] = need
        
        # Build the user-facing instructions
        instructions = need.suggested_question or (
            f"The {need.agent_name.replace('_', ' ')} agent needs additional information to continue.\n\n"
            f"**What's needed:** {need.what_is_needed}\n\n"
            f"**Why:** {need.reason}\n\n"
            f"Please provide the requested information below."
        )
        
        # Emit the structured user_input_request
        # This is returned as a special type that the execution engine will handle
        return {
            "type": "user_input_request",  # <-- Explicit structured request
            "send_to": "USER",
            "visible_reasoning": (
                f"Agent {need.agent_name} has requested user input. "
                f"Reason: {need.reason}. "
                f"I am emitting a structured request for the frontend to display."
            ),
            "collaboration": "",
            "content": (
                f"⏸️ **Input Required**\n\n"
                f"The {need.agent_name.replace('_', ' ')} team needs your input to continue.\n\n"
                f"Please respond with the requested information."
            ),
            # Structured request data for the execution engine
            "user_input_request": {
                "id": request_id,
                "requested_by": need.agent_name,
                "context_summary": need.reason,
                "instructions": instructions,
                "what_is_needed": need.what_is_needed,
            },
        }
    
    async def _handle_user_input_response(
        self,
        response: Dict[str, Any],
        context: AgentLogicContext,
    ) -> Optional[dict]:
        """
        Handle user's response to an input request.
        
        Routes the response back to the agent that originally requested input.
        """
        requesting_agent = response.get("requesting_agent")
        user_content = response.get("content", "")
        
        if not requesting_agent:
            # No specific agent - broadcast to all
            logger.info("📨 User response received - broadcasting to all agents")
            return {
                "send_to": "ALL",
                "visible_reasoning": "User provided input. Forwarding to all agents.",
                "collaboration": "",
                "content": f"📬 User Response:\n\n{user_content}",
            }
        
        logger.info(f"📨 Routing user response to agent: {requesting_agent}")
        
        # Find and clear the pending request
        for req_id, need in list(self._pending_input_requests.items()):
            if need.agent_name == requesting_agent:
                del self._pending_input_requests[req_id]
                break
        
        # Route to the specific agent
        return {
            "send_to": requesting_agent,
            "visible_reasoning": (
                f"User has provided the requested input. "
                f"Routing to {requesting_agent} to continue their work."
            ),
            "collaboration": "",
            "content": (
                f"📬 **User Response to Your Request**\n\n"
                f"{user_content}\n\n"
                f"Please continue with your task using this information."
            ),
        }
    
    async def _handle_subteam_result(
        self,
        content: str,
        context: AgentLogicContext,
    ) -> Optional[dict]:
        """Handle [subteam_result] messages from child workspaces."""
        try:
            # Parse the result payload
            payload_str = content[len("[subteam_result]"):]
            payload = json.loads(payload_str)
            
            child_workspace_id = payload.get("child_workspace_id", "unknown")
            result_message = payload.get("result_message", "")
            
            # Store the result
            self._received_results[child_workspace_id] = result_message
            
            logger.info(
                f"PlannerAgent received result from workspace {child_workspace_id}. "
                f"Progress: {len(self._received_results)}/{self.child_workspace_count}"
            )
            
            # Check if all child workspaces have completed
            if len(self._received_results) >= self.child_workspace_count > 0:
                # All teams have reported - synthesize and deliver final output
                return await self._synthesize_and_deliver()
            else:
                # Still waiting for more teams
                return {
                    "send_to": "USER",
                    "visible_reasoning": (
                        f"Received results from team. "
                        f"Progress: {len(self._received_results)}/{self.child_workspace_count} teams completed."
                    ),
                    "collaboration": "",
                    "content": (
                        f"📊 **Progress Update**: {len(self._received_results)}/{self.child_workspace_count} "
                        f"teams have completed. Waiting for remaining teams..."
                    ),
                }
                
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse subteam_result: {e}")
            return None
    
    def _handle_user_task(self, content: str, context: AgentLogicContext) -> dict:
        """Handle initial task from USER."""
        team_info = ""
        if self.child_descriptions:
            team_info = "\n".join([
                f"  • Team {i+1}: {desc}"
                for i, desc in enumerate(self.child_descriptions)
            ])
        else:
            team_info = f"  • {self.child_workspace_count} specialized teams"
        
        return {
            "send_to": "USER",
            "visible_reasoning": (
                f"Task received. Coordinating {self.child_workspace_count} specialized teams. "
                f"Each team will work on their assigned subtask in parallel."
            ),
            "collaboration": "",
            "content": (
                f"🎯 **Task Received**\n\n"
                f"I'm coordinating {self.child_workspace_count} specialized teams:\n\n"
                f"{team_info}\n\n"
                f"I'll synthesize their outputs and deliver a comprehensive result."
            ),
        }
    
    async def _synthesize_and_deliver(self) -> dict:
        """
        Synthesize all results and deliver final output as a DELIVERABLE.
        
        Returns a deliverable-type response that the execution engine will:
        1. Store as a deliverable (full content)
        2. Send only the notification to chat
        """
        # Build a summary of all results
        results_summary = "\n\n".join([
            f"=== Team {i+1} Result ===\n{result}"
            for i, (workspace_id, result) in enumerate(self._received_results.items())
        ])
        
        # Use LLM to synthesize
        try:
            synthesis_prompt = f"""Synthesize these team results into a final deliverable:

TEAM RESULTS:
{results_summary}

Create a comprehensive, well-organized output that:
1. Integrates all team contributions coherently
2. Highlights key deliverables and outcomes
3. Provides actionable next steps if applicable

Respond with synthesized content only."""

            synthesis = await self.planner_llm._call_llm(
                system_prompt="You synthesize multi-team outputs into cohesive deliverables.",
                user_prompt=synthesis_prompt,
            )
            
            final_content = synthesis
            
        except Exception as e:
            logger.warning(f"LLM synthesis failed: {e}")
            final_content = (
                "# Final Deliverable\n\n"
                + results_summary
            )
        
        # Generate title for the deliverable
        deliverable_title = "Task Deliverable - All Teams Complete"
        
        # Return a DELIVERABLE type response
        response = {
            "type": "deliverable",  # <-- DELIBERATE deliverable marker
            "send_to": "USER",
            "visible_reasoning": (
                f"All {len(self._received_results)} teams complete. "
                f"Synthesized outputs into final deliverable."
            ),
            "collaboration": "",
            # Short notification for chat
            "content": (
                f"✅ **All Teams Complete**\n\n"
                f"Your deliverable is ready! View the full document in the **Deliverables** tab.\n\n"
                f"📄 *{deliverable_title}*"
            ),
            # Full deliverable content (stored separately, not in chat)
            "deliverable_title": deliverable_title,
            "deliverable_content": final_content,
        }
        
        logger.info(f"🎯 PlannerAgent returning DELIVERABLE response!")
        logger.info(f"   type: {response.get('type')}")
        logger.info(f"   deliverable_title: {deliverable_title}")
        logger.info(f"   deliverable_content length: {len(final_content)} chars")
        
        return response
    
    def reset_results(self) -> None:
        """Reset the received results for a new task."""
        self._received_results.clear()
    
    def update_child_info(
        self,
        child_workspace_count: int,
        child_descriptions: Optional[List[str]] = None,
    ) -> None:
        """
        Update information about child workspaces.
        
        Call this after task planning to inform the PlannerAgent
        about the child workspaces it will be coordinating.
        
        Args:
            child_workspace_count: Number of child workspaces
            child_descriptions: Optional list of child workspace task descriptions
        """
        self.child_workspace_count = child_workspace_count
        self.child_descriptions = child_descriptions or []
        self.reset_results()
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"PlannerAgent(name='{self.name}', "
            f"child_workspaces={self.child_workspace_count})"
        )

