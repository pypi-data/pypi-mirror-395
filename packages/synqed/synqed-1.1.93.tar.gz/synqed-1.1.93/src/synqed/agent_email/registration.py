"""
Public Agent Registration API

Allows anyone to register agents and get email addresses for agent-to-agent communication.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry

# Create registration router
router = APIRouter(prefix="/v1/a2a", tags=["registration"])


class AgentRegistrationRequest(BaseModel):
    """
    Request to register a new agent.
    
    Fields:
        agent_id: Canonical agent URI (e.g., "agent://myorg/myagent")
        email_like: Email-like address (e.g., "myagent@myorg")
        inbox_url: HTTP endpoint where agent receives messages
        public_key: Base64-encoded Ed25519 public key for signature verification
        capabilities: List of supported capabilities
        metadata: Additional agent metadata
    """
    agent_id: str
    email_like: str
    inbox_url: HttpUrl
    public_key: str
    capabilities: List[str] = ["a2a/1.0"]
    metadata: Dict[str, Any] = {}


class AgentRegistrationResponse(BaseModel):
    """
    Response from agent registration.
    
    Fields:
        status: Registration status ("registered" or "error")
        agent_id: The registered agent's canonical URI
        email_like: The registered agent's email address
        message: Human-readable confirmation message
    """
    status: str
    agent_id: str
    email_like: str
    message: str


@router.post(
    "/register",
    response_model=AgentRegistrationResponse,
    summary="Register a new agent",
    description="""
    Register a new agent in the global registry.
    
    Anyone can register an agent! You just need:
    1. A unique agent_id (e.g., agent://yourorg/agentname)
    2. An email-like address (e.g., agentname@yourorg)
    3. An inbox URL (where to receive messages)
    4. A public key (Ed25519) for message verification
    
    After registration, your agent can:
    - Send and receive cryptographically signed messages
    - Be discovered by other agents via email address
    - Participate in agent-to-agent communication
    """,
)
async def register_agent(request: AgentRegistrationRequest) -> AgentRegistrationResponse:
    """
    Register a new agent in the global registry.
    
    Args:
        request: Agent registration details
        
    Returns:
        Registration confirmation
        
    Raises:
        409: Agent already registered
        400: Invalid agent details
    """
    registry = get_registry()
    
    # Check if agent already exists
    try:
        existing = registry.get_by_uri(request.agent_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent already registered: {request.agent_id}",
        )
    except KeyError:
        # Good - agent doesn't exist yet
        pass
    
    # Check if email already taken
    try:
        existing = registry.get_by_email(request.email_like)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email address already taken: {request.email_like}",
        )
    except KeyError:
        # Good - email is available
        pass
    
    # Register the agent
    entry = AgentRegistryEntry(
        agent_id=request.agent_id,
        email_like=request.email_like,
        inbox_url=request.inbox_url,
        public_key=request.public_key,
        capabilities=request.capabilities,
        metadata=request.metadata,
    )
    
    registry.register(entry)
    
    return AgentRegistrationResponse(
        status="registered",
        agent_id=request.agent_id,
        email_like=request.email_like,
        message=f"Agent {request.email_like} successfully registered and ready to communicate!",
    )


@router.get(
    "/agents",
    summary="List all registered agents",
    description="Get a list of all agents registered in the system.",
)
async def list_agents():
    """
    List all registered agents.
    
    Returns:
        Dictionary with count and list of agents
    """
    registry = get_registry()
    agents = registry.list_all()
    
    return {
        "count": len(agents),
        "agents": [
            {
                "agent_id": agent.agent_id,
                "email_like": agent.email_like,
                "inbox_url": str(agent.inbox_url),
                "capabilities": agent.capabilities,
                "metadata": agent.metadata,
            }
            for agent in agents
        ]
    }


@router.get(
    "/agents/{email_like}",
    summary="Lookup agent by email",
    description="Find an agent by their email-like address.",
)
async def lookup_agent(email_like: str):
    """
    Lookup an agent by their email-like address.
    
    Args:
        email_like: Email-like address (e.g., alice@wonderland)
        
    Returns:
        Agent details
        
    Raises:
        404: Agent not found
    """
    registry = get_registry()
    
    try:
        agent = registry.get_by_email(email_like)
        return {
            "agent_id": agent.agent_id,
            "email_like": agent.email_like,
            "inbox_url": str(agent.inbox_url),
            "capabilities": agent.capabilities,
            "metadata": agent.metadata,
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent not found: {email_like}",
        )


@router.delete(
    "/agents/{agent_id:path}",
    summary="Unregister an agent",
    description="Remove an agent from the registry (requires authentication in production).",
)
async def unregister_agent(agent_id: str):
    """
    Unregister an agent.
    
    Note: In production, this should require authentication.
    For now, it's open for testing purposes.
    
    Args:
        agent_id: Canonical agent URI
        
    Returns:
        Deletion confirmation
        
    Raises:
        404: Agent not found
    """
    registry = get_registry()
    
    try:
        agent = registry.get_by_uri(agent_id)
        # TODO: Add actual deletion method to registry
        # For now, just confirm agent exists
        return {
            "status": "unregistered",
            "agent_id": agent_id,
            "message": f"Agent {agent_id} would be unregistered (not implemented yet)",
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent not found: {agent_id}",
        )

