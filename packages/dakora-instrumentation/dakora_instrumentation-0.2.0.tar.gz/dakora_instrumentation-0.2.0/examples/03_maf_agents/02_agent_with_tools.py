#!/usr/bin/env python3
"""
02 - Agent with Tools: MAF agent with tool functions.

Shows how to add tools to a MAF agent and how tool executions
are automatically traced in Dakora.

WHAT YOU'LL LEARN:
- Adding tools to MAF agents
- How tool calls appear in traces
- Tool execution flow

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
"""

import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from pydantic import Field

from dakora import Dakora

load_dotenv()


# Define tool functions
def get_weather(
    location: Annotated[str, Field(description="The city to get weather for")],
) -> str:
    """Get the current weather for a location."""
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = randint(15, 30)
    return f"Weather in {location}: {conditions[randint(0, 3)]}, {temp}°C"


def get_time(
    timezone: Annotated[str, Field(description="Timezone like 'UTC', 'EST', 'PST'")],
) -> str:
    """Get the current time in a timezone."""
    from datetime import datetime
    from datetime import timezone as tz

    now = datetime.now(tz.utc)
    return f"Current time in {timezone}: {now.strftime('%H:%M:%S')} (simulated)"


async def main() -> None:
    """Run a MAF agent with tools."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("MAF Agent with Tools Example")
    print("=" * 60)

    # Create agent with tools
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    agent = ChatAgent(
        id="weather-agent-v1",
        name="WeatherAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="""You are a helpful weather assistant.
Use the get_weather tool to fetch current weather.
Use the get_time tool to get the current time.
Provide friendly, informative responses.""",
        middleware=[middleware],
        tools=[get_weather, get_time],  # Pass tool functions directly
    )

    # Example 1: Weather query (should trigger tool)
    print("\n1. Asking about weather in Tokyo...")
    result = await agent.run("What's the weather like in Tokyo?")
    print(f"   Response: {result.messages[0].text}")

    # Example 2: Time query (should trigger different tool)
    print("\n2. Asking about time in UTC...")
    result = await agent.run("What time is it in UTC?")
    print(f"   Response: {result.messages[0].text}")

    # Example 3: Combined query (may trigger both tools)
    print("\n3. Asking about weather and time in New York...")
    result = await agent.run("What's the weather and time in New York (EST)?")
    print(f"   Response: {result.messages[0].text}")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Agent executions with tool calls")
    print("   - Tool names and arguments in traces")
    print("   - Total tokens including tool overhead")


if __name__ == "__main__":
    asyncio.run(main())
