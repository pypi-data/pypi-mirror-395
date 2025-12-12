"""
Unit tests for the TaskDelegator class.

NOTE: TaskDelegator has been refactored/removed.
This test file is kept for backwards compatibility but skipped.
Use WorkspaceManager and AgentRuntimeRegistry instead.
"""

import pytest


@pytest.mark.skip(reason="TaskDelegator has been refactored - use WorkspaceManager + AgentRuntimeRegistry")
class TestTaskDelegator:
    """Tests for the TaskDelegator class (deprecated)."""
    
    def test_delegator_deprecated(self):
        """TaskDelegator functionality moved to WorkspaceManager."""
        pytest.skip("TaskDelegator has been refactored")
