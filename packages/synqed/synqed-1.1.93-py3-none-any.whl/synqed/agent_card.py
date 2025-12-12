"""
AgentCard builder for simplified card creation.
"""

from typing import Any

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentProvider,
    AgentSkill,
)


class AgentCardBuilder:
    """
    Simplified builder for creating AgentCards.
    
    This class provides a fluent interface for building agent cards
    with sensible defaults.
    
    Example:
        ```python
        builder = AgentCardBuilder(
            name="Recipe Agent",
            description="Helps with recipes",
            version="1.0.0",
            url="http://localhost:8000"
        )
        builder.add_skill(
            skill_id="search_recipes",
            name="Recipe Search",
            description="Search for recipes",
            tags=["cooking", "search"]
        )
        card = builder.build()
        ```
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        version: str,
        url: str,
        protocol_version: str = "0.3.0",
        preferred_transport: str = "JSONRPC",
    ):
        """
        Initialize the builder with required fields.
        
        Args:
            name: Agent name
            description: Agent description
            version: Agent version
            url: Base URL for the agent
            protocol_version: A2A protocol version
            preferred_transport: Preferred transport protocol
        """
        self.name = name
        self.description = description
        self.version = version
        self.url = url
        self.protocol_version = protocol_version
        self.preferred_transport = preferred_transport
        
        # Lists and dictionaries for building the card
        self._skills: list[AgentSkill] = []
        self._additional_interfaces: list[AgentInterface] = []
        self._security_schemes: dict[str, Any] = {}
        self._security: list[dict[str, list[str]]] = []
        
        # Default configurations
        self._default_input_modes = ["text/plain", "application/json"]
        self._default_output_modes = ["text/plain", "application/json"]
        
        # Capabilities
        self._capabilities = AgentCapabilities(
            streaming=True,
            push_notifications=False,
            state_transition_history=False,
        )
        
        # Provider info
        self._provider: AgentProvider | None = None
        
        # Documentation and icon
        self._documentation_url: str | None = None
        self._icon_url: str | None = None
    
    def add_skill(
        self,
        skill_id: str,
        name: str,
        description: str,
        tags: list[str],
        examples: list[str] | None = None,
        input_modes: list[str] | None = None,
        output_modes: list[str] | None = None,
    ) -> "AgentCardBuilder":
        """
        Add a skill to the agent.
        
        Args:
            skill_id: Unique identifier for the skill
            name: Human-readable name
            description: Detailed description
            tags: Keywords describing the skill
            examples: Example prompts
            input_modes: Supported input MIME types (overrides defaults)
            output_modes: Supported output MIME types (overrides defaults)
            
        Returns:
            Self for chaining
        """
        skill = AgentSkill(
            id=skill_id,
            name=name,
            description=description,
            tags=tags,
            examples=examples,
            input_modes=input_modes,
            output_modes=output_modes,
        )
        self._skills.append(skill)
        return self
    
    def set_default_input_modes(self, modes: list[str]) -> "AgentCardBuilder":
        """Set default input MIME types."""
        self._default_input_modes = modes
        return self
    
    def set_default_output_modes(self, modes: list[str]) -> "AgentCardBuilder":
        """Set default output MIME types."""
        self._default_output_modes = modes
        return self
    
    def set_capabilities(
        self,
        streaming: bool | None = None,
        push_notifications: bool | None = None,
        state_transition_history: bool | None = None,
    ) -> "AgentCardBuilder":
        """
        Set agent capabilities.
        
        Args:
            streaming: Whether the agent supports streaming
            push_notifications: Whether the agent supports push notifications
            state_transition_history: Whether the agent provides state history
            
        Returns:
            Self for chaining
        """
        if streaming is not None:
            self._capabilities.streaming = streaming
        if push_notifications is not None:
            self._capabilities.push_notifications = push_notifications
        if state_transition_history is not None:
            self._capabilities.state_transition_history = state_transition_history
        return self
    
    def add_interface(
        self,
        url: str,
        transport: str = "JSONRPC"
    ) -> "AgentCardBuilder":
        """
        Add an additional interface.
        
        Args:
            url: URL for the interface
            transport: Transport protocol (JSONRPC, GRPC, HTTP+JSON)
            
        Returns:
            Self for chaining
        """
        interface = AgentInterface(url=url, transport=transport)
        self._additional_interfaces.append(interface)
        return self
    
    def set_provider(
        self,
        organization: str,
        url: str
    ) -> "AgentCardBuilder":
        """
        Set provider information.
        
        Args:
            organization: Organization name
            url: Organization URL
            
        Returns:
            Self for chaining
        """
        self._provider = AgentProvider(organization=organization, url=url)
        return self
    
    def add_security_scheme(
        self,
        name: str,
        scheme: dict[str, Any]
    ) -> "AgentCardBuilder":
        """
        Add a security scheme.
        
        Args:
            name: Scheme name
            scheme: Scheme configuration
            
        Returns:
            Self for chaining
        """
        self._security_schemes[name] = scheme
        return self
    
    def set_security_requirements(
        self,
        requirements: list[dict[str, list[str]]]
    ) -> "AgentCardBuilder":
        """
        Set security requirements.
        
        Args:
            requirements: List of security requirement objects
            
        Returns:
            Self for chaining
        """
        self._security = requirements
        return self
    
    def set_documentation_url(self, url: str) -> "AgentCardBuilder":
        """Set documentation URL."""
        self._documentation_url = url
        return self
    
    def set_icon_url(self, url: str) -> "AgentCardBuilder":
        """Set icon URL."""
        self._icon_url = url
        return self
    
    def set_url(self, url: str) -> "AgentCardBuilder":
        """Update the agent URL."""
        self.url = url
        return self
    
    def build(self) -> AgentCard:
        """
        Build and return the AgentCard.
        
        Returns:
            Configured AgentCard instance
        """
        card_data = {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "url": self.url,
            "protocol_version": self.protocol_version,
            "preferred_transport": self.preferred_transport,
            "skills": self._skills,
            "default_input_modes": self._default_input_modes,
            "default_output_modes": self._default_output_modes,
            "capabilities": self._capabilities,
        }
        
        # Add optional fields
        if self._additional_interfaces:
            card_data["additional_interfaces"] = self._additional_interfaces
        if self._provider:
            card_data["provider"] = self._provider
        if self._security_schemes:
            card_data["security_schemes"] = self._security_schemes
        if self._security:
            card_data["security"] = self._security
        if self._documentation_url:
            card_data["documentation_url"] = self._documentation_url
        if self._icon_url:
            card_data["icon_url"] = self._icon_url
        
        return AgentCard(**card_data)

