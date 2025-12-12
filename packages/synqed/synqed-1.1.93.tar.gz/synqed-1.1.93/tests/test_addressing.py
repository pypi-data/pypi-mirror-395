"""
tests for agent addressing module.

tests AgentId parsing, formatting, and validation.
"""

import pytest
from pydantic import ValidationError

from synqed.agent_email.addressing import AgentId


class TestAgentIdFromUri:
    """tests for AgentId.from_uri()."""
    
    def test_basic_uri_parsing(self) -> None:
        """test parsing basic agent uri without version."""
        agent = AgentId.from_uri("agent://futurehouse/cosmos")
        
        assert agent.org == "futurehouse"
        assert agent.name == "cosmos"
        assert agent.version is None
    
    def test_uri_with_version(self) -> None:
        """test parsing agent uri with version."""
        agent = AgentId.from_uri("agent://google/gemini/flash-1")
        
        assert agent.org == "google"
        assert agent.name == "gemini"
        assert agent.version == "flash-1"
    
    def test_uri_with_hyphens_and_underscores(self) -> None:
        """test parsing uri with allowed special characters."""
        agent = AgentId.from_uri("agent://future-house/cosmos_v2/alpha-1")
        
        assert agent.org == "future-house"
        assert agent.name == "cosmos_v2"
        assert agent.version == "alpha-1"
    
    def test_invalid_uri_missing_prefix(self) -> None:
        """test that uri without agent:// prefix is rejected."""
        with pytest.raises(ValueError, match="must start with 'agent://'"):
            AgentId.from_uri("futurehouse/cosmos")
    
    def test_invalid_uri_missing_name(self) -> None:
        """test that uri with only org is rejected."""
        with pytest.raises(ValueError, match="must have at least org and name"):
            AgentId.from_uri("agent://futurehouse")
    
    def test_invalid_uri_too_many_segments(self) -> None:
        """test that uri with too many segments is rejected."""
        with pytest.raises(ValueError, match="too many path segments"):
            AgentId.from_uri("agent://futurehouse/cosmos/v1/extra")
    
    def test_invalid_characters_in_org(self) -> None:
        """test that org with invalid characters is rejected."""
        with pytest.raises(ValidationError):
            AgentId.from_uri("agent://future house/cosmos")


class TestAgentIdToUri:
    """tests for AgentId.to_uri()."""
    
    def test_basic_uri_format(self) -> None:
        """test formatting basic agent id to uri."""
        agent = AgentId(org="futurehouse", name="cosmos")
        
        assert agent.to_uri() == "agent://futurehouse/cosmos"
    
    def test_uri_format_with_version(self) -> None:
        """test formatting agent id with version to uri."""
        agent = AgentId(org="google", name="gemini", version="flash-1")
        
        assert agent.to_uri() == "agent://google/gemini/flash-1"
    
    def test_roundtrip_uri(self) -> None:
        """test that parsing and formatting are inverse operations."""
        original = "agent://futurehouse/cosmos/v2"
        agent = AgentId.from_uri(original)
        
        assert agent.to_uri() == original


class TestAgentIdFromEmailLike:
    """tests for AgentId.from_email_like()."""
    
    def test_basic_email_parsing(self) -> None:
        """test parsing basic email-like address."""
        agent = AgentId.from_email_like("cosmos@futurehouse")
        
        assert agent.org == "futurehouse"
        assert agent.name == "cosmos"
        assert agent.version is None
    
    def test_email_with_hyphens_and_underscores(self) -> None:
        """test parsing email with allowed special characters."""
        agent = AgentId.from_email_like("cosmos_v2@future-house")
        
        assert agent.org == "future-house"
        assert agent.name == "cosmos_v2"
    
    def test_invalid_email_missing_at(self) -> None:
        """test that email without @ is rejected."""
        with pytest.raises(ValueError, match="must contain '@'"):
            AgentId.from_email_like("cosmosfuturehouse")
    
    def test_invalid_email_multiple_ats(self) -> None:
        """test that email with multiple @ is rejected."""
        with pytest.raises(ValueError, match="must have exactly one '@'"):
            AgentId.from_email_like("cosmos@future@house")
    
    def test_invalid_email_empty_name(self) -> None:
        """test that email with empty name is rejected."""
        with pytest.raises(ValueError, match="name and org cannot be empty"):
            AgentId.from_email_like("@futurehouse")
    
    def test_invalid_email_empty_org(self) -> None:
        """test that email with empty org is rejected."""
        with pytest.raises(ValueError, match="name and org cannot be empty"):
            AgentId.from_email_like("cosmos@")


