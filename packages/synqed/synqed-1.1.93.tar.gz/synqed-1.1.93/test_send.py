"""
Test sending a signed message.
"""
import asyncio
import json
import httpx
from synqed.agent_email.inbox import sign_message

async def main():
    # Load keypair
    with open('keypairs.json', 'r') as f:
        keypairs = json.load(f)
    
    alice_keys = keypairs["agent://demo/alice"]
    
    # Create message
    message = {
        "thread_id": "test-thread-123",
        "role": "user",
        "content": "Hello from Alice!",
    }
    
    # Sign message
    signature = sign_message(
        private_key_b64=alice_keys["private_key"],
        sender="agent://demo/alice",
        recipient="agent://demo/bob",
        message=message,
        thread_id="test-thread-123",
    )
    
    # Send envelope
    envelope = {
        "sender": "agent://demo/alice",
        "recipient": "agent://demo/bob",
        "message": message,
        "signature": signature,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/v1/a2a/inbox",
            json=envelope,
            timeout=30.0,
        )
        
        result = response.json()
        print("Response:", json.dumps(result, indent=2))
        
        if result["status"] == "accepted":
            print(f"\n✓ Message accepted!")
            print(f"  Message ID: {result['message_id']}")
            print(f"  Trace ID: {result['trace_id']}")
        else:
            print(f"\n✗ Message failed: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(main())
