"""
Pytest configuration and shared fixtures.
"""

import asyncio
import pytest
from typing import Any, Callable, Coroutine

from synqed import Agent, AgentServer
from synqed.agent import AgentLogicContext


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def simple_agent_executor() -> Callable[[AgentLogicContext], Coroutine[Any, Any, str]]:
    """Create a simple agent executor for testing."""
    async def executor(context: AgentLogicContext) -> str:
        msg = context.latest_message
        if msg:
            return f"Echo: {msg.content}"
        return "Echo: No message"
    
    return executor


@pytest.fixture
def recipe_agent_executor() -> Callable[[AgentLogicContext], Coroutine[Any, Any, str]]:
    """Create a recipe agent executor for testing."""
    async def executor(context: AgentLogicContext) -> str:
        msg = context.latest_message
        content = msg.content if msg else "unknown"
        return f"Recipe Agent: Here's a recipe for {content}"
    
    return executor


@pytest.fixture
def weather_agent_executor() -> Callable[[AgentLogicContext], Coroutine[Any, Any, str]]:
    """Create a weather agent executor for testing."""
    async def executor(context: AgentLogicContext) -> str:
        msg = context.latest_message
        content = msg.content if msg else "unknown"
        return f"Weather Agent: The weather for {content} is sunny"
    
    return executor


@pytest.fixture
def simple_agent(simple_agent_executor):
    """Create a simple test agent."""
    return Agent(
        name="Test Agent",
        description="A simple test agent",
        capabilities=["echo", "test"],
        logic=simple_agent_executor
    )


@pytest.fixture
def recipe_agent(recipe_agent_executor):
    """Create a recipe agent for testing."""
    return Agent(
        name="Recipe Agent",
        description="Provides recipes",
        capabilities=["cooking", "recipes"],
        logic=recipe_agent_executor
    )


@pytest.fixture
def weather_agent(weather_agent_executor):
    """Create a weather agent for testing."""
    return Agent(
        name="Weather Agent",
        description="Provides weather information",
        capabilities=["weather", "forecast"],
        logic=weather_agent_executor
    )


@pytest.fixture
async def simple_server(simple_agent):
    """Create and start a simple test server."""
    server = AgentServer(simple_agent, host="127.0.0.1", port=8101)
    await server.start_background()
    
    # Wait for server to be ready
    await asyncio.sleep(1)
    
    yield server
    
    # Cleanup
    await server.stop()
    # Wait for port to be released
    await asyncio.sleep(0.5)


@pytest.fixture
async def recipe_server(recipe_agent):
    """Create and start a recipe agent server."""
    server = AgentServer(recipe_agent, host="127.0.0.1", port=8102)
    await server.start_background()
    await asyncio.sleep(1)
    yield server
    await server.stop()
    await asyncio.sleep(0.5)


@pytest.fixture
async def weather_server(weather_agent):
    """Create and start a weather agent server."""
    server = AgentServer(weather_agent, host="127.0.0.1", port=8103)
    await server.start_background()
    await asyncio.sleep(1)
    yield server
    await server.stop()
    await asyncio.sleep(0.5)


@pytest.fixture
def port_generator():
    """Generate unique ports for testing."""
    port = 9000
    
    def get_port():
        nonlocal port
        port += 1
        return port
    
    return get_port

