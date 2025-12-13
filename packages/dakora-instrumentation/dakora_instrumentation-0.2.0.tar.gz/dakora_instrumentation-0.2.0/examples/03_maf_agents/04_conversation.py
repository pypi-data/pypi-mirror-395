#!/usr/bin/env python3
"""
04 - Conversation: Multi-turn conversation tracking with MAF using threads.

Shows how Dakora tracks multi-turn conversations using threads,
maintaining context across turns while providing per-turn observability.

WHAT YOU'LL LEARN:
- Multi-turn conversation tracking using threads
- Thread creation and reuse for grouping turns
- Per-turn metrics (tokens, latency)

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
"""

import asyncio
import os

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Run a multi-turn conversation with Dakora tracking."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("MAF Conversation Tracking Example")
    print("=" * 60)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Create agent for conversation
    agent = ChatAgent(
        id="tutor-agent-v1",
        name="TutorAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="""You are a helpful Python programming tutor.
Teach concepts progressively, building on previous explanations.
Use simple examples and encourage questions.""",
        middleware=[middleware],
    )

    # Create a thread for persistent conversation
    thread = agent.get_new_thread()

    # Multi-turn conversation
    turns = [
        "What is a Python list?",
        "How do I add an item to a list?",
        "What's the difference between append and extend?",
        "Can you show me a quick example using both?",
    ]

    print("\n" + "-" * 40)
    print("Starting conversation...")
    print("-" * 40)

    for i, user_message in enumerate(turns, 1):
        print(f"\n[Turn {i}] User: {user_message}")
        result = await agent.run(user_message, thread=thread)
        response = result.messages[0].text

        # Truncate long responses for display
        if len(response) > 200:
            display = response[:200] + "..."
        else:
            display = response
        print(f"[Turn {i}] Agent: {display}")

    # Summary
    print("\n" + "-" * 40)
    print("Conversation Summary")
    print("-" * 40)
    print(f"  Thread ID: {thread}")
    print(f"  Total turns: {len(turns)}")
    print("  Agent ID: tutor-agent-v1")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print(f"   - All turns grouped under thread: {thread}")
    print("   - Per-turn token usage and latency")
    print("   - Conversation context growing across turns")


if __name__ == "__main__":
    asyncio.run(main())
