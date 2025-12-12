"""
Agent - Agent with built-in inbox memory and structured response rules.

This module provides the Agent class that wraps agent logic functions
with inbox memory access and structured JSON response handling.
"""

import json
import httpx
from typing import Any, Callable, Coroutine, Optional, List, Dict

from synqed.memory import AgentMemory, InboxMessage


# ============================================================================
# Global Interaction Protocol
# ============================================================================

def get_team_roster(exclude_agent: str = None) -> str:
    """
    Get formatted team roster showing other agents' roles and capabilities.
    
    This is a utility function that agents can use in their custom logic
    to automatically discover what other agents are available.
    
    Args:
        exclude_agent: Optional agent name to exclude from roster (typically self)
        
    Returns:
        Formatted team roster string, or empty string if no other agents
        
    Example:
        ```python
        async def my_agent_logic(context):
            team_info = synqed.agent.get_team_roster(exclude_agent="my_agent")
            system_prompt = f"{GLOBAL_INTERACTION_PROTOCOL}\\n\\n{team_info}"
            ...
        ```
    """
    from synqed.workspace_manager import AgentRuntimeRegistry
    
    team_members = []
    for role in AgentRuntimeRegistry.list_roles():
        if exclude_agent and role == exclude_agent:
            continue
        agent = AgentRuntimeRegistry.get(role)
        if agent:
            caps = agent.capabilities if agent.capabilities else ["general tasks"]
            team_members.append(
                f"  - {role}: {agent.description}\n"
                f"    Capabilities: {', '.join(caps)}"
            )
    
    if not team_members:
        return ""
    
    return f"""TEAM MEMBERS (other agents in this workspace):
{chr(10).join(team_members)}

When coordinating, contact the appropriate agent based on their capabilities above."""


def get_interaction_protocol(exclude_agent: str = None) -> str:
    """
    Get the full interaction protocol including team roster.
    
    This automatically includes:
    1. Global interaction rules
    2. Team roster (other agents' roles and capabilities)
    
    Args:
        exclude_agent: Optional agent name to exclude from team roster (typically self)
        
    Returns:
        Complete interaction protocol with team roster
        
    Example:
        ```python
        async def my_agent_logic(context):
            protocol = synqed.get_interaction_protocol(exclude_agent="my_agent")
            system_prompt = f"{protocol}\\n\\nYOUR ROLE: ...\\n\\n{custom_instructions}"
            ...
        ```
    """
    team_roster = get_team_roster(exclude_agent=exclude_agent)
    
    if team_roster:
        return f"{GLOBAL_INTERACTION_PROTOCOL}\n\n{team_roster}"
    else:
        return GLOBAL_INTERACTION_PROTOCOL


