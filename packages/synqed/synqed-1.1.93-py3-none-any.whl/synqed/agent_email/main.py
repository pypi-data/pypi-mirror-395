"""
main fastapi application for agent email layer.

provides unified http api for:
- agent registry (discovery)
- a2a inbox (message routing)

run with: uvicorn synqed.agent_email.main:app --reload
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from synqed.agent_email.registry.api import router as registry_router, get_registry
from synqed.agent_email.inbox.api import router as inbox_router
from synqed.agent_email.registration import router as registration_router


# create fastapi app
app = FastAPI(
    title="Agent Email Layer",
    description="Global agent addressing, discovery, and inbox API for A2A protocol",
    version="1.0.0",
)

# enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount routers
app.include_router(registry_router)
app.include_router(inbox_router)
app.include_router(registration_router)


@app.get("/")
async def root() -> dict:
    """
    root endpoint with api information.
    
    returns basic info about available endpoints.
    """
    return {
        "service": "Agent Email Layer",
        "version": "2.0.0",
        "endpoints": {
            "registration": {
                "POST /v1/a2a/register": "Register a new agent (anyone can register!)",
                "GET /v1/a2a/agents": "List all registered agents",
                "GET /v1/a2a/agents/{email}": "Lookup agent by email address",
            },
            "registry": {
                "POST /v1/agents": "Register an agent (legacy)",
                "GET /v1/agents": "List all agents (legacy)",
                "GET /v1/agents/by-uri/{uri}": "Lookup by canonical URI",
                "GET /v1/agents/by-email/{email}": "Lookup by email-like address",
            },
            "inbox": {
                "POST /v1/a2a/inbox": "Send cryptographically signed messages",
            },
        },
        "features": {
            "public_registration": "Anyone can create agents and get email addresses",
            "cryptographic_identity": "Ed25519 signatures required for all messages",
            "guaranteed_delivery": "Redis Streams queue with automatic retry",
            "rate_limiting": "100/min per sender, 500/min per IP",
            "distributed_tracing": "trace_id propagation for all messages",
        },
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict:
    """health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event() -> None:
    """initialize database on startup if using postgres."""
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        print("🔄 initializing postgres database...")
        registry = get_registry()
        
        # postgres registry has init_db method
        if hasattr(registry, 'init_db'):
            await registry.init_db()
            print("✅ database tables created")
    else:
        print("ℹ️  using in-memory registry (no DATABASE_URL set)")


if __name__ == "__main__":
    import uvicorn
    
    # run with uvicorn
    uvicorn.run(
        "synqed.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

