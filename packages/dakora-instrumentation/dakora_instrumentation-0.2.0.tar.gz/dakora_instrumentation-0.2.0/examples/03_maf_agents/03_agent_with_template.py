#!/usr/bin/env python3
"""
03 - Agent with Template and Tools: Dakora templates + documentation tools.

Shows how to use Dakora's template management to define agent instructions,
combined with tools that read real documentation from local files.

WHAT YOU'LL LEARN:
- Using templates for agent instructions
- Template version tracking in traces
- Adding tools that read local documentation
- Parameterized agent behavior

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATES:
    faq_responder - FAQ support agent
    technical_documentation - Code documentation agent
"""

import asyncio
import os
from pathlib import Path
from typing import Annotated, Any, cast

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from pydantic import Field

from dakora import Dakora

load_dotenv()

# Path to the docs folder - adjust this based on your setup
# In a real deployment, this could be an environment variable
DOCS_PATH = Path(__file__).parent.parent.parent.parent.parent / "docs"

# Map topics to their documentation files
DOCS_MAPPING: dict[str, str] = {
    "quickstart": "getting-started/quickstart.mdx",
    "getting started": "getting-started/quickstart.mdx",
    "introduction": "getting-started/introduction.mdx",
    "overview": "getting-started/introduction.mdx",
    "templates": "concepts/templates.mdx",
    "inputs": "concepts/inputs.mdx",
    "versioning": "concepts/versioning.mdx",
    "logging": "features/logging.mdx",
    "cli": "features/cli.mdx",
    "integrations": "features/integrations.mdx",
    "playground": "features/playground.mdx",
    "api keys": "guides/api-keys.mdx",
    "authentication": "guides/authentication.mdx",
    "budgets": "guides/project-budgets.mdx",
}


def get_docs(
    topic: Annotated[
        str,
        Field(
            description="The documentation topic to retrieve. Available topics: "
            "quickstart, getting started, introduction, overview, templates, "
            "inputs, versioning, logging, cli, integrations, playground, "
            "api keys, authentication, budgets"
        ),
    ],
) -> str:
    """
    Retrieve Dakora documentation for a specific topic.

    This tool reads documentation from the local docs folder to provide
    accurate, up-to-date information about Dakora features and usage.
    """
    topic_lower = topic.lower().strip()

    # Find matching doc file
    doc_file = DOCS_MAPPING.get(topic_lower)
    if not doc_file:
        # Try partial matching
        for key, value in DOCS_MAPPING.items():
            if topic_lower in key or key in topic_lower:
                doc_file = value
                break

    if not doc_file:
        available = ", ".join(sorted(set(DOCS_MAPPING.keys())))
        return f"Topic '{topic}' not found. Available topics: {available}"

    doc_path = DOCS_PATH / doc_file

    if not doc_path.exists():
        return f"Documentation file not found: {doc_file}"

    try:
        content = doc_path.read_text(encoding="utf-8")
        # Return first 3000 chars to keep response manageable
        if len(content) > 3000:
            content = content[:3000] + "\n\n... (truncated for brevity)"
        return f"# Documentation: {topic}\n\nSource: {doc_file}\n\n{content}"
    except Exception as e:
        return f"Error reading documentation: {e}"


async def main() -> None:
    """Run agents with Dakora template-driven instructions and documentation tools."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("MAF Agent with Template + Documentation Tools")
    print("=" * 60)
    print(f"Docs path: {DOCS_PATH}")
    print(f"Docs exist: {DOCS_PATH.exists()}")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Example 1: FAQ agent with get_docs tool
    # The agent can now fetch real documentation to answer questions
    print("\n" + "-" * 40)
    print("1. FAQ Agent with Documentation Tool")
    print("-" * 40)

    faq_agent = ChatAgent(
        id="faq-docs-agent-v1",
        name="FAQDocsAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions="""You are a helpful Dakora support agent.
When users ask questions about Dakora, use the get_docs tool to retrieve
accurate documentation before answering. Always base your answers on the
official documentation.

Be friendly and encouraging. If the documentation doesn't cover the topic,
say so and suggest where users might find more help.""",
        middleware=[middleware],
        tools=[get_docs],
    )

    cast(Any, faq_agent).instructions = faq_agent.chat_options.instructions  # type: ignore[attr-defined]

    result = await faq_agent.run("How do I get started with Dakora?")
    print(f"\n   Response: {result.messages[0].text[:800]}...")

    # Example 2: Technical agent asking about templates
    print("\n" + "-" * 40)
    print("2. Agent asking about Templates")
    print("-" * 40)

    result = await faq_agent.run("How do templates work in Dakora?")
    print(f"\n   Response: {result.messages[0].text[:800]}...")

    # Example 3: Template-driven agent with documentation context
    # Combines template rendering WITH the get_docs tool
    print("\n" + "-" * 40)
    print("3. Template + Docs Tool Combined")
    print("-" * 40)

    faq_instructions = await dakora.prompts.render(
        "faq_responder",
        {
            "question": "How do I set up API keys?",
            "knowledge_base": """
Use the get_docs tool to fetch the latest documentation about API keys.
The documentation contains accurate, up-to-date information about:
- Creating and managing API keys
- Authentication methods
- Security best practices
            """.strip(),
            "tone": "professional and helpful",
            "include_sources": True,
        },
    )
    print(f"   Template: faq_responder v{faq_instructions.version}")

    template_docs_agent = ChatAgent(
        id="template-docs-agent-v1",
        name="TemplatePlusDocsAgent",
        chat_client=OpenAIChatClient(model_id=model),
        instructions=f"""You are a Dakora expert support agent.

{faq_instructions.text}

You have access to the get_docs tool to retrieve official documentation.
Always verify your answers against the documentation when possible.""",
        middleware=[middleware],
        tools=[get_docs],
    )

    cast(
        Any, template_docs_agent
    ).instructions = template_docs_agent.chat_options.instructions  # type: ignore[attr-defined]

    result = await template_docs_agent.run(
        "How do I create and manage API keys in Dakora?"
    )
    print(f"\n   Response: {result.messages[0].text[:800]}...")

    # Cleanup
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Agent executions with tool calls to get_docs")
    print("   - Template usage: faq_responder")
    print("   - Tool calls showing which docs were fetched")


if __name__ == "__main__":
    asyncio.run(main())
