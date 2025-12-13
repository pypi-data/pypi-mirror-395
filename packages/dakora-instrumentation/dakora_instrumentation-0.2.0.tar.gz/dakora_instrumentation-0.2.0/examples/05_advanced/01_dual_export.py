#!/usr/bin/env python3
"""
01 - Dual Export: Send traces to both Dakora and Jaeger.

Shows how to export traces to multiple backends simultaneously,
useful for combining Dakora's LLM analytics with local debugging
via Jaeger.

WHAT YOU'LL LEARN:
- Multi-destination trace export
- Jaeger integration for local debugging
- Trace correlation across systems

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

    # Run Jaeger locally
    docker run -d -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
    JAEGER_ENDPOINT - Jaeger OTLP endpoint (default: http://localhost:4317)
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
    """Run with dual export to Dakora and Jaeger."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # Setup with Jaeger integration
    jaeger_endpoint = os.getenv("JAEGER_ENDPOINT", "http://localhost:4317")

    print("=" * 60)
    print("Dual Export: Dakora + Jaeger")
    print("=" * 60)
    print(f"\nDakora: {dakora.base_url}")
    print(f"Jaeger: {jaeger_endpoint}")

    try:
        middleware = DakoraIntegration.setup_with_jaeger(
            dakora,
            jaeger_endpoint=jaeger_endpoint,
        )
        print("\n✅ Dual export configured!")
    except Exception as e:
        print(f"\n⚠️  Jaeger setup failed: {e}")
        print("Falling back to Dakora-only export...")
        middleware = DakoraIntegration.setup(dakora)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    agent = ChatAgent(
        id="dual-export-agent-v1",
        name="DualExportAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="You are a helpful assistant. Be concise.",
        middleware=[middleware],
    )

    print("\nRunning agent...")
    result = await agent.run("What are the three primary colors?")
    print(f"\nResponse: {result.messages[0].text}")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! View traces at:")
    print("   - Dakora Studio: Your configured Dakora URL")
    print("   - Jaeger UI: http://localhost:16686")
    print("\nBoth show the same trace with the same trace ID!")


if __name__ == "__main__":
    asyncio.run(main())