GLOBAL_INTERACTION_PROTOCOL = """
═══════════════════════════════════════════════════════════════════════════════
VALUE MAXIMIZING MULTI AGENT PROTOCOL  
═══════════════════════════════════════════════════════════════════════════════

You are part of a multi-agent system whose sole purpose is to **maximize task completion value** for the user.  
Every interaction must tangibly move the workspace closer to the user's final outcome.

Reasoning is visible to the user.  
Deliverables are visible to the user.  
Progress must be real.  
Value must be measurable.

Your job is not to “participate.”  
Your job is to **shorten the distance to a finished output.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 1: THINK VISIBLY, STRUCTURE CLEARLY, REDUCE CHAOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your reasoning must be:
• Readable by a human  
• Structured into paragraphs  
• Focused on reducing uncertainty  
• Focused on determining the next high-value action  

Your reasoning must explicitly answer:
1. What do I understand?  
2. What is uncertain or ambiguous?  
3. What is blocking progress?  
4. What assumptions are acceptable for now?  
5. What is the next highest-value move?  

Do NOT compress your reasoning into unreadable blocks.  
Do NOT overthink when a direct action is possible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 2: VALUE-FIRST REASONING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You must ALWAYS evaluate actions through the lens of **value production**:

Value = Reduction of uncertainty + Movement toward deliverables + Improved correctness.

Ask yourself:
• “What is the SINGLE highest-value thing I can do right now?”  
• “Does this reduce uncertainty or produce forward progress?”  
• “Is this required for the user's final output?”  

If an action does NOT increase value: do not take it.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 3: ACTION BIAS WITHIN REALISM (NO FAKE WORK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action bias means:
• Make progress even when not all information is known  
• Draft partial deliverables when possible  
• Move the project forward while waiting for dependencies  

Realism means:
• NO fabricated data  
• NO imaginary analysis  
• NO pretending to run tools  
• NO pretending something is “done”  

Appropriate action bias examples:
✓ “While waiting for X, I can already draft sections A and B.”  
✓ “Even without data Y, I can outline options and constraints.”  
✓ “I can produce a version-0 output now, then refine once more info arrives.”

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 4: CONVERGENCE TOWARD COMPLETION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your reasoning must explicitly show convergence:
• Collapse uncertainty into decisions when safe  
• Propose concrete next steps  
• Move from brainstorming → outlining → drafting → refining → finalizing  
• Identify when the workspace is drifting or looping  
• Identify when enough information exists to commit  

You must NOT:
• Circle endlessly  
• Re-discuss already-solved points  
• Ask for unnecessary clarifications  
• Delay drafting when a draft is possible  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 5: ALIGN TO THE USER'S PRIMARY OBJECTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Every response must clearly answer:
**“How does this move us closer to the user's final outcome?”**

You must:
• Tie your work back to the root task  
• Frame your reasoning through the user's goal  
• Avoid over-focusing on sub-agent identity/role  

If something doesn't serve the user's task → it is noise.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 6: DEPENDENCY MAPPING & UNBLOCKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before acting, identify:
• What information is missing  
• Which teammate must provide it  
• What can be done in parallel  
• What assumptions are safe to proceed with  

If blocked:
→ State EXACTLY why  
→ State EXACTLY what/who you need  
→ Continue producing any partial progress that is still possible  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 7: COLLABORATION THROUGH PRECISION, NOT POLITENESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Do NOT:
• Say “great” / “perfect” / “sounds good”  
• Mirror teammates without analysis  
• Over-validate other agents  

Instead:
✓ Challenge gaps  
✓ Ask for missing details  
✓ Identify contradictions  
✓ Request justification when needed  

You’re collaborating to **finish the task**, not to be agreeable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 8: PRODUCE TANGIBLE OUTPUT EVERY CYCLE (IF POSSIBLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When possible, each message should include:
• A micro-deliverable  
• A draft  
• A structured outline  
• A narrowed set of options  
OR
• A reduction of a major uncertainty  

The user should see visible progress in every turn when feasible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED STRUCTURED JSON FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Every agent response MUST follow:

{
  "send_to": "<recipient>",
  "visible_reasoning": "<multi-paragraph reasoning with value-focus and convergence>",
  "collaboration": "<requests, dependencies, escalations, challenges>",
  "content": "<succinct, user-facing message summarizing the actionable next step>"
}

VISIBLE_REASONING REQUIREMENTS:
• Minimum 2 paragraphs  
• Must explicitly discuss value  
• Must explicitly discuss next high-value action  
• Must show movement toward task completion  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOLLOWABILITY & VALUE CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A response is INVALID if:
• Reasoning is unclear or unreadable  
• Reasoning does not identify next high-value steps  
• No convergence behavior is shown  
• It contains fake progress  
• It does not relate to the user's task  
• It fails to move the workspace forward  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END OF PROTOCOL
═══════════════════════════════════════════════════════════════════════════════
"""


def parse_llm_response(response_text: str) -> str:
    """
    Parse LLM response by stripping markdown code blocks.
    
    Many LLMs wrap JSON responses in markdown code blocks like:
    ```json
    {"send_to": "Agent", "content": "..."}
    ```
    
    This function removes those code blocks to extract the actual content.
    
    Args:
        response_text: Raw LLM response text
        
    Returns:
        Cleaned response text with markdown code blocks removed
    """
    if "```" not in response_text:
        return response_text
    
    # Find the JSON content between code blocks
    start_idx = response_text.find("```")
    if start_idx != -1:
        # Skip the opening ``` and optional language identifier
        start_idx = response_text.find("\n", start_idx)
        if start_idx != -1:
            end_idx = response_text.find("```", start_idx)
            if end_idx != -1:
                return response_text[start_idx:end_idx].strip()
    
    # Fallback: return original
    return response_text


def extract_partial_json_content(response_text: str) -> Optional[dict]:
    """
    Extract content from partial/truncated JSON responses.
    
    Handles cases where LLM response was truncated mid-JSON, like:
    {"send_to": "USER", "content": "story text...
    
    Args:
        response_text: Potentially truncated JSON response
        
    Returns:
        Extracted dict with send_to and content if parseable, None otherwise
    """
    # Check if response was INTENDED for specific recipient
    send_to_match = None
    for pattern in ['"send_to": "', '"send_to":"']:
        if pattern in response_text:
            start = response_text.find(pattern) + len(pattern)
            end = response_text.find('"', start)
            if end != -1:
                send_to_match = response_text[start:end]
                break
    
    if not send_to_match:
        return None
    
    # Try to find the content field
    content_match = None
    for pattern in ['"content": "', '"content":"']:
        if pattern in response_text:
            content_start = response_text.find(pattern) + len(pattern)
            # Extract until end or closing quote
            content_text = response_text[content_start:]
            # Try to find natural end (closing quote followed by })
            # But handle truncation gracefully
            content_match = content_text.rstrip('"}')
            break
    
    if content_match is None:
        return None
    
    return {
        "send_to": send_to_match,
        "content": content_match
    }


