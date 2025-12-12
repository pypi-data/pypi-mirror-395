"""
tests for unified MessageRouter routing.

verifies that:
- route_message() is the canonical async entrypoint
- send_message() properly wraps route_message()
- route_local_message() is backward compatible
- transcript entries are identical for sync + async
- deduplication works correctly
- message_id generation is deterministic
"""

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from synqed.router import MessageRouter


class MockAgent:
    """mock agent with memory for testing local routing."""
    
    def __init__(self, name: str):
        self.name = name
        self.memory = MockMemory()


class MockMemory:
    """mock agent memory."""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, from_agent: str, content: str, message_id: str = None, target: str = None) -> str:
        msg_id = message_id or f"mock-msg-{len(self.messages)}"
        self.messages.append({
            "from_agent": from_agent,
            "content": content,
            "message_id": msg_id,
            "target": target,
        })
        return msg_id


class MockRemoteAgent:
    """mock remote agent without memory (uses send_message)."""
    
    def __init__(self, name: str):
        self.name = name
        self.sent_messages = []
    
    async def send_message(self, inbox_msg):
        self.sent_messages.append(inbox_msg)


class TestRouterInitialization:
    """test router setup and agent registration."""
    
    def test_router_initialization(self):
        """test creating a new router."""
        router = MessageRouter()
        
        assert len(router.list_local_agents()) == 0
        assert len(router.get_transcript()) == 0
    
    def test_register_agent(self):
        """test registering a local agent."""
        router = MessageRouter()
        agent = MockAgent("Agent1")
        
        router.register_agent("Agent1", agent)
        
        assert "Agent1" in router.list_local_agents()
        assert router.has_agent("Agent1")
        assert router.get_agent("Agent1") == agent
    
    def test_unregister_agent(self):
        """test unregistering an agent."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        router.register_agent("Agent2", MockAgent("Agent2"))
        
        router.unregister_agent("Agent1")
        
        assert not router.has_agent("Agent1")
        assert router.has_agent("Agent2")


class TestAsyncRouting:
    """test the canonical async route_message() method."""
    
    @pytest.mark.asyncio
    async def test_route_message_local_agent(self):
        """test routing to a local agent via route_message()."""
        router = MessageRouter()
        agent = MockAgent("Writer")
        router.register_agent("Writer", agent)
        
        msg_id = await router.route_message(
            workspace_id="ws-123",
            sender="Planner",
            recipient="Writer",
            content="write a report"
        )
        
        # verify message was delivered to agent memory
        assert len(agent.memory.messages) == 1
        assert agent.memory.messages[0]["from_agent"] == "Planner"
        assert agent.memory.messages[0]["content"] == "write a report"
        
        # verify transcript entry was created
        transcript = router.get_transcript()
        assert len(transcript) == 1
        assert transcript[0]["from"] == "Planner"
        assert transcript[0]["to"] == "Writer"
        assert transcript[0]["message_id"] == msg_id
    
    @pytest.mark.asyncio
    async def test_route_message_generates_message_id(self):
        """test that route_message generates deterministic message_ids."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        msg_id1 = await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="message 1"
        )
        
        msg_id2 = await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="message 2"
        )
        
        # message ids should be unique
        assert msg_id1 != msg_id2
        
        # both should be in transcript
        transcript = router.get_transcript()
        assert len(transcript) == 2
    
    @pytest.mark.asyncio
    async def test_route_message_uses_provided_message_id(self):
        """test that route_message uses provided message_id."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        msg_id = await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="test message",
            message_id="custom-id-123"
        )
        
        assert msg_id == "custom-id-123"
        assert router.get_transcript()[0]["message_id"] == "custom-id-123"
    
    @pytest.mark.asyncio
    async def test_route_message_invalid_recipient(self):
        """test that route_message raises for unknown recipient."""
        router = MessageRouter()
        
        with pytest.raises(ValueError, match="Agent 'Unknown' is not registered"):
            await router.route_message(
                workspace_id="ws-123",
                sender="Sender",
                recipient="Unknown",
                content="test"
            )


class TestSyncWrapper:
    """test the sync send_message() wrapper."""
    
    def test_send_message_routes_correctly(self):
        """test that send_message routes via route_message()."""
        router = MessageRouter()
        agent = MockAgent("Writer")
        router.register_agent("Writer", agent)
        
        msg_id = router.send_message(
            from_agent="Planner",
            to_agent="Writer",
            content="write a report",
            workspace_id="ws-123"
        )
        
        # verify message was delivered
        assert len(agent.memory.messages) == 1
        assert agent.memory.messages[0]["from_agent"] == "Planner"
        
        # verify transcript entry
        transcript = router.get_transcript()
        assert len(transcript) == 1
        assert transcript[0]["message_id"] == msg_id
    
    def test_send_message_invalid_recipient(self):
        """test that send_message raises for unknown recipient."""
        router = MessageRouter()
        
        with pytest.raises(ValueError, match="Agent 'Unknown' is not registered"):
            router.send_message(
                from_agent="Sender",
                to_agent="Unknown",
                content="test"
            )


class TestBackwardCompatibility:
    """test backward-compatible route_local_message()."""
    
    @pytest.mark.asyncio
    async def test_route_local_message_wraps_route_message(self):
        """test that route_local_message delegates to route_message."""
        router = MessageRouter()
        agent = MockAgent("Agent1")
        router.register_agent("Agent1", agent)
        
        msg_id = await router.route_local_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="test message"
        )
        
        # should behave identically to route_message
        assert len(agent.memory.messages) == 1
        assert len(router.get_transcript()) == 1
        assert router.get_transcript()[0]["message_id"] == msg_id


class TestTranscriptConsistency:
    """test that sync + async produce identical transcripts."""
    
    @pytest.mark.asyncio
    async def test_sync_async_identical_transcripts(self):
        """verify sync and async routing produce identical transcript format."""
        # async routing
        async_router = MessageRouter()
        async_router.register_agent("Agent1", MockAgent("Agent1"))
        
        async_msg_id = await async_router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="test message"
        )
        
        # sync routing
        sync_router = MessageRouter()
        sync_router.register_agent("Agent1", MockAgent("Agent1"))
        
        sync_msg_id = sync_router.send_message(
            from_agent="Sender",
            to_agent="Agent1",
            content="test message",
            workspace_id="ws-123"
        )
        
        # compare transcript structure (excluding timestamp and message_id)
        async_entry = async_router.get_transcript()[0]
        sync_entry = sync_router.get_transcript()[0]
        
        assert async_entry["workspace_id"] == sync_entry["workspace_id"]
        assert async_entry["from"] == sync_entry["from"]
        assert async_entry["to"] == sync_entry["to"]
        assert async_entry["content"] == sync_entry["content"]
        
        # both should have all required keys
        required_keys = {"timestamp", "workspace_id", "from", "to", "message_id", "content"}
        assert set(async_entry.keys()) >= required_keys
        assert set(sync_entry.keys()) >= required_keys


class TestDeduplication:
    """test transcript deduplication."""
    
    @pytest.mark.asyncio
    async def test_duplicate_message_id_ignored(self):
        """test that duplicate message_ids are deduplicated."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        # first message
        await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="message 1",
            message_id="same-id"
        )
        
        # second message with same id - should be deduplicated in transcript
        await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="message 2",
            message_id="same-id"
        )
        
        # transcript should only have one entry
        assert len(router.get_transcript()) == 1
        assert router.get_transcript()[0]["content"] == "message 1"
    
    def test_clear_transcript_resets_deduplication(self):
        """test that clear_transcript resets deduplication state."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        router.send_message(
            from_agent="Sender",
            to_agent="Agent1",
            content="message 1",
            message_id="reused-id"
        )
        
        router.clear_transcript()
        
        # same id should work after clear
        router.send_message(
            from_agent="Sender",
            to_agent="Agent1",
            content="message 2",
            message_id="reused-id"
        )
        
        assert len(router.get_transcript()) == 1
        assert router.get_transcript()[0]["content"] == "message 2"


class TestMixedSyncAsync:
    """test mixing sync and async routing calls."""
    
    @pytest.mark.asyncio
    async def test_mixed_sync_async_ordering(self):
        """test that mixed sync/async calls maintain fifo order."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        # async first
        await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="async message 1"
        )
        
        # sync second (from within async context)
        # note: in real usage, this would run in a thread
        router.send_message(
            from_agent="Sender",
            to_agent="Agent1",
            content="sync message 2",
            workspace_id="ws-123"
        )
        
        # async third
        await router.route_message(
            workspace_id="ws-123",
            sender="Sender",
            recipient="Agent1",
            content="async message 3"
        )
        
        transcript = router.get_transcript()
        assert len(transcript) == 3
        assert transcript[0]["content"] == "async message 1"
        assert transcript[1]["content"] == "sync message 2"
        assert transcript[2]["content"] == "async message 3"


class TestRouterRepr:
    """test router string representation."""
    
    def test_repr(self):
        """test router __repr__."""
        router = MessageRouter()
        router.register_agent("Agent1", MockAgent("Agent1"))
        
        repr_str = repr(router)
        assert "MessageRouter" in repr_str
        assert "agents=1" in repr_str
        assert "transcript_length=0" in repr_str

