#!/usr/bin/env python3
"""
01 - OpenAI Basic: OpenAI instrumentation with Dakora templates.

Shows how to use Dakora templates with OpenAI for traceable,
versioned prompts. Uses the faq_responder template.

WHAT YOU'LL LEARN:
- OpenAI instrumentation setup
- Dakora OTLP exporter configuration
- Using templates with chat completions
- Basic trace structure with template linking

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai openai
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    DAKORA_BASE_URL - Dakora server URL (default: http://localhost:8000)
    OPENAI_API_KEY - Your OpenAI API key
    OPENAI_MODEL - Model to use (default: gpt-4o-mini)

USES TEMPLATE:
    faq_responder - Standard Dakora sample template for FAQ responses
"""

import asyncio
import os

from dotenv import load_dotenv

# Instrument OpenAI FIRST - before any OpenAI imports or usage
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()

from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Run basic OpenAI calls with Dakora tracing and templates."""

    # Setup Dakora instrumentation
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    setup_instrumentation(
        dakora_client=dakora,
        service_name="provider-openai-basic",
    )

    print("=" * 60)
    print("OpenAI Basic Example with Templates")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Example 1: FAQ about Python
    # Note: faq_responder is a default template auto-created for each project
    print(f"\nExample 1: Python FAQ ({model})...")
    rendered = await dakora.prompts.render(
        "faq_responder",
        {
            "question": "What is Python and why is it popular?",
            "knowledge_base": """
Python is a high-level, interpreted programming language created by Guido van Rossum in 1991.

Key features:
- Simple, readable syntax that emphasizes code readability
- Dynamically typed with automatic memory management
- Extensive standard library and third-party packages
- Supports multiple programming paradigms (OOP, functional, procedural)
- Cross-platform compatibility
- Large, active community and ecosystem

Popular use cases: web development, data science, AI/ML, automation, scripting.
            """.strip(),
            "tone": "helpful and educational",
            "include_sources": False,
        },
    )
    print(f"   Template: faq_responder v{rendered.version}")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": rendered.text}],
    )
    print(f"   Response: {response.choices[0].message.content}")

    # Example 2: FAQ with sources
    print(f"\nExample 2: Technical FAQ with sources ({model})...")
    rendered = await dakora.prompts.render(
        "faq_responder",
        {
            "question": "How do I handle errors in Python?",
            "knowledge_base": """
[Python Documentation] Python uses try/except blocks for error handling:
- try: Contains code that might raise an exception
- except: Handles specific exception types
- else: Runs if no exception occurs
- finally: Always runs, used for cleanup

[Best Practices Guide] Common patterns:
- Catch specific exceptions, not bare except
- Use context managers (with statement) for resources
- Log exceptions with full traceback for debugging
- Create custom exception classes for domain errors
            """.strip(),
            "tone": "technical and precise",
            "include_sources": True,
        },
    )
    print(f"   Template: faq_responder v{rendered.version}")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": rendered.text}],
    )
    print(f"   Response: {response.choices[0].message.content}")

    # Flush traces
    print("\nFlushing traces to Dakora...")
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Two traces with model, tokens, latency")
    print("   - Template: faq_responder linked to executions")
    print("   - Go to Prompts → faq_responder → Activity")


if __name__ == "__main__":
    asyncio.run(main())
