"""
Initialize agents with Ed25519 keypairs.
"""
import asyncio
import json
from synqed.agent_email.registry.api import get_registry
from synqed.agent_email.registry.models import AgentRegistryEntry
from synqed.agent_email.inbox import generate_keypair

async def main():
    """Initialize demo agents."""
    print("Initializing agents with keypairs...")
    
    registry = get_registry()
    keypairs = {}
    
    # Define demo agents
    agents = [
        {
            "agent_id": "agent://demo/alice",
            "email_like": "alice@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0", "chat"],
            "metadata": {"description": "Demo agent Alice"},
        },
        {
            "agent_id": "agent://demo/bob",
            "email_like": "bob@demo",
            "inbox_url": "http://localhost:8000/v1/a2a/inbox",
            "capabilities": ["a2a/1.0", "chat"],
            "metadata": {"description": "Demo agent Bob"},
        },
    ]
    
    # Generate keypairs and register
    for agent in agents:
        private_key, public_key = generate_keypair()
        
        registry.register(AgentRegistryEntry(
            agent_id=agent["agent_id"],
            email_like=agent["email_like"],
            inbox_url=agent["inbox_url"],
            public_key=public_key,
            capabilities=agent.get("capabilities", []),
            metadata=agent.get("metadata", {}),
        ))
        
        keypairs[agent["agent_id"]] = {
            "private_key": private_key,
            "public_key": public_key,
        }
        
        print(f"✓ Registered: {agent['agent_id']}")
    
    # Save keypairs
    with open("keypairs.json", "w") as f:
        json.dump(keypairs, f, indent=2)
    
    print(f"\n✓ Registered {len(agents)} agents")
    print("⚠️  Keypairs saved to keypairs.json - store securely in production!")

if __name__ == "__main__":
    asyncio.run(main())
