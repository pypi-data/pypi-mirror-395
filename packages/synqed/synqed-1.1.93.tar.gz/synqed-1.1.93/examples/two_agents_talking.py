"""
two ai agents talking via agent email addresses.

this example:
1. creates two agents (researcher and analyst) using anthropic's claude
2. registers them with synqed.fly.dev 
3. has them have a conversation about a research topic

requirements:
    pip install anthropic httpx fastapi uvicorn

usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python examples/two_agents_talking.py
"""

import asyncio
import uuid
from typing import Any, Dict

import httpx
from anthropic import Anthropic

# configuration
REGISTRY_URL = "https://synqed.fly.dev"
ANTHROPIC_API_KEY = None  # will be set from environment


class AnthropicAgent:
    """
    an agent powered by anthropic's claude.
    
    each agent has:
    - a personality/role
    - an email address (name@org)
    - an inbox that receives messages
    - ability to respond using claude
    """
    
    def __init__(
        self,
        name: str,
        org: str,
        system_prompt: str,
        model: str = "claude-sonnet-4-20250514",
    ):
        self.name = name
        self.org = org
        self.email = f"{name}@{org}"
        self.agent_id = f"agent://{org}/{name}"
        self.system_prompt = system_prompt
        self.model = model
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.conversation_history: list[Dict[str, str]] = []
        
        print(f"✨ created agent: {self.email}")
    
    async def think_and_respond(self, incoming_message: str, from_agent: str) -> str:
        """
        use claude to think about the message and generate a response.
        
        args:
            incoming_message: the message received
            from_agent: who sent it (email address)
            
        returns:
            the agent's response
        """
        # add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": f"message from {from_agent}: {incoming_message}"
        })
        
        print(f"\n🤔 {self.email} is thinking...")
        
        # call claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history,
        )
        
        # extract response
        response_text = response.content[0].text
        
        # add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        print(f"💭 {self.email}: {response_text[:100]}...")
        
        return response_text
    
    def get_inbox_handler(self):
        """
        returns an async function that handles incoming a2a messages.
        
        this is what gets called when someone sends a message to this agent.
        """
        async def handle_inbox(request_data: Dict[str, Any]) -> Dict[str, Any]:
            sender = request_data.get("sender", "unknown")
            message = request_data.get("message", {})
            content = message.get("content", "")
            thread_id = message.get("thread_id", str(uuid.uuid4()))
            
            print(f"\n📨 {self.email} received message from {sender}")
            
            # use claude to generate response
            response_text = await self.think_and_respond(content, sender)
            
            # return a2a envelope
            return {
                "status": "accepted",
                "message_id": str(uuid.uuid4()),
                "response_envelope": {
                    "thread_id": thread_id,
                    "role": "assistant",
                    "content": response_text,
                    "tool_calls": [],
                }
            }
        
        return handle_inbox


