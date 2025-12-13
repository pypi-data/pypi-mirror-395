#!/usr/bin/env python3
"""
02 - OpenAI with Tools: Instrument OpenAI tool/function calling.

Shows how tool calls are traced, including the initial request,
tool execution, and continuation with tool results.

WHAT YOU'LL LEARN:
- How tool calls appear in traces
- Multi-step tool execution flow
- Parent-child span relationships

PREREQUISITES:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai openai
    pip install dakora-client dakora-instrumentation

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
"""

import json
import os

from dotenv import load_dotenv

# Instrument OpenAI first
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument()

from dakora_instrumentation.generic import setup_instrumentation

from dakora import Dakora

load_dotenv()


# Define a simple tool
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulate getting weather data."""
    # In a real app, this would call a weather API
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "sunny",
        "humidity": 45,
    }


# Tool definition for OpenAI
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and country, e.g. 'London, UK'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit",
                },
            },
            "required": ["location"],
        },
    },
}


def main() -> None:
    """Run OpenAI with tool calls, fully traced."""

    # Setup Dakora instrumentation
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    setup_instrumentation(
        dakora_client=dakora,
        service_name="provider-openai-tools",
    )

    print("=" * 60)
    print("OpenAI with Tools Example")
    print("=" * 60)

    from openai import OpenAI
    from opentelemetry import trace

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    tracer = trace.get_tracer(__name__)

    # Wrap the entire tool-use flow in a parent span
    with tracer.start_as_current_span("weather-query-with-tools"):
        print(f"\n1. Initial request to {model} with tool definition...")

        # Step 1: Initial request - model may choose to call the tool
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "What's the weather like in Tokyo, Japan?"}
            ],
            tools=[WEATHER_TOOL],
        )

        message = response.choices[0].message

        # Check if model wants to use the tool
        if message.tool_calls:
            print("   Model requested tool call!")

            for tool_call in message.tool_calls:
                print(f"   → {tool_call.function.name}({tool_call.function.arguments})")

                # Step 2: Execute the tool
                args = json.loads(tool_call.function.arguments)
                result = get_weather(**args)

                print(f"   ← Tool result: {result}")

                # Step 3: Send tool result back to model
                print("\n2. Sending tool result back to model...")

                final_response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": "What's the weather like in Tokyo, Japan?",
                        },
                        message,  # Include the assistant's tool call request
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        },
                    ],
                    tools=[WEATHER_TOOL],
                )

                final_output = final_response.choices[0].message.content
                print(f"\n3. Final response:\n   {final_output}")
        else:
            # Model answered directly without using the tool
            print(f"   Model answered directly: {message.content}")

    # Flush traces
    print("\nFlushing traces to Dakora...")
    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(timeout_millis=5000)

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Parent span: 'weather-query-with-tools'")
    print("   - Child spans: Two LLM calls (request + continuation)")
    print("   - Tool call details in span attributes")


if __name__ == "__main__":
    main()
