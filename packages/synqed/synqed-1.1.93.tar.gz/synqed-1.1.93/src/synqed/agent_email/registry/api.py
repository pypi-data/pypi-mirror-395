"""
agent registry fastapi endpoints.

provides rest api for agent registration and discovery:
- POST /v1/agents: register a new agent
- GET /v1/agents/by-uri/{uri}: lookup by canonical uri
- GET /v1/agents/by-email/{email}: lookup by email-like address
- GET /v1/agents: list all registered agents
"""

from typing import List
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl, ValidationError

from synqed.agent_email.registry.models import AgentRegistryEntry, AgentRegistry
from synqed.agent_email.addressing import AgentId


# global registry instance
# todo: replace with dependency injection for better testability
_global_registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """get the global registry instance."""
    return _global_registry


# request model for registration (allows deriving agent_id from email_like)
class AgentRegistrationRequest(BaseModel):
    """
    request body for registering an agent.
    
    can provide either:
    - agent_id + email_like (both must match)
    - just email_like (agent_id will be derived)
    
    inbox_url is always required.
    """
    
    agent_id: str | None = None  # optional, will be derived if not provided
    email_like: str  # required
    inbox_url: HttpUrl  # required
    public_key: str | None = None
    capabilities: List[str] = []
    metadata: dict = {}


# create router
router = APIRouter(prefix="/v1/agents", tags=["registry"])


@router.post(
    "",
    response_model=AgentRegistryEntry,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new agent",
)
async def register_agent(request: AgentRegistrationRequest) -> AgentRegistryEntry:
    """
    register or update an agent in the registry.
    
    if agent_id is not provided, it will be derived from email_like.
    if agent_id is provided, it must match the email_like address.
    
    returns the registered entry.
    """
    registry = get_registry()
    
    # validate email_like format
    try:
        agent_from_email = AgentId.from_email_like(request.email_like)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid email_like format: {e}",
        ) from e
    
    # derive or validate agent_id
    if request.agent_id is None:
        # derive from email_like
        agent_id_str = agent_from_email.to_uri()
    else:
        # validate that provided agent_id matches email_like
        try:
            agent_from_uri = AgentId.from_uri(request.agent_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"invalid agent_id uri: {e}",
            ) from e
        
        # check consistency
        if agent_from_uri.org != agent_from_email.org or agent_from_uri.name != agent_from_email.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"agent_id '{request.agent_id}' does not match "
                    f"email_like '{request.email_like}'"
                ),
            )
        
        agent_id_str = request.agent_id
    
    # create entry
    try:
        entry = AgentRegistryEntry(
            agent_id=agent_id_str,
            email_like=request.email_like,
            inbox_url=request.inbox_url,
            public_key=request.public_key,
            capabilities=request.capabilities,
            metadata=request.metadata,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"validation error: {e}",
        ) from e
    
    # register
    registry.register(entry)
    
    return entry


@router.get(
    "/by-uri/{encoded_uri:path}",
    response_model=AgentRegistryEntry,
    summary="Lookup agent by canonical URI",
)
async def get_agent_by_uri(encoded_uri: str) -> AgentRegistryEntry:
    """
    lookup an agent by its canonical uri.
    
    the uri should be url-encoded in the path.
    
    example: /v1/agents/by-uri/agent%3A%2F%2Ffuturehouse%2Fcosmos
    
    returns 404 if not found.
    """
    registry = get_registry()
    
    # decode uri
    agent_uri = unquote(encoded_uri)
    
    # validate format
    try:
        AgentId.from_uri(agent_uri)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid agent uri format: {e}",
        ) from e
    
    # lookup
    try:
        entry = registry.get_by_uri(agent_uri)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"agent not found: {agent_uri}",
        )
    
    return entry


@router.get(
    "/by-email/{email}",
    response_model=AgentRegistryEntry,
    summary="Lookup agent by email-like address",
)
async def get_agent_by_email(email: str) -> AgentRegistryEntry:
    """
    lookup an agent by its email-like address.
    
    example: /v1/agents/by-email/cosmos@futurehouse
    
    returns 404 if not found.
    """
    registry = get_registry()
    
    # validate format
    try:
        AgentId.from_email_like(email)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid email-like format: {e}",
        ) from e
    
    # lookup
    try:
        entry = registry.get_by_email(email)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"agent not found: {email}",
        )
    
    return entry


@router.get(
    "",
    response_model=List[AgentRegistryEntry],
    summary="List all registered agents",
)
async def list_agents() -> List[AgentRegistryEntry]:
    """
    list all agents in the registry.
    
    returns empty list if no agents are registered.
    """
    registry = get_registry()
    return registry.list_all()

