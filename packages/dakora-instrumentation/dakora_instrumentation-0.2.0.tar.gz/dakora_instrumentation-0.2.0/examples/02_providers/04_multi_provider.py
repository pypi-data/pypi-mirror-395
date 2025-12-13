#!/usr/bin/env python3
"""
04 - Multi-Provider: Use OpenAI and Anthropic together with unified tracing.

Shows how to instrument multiple providers simultaneously, with all
traces flowing to the same Dakora project. Uses the research_synthesizer
template for comparing provider responses.

WHAT YOU'LL LEARN:
- Multi-provider instrumentation
- Unified trace collection
- Comparing provider responses with templates

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai openai
    pip install opentelemetry-instrumentation-anthropic anthropic
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
    ANTHROPIC_API_KEY - Your Anthropic API key

USES TEMPLATE:
    research_synthesizer - Synthesize multiple sources into cohesive summary
"""

import asyncio
import os

from dotenv import load_dotenv
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

# Instrument ALL providers at startup
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()
AnthropicInstrumentor().instrument()

from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Compare OpenAI and Anthropic responses with unified tracing."""

    # Single Dakora setup for all providers
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    setup_instrumentation(
        dakora_client=dakora,
        service_name="provider-multi-provider",
    )

    print("=" * 60)
    print("Multi-Provider Example with Templates")
    print("=" * 60)

    from anthropic import Anthropic
    from openai import OpenAI
    from opentelemetry import trace

    tracer = trace.get_tracer(__name__)

    # Initialize both clients
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")

    # Render the research_synthesizer template
    # Note: research_synthesizer is a default template auto-created for each project
    print("\nStep 1: Rendering template...")
    rendered = await dakora.prompts.render(
        "research_synthesizer",
        {
            "research_question": "What are the main benefits and challenges of microservices architecture?",
            "sources": [
                "[Martin Fowler, 2014] Microservices enable independent deployment and scaling of services. Each service can use different technologies. Teams can work autonomously on different services.",
                "[Netflix Engineering, 2016] Netflix uses 700+ microservices. Benefits include resilience and faster feature delivery. Challenges include service discovery and network latency.",
                "[ThoughtWorks, 2020] Microservices work best when there's a clear domain boundary. Monoliths are simpler for small teams. Consider organizational structure when choosing architecture.",
                "[AWS, 2023] Microservices enable auto-scaling per service. However, distributed systems are inherently more complex. Observability tools are essential for debugging.",
            ],
            "citation_style": "APA",
            "max_sources": 5,
            "output_format": "markdown",
        },
    )
    print(f"   Template: research_synthesizer v{rendered.version}")

    # Wrap both calls in a parent span for comparison
    with tracer.start_as_current_span("provider-comparison-research"):
        # OpenAI
        print(f"\nStep 3: OpenAI synthesis ({openai_model})...")
        openai_response = openai_client.chat.completions.create(
            model=openai_model,
            messages=[{"role": "user", "content": rendered.text}],
        )
        openai_text = openai_response.choices[0].message.content
        print(
            f"\n{openai_text[:500]}..."
            if len(openai_text) > 500
            else f"\n{openai_text}"
        )

        # Anthropic
        print(f"\nStep 4: Anthropic synthesis ({anthropic_model})...")
        anthropic_response = anthropic_client.messages.create(
            model=anthropic_model,
            max_tokens=1000,
            messages=[{"role": "user", "content": rendered.text}],
        )
        anthropic_text = next(
            (
                block.text
                for block in anthropic_response.content
                if hasattr(block, "text")
            ),
            None,
        )
        print(
            f"\n{anthropic_text[:500]}..."
            if anthropic_text and len(anthropic_text) > 500
            else f"\n{anthropic_text}"
        )

    # Token comparison
    print("\n" + "=" * 60)
    print("Token Usage Comparison")
    print("=" * 60)
    print(
        f"OpenAI:    {openai_response.usage.prompt_tokens} prompt + {openai_response.usage.completion_tokens} completion = {openai_response.usage.total_tokens} total"
    )
    print(
        f"Anthropic: {anthropic_response.usage.input_tokens} prompt + {anthropic_response.usage.output_tokens} completion = {anthropic_response.usage.input_tokens + anthropic_response.usage.output_tokens} total"
    )

    # Flush traces
    print("\nFlushing traces to Dakora...")
    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Parent span: 'provider-comparison-research'")
    print("   - Child spans: One for each provider")
    print("   - Template: research_synthesizer linked to both")
    print("   - Compare: tokens, latency, cost across providers")


if __name__ == "__main__":
    asyncio.run(main())
