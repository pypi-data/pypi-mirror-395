"""
Real-time message display for multi-agent execution.

This module provides a clean, real-time display of agent communications
in the terminal, showing message flow between agents.
"""

import json
from typing import Optional


class MessageDisplay:
    """
    Handles real-time display of agent messages in the terminal.
    
    Displays messages in a clean, readable format showing the flow
    of communication between agents.
    """
    
    def __init__(self):
        """Initialize the message display."""
        self.turn_counter = 0
        self.startup_displayed = False
    
    def display_initial(self, task: str, recipient: str) -> None:
        """
        Display initial task placement message.
        
        Args:
            task: Task description
            recipient: Name of the agent receiving the initial task
        """
        # Reset turn counter for new execution
        self.turn_counter = 0
        print(f"\n[Initial] Placing user task in {recipient}'s inbox...")
        print()
    
    def display_startup(self, agent_name: str) -> None:
        """
        Display startup message for an agent (only shown once).
        
        Args:
            agent_name: Name of the agent starting up
        """
        if not self.startup_displayed:
            self.startup_displayed = True
    
    def display_processing(self, agent_name: str) -> None:
        """
        Display agent processing message.
        
        Args:
            agent_name: Name of the agent processing
        """
        self.turn_counter += 1
        print(f"[Turn {self.turn_counter}] {agent_name} processing inbox and responding...")
    
    def display_message(
        self,
        sender: str,
        recipient: str,
        content: str,
        truncate_at: int = 200,
    ) -> None:
        """
        Display a message being sent from one agent to another.
        
        Args:
            sender: Name of the sending agent
            recipient: Name of the recipient agent
            content: Message content
            truncate_at: Maximum length before truncation (default: 200)
        """
        # Don't display system startup messages
        if content == "[startup]":
            return
        
        # Don't display subteam_result messages (internal)
        if content.startswith("[subteam_result]"):
            return
        
        # Truncate long content
        display_content = content
        if len(content) > truncate_at:
            display_content = content[:truncate_at] + "..."
        
        # Try to parse as JSON for cleaner display
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                # Format JSON compactly
                display_content = json.dumps(parsed, separators=(',', ': '))
                if len(display_content) > truncate_at:
                    display_content = display_content[:truncate_at] + "...}"
        except (json.JSONDecodeError, TypeError):
            # Not JSON, use as-is
            pass
        
        # Clean format without arrows
        if recipient == "ALL":
            print(f"[Turn {self.turn_counter}] {sender} (broadcast): {display_content}")
        else:
            print(f"[Turn {self.turn_counter}] {sender} to {recipient}: {display_content}")
    
    def display_completion(self, workspace_id: str, total_turns: int) -> None:
        """
        Display completion message.
        
        Args:
            workspace_id: ID of the completed workspace
            total_turns: Total number of turns executed
        """
        print(f"\n────")
        print(f"Workspace {workspace_id} completed after {total_turns} turns")
        print()
    
    def display_error(self, error_type: str, message: str) -> None:
        """
        Display an error message.
        
        Args:
            error_type: Type of error
            message: Error message
        """
        print(f"\n[ERROR: {error_type}] {message}")
        print()