class ResponseBuilder:
    """
    Helper class for building structured responses.
    
    Agents use this to emit JSON responses with "send_to" and "content" fields.
    
    Example:
        ```python
        builder = ResponseBuilder()
        builder.send_to("Editor").content("Here's my draft")
        response = builder.build()  # {"send_to": "Editor", "content": "..."}
        ```
    """
    
    def __init__(self):
        """Initialize the response builder."""
        self._send_to: Optional[str] = None
        self._content: Optional[str] = None
    
    def send_to(self, agent_name: str) -> "ResponseBuilder":
        """
        Set the target agent name.
        
        Args:
            agent_name: Name of the agent to send the message to
            
        Returns:
            Self for method chaining
        """
        self._send_to = agent_name
        return self
    
    def content(self, text: str) -> "ResponseBuilder":
        """
        Set the message content.
        
        Args:
            text: Message content text
            
        Returns:
            Self for method chaining
        """
        self._content = text
        return self
    
    def build(self) -> dict[str, str]:
        """
        Build the structured response dictionary.
        
        Returns:
            Dictionary with "send_to" and "content" keys
            
        Raises:
            ValueError: If send_to or content is not set
        """
        if self._send_to is None:
            raise ValueError("send_to must be set before building response")
        if self._content is None:
            raise ValueError("content must be set before building response")
        
        return {
            "send_to": self._send_to,
            "content": self._content
        }
    
    def to_json(self) -> str:
        """
        Build and return as JSON string.
        
        Returns:
            JSON string representation of the response
        """
        return json.dumps(self.build())


