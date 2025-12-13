#!/usr/bin/env python3
"""
02 - With Template: Add Dakora template rendering to your LLM calls.

Building on the hello world example, this shows how to use Dakora's
template management to create versioned, reusable prompts.

WHAT YOU'LL LEARN:
- How to render Dakora templates
- How template versions are automatically tracked
- How templates link to execution traces

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai openai
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    DAKORA_BASE_URL - Dakora server URL (default: http://localhost:8000)
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATE:
    faq_responder - Standard Dakora sample template for FAQ responses
"""

import asyncio
import os

from dotenv import load_dotenv

# Instrument OpenAI before any usage
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()

from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Render a Dakora template and use it with OpenAI."""

    # Initialize Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # Setup OTLP exporter
    setup_instrumentation(
        dakora_client=dakora,
        service_name="quickstart-with-template",
    )

    print("=" * 60)
    print("Dakora Quickstart: With Template")
    print("=" * 60)

    # Render the template with inputs
    # Note: faq_responder is a default template auto-created for each project
    print("\nStep 1: Rendering template...")
    rendered = await dakora.prompts.render(
        "faq_responder",
        {
            "question": "What is Dakora and how does it help with AI observability?",
            "knowledge_base": """
**Dakora** is an open-source AI observability and prompt management platform.

Key features:
- Real-time cost analytics for LLM usage
- Prompt template versioning and management
- Budget controls and policy enforcement
- OpenTelemetry-based trace collection
- Studio UI for prompt engineering

Learn more at https://dakora.io
            """.strip(),
            "tone": "helpful and informative",
            "include_sources": True,
        },
    )

    print(f"   Template: faq_responder v{rendered.version}")
    print(f"   Rendered length: {len(rendered.text)} chars")

    # Use the rendered template with OpenAI
    print("\nStep 3: Calling OpenAI with rendered template...")
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": rendered.text}],
    )

    output = response.choices[0].message.content
    print("\nResponse:")
    print("-" * 40)
    print(output)
    print("-" * 40)

    # Flush traces
    print("\nFlushing traces to Dakora...")
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - The trace with model, tokens, latency")
    print("   - Template: faq_responder linked to the execution")
    print("   - Go to Prompts → faq_responder → Activity")


if __name__ == "__main__":
    asyncio.run(main())
