"""
Integration tests for Synqed components working together.
"""

import pytest
import asyncio
from synqed import Agent, AgentServer
from synqed.client import Client


@pytest.mark.skip(reason="Integration tests require full API implementation")
class TestIntegration:
    """Integration tests for component interactions."""
    
    @pytest.mark.asyncio
    async def test_agent_server_client_flow(self, port_generator):
        """Test complete flow: create agent, start server, connect client."""
        # Create agent
        async def executor(context):
            message = context.get_user_input()
            return f"Processed: {message}"
        
        agent = Agent(
            name="Integration Test Agent",
            description="Test agent",
            capabilities=["test"],
            logic=executor
        )
        
        # Start server
        port = port_generator()
        server = AgentServer(agent, host="127.0.0.1", port=port)
        await server.start_background()
        await asyncio.sleep(1)
        
        try:
            # Connect client
            async with Client(agent_url=server.url) as client:
                response = await client.ask("Hello integration test")
                
                assert "Processed" in response
                assert "Hello integration test" in response
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_multi_agent_delegation_flow(self, port_generator):
        """Test multi-agent delegation flow."""
        # Create multiple agents
        async def agent1_executor(context):
            return f"Agent 1: {context.get_user_input()}"
        
        async def agent2_executor(context):
            return f"Agent 2: {context.get_user_input()}"
        
        agent1 = Agent(
            name="Agent One",
            description="First agent",
            capabilities=["skill1"],
            logic=agent1_executor
        )
        
        agent2 = Agent(
            name="Agent Two",
            description="Second agent",
            capabilities=["skill2"],
            logic=agent2_executor
        )
        
        # Start servers
        port1 = port_generator()
        port2 = port_generator()
        
        server1 = AgentServer(agent1, host="127.0.0.1", port=port1)
        server2 = AgentServer(agent2, host="127.0.0.1", port=port2)
        
        await server1.start_background()
        await server2.start_background()
        await asyncio.sleep(1)
        
        try:
            # Create delegator
            delegator = TaskDelegator()
            delegator.register_agent(agent=agent1)
            delegator.register_agent(agent=agent2)
            
            # Submit tasks
            result1 = await delegator.submit_task(
                "Test task 1",
                preferred_agent="Agent One"
            )
            
            result2 = await delegator.submit_task(
                "Test task 2",
                preferred_agent="Agent Two"
            )
            
            assert "Agent 1" in result1
            assert "Agent 2" in result2
            
            # Test broadcasting
            results = await delegator.submit_task_to_multiple("Broadcast task")
            assert len(results) == 2
            
            await delegator.close_all()
        finally:
            await server1.stop()
            await server2.stop()
    
    @pytest.mark.asyncio
    async def test_agent_card_propagation(self, port_generator):
        """Test that agent card is properly propagated through server to client."""
        agent = Agent(
            name="Card Test Agent",
            description="Testing card propagation",
            capabilities=["skill1", "skill2"],
            version="2.0.0"
        )
        
        port = port_generator()
        server = AgentServer(agent, host="127.0.0.1", port=port)
        await server.start_background()
        await asyncio.sleep(1)
        
        try:
            # Get card from server
            server_card = server.get_card()
            
            assert server_card.name == "Card Test Agent"
            assert server_card.version == "2.0.0"
            assert len(server_card.skills) == 2
            
            # Verify URL was updated
            assert server_card.url == server.url
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, port_generator):
        """Test handling concurrent requests to the same agent."""
        async def slow_executor(context):
            await asyncio.sleep(0.1)  # Simulate slow processing
            message = context.get_user_input()
            return f"Processed: {message}"
        
        agent = Agent(
            name="Concurrent Test Agent",
            description="Test concurrent requests",
            capabilities=["test"],
            logic=slow_executor
        )
        
        port = port_generator()
        server = AgentServer(agent, host="127.0.0.1", port=port)
        await server.start_background()
        await asyncio.sleep(1)
        
        try:
            # Create multiple clients
            clients = [Client(agent_url=server.url) for _ in range(3)]
            
            # Send concurrent requests
            tasks = [
                client.ask(f"Message {i}")
                for i, client in enumerate(clients)
            ]
            
            results = await asyncio.gather(*tasks)
            
            # All requests should complete
            assert len(results) == 3
            
            for i, result in enumerate(results):
                assert f"Message {i}" in result
            
            # Close clients
            for client in clients:
                await client.close()
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_agent_skill_based_routing(self, port_generator):
        """Test that task delegator routes based on skills."""
        # Create specialized agents
        async def cooking_executor(context):
            return "Here's a recipe"
        
        async def weather_executor(context):
            return "It's sunny"
        
        cooking_agent = Agent(
            name="Chef",
            description="Cooking agent",
            capabilities=["cooking", "recipes"],
            logic=cooking_executor
        )
        
        weather_agent = Agent(
            name="Weather",
            description="Weather agent",
            capabilities=["weather", "forecast"],
            logic=weather_executor
        )
        
        # Start servers
        port1 = port_generator()
        port2 = port_generator()
        
        server1 = AgentServer(cooking_agent, host="127.0.0.1", port=port1)
        server2 = AgentServer(weather_agent, host="127.0.0.1", port=port2)
        
        await server1.start_background()
        await server2.start_background()
        await asyncio.sleep(1)
        
        try:
            delegator = TaskDelegator()
            delegator.register_agent(agent=cooking_agent)
            delegator.register_agent(agent=weather_agent)
            
            # Request with cooking skill
            result = await delegator.submit_task(
                "Make dinner",
                require_capabilities=["cooking"]
            )
            
            assert "recipe" in result.lower()
            
            # Request with weather skill
            result = await delegator.submit_task(
                "Check weather",
                require_capabilities=["weather"]
            )
            
            assert "sunny" in result.lower()
            
            await delegator.close_all()
        finally:
            await server1.stop()
            await server2.stop()

