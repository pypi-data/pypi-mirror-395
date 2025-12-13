#!/usr/bin/env python3
"""
01 - Sequential Agents: Research → Writer pipeline.

Shows how to chain multiple agents sequentially, where the output
of one agent feeds into the next. Uses research_synthesizer to gather
and analyze information, then social_media_campaign to create content.

WHAT YOU'LL LEARN:
- Sequential agent orchestration
- Shared middleware pattern
- Pipeline trace visualization
- Using standard templates in pipelines

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATES:
    research_synthesizer - For the researcher agent
    social_media_campaign - For the content creator agent
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
    """Run a research → content creation pipeline with Dakora tracking."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    # Single middleware for all agents
    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("Sequential Agents: Research → Content Creation Pipeline")
    print("=" * 60)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    tracer = trace.get_tracer(__name__)

    # Topic: AI in Education
    topic = "the impact of AI on education and learning"

    # Step 1: Research phase - synthesize multiple sources
    # Note: research_synthesizer and social_media_campaign are default templates
    print("\n" + "-" * 40)
    print("Step 1: Research Phase - Synthesizing Sources")
    print("-" * 40)

    # Render research_synthesizer template
    research_prompt = await dakora.prompts.render(
        "research_synthesizer",
        {
            "research_question": f"What are the main benefits and challenges of {topic}?",
            "sources": [
                "[UNESCO Report, 2023] AI tutoring systems can provide personalized learning paths. Students show 30% improvement in engagement. However, digital divide remains a concern.",
                "[Stanford HAI, 2024] AI writing assistants help students improve writing skills. Teachers report mixed feelings about AI use in assignments. Clear policies needed.",
                "[EdTech Magazine, 2024] Schools using AI-powered analytics see better student outcomes. Implementation costs remain high. Teacher training is essential for success.",
                "[MIT Technology Review, 2024] AI can automate administrative tasks, freeing teacher time. Concerns about data privacy in educational AI. Students need AI literacy skills.",
            ],
            "citation_style": "APA",
            "max_sources": 5,
            "output_format": "bullet points with key themes",
        },
    )
    print(f"Template: research_synthesizer v{research_prompt.version}")

    # Create researcher agent with rendered template
    researcher = ChatAgent(
        id="researcher-v1",
        name="Researcher",
        chat_client=OpenAIChatClient(model_id=model),
        instructions=f"You are a research analyst. Use this prompt to synthesize information:\n\n{research_prompt.text}",
        middleware=[middleware],
    )

    # Run pipeline in a parent span
    with tracer.start_as_current_span("research-to-campaign-pipeline"):
        # Execute research
        print(f"\nAnalyzing topic: {topic}")
        research_result = await researcher.run(f"Synthesize the research on: {topic}")
        research_text = research_result.messages[0].text

        print(f"\nResearch output ({len(research_text)} chars):")
        print(
            research_text[:400] + "..." if len(research_text) > 400 else research_text
        )

        # Step 2: Content creation phase
        print("\n" + "-" * 40)
        print("Step 2: Content Creation Phase")
        print("-" * 40)

        # Render social_media_campaign template
        campaign_prompt = await dakora.prompts.render(
            "social_media_campaign",
            {
                "campaign_brief": f"Create engaging social media content about {topic}, based on this research:\n\n{research_text[:500]}",
                "platforms": ["Twitter", "LinkedIn"],
                "hashtags": ["AIinEducation", "EdTech", "FutureOfLearning"],
                "include_image_prompts": True,
            },
        )
        print(f"Template: social_media_campaign v{campaign_prompt.version}")

        # Create content creator agent
        content_creator = ChatAgent(
            id="content-creator-v1",
            name="ContentCreator",
            chat_client=OpenAIChatClient(model_id=model),
            instructions=f"You are a social media content creator. Use this prompt:\n\n{campaign_prompt.text}",
            middleware=[middleware],
        )

        # Execute content creation
        campaign_result = await content_creator.run(
            "Create the social media campaign posts"
        )
        campaign_text = campaign_result.messages[0].text

        print(f"\nCampaign output ({len(campaign_text)} chars):")
        print(
            campaign_text[:600] + "..." if len(campaign_text) > 600 else campaign_text
        )

    # Cleanup
    print("\n" + "-" * 40)
    print("Pipeline Complete!")
    print("-" * 40)

    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Parent span: 'research-to-campaign-pipeline'")
    print("   - Child spans: researcher, content_creator")
    print("   - Templates: research_synthesizer, social_media_campaign")
    print("   - Total pipeline cost and latency")


if __name__ == "__main__":
    asyncio.run(main())
