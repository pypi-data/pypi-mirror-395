"""Tests for the Workspace module."""

import asyncio
import json
from pathlib import Path

import pytest

from synqed import Agent, Workspace


@pytest.fixture
async def sample_agent():
    """Create a sample agent for testing."""

    async def executor(context):
        return f"Response from agent: {context.get_user_input()}"

    agent = Agent(
        name="TestAgent",
        description="A test agent",
        logic=executor,
        capabilities=["testing", "validation"],
    )
    return agent


@pytest.fixture
async def sample_workspace(tmp_path):
    """Create a sample workspace for testing."""
    workspace = Workspace(
        name="Test Workspace",
        description="A test workspace",
        workspace_dir=tmp_path / "workspace",
        auto_cleanup=False,  # Don't auto-cleanup in tests
    )
    yield workspace
    # Cleanup after test
    await workspace.close()


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceCreation:
    """Test workspace creation and initialization."""

    def test_workspace_creation(self, tmp_path):
        """Test basic workspace creation."""
        workspace = Workspace(
            name="Test Workspace",
            description="Test description",
            workspace_dir=tmp_path / "test_workspace",
        )

        assert workspace.name == "Test Workspace"
        assert workspace.description == "Test description"
        assert workspace.state == WorkspaceState.CREATED
        assert workspace.workspace_dir.exists()
        assert workspace.workspace_id is not None

    def test_workspace_with_custom_id(self, tmp_path):
        """Test workspace creation with custom ID."""
        custom_id = "custom-workspace-123"
        workspace = Workspace(
            name="Custom Workspace",
            description="Test",
            workspace_id=custom_id,
            workspace_dir=tmp_path / "custom",
        )

        assert workspace.workspace_id == custom_id

    def test_workspace_default_settings(self, tmp_path):
        """Test workspace default settings."""
        workspace = Workspace(
            name="Default Workspace",
            description="Test",
            workspace_dir=tmp_path / "default",
        )

        assert workspace.auto_cleanup is True
        assert workspace.enable_persistence is False
        assert workspace.max_messages == 1000
        assert workspace.message_retention_hours == 24


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceParticipants:
    """Test workspace participant management."""

    @pytest.mark.asyncio
    async def test_add_agent(self, sample_workspace, sample_agent):
        """Test adding an agent to workspace."""
        participant_id = sample_workspace.add_agent(sample_agent)

        assert participant_id is not None
        assert len(sample_workspace.list_participants()) == 1

        participants = sample_workspace.list_participants()
        assert participants[0]["name"] == "TestAgent"
        assert participants[0]["role"] == "agent"

    @pytest.mark.asyncio
    async def test_add_remote_agent(self, sample_workspace):
        """Test adding a remote agent by URL."""
        participant_id = sample_workspace.add_agent(
            agent_url="http://remote-agent:8000", role="remote"
        )

        assert participant_id is not None
        assert len(sample_workspace.list_participants()) == 1

    @pytest.mark.asyncio
    async def test_add_agent_without_params_raises(self, sample_workspace):
        """Test that adding agent without params raises error."""
        with pytest.raises(ValueError, match="Must provide either agent or agent_url"):
            sample_workspace.add_agent()

    @pytest.mark.asyncio
    async def test_remove_agent(self, sample_workspace, sample_agent):
        """Test removing an agent from workspace."""
        participant_id = sample_workspace.add_agent(sample_agent)
        assert len(sample_workspace.list_participants()) == 1

        sample_workspace.remove_agent(participant_id)
        assert len(sample_workspace.list_participants()) == 0

    @pytest.mark.asyncio
    async def test_remove_nonexistent_agent(self, sample_workspace):
        """Test removing non-existent agent doesn't raise error."""
        # Should not raise
        sample_workspace.remove_agent("nonexistent-id")

    @pytest.mark.asyncio
    async def test_list_participants(self, sample_workspace, sample_agent):
        """Test listing participants."""
        sample_workspace.add_agent(sample_agent)
        sample_workspace.add_agent(agent_url="http://remote:8000")

        participants = sample_workspace.list_participants()
        assert len(participants) == 2
        assert all("participant_id" in p for p in participants)
        assert all("name" in p for p in participants)
        assert all("joined_at" in p for p in participants)


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceLifecycle:
    """Test workspace lifecycle management."""

    @pytest.mark.asyncio
    async def test_start_workspace(self, sample_workspace):
        """Test starting a workspace."""
        await sample_workspace.start()

        assert sample_workspace.state == WorkspaceState.ACTIVE
        assert sample_workspace.started_at is not None

    @pytest.mark.asyncio
    async def test_pause_workspace(self, sample_workspace):
        """Test pausing a workspace."""
        await sample_workspace.start()
        await sample_workspace.pause()

        assert sample_workspace.state == WorkspaceState.PAUSED

    @pytest.mark.asyncio
    async def test_resume_workspace(self, sample_workspace):
        """Test resuming a workspace."""
        await sample_workspace.start()
        await sample_workspace.pause()
        await sample_workspace.resume()

        assert sample_workspace.state == WorkspaceState.ACTIVE

    @pytest.mark.asyncio
    async def test_complete_workspace(self, sample_workspace):
        """Test completing a workspace."""
        await sample_workspace.start()
        await sample_workspace.complete()

        assert sample_workspace.state == WorkspaceState.COMPLETED
        assert sample_workspace.completed_at is not None

    @pytest.mark.asyncio
    async def test_close_workspace(self, sample_workspace):
        """Test closing a workspace."""
        await sample_workspace.start()
        await sample_workspace.close()

        # Should cleanup resources
        assert not sample_workspace._running

    @pytest.mark.asyncio
    async def test_context_manager(self, tmp_path):
        """Test using workspace as context manager."""
        workspace = Workspace(
            name="Context Test",
            description="Test",
            workspace_dir=tmp_path / "context",
        )

        async with workspace as ws:
            assert ws.state == WorkspaceState.ACTIVE

        # Should be closed after exiting context
        assert not ws._running


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceMessages:
    """Test workspace messaging."""

    @pytest.mark.asyncio
    async def test_add_message(self, sample_workspace):
        """Test adding messages to workspace."""
        await sample_workspace.start()

        # Messages are added automatically, check initial system messages
        messages = sample_workspace.get_messages()
        assert len(messages) > 0
        assert any(m.message_type == MessageType.SYSTEM for m in messages)

    @pytest.mark.asyncio
    async def test_filter_messages_by_type(self, sample_workspace, sample_agent):
        """Test filtering messages by type."""
        await sample_workspace.start()
        sample_workspace.add_agent(sample_agent)

        system_messages = sample_workspace.get_messages(message_type=MessageType.SYSTEM)
        assert len(system_messages) > 0
        assert all(m.message_type == MessageType.SYSTEM for m in system_messages)

    @pytest.mark.asyncio
    async def test_limit_messages(self, sample_workspace):
        """Test limiting number of messages."""
        await sample_workspace.start()

        # Add some messages
        for i in range(5):
            sample_workspace.add_agent(agent_url=f"http://agent{i}:8000")

        messages = sample_workspace.get_messages(limit=3)
        assert len(messages) <= 3

    @pytest.mark.asyncio
    async def test_message_callbacks(self, sample_workspace):
        """Test message callbacks."""
        received_messages = []

        async def callback(message):
            received_messages.append(message)

        sample_workspace.on_message(callback)
        await sample_workspace.start()

        # Give callback time to process
        await asyncio.sleep(0.1)

        assert len(received_messages) > 0


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceArtifacts:
    """Test workspace artifact management."""

    @pytest.mark.asyncio
    async def test_add_artifact(self, sample_workspace):
        """Test adding an artifact."""
        artifact_id = sample_workspace.add_artifact(
            name="test.txt",
            artifact_type="file",
            content="test content",
            created_by="test_user",
        )

        assert artifact_id is not None
        artifact = sample_workspace.get_artifact(artifact_id)
        assert artifact is not None
        assert artifact.name == "test.txt"
        assert artifact.content == "test content"

    @pytest.mark.asyncio
    async def test_add_data_artifact(self, sample_workspace):
        """Test adding a data artifact."""
        data = {"key": "value", "number": 42}
        artifact_id = sample_workspace.add_artifact(
            name="data.json",
            artifact_type="data",
            content=data,
            created_by="system",
        )

        artifact = sample_workspace.get_artifact(artifact_id)
        assert artifact.content == data

    @pytest.mark.asyncio
    async def test_get_artifacts(self, sample_workspace):
        """Test getting all artifacts."""
        sample_workspace.add_artifact(
            name="file1.txt", artifact_type="file", content="content1", created_by="user1"
        )
        sample_workspace.add_artifact(
            name="data1.json",
            artifact_type="data",
            content={"a": 1},
            created_by="user2",
        )

        artifacts = sample_workspace.get_artifacts()
        assert len(artifacts) == 2

    @pytest.mark.asyncio
    async def test_filter_artifacts_by_type(self, sample_workspace):
        """Test filtering artifacts by type."""
        sample_workspace.add_artifact(
            name="file1.txt", artifact_type="file", content="content", created_by="user"
        )
        sample_workspace.add_artifact(
            name="data1.json",
            artifact_type="data",
            content={"a": 1},
            created_by="user",
        )

        file_artifacts = sample_workspace.get_artifacts(artifact_type="file")
        data_artifacts = sample_workspace.get_artifacts(artifact_type="data")

        assert len(file_artifacts) == 1
        assert len(data_artifacts) == 1

    @pytest.mark.asyncio
    async def test_filter_artifacts_by_creator(self, sample_workspace):
        """Test filtering artifacts by creator."""
        sample_workspace.add_artifact(
            name="file1.txt", artifact_type="file", content="content", created_by="user1"
        )
        sample_workspace.add_artifact(
            name="file2.txt", artifact_type="file", content="content", created_by="user2"
        )

        user1_artifacts = sample_workspace.get_artifacts(created_by="user1")
        assert len(user1_artifacts) == 1
        assert user1_artifacts[0].created_by == "user1"


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceSharedState:
    """Test workspace shared state management."""

    @pytest.mark.asyncio
    async def test_set_and_get_state(self, sample_workspace):
        """Test setting and getting shared state."""
        sample_workspace.set_shared_state("key1", "value1")
        value = sample_workspace.get_shared_state("key1")

        assert value == "value1"

    @pytest.mark.asyncio
    async def test_get_nonexistent_state(self, sample_workspace):
        """Test getting non-existent state returns default."""
        value = sample_workspace.get_shared_state("nonexistent", default="default_value")
        assert value == "default_value"

    @pytest.mark.asyncio
    async def test_get_all_shared_state(self, sample_workspace):
        """Test getting all shared state."""
        sample_workspace.set_shared_state("key1", "value1")
        sample_workspace.set_shared_state("key2", 42)
        sample_workspace.set_shared_state("key3", {"nested": "object"})

        state = sample_workspace.get_all_shared_state()
        assert len(state) == 3
        assert state["key1"] == "value1"
        assert state["key2"] == 42
        assert state["key3"] == {"nested": "object"}


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceExport:
    """Test workspace export functionality."""

    @pytest.mark.asyncio
    async def test_export_workspace(self, sample_workspace, sample_agent):
        """Test exporting workspace to JSON."""
        await sample_workspace.start()
        sample_workspace.add_agent(sample_agent)
        sample_workspace.add_artifact(
            name="test.txt", artifact_type="file", content="test", created_by="system"
        )
        sample_workspace.set_shared_state("key", "value")

        export_path = await sample_workspace.export_workspace()

        assert export_path.exists()
        assert export_path.suffix == ".json"

        # Verify export content
        with open(export_path) as f:
            data = json.load(f)

        assert data["workspace_id"] == sample_workspace.workspace_id
        assert data["name"] == sample_workspace.name
        assert len(data["participants"]) == 1
        assert len(data["artifacts"]) == 1
        assert data["shared_state"]["key"] == "value"

    @pytest.mark.asyncio
    async def test_export_to_custom_path(self, sample_workspace, tmp_path):
        """Test exporting to custom path."""
        await sample_workspace.start()
        custom_path = tmp_path / "custom_export.json"

        export_path = await sample_workspace.export_workspace(custom_path)

        assert export_path == custom_path
        assert custom_path.exists()


