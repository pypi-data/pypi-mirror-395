#!/usr/bin/env python3
"""
02 - Budget Checking: Pre-execution budget validation.

Shows how Dakora can check project budgets before executing LLM calls,
preventing overspend with configurable caching for performance.

WHAT YOU'LL LEARN:
- Pre-execution budget validation
- Budget check caching
- Handling budget exceeded scenarios

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

NOTE:
    Budget checking requires budget limits to be configured in
    Dakora Studio for your project.
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
    """Run with budget checking enabled."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # Enable budget checking with caching
    # Cache TTL of 30 seconds reduces API calls for frequent operations
    middleware = DakoraIntegration.setup(
        dakora,
        enable_sensitive_data=True,
        budget_check_cache_ttl=30,  # Cache budget status for 30 seconds
    )

    print("=" * 60)
    print("Budget Checking Example")
    print("=" * 60)
    print("\nBudget check cache TTL: 30 seconds")
    print("Note: Set budget limits in Dakora Studio for your project")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    agent = ChatAgent(
        id="budget-checked-agent-v1",
        name="BudgetCheckedAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="You are a helpful assistant. Be concise.",
        middleware=[middleware],
    )

    # Run multiple requests to demonstrate caching
    queries = [
        "What is 2 + 2?",
        "What is the capital of France?",
        "Name three colors.",
    ]

    print("\nRunning multiple queries...")
    print("(Budget is checked and cached on first call)")
    print()

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        try:
            result = await agent.run(query)
            print(f"Response: {result.messages[0].text}\n")
        except Exception as e:
            if "budget" in str(e).lower():
                print(f"❌ Budget exceeded: {e}\n")
            else:
                raise

    # Cleanup
    print("Flushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Budget checks:")
    print("   - First call: Checked with Dakora API")
    print("   - Subsequent calls: Used cached result (30s)")
    print("   - View budget usage in Dakora Studio")


if __name__ == "__main__":
    asyncio.run(main())
