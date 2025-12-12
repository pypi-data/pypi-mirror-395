"""
simplest possible example: two ai agents chatting.

this is a minimal demo - just run it and watch two agents talk!

requirements:
    pip install anthropic httpx

usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python examples/simple_chat.py
"""

import asyncio
import os
from anthropic import Anthropic
import httpx

# your deployed registry
REGISTRY_URL = "https://synqed.fly.dev"

# get api key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


async def create_and_chat():
    """two agents have a quick conversation."""
    
    print("\n🤖 creating two ai agents...\n")
    
    # agent 1: alice (optimistic futurist)
    alice_email = "alice@futurists"
    alice_prompt = "you're alice, an optimistic ai researcher who believes ai will solve humanity's problems. be enthusiastic and brief (1-2 sentences)."
    
    # agent 2: bob (skeptical pragmatist)
    bob_email = "bob@skeptics"
    bob_prompt = "you're bob, a skeptical engineer who questions ai hype. be critical but constructive. keep it brief (1-2 sentences)."
    
    # register them
    async with httpx.AsyncClient() as http:
        for email, prompt in [(alice_email, alice_prompt), (bob_email, bob_prompt)]:
            await http.post(
                f"{REGISTRY_URL}/v1/agents",
                json={
                    "email_like": email,
                    "inbox_url": "http://example.com/inbox",  # dummy for demo
                    "capabilities": ["chat"],
                    "metadata": {"system": prompt}
                }
            )
            print(f"✅ registered {email}")
    
    print("\n💬 starting conversation...\n")
    
    # conversation history
    alice_history = []
    bob_history = []
    
    # alice starts
    alice_msg = "i just read about ai agents being able to coordinate to solve complex problems - this is the future!"
    print(f"alice: {alice_msg}\n")
    
    # bob responds
    bob_history.append({"role": "user", "content": f"alice said: {alice_msg}"})
    bob_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        system=bob_prompt,
        messages=bob_history
    )
    bob_msg = bob_response.content[0].text
    bob_history.append({"role": "assistant", "content": bob_msg})
    print(f"bob: {bob_msg}\n")
    
    # alice responds back
    alice_history.append({"role": "user", "content": f"bob said: {bob_msg}"})
    alice_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        system=alice_prompt,
        messages=alice_history
    )
    alice_msg = alice_response.content[0].text
    alice_history.append({"role": "assistant", "content": alice_msg})
    print(f"alice: {alice_msg}\n")
    
    # one more from bob
    bob_history.append({"role": "user", "content": f"alice said: {alice_msg}"})
    bob_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        system=bob_prompt,
        messages=bob_history
    )
    bob_msg = bob_response.content[0].text
    print(f"bob: {bob_msg}\n")
    
    print("✅ conversation complete!")
    print(f"\n🌐 these agents are now registered at:")
    print(f"   https://synqed.fly.dev/v1/agents/by-email/alice@futurists")
    print(f"   https://synqed.fly.dev/v1/agents/by-email/bob@skeptics")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ please set ANTHROPIC_API_KEY environment variable")
        print("   export ANTHROPIC_API_KEY='sk-ant-...'")
    else:
        asyncio.run(create_and_chat())

