# Synqed

A Python SDK for building multi-agent systems with workspace-based orchestration.

## Installation

```bash
pip install synqed
```

## Quick Start

```python
import synqed
from synqed import PlannerLLM, WorkspaceExecutionEngine, WorkspaceManager

# Initialize the planner
planner = PlannerLLM(
    provider="anthropic",
    api_key="your-api-key",
)

# Plan a task and create agents
task_plan, agent_specs = await planner.plan_task_and_create_agent_specs(
    user_task="Your task description",
    agent_provider="anthropic",
    agent_api_key="your-api-key",
)

# Create agents from specs
agents = synqed.create_agents_from_specs(agent_specs)

# Register agents
for agent in agents:
    synqed.AgentRuntimeRegistry.register(agent.name, agent)

# Create workspace manager and execution engine
workspace_manager = synqed.WorkspaceManager()
execution_engine = synqed.WorkspaceExecutionEngine(
    planner=planner,
    workspace_manager=workspace_manager,
)

# Create and run workspaces
root_workspace = await workspace_manager.create_workspace(
    task_tree_node=task_plan.root,
    parent_workspace_id=None,
)

await execution_engine.run_workspace(root_workspace.workspace_id)
```

## Features

- **PlannerLLM**: Task decomposition and agent specification generation
- **WorkspaceManager**: Hierarchical workspace creation and management
- **WorkspaceExecutionEngine**: Multi-agent execution with message routing
- **PlannerAgent**: CEO-style coordinator for root workspaces
- **Agent**: Flexible agent creation with custom logic functions
- **MCP Integration**: Optional Model Context Protocol support

## Development

### Install for Development

```bash
make install
```

### Run Tests

```bash
make test           # core tests only
make test-examples  # example tests
make test-all       # all tests with coverage
```

### Lint & Format

```bash
make lint    # run linters
make format  # format code
```

## Publishing to PyPI

### Prerequisites

```bash
pip install build twine
```

Create a `.env` file with your PyPI tokens:

```bash
TWINE_PASSWORD=pypi-your-production-token
TWINE_TEST_PASSWORD=pypi-your-test-token  # optional
```

### Publish

```bash
# publish to production pypi (recommended)
./scripts/publish.sh --prod

# or publish to test pypi first
./scripts/publish.sh --test
```

The `publish.sh` script automatically:
- Increments the patch version (e.g., 1.1.91 → 1.1.92)
- Updates `pyproject.toml` and `src/synqed/__init__.py`
- Updates `python-backend/requirements.txt` to use the new version
- Cleans, builds, and uploads the package
- Prompts for confirmation before production publish

After publishing, commit the version bump:

```bash
git add -A && git commit -m "Release synqed v$(grep 'version = ' pyproject.toml | cut -d'"' -f2)"
git push origin main
```

## License

MIT

