#!/usr/bin/env python3
"""
01 - Simple Agent: Basic MAF agent with Dakora tracking.

Shows the simplest MAF + Dakora setup. No tools, no templates -
just a basic chat agent with automatic observability.

WHAT YOU'LL LEARN:
- MAF ChatAgent basics
- DakoraIntegration middleware setup
- How agents appear in traces

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
    """Run a simple MAF agent with Dakora tracking."""

    # Setup Dakora and middleware
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # One line to enable full observability
    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("MAF Simple Agent Example")
    print("=" * 60)

    # Create a basic agent
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    agent = ChatAgent(
        id="simple-agent-v1",
        name="VacationPlanner",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="You are a helpful assistant. Be concise and friendly.",
        middleware=[middleware],
    )

    # Run the agent
    print("\nAsking agent: What is the capital of France?")
    result = await agent.run("What is the capital of France?")
    print(f"\nAgent response: {result.messages[0].text}")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Agent ID: simple-agent-v1")
    print("   - Agent name: SimpleAgent")
    print("   - Tokens, latency, cost")


if __name__ == "__main__":
    asyncio.run(main())
