"""
Cloud Email Simple Demo: Agents Communicating via Email Addresses Only

This demo shows the simplest way to have agents communicate via email:
1. Create agents with email addresses
2. Register them on cloud
3. Register their runtimes (enables auto-workspace creation)
4. Send ONE message - synqed handles everything else automatically!

The synqed API automatically:
- Creates workspaces in the background when agents communicate
- Routes messages through the workspace
- Calls agent logic functions to process messages
- Sends responses back via cloud

This is the SIMPLEST way to use synqed - no manual workspace creation!

Requirements:
- pip install synqed anthropic python-dotenv
- Set ANTHROPIC_API_KEY in .env file
"""

import asyncio
import os
from pathlib import Path
from anthropic import AsyncAnthropic
import synqed

# Load your own .env file
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass


async def main():
    """
    Demo: Agents communicate via email addresses with automatic workspace creation.
    """
    
    print("=" * 70)
    print("🌍 Synqed Agents - Email Communication (Simplified)")
    print("=" * 70)
    print()
    
    # Get API key
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("   Add to .env: ANTHROPIC_API_KEY=sk-ant-...")
        return
    
    anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    # Step 1: Create agents with logic functions
    print("STEP 1: Creating agents with email addresses...")
    print()
    
    # Alice - curious explorer
    async def alice_logic(context):
        """Alice's AI logic - curious explorer"""
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        history = context.get_conversation_history()
        system_prompt = (
            "You are Alice (alice@wonderland), a curious explorer. "
            "You're talking with Bob (bob@builder), a helpful construction worker. "
            "Respond naturally. Keep responses to 1-2 sentences. "
            "If the conversation feels complete, say goodbye politely."
        )
        
        conversation_text = f"Conversation:\n{history}\n\nRespond to Bob:"
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation_text}],
        )
        
        return context.send("bob", response.content[0].text.strip())
    
    alice = synqed.Agent(
        name="alice",
        description="A curious explorer who loves asking questions",
        logic=alice_logic,
        role="wonderland",  # Email: alice@wonderland
    )
    print(f"✓ Created {alice.email}")
    
    # Bob - builder
    async def bob_logic(context):
        """Bob's AI logic - helpful builder"""
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        history = context.get_conversation_history()
        system_prompt = (
            "You are Bob (bob@builder), a helpful construction worker. "
            "You're talking with Alice (alice@wonderland), a curious explorer. "
            "Respond helpfully. Keep responses to 1-2 sentences. "
            "If she says goodbye, say goodbye back."
        )
        
        conversation_text = f"Conversation:\n{history}\n\nRespond to Alice:"
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation_text}],
        )
        
        return context.send("alice", response.content[0].text.strip())
    
    bob = synqed.Agent(
        name="bob",
        description="A helpful construction worker who solves problems",
        logic=bob_logic,
        role="builder",  # Email: bob@builder
    )
    print(f"✓ Created {bob.email}")
    
    print()
    
    # Step 2: Register on cloud
    print("STEP 2: Registering agents on cloud...")
    print()
    
    for agent in [alice, bob]:
        try:
            await agent.register()
            print(f"✓ Registered {agent.email}")
        except Exception as e:
            if "409" in str(e):
                print(f"✓ {agent.email} (already registered)")
            else:
                print(f"❌ Registration failed for {agent.email}: {e}")
                return
    
    print()
    
    # Step 3: Register agent runtimes (enables automatic workspace creation)
    print("STEP 3: Registering agent runtimes...")
    print("        (This enables automatic workspace creation when agents communicate)")
    print()
    
    synqed.register_agent_runtime(alice.agent_id, alice)
    synqed.register_agent_runtime(bob.agent_id, bob)
    
    print(f"✓ Registered runtime for {alice.email}")
    print(f"✓ Registered runtime for {bob.email}")
    
    print()
    
    # Step 4: Send message via cloud - workspace is automatically created!
    print("STEP 4: Sending message via cloud...")
    print("        (Workspace will be automatically created in the background)")
    print()
    
    initial_message = "Hi Bob! I want to build something amazing. Can you help me?"
    print(f"💬 {alice.email} → {bob.email}")
    print(f"   \"{initial_message}\"")
    print()
    
    try:
        # Send message via cloud
        result = await alice.send(
            to=bob.email,
            content=initial_message,
            via_cloud=True,
        )
        
        print(f"✅ Message sent successfully!")
        print(f"   Message ID: {result.get('message_id', 'N/A')}")
        print()
        
        print("🔄 Simulating background processing:")
        print("   (In production, the inbox worker would process this automatically)")
        print()
        
        # Simulate what the worker would do: use auto-workspace routing
        
        
        auto_ws_manager = synqed.get_auto_workspace_manager()
        
        # Simulate the envelope that would be processed by the worker
        envelope = {
            "thread_id": f"conversation-{alice.name}",
            "role": "user",
            "content": initial_message,
        }
        
        print("   • Auto-workspace manager creating workspace...")
        response = await auto_ws_manager.route_message_via_workspace(
            sender=alice.agent_id,
            recipient=bob.agent_id,
            envelope=envelope,
        )
        
        if response:
            print(f"   • Bob processed the message!")
            print(f"   • Bob's response: \"{response.get('content', 'N/A')}\"")
        else:
            print("   • Bob processed the message (no immediate response)")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print()
    
    print("What just happened:")
    print("  1. Created 2 agents with email addresses")
    print("  2. Registered them on cloud with cryptographic keys")
    print("  3. Registered their runtimes (enables auto-workspace)")
    print("  4. Sent ONE message from alice to bob via cloud")
    print("  5. Synqed AUTOMATICALLY:")
    print("     • Created a workspace in the background")
    print("     • Routed the message through the workspace")
    print("     • Called bob's logic function")
    print("     • Will send bob's response back to alice")
    print()
    
    print("Key benefit:")
    print("  ✨ No manual workspace creation needed!")
    print("  ✨ Just send messages via email addresses")
    print("  ✨ Synqed handles orchestration automatically")
    print()
    
    print("This is the SIMPLEST way to use synqed:")
    print("  • Create agents with logic + email (name@role)")
    print("  • Register on cloud: await agent.register()")
    print("  • Register runtime: synqed.register_agent_runtime(agent.agent_id, agent)")
    print("  • Send messages: await agent.send(\"other@email\", \"message\")")
    print("  • That's it! Synqed handles everything else.")
    print()


if __name__ == "__main__":
    asyncio.run(main())