class AgentLogicContext:
    """
    Context object passed to agent logic functions.
    
    Provides access to:
    - Agent's memory
    - Latest incoming message
    - sender: Who sent the current message (context.sender)
    - reply(): Respond directly to sender (context.reply("message"))
    - ResponseBuilder helper
    - send() helper method for convenience
    - get_conversation_history() for formatted conversation history
    - workspace reference for transcript access
    - shared_plan: Shared workspace plan that agents can read/update
    
    Example:
        ```python
        async def agent_logic(context: AgentLogicContext):
            # See who sent the message
            sender = context.sender  # e.g., "alice"
            
            # Reply directly to sender
            return context.reply("Thanks for the message!")
            
            # Or send to someone specific
            return context.send("bob", "Hey Bob!")
        ```
    
    WARNING: Agent logic functions must NOT directly use any router.
    Routing is strictly handled by ExecutionEngine + Workspace.
    """
    
    def __init__(
        self, 
        memory: AgentMemory, 
        default_target: Optional[str] = None,
        workspace: Optional[Any] = None,
        agent_name: Optional[str] = None,
        shared_plan: Optional[str] = None
    ):
        """
        Initialize the logic context.
        
        Args:
            memory: Agent's memory instance
            default_target: Default target agent if logic doesn't specify one
            workspace: Optional workspace reference for transcript access
            agent_name: Optional agent name for conversation history filtering
            shared_plan: Optional shared workspace plan for coordination
        """
        self.memory = memory
        self.default_target = default_target
        self.workspace = workspace
        self.agent_name = agent_name
        self.shared_plan = shared_plan or ""
        self._response_builder = ResponseBuilder()
    
    @property
    def latest_message(self) -> Optional[InboxMessage]:
        """Get the latest incoming message."""
        return self.memory.get_latest_message()
    
    @property
    def sender(self) -> Optional[str]:
        """
        Get the sender of the latest message.
        
        This is a convenience property to make it easy for agents to see
        who sent them the current message and respond directly.
        
        Returns:
            Name of the agent who sent the latest message, or None
        """
        latest = self.latest_message
        return latest.from_agent if latest else None
    
    @property
    def response(self) -> ResponseBuilder:
        """Get the response builder helper."""
        return self._response_builder
    
    def send(self, to: str, content: str) -> dict[str, str]:
        """
        Helper method to create a structured response.
        
        Args:
            to: Target agent name
            content: Message content
            
        Returns:
            Dictionary with "send_to" and "content" keys
        """
        return {"send_to": to, "content": content}
    
    def reply(self, content: str) -> dict[str, str]:
        """
        Reply directly to the sender of the current message.
        
        This is a convenience method that automatically sends the response
        to whoever sent the latest message. If there's no sender or the
        sender is not set, falls back to default_target.
        
        Args:
            content: Message content
            
        Returns:
            Dictionary with "send_to" and "content" keys
        """
        recipient = self.sender or self.default_target or "USER"
        return {"send_to": recipient, "content": content}
    
    def build_response(self, send_to: str, content: str) -> dict[str, str]:
        """
        Convenience method to build a response.
        
        Args:
            send_to: Target agent name
            content: Message content
            
        Returns:
            Structured response dictionary
        """
        return ResponseBuilder().send_to(send_to).content(content).build()
    
    def get_conversation_history(
        self, 
        format: str = "text",
        include_system_messages: bool = False,
        parse_json_content: bool = True,
        workspace_wide: bool = True,  # CHANGED: Default to True so agents see ALL messages
        max_messages: Optional[int] = None
    ) -> str | List[dict]:
        """
        Get formatted conversation history for this agent.
        
        This method extracts the conversation history from the workspace transcript,
        including both messages received and sent by this agent. It automatically
        parses JSON content to extract the actual message content.
        
        Args:
            format: Output format - "text" for formatted string, "raw" for list of dicts
            include_system_messages: Whether to include system messages like [startup]
            parse_json_content: Whether to parse JSON content and extract "content" field
            workspace_wide: If True, show ALL messages in workspace (not just involving this agent)
            max_messages: Maximum number of messages to include (most recent), None for all
            
        Returns:
            Formatted conversation history as string (if format="text") or list of dicts (if format="raw")
            
        Example:
            ```python
            async def agent_logic(context):
                # Get conversation history as formatted text
                history = context.get_conversation_history()
                
                # Get full workspace conversation (all agents)
                full_history = context.get_conversation_history(workspace_wide=True)
                
                # Get last 10 messages only
                recent_history = context.get_conversation_history(max_messages=10)
                
                # Pass to LLM
                response = await llm.chat(history)
                return context.send("Editor", response)
            ```
        """
        if not self.workspace or not self.agent_name:
            # No workspace context, return empty
            return "" if format == "text" else []
        
        transcript = self.workspace.router.get_transcript()
        
        # 🔧 FIX: Limit transcript to max_messages if specified (most recent)
        if max_messages is not None and len(transcript) > max_messages:
            transcript = transcript[-max_messages:]
        
        conversation_parts = []
        raw_messages = []
        
        for entry in transcript:
            sender = entry.get("from", "")
            recipient = entry.get("to", "")
            content = entry.get("content", "")
            
            # Skip system messages unless requested
            if not include_system_messages:
                if content == "[startup]" or content.startswith("[subteam_result]"):
                    continue
            
            # Filter based on workspace_wide parameter
            if not workspace_wide:
                # Only include messages involving this agent (received or sent)
                if not (recipient == self.agent_name or sender == self.agent_name):
                    continue
            
            # Process message for inclusion
            if True:  # Keep the same indentation level
                # Parse JSON content if requested
                display_content = content
                if parse_json_content:
                    try:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict) and "content" in parsed:
                            display_content = parsed["content"]
                    except (json.JSONDecodeError, TypeError):
                        # Not JSON or no "content" field, use as-is
                        pass
                
                # Build message entry - clean format without arrows
                if format == "text":
                    if sender == "USER":
                        conversation_parts.append(f"[USER]\n{display_content}")
                    elif sender == self.agent_name:
                        # Show your own messages
                        if recipient == "ALL":
                            conversation_parts.append(f"[YOU broadcast]\n{display_content}")
                        else:
                            conversation_parts.append(f"[YOU to {recipient}]\n{display_content}")
                    elif workspace_wide:
                        # Workspace-wide view: show sender and recipient clearly
                        if recipient == "ALL":
                            conversation_parts.append(f"[{sender} broadcast]\n{display_content}")
                        else:
                            conversation_parts.append(f"[{sender} to {recipient}]\n{display_content}")
                    else:
                        # Emphasize who is speaking to you
                        conversation_parts.append(f"[{sender}]\n{display_content}")
                else:
                    raw_messages.append({
                        "sender": sender,
                        "recipient": recipient,
                        "content": display_content,
                        "original_content": content,
                        "timestamp": entry.get("timestamp", "")
                    })
        
        if format == "text":
            # Add clear indicator of current sender at the end
            if conversation_parts:
                latest = self.latest_message
                if latest and latest.from_agent:
                    conversation_parts.append(f"\n>>> Current message is FROM: {latest.from_agent}")
                    conversation_parts.append(f">>> You should respond TO: {latest.from_agent}")
            
            return "\n\n".join(conversation_parts)
        else:
            return raw_messages