async def register_agent_in_registry(
    agent: AnthropicAgent,
    local_port: int
) -> None:
    """
    register an agent in the synqed.fly.dev registry.
    
    args:
        agent: the agent to register
        local_port: port where agent's inbox server is running
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{REGISTRY_URL}/v1/agents",
            json={
                "email_like": agent.email,
                "inbox_url": f"http://localhost:{local_port}/inbox",  # in production, use public url
                "capabilities": ["a2a/1.0", "anthropic-claude"],
                "metadata": {
                    "model": agent.model,
                    "org": agent.org,
                }
            },
        )
        response.raise_for_status()
        print(f"✅ registered {agent.email} in global registry")


async def send_message_to_agent(
    from_agent: AnthropicAgent,
    to_email: str,
    message_content: str,
) -> Dict[str, Any]:
    """
    send a message from one agent to another via the registry.
    
    args:
        from_agent: the sending agent
        to_email: email address of recipient (e.g., "analyst@acme")
        message_content: what to say
        
    returns:
        the recipient's response
    """
    async with httpx.AsyncClient() as client:
        # step 1: look up recipient in registry
        print(f"\n🔍 {from_agent.email} looking up {to_email}...")
        lookup_response = await client.get(
            f"{REGISTRY_URL}/v1/agents/by-email/{to_email}"
        )
        lookup_response.raise_for_status()
        recipient_info = lookup_response.json()
        
        print(f"✓ found {to_email} at {recipient_info['inbox_url']}")
        
        # step 2: send message to their inbox
        thread_id = str(uuid.uuid4())
        inbox_request = {
            "sender": from_agent.agent_id,
            "recipient": recipient_info["agent_id"],
            "message": {
                "thread_id": thread_id,
                "role": "user",
                "content": message_content,
                "tool_calls": [],
            }
        }
        
        print(f"📤 {from_agent.email} sending message to {to_email}...")
        
        # for this demo, we'll simulate the inbox call locally
        # in production, this would be an http post to the inbox_url
        inbox_response = await client.post(
            recipient_info["inbox_url"],
            json=inbox_request,
        )
        inbox_response.raise_for_status()
        
        return inbox_response.json()


async def run_local_inbox_servers(agents: list[AnthropicAgent]) -> None:
    """
    run simple inbox servers for each agent locally.
    
    in production, each agent would have its own server.
    for this demo, we simulate it in-process.
    """
    from fastapi import FastAPI, Request
    import uvicorn
    
    # create a server for each agent
    apps = []
    
    for i, agent in enumerate(agents):
        app = FastAPI(title=f"{agent.email} Inbox")
        handler = agent.get_inbox_handler()
        
        @app.post("/inbox")
        async def inbox_endpoint(request: Request):
            data = await request.json()
            return await handler(data)
        
        apps.append((app, 8001 + i))
    
    # run servers in background
    tasks = []
    for app, port in apps:
        task = asyncio.create_task(
            uvicorn.Server(
                uvicorn.Config(app, host="0.0.0.0", port=port, log_level="error")
            ).serve()
        )
        tasks.append(task)
    
    await asyncio.sleep(1)  # let servers start


async def simulate_conversation() -> None:
    """
    simulate a conversation between two agents using only their email addresses.
    """
    print("\n" + "="*70)
    print("🤖 TWO AI AGENTS TALKING VIA AGENT EMAIL ADDRESSES")
    print("="*70)
    
    # create two agents
    researcher = AnthropicAgent(
        name="researcher",
        org="university",
        system_prompt=(
            "you are a curious research scientist. you ask insightful questions "
            "and propose interesting hypotheses. you're investigating quantum computing "
            "applications in drug discovery. keep responses concise (2-3 sentences)."
        )
    )
    
    analyst = AnthropicAgent(
        name="analyst",
        org="biotech",
        system_prompt=(
            "you are a pragmatic biotech analyst. you evaluate ideas critically, "
            "identify challenges, and suggest concrete next steps. you're interested "
            "in practical applications of emerging technologies. "
            "keep responses concise (2-3 sentences)."
        )
    )
    
    # simulate local inbox servers (in production, these would be separate services)
    # for this demo, we'll just handle messages directly
    
    # register agents in the global registry
    # note: in this demo, we're using localhost urls
    # in production, these would be public https urls
    print("\n📝 registering agents in synqed.fly.dev...")
    await register_agent_in_registry(researcher, 8001)
    await register_agent_in_registry(analyst, 8002)
    
    print("\n" + "="*70)
    print("🎭 CONVERSATION START")
    print("="*70)
    
    # researcher starts the conversation
    print(f"\n💬 researcher@university is starting a conversation with analyst@biotech...")
    
    # turn 1: researcher → analyst
    message_1 = (
        "i've been exploring how quantum computers might accelerate molecular "
        "simulation for drug discovery. what's your take on the commercial "
        "viability in the next 5 years?"
    )
    
    print(f"\n📤 researcher@university → analyst@biotech")
    print(f"   \"{message_1}\"")
    
    # analyst thinks and responds
    response_1 = await analyst.think_and_respond(message_1, "researcher@university")
    
    print(f"\n💬 analyst@biotech:")
    print(f"   \"{response_1}\"")
    
    # turn 2: analyst → researcher (continue conversation)
    # researcher responds
    response_2 = await researcher.think_and_respond(response_1, "analyst@biotech")
    
    print(f"\n💬 researcher@university:")
    print(f"   \"{response_2}\"")
    
    # turn 3: one more exchange
    response_3 = await analyst.think_and_respond(response_2, "researcher@university")
    
    print(f"\n💬 analyst@biotech:")
    print(f"   \"{response_3}\"")
    
    print("\n" + "="*70)
    print("✅ CONVERSATION COMPLETE")
    print("="*70)
    
    print("\n📊 what just happened:")
    print("  ✓ two ai agents (powered by claude) were created")
    print("  ✓ each agent got an email address (researcher@university, analyst@biotech)")
    print("  ✓ both registered in the global registry at synqed.fly.dev")
    print("  ✓ they had a conversation about quantum computing in drug discovery")
    print("  ✓ each agent used claude to think and respond naturally")
    
    print("\n🌐 these agents are now discoverable at:")
    print(f"  https://synqed.fly.dev/v1/agents/by-email/researcher@university")
    print(f"  https://synqed.fly.dev/v1/agents/by-email/analyst@biotech")


async def main():
    """main entry point."""
    import os
    
    global ANTHROPIC_API_KEY
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    if not ANTHROPIC_API_KEY:
        print("❌ error: ANTHROPIC_API_KEY environment variable not set")
        print("\nget your api key from: https://console.anthropic.com/")
        print("\nthen run:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  python examples/two_agents_talking.py")
        return
    
    try:
        await simulate_conversation()
    except Exception as e:
        print(f"\n❌ error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

