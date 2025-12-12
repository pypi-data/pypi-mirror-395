"""
production-grade a2a inbox system.

provides enterprise messaging infrastructure with:
- cryptographic identity (ed25519 signatures)
- guaranteed delivery (redis streams queue)
- rate limiting and abuse protection
- distributed tracing
- automatic retry with exponential backoff
- dead letter queue for failed messages
"""

from synqed.agent_email.inbox.api import (
    A2AInboxRequest,
    A2AInboxResponse,
    LocalAgentRuntime,
    register_agent_runtime,
    get_agent_runtime,
    clear_agent_runtimes,
    router,
)
from synqed.agent_email.inbox.crypto import (
    verify_signature,
    sign_message,
    generate_keypair,
    SignatureVerificationError,
)
from synqed.agent_email.inbox.queue import (
    MessageQueue,
    get_message_queue,
    initialize_queue,
    shutdown_queue,
    QueueError,
)
from synqed.agent_email.inbox.rate_limiter import (
    RateLimiter,
    get_rate_limiter,
)
from synqed.agent_email.inbox.worker import (
    MessageWorker,
    get_message_worker,
    start_workers_for_all_agents,
    shutdown_workers,
)

__all__ = [
    # api
    "A2AInboxRequest",
    "A2AInboxResponse",
    "LocalAgentRuntime",
    "register_agent_runtime",
    "get_agent_runtime",
    "clear_agent_runtimes",
    "router",
    # crypto
    "verify_signature",
    "sign_message",
    "generate_keypair",
    "SignatureVerificationError",
    # queue
    "MessageQueue",
    "get_message_queue",
    "initialize_queue",
    "shutdown_queue",
    "QueueError",
    # rate limiting
    "RateLimiter",
    "get_rate_limiter",
    # worker
    "MessageWorker",
    "get_message_worker",
    "start_workers_for_all_agents",
    "shutdown_workers",
]