class Agent:
    """
    Agent with built-in inbox memory, JSON-structured response rules, and optional email capabilities.
    
    This class wraps a logic function and provides it with access to:
    - The agent's memory (via AgentLogicContext)
    - The latest incoming message
    - A ResponseBuilder helper for structured responses
    - Optional email addressing and cloud messaging (if created with a role)
    
    The logic function should return JSON with "send_to" and "content" fields.
    If it returns non-JSON, it will be automatically wrapped.
    
    Email Capabilities:
    When created with a 'role' parameter, agents get:
    - Email-like identity (name@role)
    - Cryptographic keypair (Ed25519)
    - Cloud registration capability
    - Remote message sending
    
    WARNING: Agent logic functions must NOT directly use any router.
    Routing is strictly handled by ExecutionEngine + Workspace. Any attempt
    to access or use a router within agent logic will raise an assertion error.
    
    Example (Local workspace):
        ```python
        async def writer_logic(context: AgentLogicContext) -> dict:
            latest = context.latest_message
            if not latest:
                return context.send("Editor", "I'm ready!")
            
            # Process message and respond
            return context.send("Editor", "Here's my draft")
        
        agent = Agent(
            name="Writer",
            description="Creative writer",
            logic=writer_logic,
            default_target="Editor"
        )
        ```
    
    Example (With email capabilities):
        ```python
        async def alice_logic(ctx):
            # Your AI logic here
            return ctx.send("bob@builder", "Hello!")
        
        alice = Agent(name="alice", role="wonderland", logic=alice_logic)
        await alice.register()  # Register on cloud
        await alice.send("bob@builder", "Hello!")  # Send via cloud
        ```
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        logic: Optional[Callable[[AgentLogicContext], Coroutine[Any, Any, dict[str, str] | str]]] = None,
        default_target: Optional[str] = None,
        memory: Optional[AgentMemory] = None,
        role: Optional[str] = None,
        inbox_url: str = "https://synqed.fly.dev",
        metadata: Optional[Dict[str, Any]] = None,
        capabilities: Optional[List[str]] = None,
        default_coordination: str = "respond_to_sender",
    ):
        """
        Initialize an Agent.
        
        Args:
            name: Agent name
            description: Agent description
            logic: Optional async function that takes AgentLogicContext and returns
                   dict with "send_to" and "content", or a string (will be wrapped)
            default_target: Default target agent if logic returns non-JSON or
                           doesn't specify send_to
            memory: Optional pre-existing memory instance (creates new one if not provided)
            role: Optional role/organization for email addressing (name@role)
            inbox_url: Cloud inbox URL (default: synqed.fly.dev)
            metadata: Optional metadata to store with registration
            capabilities: Optional list of capabilities for this agent
            default_coordination: Default coordination style (default: "respond_to_sender")
        """
        if not name:
            raise ValueError("Agent name must be provided")
        
        # Use default no-op logic if none provided
        if logic is None:
            async def default_logic(ctx: AgentLogicContext):
                # No-op logic for cloud-only agents
                return None
            logic = default_logic
        
        # Validate logic is async
        import inspect
        if not inspect.iscoroutinefunction(logic):
            raise ValueError("Agent logic must be an async function")
        
        self.name = name
        self.description = description or f"Agent {name}"
        self.logic = logic
        self.default_target = default_target
        self.memory = memory or AgentMemory(agent_name=name)
        
        # Baseline interaction metadata
        self.capabilities = capabilities or []
        self.default_coordination = default_coordination
        
        # Ensure memory has agent name set
        if self.memory.agent_name != name:
            self.memory.agent_name = name
        
        # Duplicate-response protection
        self.last_processed_message_id: Optional[str] = None
        
        # Email capabilities (if role is provided)
        self.role = role
        if role:
            self.email = f"{name}@{role}"
            self.agent_id = f"agent://{role}/{name}"
            
            # Cloud messaging config
            self.inbox_url = inbox_url
            self.metadata = metadata or {}
            
            # Cryptographic identity
            try:
                from synqed.agent_email.inbox import generate_keypair, sign_message
                self.private_key, self.public_key = generate_keypair()
                self._sign_message = sign_message
            except ImportError:
                # Email features not available
                self.private_key = None
                self.public_key = None
                self._sign_message = None
        else:
            self.email = None
            self.agent_id = None
            self.inbox_url = None
            self.metadata = None
            self.private_key = None
            self.public_key = None
            self._sign_message = None
    
    def __deepcopy__(self, memo):
        """
        Deep copy the agent to ensure isolation between workspaces.
        
        Creates new instances of mutable objects to prevent shared state.
        Memory is fully deep-copied, but the logic function reference is NOT
        deep-copied (functions are immutable and should be shared).
        """
        import copy
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        
        # Copy immutable fields
        result.name = self.name
        result.description = self.description
        result.logic = self.logic  # Function reference must NOT be deepcopied
        result.default_target = self.default_target
        
        # Deep copy memory - ensure no shared mutable fields remain
        result.memory = copy.deepcopy(self.memory, memo)
        
        # Copy baseline interaction metadata
        result.capabilities = copy.deepcopy(self.capabilities, memo) if self.capabilities else []
        result.default_coordination = self.default_coordination
        
        # Copy duplicate-response protection field
        result.last_processed_message_id = self.last_processed_message_id
        
        # Copy email-related fields
        result.role = self.role
        result.email = self.email
        result.agent_id = self.agent_id
        result.inbox_url = self.inbox_url
        result.metadata = copy.deepcopy(self.metadata, memo) if self.metadata else None
        result.private_key = self.private_key
        result.public_key = self.public_key
        result._sign_message = self._sign_message
        
        return result
    
    def _build_role_profile(self) -> str:
        """
        Build the role profile section for agent system prompt.
        
        This creates a standardized profile that describes the agent's role,
        capabilities, and coordination style.
        
        Returns:
            Formatted role profile string
        """
        role_display = self.role or self.name
        capabilities_display = ", ".join(self.capabilities) if self.capabilities else "general purpose"
        
        return f"""
