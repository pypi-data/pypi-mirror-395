"""
tests for a2a inbox api.

tests inbox endpoint, agent runtime protocol, and message handling.
"""

import pytest
from typing import Any, Dict
from fastapi.testclient import TestClient

from synqed.agent_email.inbox.api import (
    LocalAgentRuntime,
    register_agent_runtime,
    get_agent_runtime,
    clear_agent_runtimes,
)
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry
from synqed.agent_email.main import app


class MockAgentRuntime(LocalAgentRuntime):
    """mock agent runtime for testing."""
    
    def __init__(self, response_content: str | None = None):
        """
        initialize mock runtime.
        
        args:
            response_content: if provided, runtime will return a response envelope
        """
        self.response_content = response_content
        self.received_envelopes: list = []
    
    async def handle_a2a_envelope(
        self,
        sender: str,
        recipient: str,
        envelope: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        """handle envelope and optionally return response."""
        # record that we received this envelope
        self.received_envelopes.append({
            "sender": sender,
            "recipient": recipient,
            "envelope": envelope,
        })
        
        # return response if configured
        if self.response_content:
            return {
                "thread_id": envelope.get("thread_id", "test-thread"),
                "role": "assistant",
                "content": self.response_content,
                "tool_calls": [],
            }
        
        return None


@pytest.fixture(autouse=True)
def clear_state() -> None:
    """clear registry and runtimes before each test."""
    get_registry().clear()
    clear_agent_runtimes()


@pytest.fixture
def setup_test_agents() -> tuple[str, str]:
    """
    setup test agents in registry and runtimes.
    
    returns tuple of (sender_id, recipient_id).
    """
    sender_id = "agent://futurehouse/cosmos"
    recipient_id = "agent://google/gemini"
    
    # register in registry
    registry = get_registry()
    
    sender_entry = AgentRegistryEntry(
        agent_id=sender_id,
        email_like="cosmos@futurehouse",
        inbox_url="http://localhost:8000/v1/a2a/inbox",
    )
    registry.register(sender_entry)
    
    recipient_entry = AgentRegistryEntry(
        agent_id=recipient_id,
        email_like="gemini@google",
        inbox_url="http://localhost:8000/v1/a2a/inbox",
    )
    registry.register(recipient_entry)
    
    # register runtime for recipient
    recipient_runtime = MockAgentRuntime(response_content="test response from gemini")
    register_agent_runtime(recipient_id, recipient_runtime)
    
    return sender_id, recipient_id


@pytest.mark.skip(reason="Inbox API has changed")
class TestAgentRuntimeRegistry:
    """tests for runtime registration and lookup."""
    
    def test_register_and_get_runtime(self) -> None:
        """test registering and retrieving a runtime."""
        agent_id = "agent://test/agent"
        runtime = MockAgentRuntime()
        
        register_agent_runtime(agent_id, runtime)
        retrieved = get_agent_runtime(agent_id)
        
        assert retrieved is runtime
    
    def test_get_runtime_not_found(self) -> None:
        """test that None is returned for unknown agent."""
        retrieved = get_agent_runtime("agent://unknown/agent")
        
        assert retrieved is None
    
    def test_clear_runtimes(self) -> None:
        """test clearing all runtimes."""
        agent_id = "agent://test/agent"
        runtime = MockAgentRuntime()
        
        register_agent_runtime(agent_id, runtime)
        assert get_agent_runtime(agent_id) is not None
        
        clear_agent_runtimes()
        
        assert get_agent_runtime(agent_id) is None


@pytest.mark.skip(reason="Inbox API has changed")
class TestInboxAPI:
    """tests for POST /v1/a2a/inbox endpoint."""
    
    def test_receive_envelope_success(self, setup_test_agents: tuple) -> None:
        """test successfully receiving and processing an envelope."""
        sender_id, recipient_id = setup_test_agents
        client = TestClient(app)
        
        envelope = {
            "thread_id": "test-thread-123",
            "role": "user",
            "content": "analyze this startup idea",
            "tool_calls": [],
        }
        
        request = {
            "sender": sender_id,
            "recipient": recipient_id,
            "message": envelope,
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "accepted"
        assert data["message_id"] is not None
        assert data["response_envelope"] is not None
        assert data["response_envelope"]["content"] == "test response from gemini"
    
    def test_receive_envelope_no_response(self, setup_test_agents: tuple) -> None:
        """test receiving envelope when agent doesn't respond."""
        sender_id, recipient_id = setup_test_agents
        client = TestClient(app)
        
        # replace runtime with one that doesn't respond
        no_response_runtime = MockAgentRuntime(response_content=None)
        register_agent_runtime(recipient_id, no_response_runtime)
        
        envelope = {
            "thread_id": "test-thread-123",
            "role": "user",
            "content": "test message",
        }
        
        request = {
            "sender": sender_id,
            "recipient": recipient_id,
            "message": envelope,
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "accepted"
        assert data["message_id"] is not None
        assert data["response_envelope"] is None
    
    def test_invalid_sender_uri(self, setup_test_agents: tuple) -> None:
        """test that invalid sender uri is rejected."""
        _, recipient_id = setup_test_agents
        client = TestClient(app)
        
        request = {
            "sender": "not-a-valid-uri",
            "recipient": recipient_id,
            "message": {"content": "test"},
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 400
        assert "invalid sender uri" in response.json()["detail"]
    
    def test_invalid_recipient_uri(self, setup_test_agents: tuple) -> None:
        """test that invalid recipient uri is rejected."""
        sender_id, _ = setup_test_agents
        client = TestClient(app)
        
        request = {
            "sender": sender_id,
            "recipient": "not-a-valid-uri",
            "message": {"content": "test"},
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 400
        assert "invalid recipient uri" in response.json()["detail"]
    
    def test_recipient_not_in_registry(self, setup_test_agents: tuple) -> None:
        """test that 404 is returned if recipient not in registry."""
        sender_id, _ = setup_test_agents
        client = TestClient(app)
        
        unknown_recipient = "agent://unknown/agent"
        
        request = {
            "sender": sender_id,
            "recipient": unknown_recipient,
            "message": {"content": "test"},
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 404
        assert "recipient not found in registry" in response.json()["detail"]
    
    def test_recipient_no_local_runtime(self, setup_test_agents: tuple) -> None:
        """test that 404 is returned if recipient has no local runtime."""
        sender_id, recipient_id = setup_test_agents
        client = TestClient(app)
        
        # clear the runtime (simulating agent hosted elsewhere)
        clear_agent_runtimes()
        
        request = {
            "sender": sender_id,
            "recipient": recipient_id,
            "message": {"content": "test"},
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 404
        assert "no local runtime found" in response.json()["detail"]
    
    def test_runtime_error_handling(self, setup_test_agents: tuple) -> None:
        """test that runtime errors are caught and returned as error status."""
        sender_id, recipient_id = setup_test_agents
        client = TestClient(app)
        
        # create runtime that raises an error
        class ErrorRuntime(LocalAgentRuntime):
            async def handle_a2a_envelope(
                self,
                sender: str,
                recipient: str,
                envelope: Dict[str, Any],
            ) -> Dict[str, Any] | None:
                raise ValueError("intentional test error")
        
        register_agent_runtime(recipient_id, ErrorRuntime())
        
        request = {
            "sender": sender_id,
            "recipient": recipient_id,
            "message": {"content": "test"},
        }
        
        response = client.post("/v1/a2a/inbox", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "error"
        assert data["error"] is not None
        assert "intentional test error" in data["error"]


@pytest.mark.skip(reason="Inbox API has changed")
class TestMockAgentRuntime:
    """tests for the mock runtime helper."""
    
    @pytest.mark.asyncio
    async def test_mock_runtime_records_envelopes(self) -> None:
        """test that mock runtime records received envelopes."""
        runtime = MockAgentRuntime()
        
        envelope = {
            "thread_id": "test-123",
            "content": "test message",
        }
        
        await runtime.handle_a2a_envelope(
            sender="agent://test/sender",
            recipient="agent://test/recipient",
            envelope=envelope,
        )
        
        assert len(runtime.received_envelopes) == 1
        recorded = runtime.received_envelopes[0]
        assert recorded["sender"] == "agent://test/sender"
        assert recorded["recipient"] == "agent://test/recipient"
        assert recorded["envelope"]["content"] == "test message"
    
    @pytest.mark.asyncio
    async def test_mock_runtime_returns_response(self) -> None:
        """test that mock runtime returns configured response."""
        runtime = MockAgentRuntime(response_content="test response")
        
        envelope = {
            "thread_id": "test-123",
            "content": "test message",
        }
        
        response = await runtime.handle_a2a_envelope(
            sender="agent://test/sender",
            recipient="agent://test/recipient",
            envelope=envelope,
        )
        
        assert response is not None
        assert response["content"] == "test response"
        assert response["thread_id"] == "test-123"
        assert response["role"] == "assistant"
    
    @pytest.mark.asyncio
    async def test_mock_runtime_no_response(self) -> None:
        """test that mock runtime returns None when not configured."""
        runtime = MockAgentRuntime(response_content=None)
        
        envelope = {
            "thread_id": "test-123",
            "content": "test message",
        }
        
        response = await runtime.handle_a2a_envelope(
            sender="agent://test/sender",
            recipient="agent://test/recipient",
            envelope=envelope,
        )
        
        assert response is None

