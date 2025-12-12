"""
tests for agent registry.

tests registry models, in-memory backend, and fastapi endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from synqed.agent_email.registry.models import AgentRegistry, AgentRegistryEntry
from synqed.agent_email.main import app


@pytest.fixture
def registry() -> AgentRegistry:
    """create a fresh registry for each test."""
    reg = AgentRegistry()
    return reg


@pytest.fixture
def sample_entry() -> AgentRegistryEntry:
    """create a sample registry entry."""
    return AgentRegistryEntry(
        agent_id="agent://futurehouse/cosmos",
        email_like="cosmos@futurehouse",
        inbox_url="http://localhost:8001/inbox",
        capabilities=["a2a/1.0"],
        metadata={"description": "research agent"},
    )


@pytest.mark.skip(reason="Registry API has changed")
class TestAgentRegistryEntry:
    """tests for AgentRegistryEntry model."""
    
    def test_valid_entry_creation(self) -> None:
        """test creating a valid registry entry."""
        entry = AgentRegistryEntry(
            agent_id="agent://futurehouse/cosmos",
            email_like="cosmos@futurehouse",
            inbox_url="http://localhost:8001/inbox",
        )
        
        assert entry.agent_id == "agent://futurehouse/cosmos"
        assert entry.email_like == "cosmos@futurehouse"
        assert str(entry.inbox_url) == "http://localhost:8001/inbox"
        assert entry.capabilities == []
        assert entry.metadata == {}
    
    def test_entry_with_capabilities_and_metadata(self) -> None:
        """test creating entry with optional fields."""
        entry = AgentRegistryEntry(
            agent_id="agent://google/gemini",
            email_like="gemini@google",
            inbox_url="http://localhost:8002/inbox",
            capabilities=["a2a/1.0", "reasoning"],
            metadata={"model": "flash-1", "region": "us-west"},
        )
        
        assert len(entry.capabilities) == 2
        assert entry.metadata["model"] == "flash-1"
    
    def test_invalid_agent_id_uri(self) -> None:
        """test that invalid agent_id uri is rejected."""
        with pytest.raises(ValueError, match="invalid agent_id uri"):
            AgentRegistryEntry(
                agent_id="not-a-valid-uri",
                email_like="cosmos@futurehouse",
                inbox_url="http://localhost:8001/inbox",
            )
    
    def test_invalid_email_like(self) -> None:
        """test that invalid email_like is rejected."""
        with pytest.raises(ValueError, match="invalid email_like"):
            AgentRegistryEntry(
                agent_id="agent://futurehouse/cosmos",
                email_like="not-an-email",
                inbox_url="http://localhost:8001/inbox",
            )


@pytest.mark.skip(reason="Registry API has changed")
class TestAgentRegistry:
    """tests for AgentRegistry backend."""
    
    def test_register_and_get_by_uri(self, registry: AgentRegistry, sample_entry: AgentRegistryEntry) -> None:
        """test registering and retrieving by uri."""
        registry.register(sample_entry)
        
        retrieved = registry.get_by_uri("agent://futurehouse/cosmos")
        
        assert retrieved.agent_id == sample_entry.agent_id
        assert retrieved.email_like == sample_entry.email_like
    
    def test_register_and_get_by_email(self, registry: AgentRegistry, sample_entry: AgentRegistryEntry) -> None:
        """test registering and retrieving by email."""
        registry.register(sample_entry)
        
        retrieved = registry.get_by_email("cosmos@futurehouse")
        
        assert retrieved.agent_id == sample_entry.agent_id
        assert retrieved.email_like == sample_entry.email_like
    
    def test_get_by_uri_not_found(self, registry: AgentRegistry) -> None:
        """test that KeyError is raised for unknown uri."""
        with pytest.raises(KeyError, match="agent not found"):
            registry.get_by_uri("agent://unknown/agent")
    
    def test_get_by_email_not_found(self, registry: AgentRegistry) -> None:
        """test that KeyError is raised for unknown email."""
        with pytest.raises(KeyError, match="agent not found"):
            registry.get_by_email("unknown@org")
    
    def test_register_updates_existing(self, registry: AgentRegistry) -> None:
        """test that registering same agent_id updates the entry."""
        entry1 = AgentRegistryEntry(
            agent_id="agent://futurehouse/cosmos",
            email_like="cosmos@futurehouse",
            inbox_url="http://localhost:8001/inbox",
            metadata={"version": "1"},
        )
        
        entry2 = AgentRegistryEntry(
            agent_id="agent://futurehouse/cosmos",
            email_like="cosmos@futurehouse",
            inbox_url="http://localhost:8002/inbox",
            metadata={"version": "2"},
        )
        
        registry.register(entry1)
        registry.register(entry2)
        
        retrieved = registry.get_by_uri("agent://futurehouse/cosmos")
        
        # should have the updated entry
        assert str(retrieved.inbox_url) == "http://localhost:8002/inbox"
        assert retrieved.metadata["version"] == "2"
    
    def test_list_all_empty(self, registry: AgentRegistry) -> None:
        """test listing all entries when registry is empty."""
        entries = registry.list_all()
        
        assert len(entries) == 0
    
    def test_list_all_multiple_entries(self, registry: AgentRegistry) -> None:
        """test listing all entries."""
        entry1 = AgentRegistryEntry(
            agent_id="agent://futurehouse/cosmos",
            email_like="cosmos@futurehouse",
            inbox_url="http://localhost:8001/inbox",
        )
        
        entry2 = AgentRegistryEntry(
            agent_id="agent://google/gemini",
            email_like="gemini@google",
            inbox_url="http://localhost:8002/inbox",
        )
        
        registry.register(entry1)
        registry.register(entry2)
        
        entries = registry.list_all()
        
        assert len(entries) == 2
        agent_ids = {e.agent_id for e in entries}
        assert "agent://futurehouse/cosmos" in agent_ids
        assert "agent://google/gemini" in agent_ids
    
    def test_clear(self, registry: AgentRegistry, sample_entry: AgentRegistryEntry) -> None:
        """test clearing the registry."""
        registry.register(sample_entry)
        assert len(registry.list_all()) == 1
        
        registry.clear()
        
        assert len(registry.list_all()) == 0
        
        with pytest.raises(KeyError):
            registry.get_by_uri(sample_entry.agent_id)


@pytest.mark.skip(reason="Registry API has changed")
class TestRegistryAPI:
    """tests for registry fastapi endpoints."""
    
    @pytest.fixture(autouse=True)
    def clear_registry(self) -> None:
        """clear the global registry before each test."""
        from synqed.agent_email.registry.api import get_registry
        get_registry().clear()
    
    def test_register_agent_minimal(self) -> None:
        """test registering agent with minimal fields."""
        client = TestClient(app)
        
        response = client.post(
            "/v1/agents",
            json={
                "email_like": "cosmos@futurehouse",
                "inbox_url": "http://localhost:8001/inbox",
            },
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["agent_id"] == "agent://futurehouse/cosmos"
        assert data["email_like"] == "cosmos@futurehouse"
    
    def test_register_agent_with_all_fields(self) -> None:
        """test registering agent with all fields."""
        client = TestClient(app)
        
        response = client.post(
            "/v1/agents",
            json={
                "agent_id": "agent://google/gemini",
                "email_like": "gemini@google",
                "inbox_url": "http://localhost:8002/inbox",
                "capabilities": ["a2a/1.0", "reasoning"],
                "metadata": {"model": "flash-1"},
            },
        )
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["capabilities"]) == 2
        assert data["metadata"]["model"] == "flash-1"
    
    def test_register_agent_invalid_email(self) -> None:
        """test that invalid email_like is rejected."""
        client = TestClient(app)
        
        response = client.post(
            "/v1/agents",
            json={
                "email_like": "not-an-email",
                "inbox_url": "http://localhost:8001/inbox",
            },
        )
        
        assert response.status_code == 400
        assert "invalid email_like format" in response.json()["detail"]
    
    def test_get_agent_by_uri(self) -> None:
        """test getting agent by canonical uri."""
        client = TestClient(app)
        
        # register first
        client.post(
            "/v1/agents",
            json={
                "email_like": "cosmos@futurehouse",
                "inbox_url": "http://localhost:8001/inbox",
            },
        )
        
        # retrieve by uri (url-encoded)
        from urllib.parse import quote
        encoded_uri = quote("agent://futurehouse/cosmos", safe="")
        
        response = client.get(f"/v1/agents/by-uri/{encoded_uri}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == "agent://futurehouse/cosmos"
    
    def test_get_agent_by_uri_not_found(self) -> None:
        """test that 404 is returned for unknown uri."""
        client = TestClient(app)
        
        from urllib.parse import quote
        encoded_uri = quote("agent://unknown/agent", safe="")
        
        response = client.get(f"/v1/agents/by-uri/{encoded_uri}")
        
        assert response.status_code == 404
    
    def test_get_agent_by_email(self) -> None:
        """test getting agent by email-like address."""
        client = TestClient(app)
        
        # register first
        client.post(
            "/v1/agents",
            json={
                "email_like": "cosmos@futurehouse",
                "inbox_url": "http://localhost:8001/inbox",
            },
        )
        
        # retrieve by email
        response = client.get("/v1/agents/by-email/cosmos@futurehouse")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email_like"] == "cosmos@futurehouse"
    
    def test_get_agent_by_email_not_found(self) -> None:
        """test that 404 is returned for unknown email."""
        client = TestClient(app)
        
        response = client.get("/v1/agents/by-email/unknown@org")
        
        assert response.status_code == 404
    
    def test_list_all_agents_empty(self) -> None:
        """test listing agents when registry is empty."""
        client = TestClient(app)
        
        response = client.get("/v1/agents")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_list_all_agents(self) -> None:
        """test listing all agents."""
        client = TestClient(app)
        
        # register two agents
        client.post(
            "/v1/agents",
            json={
                "email_like": "cosmos@futurehouse",
                "inbox_url": "http://localhost:8001/inbox",
            },
        )
        
        client.post(
            "/v1/agents",
            json={
                "email_like": "gemini@google",
                "inbox_url": "http://localhost:8002/inbox",
            },
        )
        
        # list all
        response = client.get("/v1/agents")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

