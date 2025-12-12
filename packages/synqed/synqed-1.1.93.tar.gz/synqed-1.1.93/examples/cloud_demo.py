"""
Cloud Demo: Synqed Agents Communicating via Email Addresses Over Cloud

This demo demonstrates EMAIL-STYLE CLOUD COMMUNICATION between AI agents:

1. Agents are created with email-style addresses (name@org)
2. Agents are registered with the cloud registry
3. Agent A sends a message to Agent B using ONLY THE EMAIL ADDRESS via cloud
4. Message is routed via cloud inbox to Agent B
5. Agent B's logic processes the message and sends response back via cloud
6. Conversation continues over cloud until completion
7. Workspace is automatically created/managed in the background

Key Features:
- 📧 Email-style addressing (alice@wonderland, bob@builder)
- 🌍 Network-based cloud communication (via synqed.fly.dev)
- 🔄 Automatic workspace creation in background
- 🤖 Autonomous agent conversations via cloud messages
- ✅ Conversation ends when agent sends to USER
- 🛡️  Error handling for unknown/unregistered agents

Requirements:
- pip install synqed anthropic python-dotenv
- Set ANTHROPIC_API_KEY in .env file
"""

import asyncio
import os
import logging
from pathlib import Path
from anthropic import AsyncAnthropic
import synqed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass


async def send_cloud_message(sender: synqed.Agent, recipient_email: str, content: str) -> dict:
    """
    Send a message via cloud and simulate inbox worker processing.
    
    In production, the inbox worker runs as a separate service.
    For this demo, we simulate what the worker does.
    
    Args:
        sender: Sending agent
        recipient_email: Recipient's email address
        content: Message content
        
    Returns:
        Response envelope from recipient (if any)
    """
    print(f"📤 {sender.email} → {recipient_email}")
    print(f"   Via cloud: {sender.inbox_url}")
    print(f"   \"{content[:100]}{'...' if len(content) > 100 else ''}\"")
    print()
    
    # Send message via cloud
    try:
        result = await sender.send(
            to=recipient_email,
            content=content,
            via_cloud=True,
        )
        
        print(f"   ✅ Message accepted by cloud inbox")
        print(f"   Message ID: {result.get('message_id', 'N/A')}")
        print()
    except Exception as e:
        print(f"   ❌ Failed to send message: {e}")
        raise
    
    # Simulate inbox worker processing
    # In production, this happens asynchronously in the background
    print(f"   🔄 [Inbox Worker] Processing message...")
    
    # Convert email to agent_id
    recipient_parts = recipient_email.split("@")
    recipient_id = f"agent://{recipient_parts[1]}/{recipient_parts[0]}"
    
    # Create envelope
    envelope = {
        "thread_id": f"conversation-{sender.name}",
        "role": "user",
        "content": content,
    }
    
    # Route via auto-workspace (this is what the inbox worker does)
    auto_ws_manager = synqed.get_auto_workspace_manager()
    
    try:
        response_envelope = await auto_ws_manager.route_message_via_workspace(
            sender=sender.agent_id,
            recipient=recipient_id,
            envelope=envelope,
        )
        
        if response_envelope:
            print(f"   ✅ [Inbox Worker] Message processed, response generated")
            print()
            return response_envelope
        else:
            print(f"   ℹ️  [Inbox Worker] Message processed, no response")
            print()
            return None
    except Exception as e:
        print(f"   ❌ [Inbox Worker] Error processing message: {e}")
        raise


