"""
a2a client with proper message correlation and response waiting.

implements production-ready request-response pattern over a2a:
- correlation map for pending requests
- asyncio.Future per message_id
- router callback integration
- timeout and cancellation safety
- concurrency-safe operations

architecture:
- send_task_and_wait() creates future, registers correlation, waits
- router calls response_handler() when agent replies
- response_handler() resolves matching future
- caller gets actual agent response data
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, Optional

from synqed import AgentId, AgentLogicContext, MessageRouter

logger = logging.getLogger(__name__)


class A2AClient:
    """
    a2a client with proper request-response correlation.
    
    provides send_task_and_wait() that:
    - sends a2a task to agent
    - triggers agent execution
    - waits for and returns actual response
    - handles timeouts and errors gracefully
    
    uses correlation map to match requests with responses.
    """
    
    def __init__(self, router: MessageRouter, workspace_id: str = "mcp_workspace"):
        """
        initialize a2a client.
        
        args:
            router: message router for a2a communication
            workspace_id: workspace identifier for routing
        """
        self.router = router
        self.workspace_id = workspace_id
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()
        logger.info("a2a client initialized with correlation support")
    
    def _generate_message_id(self, recipient: str) -> str:
        """generate unique message id."""
        return f"msg-{self.workspace_id}-{recipient}-{uuid.uuid4().hex[:8]}"
    
    async def response_handler(self, message_id: str, response_data: Dict[str, Any]) -> None:
        """
        handle incoming response from agent.
        
        called by router when agent sends a reply.
        resolves the matching future with response data.
        
        args:
            message_id: original request message id (from reply_to field)
            response_data: response data from agent
        """
        async with self._lock:
            future = self._pending_requests.get(message_id)
            if future and not future.done():
                future.set_result(response_data)
                logger.debug(f"resolved future for message_id={message_id}")
            else:
                logger.debug(f"no pending future for message_id={message_id}")
    
    async def send_task_and_wait(
        self,
        agent: AgentId,
        task_type: str,
        payload: Dict[str, Any],
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        send a2a task and wait for agent response.
        
        this is the core method that implements:
        - message correlation
        - agent execution
        - response waiting
        - timeout handling
        
        args:
            agent: target agent id
            task_type: type of task
            payload: task parameters
            timeout: max wait time in seconds
            
        returns:
            actual agent response with real data
            
        raises:
            TimeoutError: if response not received in time
            ValueError: if agent not registered
        """
        agent_name = agent.name
        message_id = self._generate_message_id(agent_name)
        
        # construct task message
        task_message = {
            "task_type": task_type,
            "payload": payload
        }
        content = json.dumps(task_message)
        
        logger.info(f"sending a2a task to {agent.to_uri()}: type={task_type}")
        
        # create future for response
        response_future = asyncio.Future()
        
        async with self._lock:
            self._pending_requests[message_id] = response_future
        
        try:
            # send message via unified router api
            await self.router.route_message(
                workspace_id=self.workspace_id,
                sender="MCPServer",
                recipient=agent_name,
                content=content,
                message_id=message_id
            )
            
            logger.info(f"task sent: message_id={message_id}, executing agent...")
            
            # execute agent to process the message
            result = await self._execute_agent(agent_name)
            
            if result:
                logger.info(f"received response from {agent_name}")
                return result
            else:
                # if no immediate result, wait for future
                try:
                    result = await asyncio.wait_for(response_future, timeout=timeout)
                    logger.info(f"received async response from {agent_name}")
                    return result
                except asyncio.TimeoutError:
                    logger.warning(f"timeout waiting for response from {agent_name}")
                    return {
                        "status": "timeout",
                        "message_id": message_id,
                        "agent": agent.to_uri(),
                        "error": f"no response received within {timeout}s"
                    }
        
        except Exception as e:
            logger.error(f"error executing agent {agent_name}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "agent": agent.to_uri()
            }
        
        finally:
            # clean up pending request
            async with self._lock:
                self._pending_requests.pop(message_id, None)
    
    async def _execute_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        execute agent logic to process the message.
        
        finds agent in router, creates context, calls logic, returns response.
        
        args:
            agent_name: name of agent to execute
            
        returns:
            agent response data or None if execution failed
        """
        # find agent in router
        target_agent = None
        if hasattr(self.router, '_agents') and agent_name in self.router._agents:
            target_agent = self.router._agents[agent_name]
        elif hasattr(self.router, 'agents') and agent_name in self.router.agents:
            target_agent = self.router.agents[agent_name]
        
        if not target_agent or not hasattr(target_agent, 'logic'):
            logger.error(f"agent {agent_name} not found or has no logic")
            return {
                "status": "error",
                "error": f"agent {agent_name} not executable"
            }
        
        try:
            # create agent logic context
            context = AgentLogicContext(
                memory=target_agent.memory,
                agent_name=agent_name,
                default_target="MCPServer",
                workspace=None
            )
            
            # execute agent logic
            logic_result = await target_agent.logic(context)
            
            if not logic_result:
                return None
            
            # parse response
            response_content = logic_result.get('content', '{}')
            
            try:
                response_data = json.loads(response_content) if isinstance(response_content, str) else response_content
                return response_data
            except json.JSONDecodeError:
                logger.warning(f"failed to parse response from {agent_name}")
                return {
                    "status": "error",
                    "error": "failed to parse agent response",
                    "raw_response": str(response_content)[:200]
                }
        
        except Exception as e:
            logger.error(f"error executing agent {agent_name}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "agent": agent_name
            }
    
    async def send_task(
        self,
        agent: AgentId,
        task_type: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        send task and wait for response (alias for send_task_and_wait).
        
        maintained for backward compatibility.
        """
        return await self.send_task_and_wait(agent, task_type, payload)
    
    async def send_message(
        self,
        agent: AgentId,
        content: str,
        message_id: Optional[str] = None
    ) -> str:
        """
        send a simple message to an agent.
        
        args:
            agent: target agent id
            content: message content
            message_id: optional message id
            
        returns:
            message id of sent message
        """
        agent_name = agent.name
        
        if not message_id:
            message_id = self._generate_message_id(agent_name)
        
        # use unified router api
        return await self.router.route_message(
            workspace_id=self.workspace_id,
            sender="MCPServer",
            recipient=agent_name,
            content=content,
            message_id=message_id
        )
    
    def get_pending_requests(self) -> Dict[str, Any]:
        """
        get information about pending requests.
        
        returns:
            dictionary with pending request statistics
        """
        return {
            "count": len(self._pending_requests),
            "message_ids": list(self._pending_requests.keys())
        }