class TestAgentIdToEmailLike:
    """tests for AgentId.to_email_like()."""
    
    def test_basic_email_format(self) -> None:
        """test formatting basic agent id to email."""
        agent = AgentId(org="futurehouse", name="cosmos")
        
        assert agent.to_email_like() == "cosmos@futurehouse"
    
    def test_email_format_ignores_version(self) -> None:
        """test that version is ignored in email format."""
        agent = AgentId(org="google", name="gemini", version="flash-1")
        
        assert agent.to_email_like() == "gemini@google"
    
    def test_roundtrip_email(self) -> None:
        """test that parsing and formatting are inverse operations."""
        original = "cosmos@futurehouse"
        agent = AgentId.from_email_like(original)
        
        assert agent.to_email_like() == original


class TestAgentIdConversions:
    """tests for converting between uri and email formats."""
    
    def test_uri_to_email(self) -> None:
        """test converting from uri to email-like."""
        agent = AgentId.from_uri("agent://futurehouse/cosmos")
        
        assert agent.to_email_like() == "cosmos@futurehouse"
    
    def test_email_to_uri(self) -> None:
        """test converting from email-like to uri."""
        agent = AgentId.from_email_like("cosmos@futurehouse")
        
        assert agent.to_uri() == "agent://futurehouse/cosmos"
    
    def test_uri_with_version_to_email(self) -> None:
        """test that version is preserved when converting to email."""
        agent = AgentId.from_uri("agent://google/gemini/flash-1")
        email = agent.to_email_like()
        
        # version should be lost in email format
        assert email == "gemini@google"
        
        # but original agent still has version
        assert agent.version == "flash-1"


class TestAgentIdValidation:
    """tests for agent id validation."""
    
    def test_valid_alphanumeric(self) -> None:
        """test that alphanumeric characters are allowed."""
        agent = AgentId(org="org123", name="agent456")
        
        assert agent.org == "org123"
        assert agent.name == "agent456"
    
    def test_valid_hyphens_and_underscores(self) -> None:
        """test that hyphens and underscores are allowed."""
        agent = AgentId(org="future-house", name="cosmos_v2")
        
        assert agent.org == "future-house"
        assert agent.name == "cosmos_v2"
    
    def test_invalid_spaces(self) -> None:
        """test that spaces are not allowed."""
        with pytest.raises(ValidationError):
            AgentId(org="future house", name="cosmos")
    
    def test_invalid_special_characters(self) -> None:
        """test that special characters are not allowed."""
        with pytest.raises(ValidationError):
            AgentId(org="future@house", name="cosmos")
    
    def test_invalid_empty_org(self) -> None:
        """test that empty org is not allowed."""
        with pytest.raises(ValidationError):
            AgentId(org="", name="cosmos")
    
    def test_invalid_empty_name(self) -> None:
        """test that empty name is not allowed."""
        with pytest.raises(ValidationError):
            AgentId(org="futurehouse", name="")


class TestAgentIdStringRepresentations:
    """tests for __str__ and __repr__."""
    
    def test_str_uses_uri_format(self) -> None:
        """test that str() uses canonical uri format."""
        agent = AgentId(org="futurehouse", name="cosmos")
        
        assert str(agent) == "agent://futurehouse/cosmos"
    
    def test_repr_shows_all_fields(self) -> None:
        """test that repr() shows all fields."""
        agent = AgentId(org="futurehouse", name="cosmos", version="v2")
        
        repr_str = repr(agent)
        assert "futurehouse" in repr_str
        assert "cosmos" in repr_str
        assert "v2" in repr_str