async def run_cloud_conversation(
    alice: synqed.Agent,
    bob: synqed.Agent,
    initial_message: str,
    max_turns: int = 8
) -> None:
    """
    Run a full conversation via cloud email messages.
    
    This simulates what happens in production:
    1. Agent A sends message to Agent B via cloud (using email address)
    2. Cloud inbox receives message
    3. Inbox worker routes to Agent B
    4. Agent B's logic processes and generates response
    5. Response sent back to Agent A via cloud
    6. Repeat until conversation ends
    
    Args:
        alice: First agent
        bob: Second agent
        initial_message: Initial message to start conversation
        max_turns: Maximum conversation turns
    """
    print("=" * 80)
    print("🔄 CLOUD CONVERSATION")
    print("=" * 80)
    print()
    print("All messages are sent via cloud using EMAIL ADDRESSES.")
    print("The inbox worker automatically creates workspaces in the background.")
    print()
    print("-" * 80)
    print()
    
    # Track conversation state
    current_sender = alice
    current_recipient = bob
    message_content = initial_message
    turn_count = 0
    conversation_ended = False
    
    while turn_count < max_turns and not conversation_ended:
        turn_count += 1
        print(f"[Turn {turn_count}]")
        
        # Send message via cloud using EMAIL ADDRESS
        try:
            response_envelope = await send_cloud_message(
                sender=current_sender,
                recipient_email=current_recipient.email,
                content=message_content,
            )
            
            if response_envelope:
                response_content = response_envelope.get("content", "")
                
                # Check if message was sent to USER (conversation complete)
                if "send_to" in response_envelope:
                    send_to = response_envelope["send_to"]
                    if send_to == "USER":
                        print(f"✅ {current_recipient.email} sent to USER - conversation complete!")
                        print()
                        conversation_ended = True
                        break
                
                # Prepare for next turn (swap sender/recipient)
                message_content = response_content
                current_sender, current_recipient = current_recipient, current_sender
            else:
                print(f"⚠️  No response from {current_recipient.email}")
                break
        
        except Exception as e:
            print(f"❌ Error during cloud message: {e}")
            import traceback
            traceback.print_exc()
            break
        
        print("-" * 80)
        print()
    
    if turn_count >= max_turns and not conversation_ended:
        print(f"⚠️  Reached maximum turns ({max_turns})")
        print()
    
    # Display final transcript from workspace
    print("=" * 80)
    print("📝 CONVERSATION TRANSCRIPT")
    print("=" * 80)
    print()
    
    auto_ws_manager = synqed.get_auto_workspace_manager()
    thread_id = f"conversation-{alice.name}"
    workspace_id = auto_ws_manager._thread_to_workspace.get(thread_id)
    
    if workspace_id:
        workspace = auto_ws_manager.workspace_manager.workspaces.get(workspace_id)
        if workspace:
            workspace.display_transcript(
                include_system_messages=False,
                parse_json_content=True
            )
            
            # Display summary
            status = workspace.get_completion_status()
            print("=" * 80)
            print("📊 CONVERSATION SUMMARY")
            print("=" * 80)
            print(f"Workspace ID: {workspace_id}")
            print(f"Total messages: {status['total_messages']}")
            print(f"Conversation turns: {turn_count}")
            print(f"Status: {status['status_message']}")
            print()
    else:
        print("⚠️  No workspace found (messages may not have been processed)")
        print()


async def cleanup_conversation(alice: synqed.Agent) -> None:
    """Clean up the workspace after conversation ends."""
    print("=" * 80)
    print("🧹 WORKSPACE CLEANUP")
    print("=" * 80)
    print()
    
    auto_ws_manager = synqed.get_auto_workspace_manager()
    thread_id = f"conversation-{alice.name}"
    
    workspace_id = auto_ws_manager._thread_to_workspace.get(thread_id)
    
    if workspace_id:
        print(f"Cleaning up workspace: {workspace_id}")
        await auto_ws_manager.cleanup_workspace(workspace_id)
        print(f"✅ Workspace cleaned up successfully")
    else:
        print(f"⚠️  No workspace found for thread: {thread_id}")
    
    print()


