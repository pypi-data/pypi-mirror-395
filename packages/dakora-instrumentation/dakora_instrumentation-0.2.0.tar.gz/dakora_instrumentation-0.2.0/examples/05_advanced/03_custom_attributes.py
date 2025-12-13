#!/usr/bin/env python3
"""
03 - Custom Attributes: Add business context to spans.

Shows how to add custom attributes to OpenTelemetry spans for
richer observability and filtering in Dakora Studio. Uses the
faq_responder template for a customer support scenario.

WHAT YOU'LL LEARN:
- Adding custom span attributes
- Creating nested spans
- Business context in traces with templates

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATE:
    faq_responder - For customer support FAQ responses
"""

import asyncio
import os
import uuid

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from opentelemetry import trace

from dakora import Dakora

load_dotenv()


async def main() -> None:
    """Run with custom span attributes and FAQ template."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("Custom Attributes Example with Templates")
    print("=" * 60)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    tracer = trace.get_tracer("custom-attributes-example")

    # Simulate a customer support scenario with business context
    # Note: faq_responder is a default template auto-created for each project
    customer_id = f"cust-{uuid.uuid4().hex[:8]}"
    ticket_id = f"ticket-{uuid.uuid4().hex[:8]}"
    support_tier = "premium"

    print("\nSimulating customer support request:")
    print(f"  Customer ID: {customer_id}")
    print(f"  Ticket ID: {ticket_id}")
    print(f"  Support Tier: {support_tier}")

    # Customer support knowledge base
    support_kb = """
**Billing & Subscription Support**

Duplicate Charges:
- Review transaction history in customer portal
- Duplicate charges are automatically refunded within 5-7 business days
- If charge persists after 7 days, escalate to billing team
- Reference: KB-BILLING-001

Refund Policy:
- Full refunds available within 30 days of purchase
- Pro-rated refunds for annual subscriptions after 30 days
- Refunds processed to original payment method
- Processing time: 3-5 business days

Contact Escalation:
- Tier 1: Chat/Email support
- Tier 2: Phone support for premium customers
- Tier 3: Account manager for enterprise
    """.strip()

    # Create a span with custom business attributes
    with tracer.start_as_current_span("customer-support-request") as span:
        # Add business context as span attributes
        span.set_attribute("customer.id", customer_id)
        span.set_attribute("support.ticket_id", ticket_id)
        span.set_attribute("support.tier", support_tier)
        span.set_attribute("support.channel", "chat")
        span.set_attribute("support.category", "billing")

        print("\nProcessing support request...")

        # First: Understand the issue using faq_responder
        with tracer.start_as_current_span("analyze-issue") as child_span:
            child_span.set_attribute("step", "analysis")

            # Render faq_responder for initial analysis
            analysis_prompt = await dakora.prompts.render(
                "faq_responder",
                {
                    "question": "Customer reports: I was charged twice for my subscription last month. What should I do?",
                    "knowledge_base": support_kb,
                    "tone": "analytical and thorough",
                    "include_sources": True,
                },
            )

            agent = ChatAgent(
                id="support-analyzer-v1",
                name="SupportAnalyzer",
                chat_client=OpenAIChatClient(model_id=model),
                instructions=f"You are a support analyst. Analyze this issue:\n\n{analysis_prompt.text}",
                middleware=[middleware],
            )

            result = await agent.run(
                "Analyze this billing issue and identify the resolution path"
            )

            child_span.set_attribute("issue.type", "duplicate_charge")
            child_span.set_attribute("issue.identified", True)
            print(f"\nAnalysis ({len(result.messages[0].text)} chars):")
            print(result.messages[0].text[:300] + "...")

        # Second: Generate customer response
        with tracer.start_as_current_span("generate-response") as child_span:
            child_span.set_attribute("step", "response-generation")
            child_span.set_attribute("response.type", "empathetic")

            # Render faq_responder for customer-facing response
            response_prompt = await dakora.prompts.render(
                "faq_responder",
                {
                    "question": "I was charged twice for my subscription. Can you help?",
                    "knowledge_base": support_kb,
                    "tone": "empathetic, professional, and reassuring",
                    "include_sources": False,
                },
            )

            response_agent = ChatAgent(
                id="support-responder-v1",
                name="SupportResponder",
                chat_client=OpenAIChatClient(model_id=model),
                instructions=f"You are a customer support representative for a premium customer. Generate a response based on:\n\n{response_prompt.text}",
                middleware=[middleware],
            )

            result = await response_agent.run(
                "Draft a helpful response to the customer about their duplicate charge"
            )

            child_span.set_attribute("response.generated", True)
            child_span.set_attribute("response.length", len(result.messages[0].text))

            print(f"\nCustomer Response:\n{result.messages[0].text}")

        # Mark resolution
        span.set_attribute("support.resolved", True)
        span.set_attribute("support.resolution_type", "refund_initiated")
        span.set_attribute("template.used", "faq_responder")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Parent span: 'customer-support-request'")
    print("   - Custom attributes: customer.id, ticket_id, tier")
    print("   - Child spans: 'analyze-issue', 'generate-response'")
    print("   - Template: faq_responder used in both steps")
    print("   - Filter by: support.tier='premium' or support.category='billing'")


if __name__ == "__main__":
    asyncio.run(main())