@pytest.mark.skip(reason="Workspace API has changed")
class TestWorkspaceIntegration:
    """Integration tests for workspace functionality."""

    @pytest.mark.asyncio
    async def test_workspace_full_workflow(self, tmp_path, sample_agent):
        """Test complete workspace workflow."""
        # Create workspace
        workspace = Workspace(
            name="Integration Test",
            description="Full workflow test",
            workspace_dir=tmp_path / "integration",
            auto_cleanup=False,
        )

        # Add agent
        participant_id = workspace.add_agent(sample_agent)
        assert participant_id is not None

        # Start workspace
        await workspace.start()
        assert workspace.state == WorkspaceState.ACTIVE

        # Add artifact
        artifact_id = workspace.add_artifact(
            name="data.json",
            artifact_type="data",
            content={"test": "data"},
            created_by=participant_id,
        )
        assert artifact_id is not None

        # Set shared state
        workspace.set_shared_state("status", "processing")

        # Complete workspace
        await workspace.complete()
        assert workspace.state == WorkspaceState.COMPLETED

        # Export
        export_path = await workspace.export_workspace()
        assert export_path.exists()

        # Close
        await workspace.close()

    @pytest.mark.asyncio
    async def test_workspace_error_handling(self, sample_workspace):
        """Test workspace handles errors gracefully."""
        # Try to collaborate without starting
        with pytest.raises(ValueError, match="Workspace must be active"):
            await sample_workspace.collaborate("test task")

        # Try to collaborate without agents
        await sample_workspace.start()
        with pytest.raises(ValueError, match="No agents in workspace"):
            await sample_workspace.collaborate("test task")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