async def test_error_handling() -> None:
    """Test error handling for unknown/unregistered agents."""
    print("=" * 80)
    print("🔍 ERROR HANDLING TEST")
    print("=" * 80)
    print()
    print("Testing: Send to unknown agent (not in registry)")
    print()
    
    try:
        # Create a temporary agent (not registered)
        async def temp_logic(ctx):
            return None
        
        temp_agent = synqed.Agent(
            name="temp",
            role="testing",
            logic=temp_logic,
        )
        
        # Try to send to non-existent agent via cloud
        try:
            await temp_agent.send(
                to="nonexistent@nowhere",
                content="Hello?",
                via_cloud=True
            )
            print("❌ Should have failed but didn't")
        except Exception as e:
            print(f"✅ Correctly handled unknown recipient")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Error: {str(e)[:100]}")
    except Exception as e:
        print(f"✅ Error handling working: {e}")
    
    print()


async def main():
    """
    Main demo: Cloud-based email communication between AI agents.
    """
    
    print()
    print("=" * 80)
    print("🌍 SYNQED CLOUD DEMO: EMAIL-STYLE AGENT COMMUNICATION")
    print("=" * 80)
    print()
    print("This demo demonstrates:")
    print("  📧 Email-style addressing (name@org)")
    print("  🌍 Cloud-based message routing (via synqed.fly.dev)")
    print("  🔄 Automatic workspace creation in background")
    print("  🤖 Autonomous agent conversations via email")
    print("  ✅ Natural conversation completion")
    print("  🛡️  Error handling for unknown agents")
    print()
    
    # Check API key
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print()
        print("To run this demo:")
        print("  1. Add to .env: ANTHROPIC_API_KEY=sk-ant-...")
        print("  2. Or: export ANTHROPIC_API_KEY=sk-ant-...")
        print()
        return
    
    anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    # ========================================================================
    # STEP 1: Create agents with email addresses and AI logic
    # ========================================================================
    print("=" * 80)
    print("STEP 1: Creating agents with email addresses")
    print("=" * 80)
    print()
    
    # Alice - curious explorer who asks questions
    async def alice_logic(context):
        """Alice's AI logic - curious explorer"""
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        history = context.get_conversation_history()
        
        system_prompt = (
            "You are Alice (alice@wonderland), a curious explorer. "
            "You're talking with Bob (bob@builder), a helpful construction worker. "
            "Ask him questions and learn from his advice. Keep responses to 1-2 sentences. "
            "After Bob has given you helpful advice (2-3 exchanges), "
            "send a thank you summary to USER with: "
            '{"send_to": "USER", "content": "Thanks! I learned: [brief summary]"}. '
            "Until then, respond to Bob: "
            '{"send_to": "bob", "content": "your question or response"}'
        )
        
        conversation_text = f"Conversation:\n{history}\n\nRespond with JSON:"
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation_text}],
        )
        
        return response.content[0].text.strip()
    
    alice = synqed.Agent(
        name="alice",
        description="A curious explorer",
        logic=alice_logic,
        role="wonderland",
        default_target="bob"
    )
    
    print(f"✓ Created: {alice.email}")
    print(f"  Agent ID: {alice.agent_id}")
    print()
    
    # Bob - helpful builder
    async def bob_logic(context):
        """Bob's AI logic - helpful builder"""
        latest = context.latest_message
        if not latest or not latest.content:
            return None
        
        history = context.get_conversation_history()
        
        system_prompt = (
            "You are Bob (bob@builder), a helpful construction worker. "
            "You're talking with Alice. Give practical advice. "
            "Keep responses to 1-2 sentences. Be helpful and friendly. "
            '{"send_to": "alice", "content": "your helpful response"}'
        )
        
        conversation_text = f"Conversation:\n{history}\n\nRespond with JSON:"
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation_text}],
        )
        
        return response.content[0].text.strip()
    
    bob = synqed.Agent(
        name="bob",
        description="A helpful construction worker",
        logic=bob_logic,
        role="builder",
        default_target="alice"
    )
    
    print(f"✓ Created: {bob.email}")
    print(f"  Agent ID: {bob.agent_id}")
    print()
    
    # ========================================================================
    # STEP 2: Register agents with cloud registry
    # ========================================================================
    print("=" * 80)
    print("STEP 2: Registering agents with cloud registry")
    print("=" * 80)
    print()
    print("Registry URL: https://synqed.fly.dev/v1/agents")
    print()
    
    for agent in [alice, bob]:
        try:
            result = await agent.register()
            print(f"✓ Registered: {agent.email}")
            print(f"  Public key: {agent.public_key[:20]}...")
            print(f"  Inbox URL: {agent.inbox_url}")
        except Exception as e:
            if "409" in str(e) or "Conflict" in str(e):
                print(f"✓ Already registered: {agent.email}")
            else:
                print(f"❌ Registration failed: {e}")
                print()
                print("Note: Demo requires cloud connectivity to synqed.fly.dev")
                return
    
    print()
    
    # ========================================================================
    # STEP 3: Register agent runtimes (enables auto-workspace)
    # ========================================================================
    print("=" * 80)
    print("STEP 3: Registering agent runtimes")
    print("=" * 80)
    print()
    print("This enables automatic workspace creation when messages arrive.")
    print()
    
    synqed.register_agent_runtime(alice.agent_id, alice)
    synqed.register_agent_runtime(bob.agent_id, bob)
    
    print(f"✓ Runtime registered: {alice.email}")
    print(f"✓ Runtime registered: {bob.email}")
    print()
    
    # ========================================================================
    # STEP 4: Run cloud conversation using EMAIL ADDRESSES
    # ========================================================================
    print("=" * 80)
    print("STEP 4: Cloud conversation via email addresses")
    print("=" * 80)
    print()
    print("Alice will send a message to Bob using ONLY HIS EMAIL ADDRESS.")
    print("All messages will be routed via the cloud inbox.")
    print("Workspaces will be created automatically in the background.")
    print()
    
    initial_message = "Hi Bob! I'm planning to build a treehouse. What should I start with?"
    
    await run_cloud_conversation(
        alice=alice,
        bob=bob,
        initial_message=initial_message,
        max_turns=8
    )
    
    # ========================================================================
    # STEP 5: Clean up
    # ========================================================================
    await cleanup_conversation(alice)
    
    # ========================================================================
    # STEP 6: Error handling test
    # ========================================================================
    await test_error_handling()
    
    # ========================================================================
    # DEMO COMPLETE
    # ========================================================================
    print("=" * 80)
    print("✅ DEMO COMPLETE!")
    print("=" * 80)
    print()
    
    print("What you just saw:")
    print()
    print("  1. ✅ Created agents with email addresses (alice@wonderland, bob@builder)")
    print("  2. ✅ Registered them with cloud registry (synqed.fly.dev)")
    print("  3. ✅ Registered local runtimes for auto-workspace creation")
    print("  4. ✅ Agents communicated using ONLY email addresses")
    print("  5. ✅ All messages routed via cloud inbox")
    print("  6. ✅ Workspaces automatically created in background")
    print("  7. ✅ Conversation naturally completed when Alice sent to USER")
    print("  8. ✅ Workspace automatically cleaned up")
    print("  9. ✅ Error handling for unknown agents")
    print()
    
    print("Key cloud features demonstrated:")
    print()
    print("  📧 Email addressing: agent.send('bob@builder', 'message', via_cloud=True)")
    print("  🌍 Cloud routing: Messages sent to https://synqed.fly.dev")
    print("  🔑 Cryptographic auth: Ed25519 signatures on all messages")
    print("  🔄 Auto-workspace: Workspaces created transparently")
    print("  📝 Registry: Agents discoverable by email address")
    print("  🛡️  Error handling: Unknown agents rejected gracefully")
    print()
    
    print("This is synqed's email-style cloud communication:")
    print()
    print("  # Create with email")
    print("  alice = Agent(name='alice', role='wonderland', logic=...)")
    print()
    print("  # Register on cloud")
    print("  await alice.register()")
    print()
    print("  # Register local runtime")
    print("  synqed.register_agent_runtime(alice.agent_id, alice)")
    print()
    print("  # Send via cloud using EMAIL")
    print("  await alice.send('bob@builder', 'Hello!', via_cloud=True)")
    print()
    print("  # Everything else is automatic!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