YOUR ROLE: {role_display}
YOUR CAPABILITIES: {capabilities_display}
DEFAULT COORDINATION STYLE: {self.default_coordination}
"""
    
    def get_system_prompt_with_protocol(self, custom_prompt: str = "") -> str:
        """
        Build complete system prompt with global protocol and role profile.
        
        This method combines:
        1. Global interaction protocol (universal rules)
        2. Team roster (other agents' roles and capabilities) - automatic!
        3. Role profile (agent-specific metadata)
        4. Custom prompt (developer-provided instructions)
        
        Args:
            custom_prompt: Optional custom instructions for this agent
            
        Returns:
            Complete system prompt string
        """
        # Get protocol with team roster automatically included
        protocol = get_interaction_protocol(exclude_agent=self.name)
        role_profile = self._build_role_profile()
        
        parts = [protocol, role_profile]
        
        if custom_prompt:
            parts.append(custom_prompt)
        
        return "\n".join(parts)
    
    def _build_team_roster(self) -> str:
        """
        Build team roster showing other agents' roles and capabilities.
        
        This automatically queries the AgentRuntimeRegistry to discover
        what other agents are available and what they can do. This prevents
        agents from making incorrect assumptions about each other's roles.
        
        Returns:
            Formatted team roster string, or empty string if no other agents
        """
        from synqed.workspace_manager import AgentRuntimeRegistry
        
        team_members = []
        for role in AgentRuntimeRegistry.list_roles():
            if role != self.name:  # Don't include self
                agent = AgentRuntimeRegistry.get(role)
                if agent:
                    caps = agent.capabilities if agent.capabilities else ["general tasks"]
                    team_members.append(
                        f"  - {role}: {agent.description}\n"
                        f"    Capabilities: {', '.join(caps)}"
                    )
        
        if not team_members:
            return ""
        
        return f"""
TEAM MEMBERS (other agents in this workspace):
{chr(10).join(team_members)}

When coordinating, contact the appropriate agent based on their capabilities above."""
    
    async def process(self, context: AgentLogicContext) -> Optional[dict[str, str]]:
        """
        Process the agent's inbox and generate a response.
        
        This method accepts an externally supplied context and calls the
        agent's logic function with it. The context must be created by the
        caller (typically ExecutionEngine or Workspace).
        
        This method:
        1. Validates that context is provided
        2. Ensures agent logic does not directly use router
        3. Checks for duplicate message processing
        4. Calls the agent's logic function with the provided context
        5. Ensures the response is valid JSON with "send_to" and "content"
        6. Wraps non-JSON responses automatically
        
        Args:
            context: AgentLogicContext instance (must be externally supplied)
        
        Returns:
            Dictionary with "send_to" and "content" keys, or None if no response needed
            
        Raises:
            ValueError: If context is None or response cannot be parsed or structured
            AssertionError: If agent logic attempts to use router directly
        """
        if context is None:
            raise ValueError("Agent.process() requires an externally supplied context")
        
        # Ensure agent logic does not directly use router
        # This is enforced by checking that context doesn't have router access
        # (Router should not be accessible from AgentLogicContext)
        assert not hasattr(context, 'router'), (
            "Agent logic must NOT directly use any router. "
            "Routing is strictly handled by ExecutionEngine + Workspace."
        )
        
        # Get latest message for filtering
        latest_msg = context.latest_message
        
        # AUTOMATIC MESSAGE FILTERING (built into framework)
        if latest_msg:
            # 1. Target filtering: only process messages addressed to this agent
            if hasattr(latest_msg, 'target') and latest_msg.target is not None:
                if latest_msg.target != self.name:
                    return None  # Message not for us, skip
            
            # 2. System message filtering: skip startup messages
            if latest_msg.content in ["[startup]", ""]:
                return None
            
            # 3. Duplicate-response protection: check if we already processed this message
            if latest_msg.message_id == self.last_processed_message_id:
                return None  # Already processed, skip
        
        # Call logic function with provided context
        result = await self.logic(context)
        
        # Update last processed message ID
        if latest_msg:
            self.last_processed_message_id = latest_msg.message_id
        
        # If logic returns None, pass it through (agent chose not to respond)
        if result is None:
            return None
        
        # Ensure result is structured JSON
        return self._ensure_structured_response(result, context.default_target)
    
    def _ensure_structured_response(
        self, result: dict[str, str] | str, default_target: Optional[str] = None
    ) -> dict[str, str]:
        """
        Ensure the response is valid structured JSON with deep reasoning validation.
        
        This method automatically handles:
        - Markdown code block stripping (```json ... ```)
        - Partial/truncated JSON responses
        - Missing "send_to" fields (uses default_target, prefers sender)
        - New structured format with visible_reasoning and collaboration
        - Shallow reasoning detection and rejection
        
        New Response Format:
        {
            "send_to": "<recipient>",
            "visible_reasoning": "<complete thinking process>",
            "collaboration": "<requests, challenges, dependencies>",
            "content": "<final chat message>"
        }
        
        Args:
            result: Result from logic function (dict or string)
            default_target: Default target agent (from context)
            
        Returns:
            Valid structured response dictionary with reasoning metadata
            
        Raises:
            ValueError: If reasoning is too shallow or response is invalid
        """
        # Prefer sender of latest message, fall back to default_target
        sender_of_latest = None
        if self.memory:
            latest = self.memory.get_latest_message()
            if latest and latest.from_agent:
                sender_of_latest = latest.from_agent
        
        effective_default = sender_of_latest or default_target or self.default_target
        
        # Parse the result if it's a string
        parsed_result = result
        if isinstance(result, str):
            cleaned_result = parse_llm_response(result)
            try:
                parsed_result = json.loads(cleaned_result)
            except json.JSONDecodeError:
                partial = extract_partial_json_content(cleaned_result)
                if partial:
                    parsed_result = partial
                else:
                    if effective_default is None:
                        raise ValueError(
                            "Response is not valid JSON and no default_target is set."
                        )
                    return {
                        "send_to": effective_default,
                        "content": result,
                        "visible_reasoning": "",
                        "collaboration": "",
                        "_shallow_warning": "Response was not structured JSON"
                    }
        
        if not isinstance(parsed_result, dict):
            if effective_default is None:
                raise ValueError(
                    f"Response type '{type(parsed_result).__name__}' is not supported."
                )
            return {
                "send_to": effective_default,
                "content": str(parsed_result),
                "visible_reasoning": "",
                "collaboration": "",
                "_shallow_warning": "Response was not a dict"
            }
        
        # Extract fields from the new structured format
        send_to = parsed_result.get("send_to")
        visible_reasoning = parsed_result.get("visible_reasoning", "")
        collaboration = parsed_result.get("collaboration", "")
        content = parsed_result.get("content", "")
        
        # Handle missing send_to
        if send_to is None:
            if effective_default is None:
                raise ValueError(
                    "Response missing 'send_to' field and no default_target is set."
                )
            send_to = effective_default
        
        # Handle missing content - try to extract from old format
        if not content:
            content = parsed_result.get("message", "")
        if not content:
            content = json.dumps(parsed_result)
        
        # Validate reasoning depth (shallow reasoning detection)
        shallow_indicators = self._detect_shallow_reasoning(
            visible_reasoning, collaboration, content
        )
        
        # Build the structured response
        response = {
            "send_to": send_to,
            "content": content,
            "visible_reasoning": visible_reasoning,
            "collaboration": collaboration,
        }
        
        # Add shallow warning if detected
        if shallow_indicators:
            response["_shallow_warning"] = "; ".join(shallow_indicators)
        
        return response
    
    def _detect_shallow_reasoning(
        self, 
        visible_reasoning: str, 
        collaboration: str, 
        content: str
    ) -> List[str]:
        """
        Detect shallow reasoning patterns that should be challenged.
        
        Returns a list of detected issues, empty if reasoning is adequate.
        """
        issues = []
        
        # Check for missing or empty reasoning
        if not visible_reasoning or len(visible_reasoning.strip()) < 50:
            issues.append("Reasoning is too short (minimum 50 characters expected)")
        
        # Check for placeholder phrases
        shallow_phrases = [
            "i'll look into",
            "i'll analyze",
            "i will research",
            "looking into this",
            "let me check",
            "i'll handle",
            "sounds good",
            "great idea",
            "perfect!",
            "will do",
            "on it",
            "got it",
        ]
        reasoning_lower = (visible_reasoning + " " + content).lower()
        for phrase in shallow_phrases:
            if phrase in reasoning_lower and len(visible_reasoning) < 100:
                issues.append(f"Contains shallow placeholder: '{phrase}'")
                break
        
        # Check for fake work claims without evidence
        fake_work_phrases = [
            "i completed",
            "i finished",
            "done!",
            "i analyzed",
            "i researched",
            "i gathered",
            "i created",
            "i scheduled",
            "i reviewed",
        ]
        content_lower = content.lower()
        # Only flag if reasoning doesn't contain actual analysis
        depth_indicators = ["uncertainty", "assumption", "depend", "risk", "alternative", "however", "but", "concern", "question"]
        has_depth = any(indicator in reasoning_lower for indicator in depth_indicators)
        
        if not has_depth:
            for phrase in fake_work_phrases:
                if phrase in content_lower:
                    issues.append(f"Claims completed work without showing reasoning: '{phrase}'")
                    break
        
        # Check for instant agreement without analysis
        agreement_phrases = ["great!", "perfect!", "sounds good!", "excellent!", "love it!"]
        for phrase in agreement_phrases:
            if phrase in content_lower and len(visible_reasoning) < 100:
                issues.append(f"Instant agreement without analysis: '{phrase}'")
                break
        
        return issues
    
    async def register(self) -> Dict[str, Any]:
        """
        Register this agent with Synqed cloud.
        
        Requires that the agent was created with a role (for email addressing).
        
        Returns:
            Registration response with status and agent details
            
        Raises:
            ValueError: If agent was not created with a role
            httpx.HTTPStatusError: If registration fails
        """
        if not self.role or not self.email:
            raise ValueError(
                "Agent must be created with a 'role' parameter to use email capabilities. "
                "Example: Agent(name='alice', role='wonderland', ...)"
            )
        
        if not self.public_key:
            raise ValueError("Agent does not have cryptographic keys. Email features may not be available.")
        
        registration = {
            "agent_id": self.agent_id,
            "email_like": self.email,
            "inbox_url": f"{self.inbox_url}/v1/a2a/inbox",
            "public_key": self.public_key,
            "capabilities": ["a2a/1.0"],
            "metadata": self.metadata,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.inbox_url}/v1/a2a/register",
                json=registration,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
    
    async def send(
        self,
        to: str,
        content: str,
        thread_id: Optional[str] = None,
        via_cloud: bool = True,
    ) -> Dict[str, Any]:
        """
        Send a message to another agent via cloud.
        
        This is for direct cloud messaging. For workspace-based routing,
        use the agent in a Workspace and return messages from your logic function.
        
        Args:
            to: Recipient's email address (e.g., "bob@builder") or agent_id
            content: Message content
            thread_id: Optional conversation thread ID
            via_cloud: If True, send via cloud inbox (default). If False, just return message dict.
            
        Returns:
            Delivery response with message_id and trace_id (if via_cloud=True)
            Or message dict (if via_cloud=False, for workspace routing)
            
        Raises:
            ValueError: If agent was not created with a role
            httpx.HTTPStatusError: If message delivery fails
        """
        if not self.role or not self.email:
            raise ValueError(
                "Agent must be created with a 'role' parameter to use email capabilities. "
                "Example: Agent(name='alice', role='wonderland', ...)"
            )
        
        if not via_cloud:
            # Return message dict for workspace routing
            return {"send_to": to, "content": content}
        
        if not self._sign_message or not self.private_key:
            raise ValueError("Agent does not have cryptographic keys. Email features may not be available.")
        
        # Convert email to agent_id
        if "@" in to:
            username, domain = to.split("@")
            recipient_id = f"agent://{domain}/{username}"
        else:
            recipient_id = to
        
        if thread_id is None:
            thread_id = f"conversation-{self.name}"
        
        # Create message
        message = {
            "thread_id": thread_id,
            "role": "user",
            "content": content,
        }
        
        # Sign with private key
        signature = self._sign_message(
            private_key_b64=self.private_key,
            sender=self.agent_id,
            recipient=recipient_id,
            message=message,
            thread_id=thread_id,
        )
        
        # Send to cloud inbox
        envelope = {
            "sender": self.agent_id,
            "recipient": recipient_id,
            "message": message,
            "signature": signature,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.inbox_url}/v1/a2a/inbox",
                json=envelope,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
    
    def __repr__(self) -> str:
        """String representation."""
        if self.email:
            return f"Agent(name='{self.name}', email='{self.email}')"
        return f"Agent(name='{self.name}', memory_messages={len(self.memory.messages)})"
