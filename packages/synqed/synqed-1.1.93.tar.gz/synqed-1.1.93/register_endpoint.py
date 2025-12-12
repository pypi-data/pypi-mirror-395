"""
Public Agent Registration Endpoint

Add this to your main.py to allow anyone to register agents.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry

# Create registration router
registration_router = APIRouter(prefix="/v1/a2a", tags=["registration"])


class AgentRegistrationRequest(BaseModel):
    """Request to register a new agent."""
    agent_id: str  # e.g., "agent://myorg/myagent"
    email_like: str  # e.g., "myagent@myorg"
    inbox_url: HttpUrl  # e.g., "https://synqed.fly.dev/v1/a2a/inbox"
    public_key: str  # base64-encoded Ed25519 public key
    capabilities: List[str] = ["a2a/1.0"]
    metadata: Dict[str, Any] = {}


class AgentRegistrationResponse(BaseModel):
    """Response from registration."""
    status: str
    agent_id: str
    email_like: str
    message: str


@registration_router.post(
    "/register",
    response_model=AgentRegistrationResponse,
    summary="Register a new agent",
)
async def register_agent(request: AgentRegistrationRequest) -> AgentRegistrationResponse:
    """
    Register a new agent in the global registry.
    
    Anyone can register an agent by providing:
    - Unique agent_id (canonical URI)
    - Email-like address
    - Inbox URL (where to send messages)
    - Public key (for signature verification)
    
    Returns:
        Registration confirmation with agent details
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
        message=f"Agent {request.email_like} successfully registered and ready to receive messages",
    )


@registration_router.get(
    "/agents",
    summary="List all registered agents",
)
async def list_agents():
    """
    List all registered agents.
    
    Returns:
        List of all agents in the registry
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


@registration_router.get(
    "/agents/{email_like}",
    summary="Lookup agent by email",
)
async def lookup_agent(email_like: str):
    """
    Lookup an agent by their email-like address.
    
    Args:
        email_like: Email-like address (e.g., alice@wonderland)
    
    Returns:
        Agent details
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


# Add this to your main.py:
# from register_endpoint import registration_router
# app.include_router(registration_router)

