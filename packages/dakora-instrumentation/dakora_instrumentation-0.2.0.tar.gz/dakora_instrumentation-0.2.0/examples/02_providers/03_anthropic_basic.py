#!/usr/bin/env python3
"""
03 - Anthropic Basic: Instrument Anthropic Claude API with templates.

Shows how to use Dakora with Anthropic's Claude models and the
technical_documentation template for code documentation.

WHAT YOU'LL LEARN:
- Anthropic SDK instrumentation
- Claude-specific response handling
- Using templates with Anthropic

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-anthropic anthropic
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    ANTHROPIC_API_KEY - Your Anthropic API key
    ANTHROPIC_MODEL - Model to use (default: claude-3-5-haiku-20241022)

USES TEMPLATE:
    technical_documentation - Generate comprehensive code documentation
"""

import asyncio
import os

from dotenv import load_dotenv

# Instrument Anthropic first
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

AnthropicInstrumentor().instrument()

from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Run Anthropic Claude calls with Dakora tracing and templates."""

    # Setup Dakora instrumentation
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    setup_instrumentation(
        dakora_client=dakora,
        service_name="provider-anthropic-basic",
    )

    print("=" * 60)
    print("Anthropic Basic Example with Templates")
    print("=" * 60)

    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")

    # Example 1: Document a Python function
    # Note: technical_documentation is a default template auto-created for each project
    print(f"\nExample 1: Document a Python function ({model})...")
    rendered = await dakora.prompts.render(
        "technical_documentation",
        {
            "code_snippet": '''def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
) -> Any:
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            time.sleep(delay)''',
            "doc_sections": ["Overview", "Parameters", "Returns", "Examples", "Notes"],
            "example_count": 2,
            "include_troubleshooting": True,
        },
    )
    print(f"   Template: technical_documentation v{rendered.version}")

    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": rendered.text}],
    )

    text = next(
        (block.text for block in response.content if hasattr(block, "text")), None
    )
    print(f"   Response:\n{text}")

    # Example 2: Document a class
    print(f"\nExample 2: Document a Python class ({model})...")
    rendered = await dakora.prompts.render(
        "technical_documentation",
        {
            "code_snippet": '''class RateLimiter:
    """Rate limiter using token bucket algorithm."""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()

    def acquire(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now''',
            "doc_sections": ["Overview", "Parameters", "Methods", "Examples"],
            "example_count": 1,
            "include_troubleshooting": False,
        },
    )
    print(f"   Template: technical_documentation v{rendered.version}")

    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": rendered.text}],
    )

    text = next(
        (block.text for block in response.content if hasattr(block, "text")), None
    )
    print(f"   Response:\n{text}")

    # Flush traces
    print("\nFlushing traces to Dakora...")
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Two Claude traces with template linking")
    print("   - Template: technical_documentation in traces")
    print("   - Go to Prompts → technical_documentation → Activity")


if __name__ == "__main__":
    asyncio.run(main())
