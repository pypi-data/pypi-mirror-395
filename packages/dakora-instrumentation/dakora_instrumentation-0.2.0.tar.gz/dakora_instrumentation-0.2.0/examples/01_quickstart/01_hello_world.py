#!/usr/bin/env python3
"""
01 - Hello World: The simplest possible Dakora instrumentation example.

This example shows the absolute minimum setup to send LLM telemetry to Dakora.
No templates, no agents, just one OpenAI call with automatic tracing.

WHAT YOU'LL LEARN:
- How to instrument OpenAI with OpenTelemetry
- How to configure the Dakora OTLP exporter
- How traces flow from your app to Dakora

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai openai
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    DAKORA_BASE_URL - Dakora server URL (default: http://localhost:8000)
    OPENAI_API_KEY - Your OpenAI API key
"""

import os

from dotenv import load_dotenv

# Step 1: Import and instrument OpenAI BEFORE any OpenAI usage
# This must happen early - it patches the OpenAI client globally
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()

# Step 2: Import Dakora client and instrumentation helper
from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


def main() -> None:
    """Run a single OpenAI call with Dakora tracing."""

    # Step 3: Initialize Dakora client
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # Step 4: Setup OTLP exporter to send traces to Dakora
    setup_instrumentation(
        dakora_client=dakora,
        service_name="quickstart-hello-world",
    )

    print("=" * 60)
    print("Dakora Quickstart: Hello World")
    print("=" * 60)

    # Step 5: Use OpenAI normally - it's automatically traced!
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    print(f"\nCalling OpenAI ({model})...")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in exactly 5 words."}],
    )

    output = response.choices[0].message.content
    print(f"\nResponse: {output}")

    # Step 6: Flush traces before exit (important for short-lived scripts)
    print("\nFlushing traces to Dakora...")
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    print("\n✅ Done! Check Dakora Studio to see your trace.")
    print("   - Go to: Traces in Dakora Studio")
    print("   - You'll see: model, tokens, latency, cost")


if __name__ == "__main__":
    main()
