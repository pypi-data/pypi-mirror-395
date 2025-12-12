"""
agent addressing module.

provides canonical agent id format (agent://{org}/{name}[/version])
and human-friendly email-like format ({name}@{org}).
"""

import re
from typing import Optional
from pydantic import BaseModel, field_validator


# allowed charset for agent id parts: alphanumeric, hyphens, underscores (no spaces)
VALID_PART_PATTERN = re.compile(r"^[a-z0-9_-]+$", re.IGNORECASE)


class AgentId(BaseModel):
    """
    represents an agent identity with org, name, and optional version.
    
    supports parsing from:
    - uri format: agent://futurehouse/cosmos or agent://futurehouse/cosmos/v1
    - email-like format: cosmos@futurehouse
    
    examples:
        >>> agent = AgentId.from_uri("agent://futurehouse/cosmos")
        >>> agent.to_email_like()
        'cosmos@futurehouse'
        
        >>> agent = AgentId.from_email_like("gemini@google")
        >>> agent.to_uri()
        'agent://google/gemini'
    """
    
    org: str
    name: str
    version: Optional[str] = None
    
    @field_validator("org", "name", "version")
    @classmethod
    def validate_part(cls, v: Optional[str]) -> Optional[str]:
        """validate that org, name, and version contain only allowed characters."""
        if v is None:
            return v
        if not v:
            raise ValueError("org/name/version cannot be empty string")
        if not VALID_PART_PATTERN.match(v):
            raise ValueError(
                f"invalid characters in '{v}': only alphanumeric, hyphens, "
                "and underscores allowed"
            )
        return v
    
    @classmethod
    def from_uri(cls, uri: str) -> "AgentId":
        """
        parse agent id from uri format.
        
        format: agent://{org}/{name}[/version]
        
        examples:
            - agent://futurehouse/cosmos
            - agent://google/gemini/flash-1
        
        args:
            uri: the agent uri string
            
        returns:
            AgentId instance
            
        raises:
            ValueError: if uri format is invalid
        """
        if not uri.startswith("agent://"):
            raise ValueError(
                f"invalid agent uri '{uri}': must start with 'agent://'"
            )
        
        path = uri[len("agent://"):]
        parts = path.split("/")
        
        if len(parts) < 2:
            raise ValueError(
                f"invalid agent uri '{uri}': must have at least org and name"
            )
        if len(parts) > 3:
            raise ValueError(
                f"invalid agent uri '{uri}': too many path segments"
            )
        
        org = parts[0]
        name = parts[1]
        version = parts[2] if len(parts) == 3 else None
        
        return cls(org=org, name=name, version=version)
    
    def to_uri(self) -> str:
        """
        convert agent id to canonical uri format.
        
        returns:
            uri string like 'agent://google/gemini' or 'agent://google/gemini/v1'
        """
        base = f"agent://{self.org}/{self.name}"
        if self.version:
            return f"{base}/{self.version}"
        return base
    
    @classmethod
    def from_email_like(cls, addr: str) -> "AgentId":
        """
        parse agent id from email-like address.
        
        format: {name}@{org}
        
        examples:
            - cosmos@futurehouse
            - gemini@google
        
        note: email-like format does not support version field
        
        args:
            addr: the email-like address string
            
        returns:
            AgentId instance with version=None
            
        raises:
            ValueError: if address format is invalid
        """
        if "@" not in addr:
            raise ValueError(
                f"invalid email-like address '{addr}': must contain '@'"
            )
        
        parts = addr.split("@")
        if len(parts) != 2:
            raise ValueError(
                f"invalid email-like address '{addr}': must have exactly one '@'"
            )
        
        name = parts[0]
        org = parts[1]
        
        if not name or not org:
            raise ValueError(
                f"invalid email-like address '{addr}': name and org cannot be empty"
            )
        
        return cls(org=org, name=name, version=None)
    
    def to_email_like(self) -> str:
        """
        convert agent id to email-like format.
        
        note: version field is ignored in email-like format
        
        returns:
            email-like string like 'cosmos@futurehouse'
        """
        return f"{self.name}@{self.org}"
    
    def __str__(self) -> str:
        """string representation uses canonical uri format."""
        return self.to_uri()
    
    def __repr__(self) -> str:
        """repr includes all fields."""
        return f"AgentId(org='{self.org}', name='{self.name}', version={self.version!r})"

