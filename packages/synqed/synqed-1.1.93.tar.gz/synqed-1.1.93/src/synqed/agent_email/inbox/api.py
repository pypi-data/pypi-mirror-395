"""
production-grade a2a inbox fastapi endpoint.

provides enterprise-ready inbox contract with:
- cryptographic signature verification (ed25519)
- rate limiting per sender and IP
- guaranteed delivery via redis streams queue
- async processing with automatic retry
- distributed tracing with trace_id propagation
- dead letter queue for failed messages

architecture:
1. POST /v1/a2a/inbox: validates, signs, queues message (returns immediately)
2. worker processes queue asynchronously:
   - tries local runtime (LocalAgentRuntime protocol)
   - falls back to remote inbox_url forwarding
   - retries with exponential backoff
   - moves to DLQ after max retries

agents can implement LocalAgentRuntime protocol for local processing,
or rely on remote HTTP forwarding to their registered inbox_url.
"""

import uuid
from typing import Any, Dict, Literal, Optional, Protocol
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from synqed.agent_email.addressing import AgentId
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.inbox.crypto import verify_signature, SignatureVerificationError
from synqed.agent_email.inbox.rate_limiter import get_rate_limiter
from synqed.agent_email.inbox.queue import get_message_queue


class A2AInboxRequest(BaseModel):
    """
    request for sending an a2a envelope to an agent's inbox.
    
    fields:
        sender: canonical agent uri of sender (e.g., agent://futurehouse/cosmos)
        recipient: canonical agent uri of recipient (e.g., agent://google/gemini)
        message: raw a2a envelope as dict (must contain thread_id, role, content)
        signature: ed25519 signature over sender+recipient+message+thread_id
        token: optional bearer-like auth token (placeholder for future auth)
        trace_id: optional distributed trace id (auto-generated if not provided)
        parent_trace_id: optional parent trace id for nested operations
    """
    
    sender: str
    recipient: str
    message: Dict[str, Any]
    signature: str
    token: Optional[str] = None
    trace_id: Optional[str] = None
    parent_trace_id: Optional[str] = None
    
    def model_post_init(self, __context: Any) -> None:
        """validate message structure after init."""
        # ensure message contains required fields
        required_fields = {"thread_id", "role", "content"}
        missing = required_fields - set(self.message.keys())
        if missing:
            raise ValueError(f"message missing required fields: {missing}")


class A2AInboxResponse(BaseModel):
    """
    response from inbox endpoint.
    
    fields:
        status: "accepted", "rejected", or "error"
        message_id: unique id assigned to this message (if accepted)
        remote_message_id: optional remote message id (if forwarded)
        trace_id: distributed trace id for this message
        error: error description (if status is "rejected" or "error")
        retryable: whether the error is retryable (if status is "error")
        response_envelope: optional a2a response envelope from the agent
    """
    
    status: Literal["accepted", "rejected", "error"]
    message_id: Optional[str] = None
    remote_message_id: Optional[str] = None
    trace_id: Optional[str] = None
    error: Optional[str] = None
    retryable: Optional[bool] = None
    response_envelope: Optional[Dict[str, Any]] = None


