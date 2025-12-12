"""
agent registry models and in-memory backend.

provides:
- AgentRegistryEntry: schema for agent metadata + inbox url
- AgentRegistry: in-memory storage with get_by_uri and get_by_email
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, HttpUrl

from synqed.agent_email.addressing import AgentId


class AgentRegistryEntry(BaseModel):
    """
    registry entry for an agent.
    
    contains all metadata needed to discover and communicate with an agent,
    including its canonical uri, email-like address, inbox endpoint, and capabilities.
    
    fields:
        agent_id: canonical uri (e.g., agent://futurehouse/cosmos)
        email_like: human-friendly address (e.g., cosmos@futurehouse)
        inbox_url: http endpoint where a2a envelopes should be sent
        public_key: base64-encoded ed25519 public key for signature verification (required)
        capabilities: freeform tags describing agent features (e.g., ["a2a/1.0"])
        metadata: arbitrary additional data
    """
    
    agent_id: str  # canonical uri
    email_like: str  # email-like format
    inbox_url: HttpUrl  # http inbox endpoint
    public_key: str  # base64-encoded ed25519 public key (32 bytes)
    capabilities: List[str] = []
    metadata: Dict[str, Any] = {}
    
    def model_post_init(self, __context: Any) -> None:
        """validate that agent_id and email_like are parseable after init."""
        # ensure agent_id is valid uri
        try:
            AgentId.from_uri(self.agent_id)
        except ValueError as e:
            raise ValueError(f"invalid agent_id uri: {e}") from e
        
        # ensure email_like is valid
        try:
            AgentId.from_email_like(self.email_like)
        except ValueError as e:
            raise ValueError(f"invalid email_like address: {e}") from e


class AgentRegistry:
    """
    in-memory agent registry.
    
    provides lookup by canonical uri or email-like address.
    designed to be easily replaceable with a database-backed implementation later.
    
    thread-safety note: this implementation is not thread-safe.
    for production use with multiple workers, replace with a shared backend (postgres, redis, etc.).
    """
    
    def __init__(self) -> None:
        """initialize empty registry."""
        # primary store: agent_id (uri) -> entry
        self._by_uri: Dict[str, AgentRegistryEntry] = {}
        # secondary index: email_like -> agent_id (uri)
        self._by_email: Dict[str, str] = {}
    
    def register(self, entry: AgentRegistryEntry) -> None:
        """
        register or update an agent entry.
        
        if an agent with the same agent_id already exists, it will be replaced.
        
        args:
            entry: the registry entry to register
        """
        # store in primary index
        self._by_uri[entry.agent_id] = entry
        # update secondary index
        self._by_email[entry.email_like] = entry.agent_id
    
    def get_by_uri(self, agent_uri: str) -> AgentRegistryEntry:
        """
        lookup agent by canonical uri.
        
        args:
            agent_uri: canonical agent uri (e.g., agent://futurehouse/cosmos)
            
        returns:
            the registry entry
            
        raises:
            KeyError: if agent not found
        """
        if agent_uri not in self._by_uri:
            raise KeyError(f"agent not found: {agent_uri}")
        return self._by_uri[agent_uri]
    
    def get_by_email(self, email_like: str) -> AgentRegistryEntry:
        """
        lookup agent by email-like address.
        
        args:
            email_like: email-like address (e.g., cosmos@futurehouse)
            
        returns:
            the registry entry
            
        raises:
            KeyError: if agent not found
        """
        if email_like not in self._by_email:
            raise KeyError(f"agent not found: {email_like}")
        
        agent_uri = self._by_email[email_like]
        return self._by_uri[agent_uri]
    
    def list_all(self) -> List[AgentRegistryEntry]:
        """
        get all registered agents.
        
        returns:
            list of all registry entries
        """
        return list(self._by_uri.values())
    
    def clear(self) -> None:
        """remove all entries (useful for testing)."""
        self._by_uri.clear()
        self._by_email.clear()

