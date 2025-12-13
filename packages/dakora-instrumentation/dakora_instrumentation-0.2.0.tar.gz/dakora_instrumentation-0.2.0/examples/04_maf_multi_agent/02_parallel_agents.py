#!/usr/bin/env python3
"""
02 - Parallel Agents: Run multiple agents concurrently.

Shows how to run multiple agents in parallel using asyncio.gather,
with all executions tracked in a single parent trace. Uses the
faq_responder template with different tones for each perspective.

WHAT YOU'LL LEARN:
- Concurrent agent execution
- Parallel trace visualization
- Comparing agent responses with same template, different parameters

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATE:
    faq_responder - Same template, different tone parameters for each agent
"""

import asyncio
import os

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from opentelemetry import trace

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Run multiple agents in parallel with Dakora tracking."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("Parallel Agents Example with Templates")
    print("=" * 60)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    tracer = trace.get_tracer(__name__)

    # Shared knowledge base about the topic
    # Note: faq_responder is a default template auto-created for each project
    knowledge_base = """
**AI-Powered Productivity App Analysis**

Market Data:
- Productivity app market valued at $92B in 2024
- AI integration increases user retention by 40%
- Average user spends 3.2 hours daily on productivity tools

Technical Considerations:
- GPT-4 integration costs approximately $0.03 per request
- Privacy concerns affect 68% of enterprise decisions
- Cloud infrastructure requirements vary by scale

User Research:
- 73% of users want AI to automate repetitive tasks
- 45% worry about AI making mistakes
- Premium pricing accepted for reliable AI features
    """.strip()

    question = "Should we launch a new AI-powered productivity app?"

    # Render three variations of faq_responder with different tones
    analyst_prompt = await dakora.prompts.render(
        "faq_responder",
        {
            "question": question,
            "knowledge_base": knowledge_base,
            "tone": "analytical and data-focused - cite numbers and metrics",
            "include_sources": True,
        },
    )

    strategist_prompt = await dakora.prompts.render(
        "faq_responder",
        {
            "question": question,
            "knowledge_base": knowledge_base,
            "tone": "strategic and opportunity-focused - highlight market potential",
            "include_sources": True,
        },
    )

    critic_prompt = await dakora.prompts.render(
        "faq_responder",
        {
            "question": question,
            "knowledge_base": knowledge_base,
            "tone": "critical and risk-focused - identify potential problems",
            "include_sources": True,
        },
    )

    print(f"Template: faq_responder v{analyst_prompt.version} (3 variations)")

    # Create three specialized agents with different rendered prompts
    analyst = ChatAgent(
        id="analyst-v1",
        name="Analyst",
        chat_client=OpenAIChatClient(model_id=model),
        instructions=f"Respond to this analysis request:\n\n{analyst_prompt.text}",
        middleware=[middleware],
    )

    strategist = ChatAgent(
        id="strategist-v1",
        name="Strategist",
        chat_client=OpenAIChatClient(model_id=model),
        instructions=f"Respond to this strategic question:\n\n{strategist_prompt.text}",
        middleware=[middleware],
    )

    critic = ChatAgent(
        id="critic-v1",
        name="Critic",
        chat_client=OpenAIChatClient(model_id=model),
        instructions=f"Respond to this risk assessment:\n\n{critic_prompt.text}",
        middleware=[middleware],
    )

    # Run all agents in parallel within a parent span
    with tracer.start_as_current_span("parallel-analysis-faq"):
        print(f"\nQuestion: {question}")
        print("\nRunning three agents in parallel...")
        print("(Same template, different tone parameters)")

        # Execute concurrently
        results = await asyncio.gather(
            analyst.run("Provide your analysis"),
            strategist.run("Provide your strategic view"),
            critic.run("Provide your risk assessment"),
        )

        analyst_result, strategist_result, critic_result = results

    # Display results
    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)

    print("\n[Analyst - Data-Focused]")
    print("-" * 40)
    text = analyst_result.messages[0].text
    print(text[:400] + "..." if len(text) > 400 else text)

    print("\n[Strategist - Opportunity-Focused]")
    print("-" * 40)
    text = strategist_result.messages[0].text
    print(text[:400] + "..." if len(text) > 400 else text)

    print("\n[Critic - Risk-Focused]")
    print("-" * 40)
    text = critic_result.messages[0].text
    print(text[:400] + "..." if len(text) > 400 else text)

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Parent span: 'parallel-analysis-faq'")
    print("   - Three child spans running in parallel")
    print("   - Template: faq_responder used by all three")
    print("   - Compare: same template, different tone parameters")


if __name__ == "__main__":
    asyncio.run(main())