class LocalAgentRuntime(Protocol):
    """
    protocol for local agent implementations.
    
    agents must implement handle_a2a_envelope to process incoming messages.
    """
    
    async def handle_a2a_envelope(
        self,
        sender: str,
        recipient: str,
        envelope: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        """
        handle an incoming a2a envelope.
        
        args:
            sender: canonical uri of sender
            recipient: canonical uri of recipient
            envelope: the a2a message envelope
            
        returns:
            optional response envelope (or None if no response)
        """
        ...


# global runtime registry: agent_id -> runtime instance
# in a real system, this would be a proper dependency injection container
_agent_runtimes: Dict[str, LocalAgentRuntime] = {}


def register_agent_runtime(agent_id: str, runtime: LocalAgentRuntime) -> None:
    """
    register a local agent runtime.
    
    this associates an agent_id with a runtime implementation
    so the inbox endpoint can route messages to it.
    
    args:
        agent_id: canonical agent uri
        runtime: the runtime instance
    """
    _agent_runtimes[agent_id] = runtime


def get_agent_runtime(agent_id: str) -> LocalAgentRuntime | None:
    """
    get the runtime for an agent.
    
    args:
        agent_id: canonical agent uri
        
    returns:
        runtime instance or None if not found
    """
    return _agent_runtimes.get(agent_id)


def clear_agent_runtimes() -> None:
    """clear all registered runtimes (useful for testing)."""
    _agent_runtimes.clear()


async def validate_auth(token: Optional[str]) -> bool:
    """
    validate auth token.
    
    placeholder for future authentication.
    currently accepts all requests.
    
    args:
        token: optional bearer token
        
    returns:
        True if auth is valid
    """
    # todo: implement real authentication
    # for now, accept all requests
    return True


# create router
router = APIRouter(prefix="/v1/a2a", tags=["inbox"])


@router.post(
    "/inbox",
    response_model=A2AInboxResponse,
    summary="Receive A2A envelope",
)
async def receive_a2a_envelope(
    envelope: A2AInboxRequest,
    request: Request,
) -> A2AInboxResponse:
    """
    receive and queue an a2a envelope for async processing.
    
    production-grade inbox with:
    - cryptographic signature verification
    - rate limiting per sender and IP
    - guaranteed delivery via redis streams queue
    - distributed tracing with trace_id propagation
    - strict input validation
    
    this endpoint validates and queues messages immediately.
    actual delivery (local runtime or remote forwarding) happens async via workers.
    
    returns:
        - 200 with status="accepted" if queued successfully
        - 200 with status="rejected" if validation fails
        - 200 with status="error" if internal error occurs
        - 429 if rate limit exceeded
        - 400 if invalid input
        - 404 if recipient not found
    """
    # generate or use provided trace_id
    trace_id = envelope.trace_id or str(uuid.uuid4())
    
    # generate message id
    message_id = str(uuid.uuid4())
    
    try:
        # 1. validate auth
        if not await validate_auth(envelope.token):
            return A2AInboxResponse(
                status="rejected",
                message_id=message_id,
                trace_id=trace_id,
                error="authentication failed",
                retryable=False,
            )
        
        # 2. check rate limits
        client_ip = request.client.host if request.client else "unknown"
        rate_limiter = get_rate_limiter()
        
        is_allowed, rate_error = rate_limiter.check_and_record(
            sender=envelope.sender,
            ip_address=client_ip,
        )
        
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=rate_error,
            )
        
        # 3. validate sender uri
        try:
            AgentId.from_uri(envelope.sender)
        except ValueError as e:
            return A2AInboxResponse(
                status="rejected",
                message_id=message_id,
                trace_id=trace_id,
                error=f"invalid sender uri: {e}",
                retryable=False,
            )
        
        # 4. validate recipient uri
        try:
            AgentId.from_uri(envelope.recipient)
        except ValueError as e:
            return A2AInboxResponse(
                status="rejected",
                message_id=message_id,
                trace_id=trace_id,
                error=f"invalid recipient uri: {e}",
                retryable=False,
            )
        
        # 5. verify recipient exists in registry
        registry = get_registry()
        try:
            recipient_entry = registry.get_by_uri(envelope.recipient)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"recipient not found in registry: {envelope.recipient}",
            )
        
        # 6. lookup sender in registry for public key
        try:
            sender_entry = registry.get_by_uri(envelope.sender)
        except KeyError:
            return A2AInboxResponse(
                status="rejected",
                message_id=message_id,
                trace_id=trace_id,
                error=f"sender not found in registry: {envelope.sender}",
                retryable=False,
            )
        
        # 7. verify signature
        try:
            thread_id = envelope.message.get("thread_id", "")
            is_valid = verify_signature(
                public_key_b64=sender_entry.public_key,
                signature_b64=envelope.signature,
                sender=envelope.sender,
                recipient=envelope.recipient,
                message=envelope.message,
                thread_id=thread_id,
            )
            
            if not is_valid:
                return A2AInboxResponse(
                    status="rejected",
                    message_id=message_id,
                    trace_id=trace_id,
                    error="signature verification failed",
                    retryable=False,
                )
        
        except SignatureVerificationError as e:
            return A2AInboxResponse(
                status="error",
                message_id=message_id,
                trace_id=trace_id,
                error=f"signature verification error: {e}",
                retryable=False,
            )
        
        # 8. queue message for async processing
        queue = get_message_queue()
        
        # prepare envelope for queue
        envelope_dict = {
            "sender": envelope.sender,
            "recipient": envelope.recipient,
            "message": envelope.message,
            "signature": envelope.signature,
            "token": envelope.token,
            "trace_id": trace_id,
            "parent_trace_id": envelope.parent_trace_id,
            "message_id": message_id,
        }
        
        await queue.push(
            agent_id=envelope.recipient,
            envelope=envelope_dict,
            message_id=message_id,
        )
        
        # 9. return accepted response immediately
        return A2AInboxResponse(
            status="accepted",
            message_id=message_id,
            trace_id=trace_id,
        )
    
    except HTTPException:
        # re-raise http exceptions
        raise
    
    except Exception as e:
        # internal error
        import traceback
        error_detail = f"internal error: {str(e)}\n{traceback.format_exc()}"
        
        return A2AInboxResponse(
            status="error",
            message_id=message_id,
            trace_id=trace_id,
            error=error_detail,
            retryable=True,
        )

