#!/usr/bin/env python3
"""
03 - Workflow Builder: Conditional routing with MAF WorkflowBuilder.

Shows how to build complex workflows with conditional routing,
where the path depends on structured output from agents.
Uses technical_documentation template for the writing phase.

WHAT YOU'LL LEARN:
- MAF WorkflowBuilder usage
- Conditional routing with structured output
- Complex workflow tracing with templates

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]'

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key

USES TEMPLATE:
    technical_documentation - For the documentation writer agent

WORKFLOW:
    Writer → Reviewer → [if score >= 80: Publisher | else: Editor → Publisher]
"""

import asyncio
import os
from typing import Any

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from pydantic import BaseModel

from dakora import Dakora

load_dotenv()


# Structured output for review
class ReviewResult(BaseModel):
    """Review evaluation with scores."""

    score: int  # 0-100
    feedback: str
    approved: bool


# Routing conditions
def needs_editing(message: Any) -> bool:
    """Route to editor if score < 80."""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        review = ReviewResult.model_validate_json(message.agent_run_response.text)
        return review.score < 80
    except Exception:
        return False


def is_approved(message: Any) -> bool:
    """Route to publisher if score >= 80."""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        review = ReviewResult.model_validate_json(message.agent_run_response.text)
        return review.score >= 80
    except Exception:
        return True


async def main() -> None:
    """Run a content review workflow with conditional routing."""

    # Setup Dakora
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY", "dk_proj_..."),
        base_url=os.getenv("DAKORA_BASE_URL", "http://localhost:8000"),
    )

    middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)

    print("=" * 60)
    print("Workflow Builder: Documentation Review Pipeline")
    print("=" * 60)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    chat_client = OpenAIChatClient(model_id=model)

    # Code to document
    # Note: technical_documentation is a default template auto-created for each project
    code_to_document = '''async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    timeout: float = 30.0,
    backoff_factor: float = 2.0
) -> dict:
    """Fetch data from URL with exponential backoff retry logic."""
    last_error = None
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            last_error = e
            if attempt < max_retries - 1:
                await asyncio.sleep(backoff_factor ** attempt)
    raise last_error'''

    # Render technical_documentation template
    doc_prompt = await dakora.prompts.render(
        "technical_documentation",
        {
            "code_snippet": code_to_document,
            "doc_sections": ["Overview", "Parameters", "Returns", "Raises", "Examples"],
            "example_count": 2,
            "include_troubleshooting": True,
        },
    )
    print(f"Template: technical_documentation v{doc_prompt.version}")

    # Create agents
    writer = chat_client.create_agent(
        id="doc-writer-v1",
        name="DocWriter",
        instructions=f"You are a technical documentation writer. Generate documentation based on this prompt:\n\n{doc_prompt.text}",
        middleware=[middleware],
    )

    reviewer = chat_client.create_agent(
        id="doc-reviewer-v1",
        name="DocReviewer",
        instructions="""You are a technical documentation reviewer.
Evaluate documentation based on:
1. Clarity - Is it easy to understand?
2. Completeness - Does it cover all parameters, return values, and exceptions?
3. Accuracy - Is the information correct?
4. Examples - Are the examples helpful and runnable?

Return a JSON object with:
{
  "score": <overall quality 0-100>,
  "feedback": "<concise, actionable feedback>",
  "approved": <true if score >= 80>
}""",
        response_format=ReviewResult,
        middleware=[middleware],
    )

    editor = chat_client.create_agent(
        id="doc-editor-v1",
        name="DocEditor",
        instructions="You are a technical editor. Improve the documentation based on reviewer feedback. Fix issues, enhance clarity, and add missing information.",
        middleware=[middleware],
    )

    publisher = chat_client.create_agent(
        id="doc-publisher-v1",
        name="DocPublisher",
        instructions="You are a documentation publisher. Format the final documentation with proper markdown structure, consistent headers, and clean presentation.",
        middleware=[middleware],
    )

    # Build workflow with conditional routing
    workflow = (
        WorkflowBuilder(
            name="Documentation Review Workflow",
            description="Write → Review → (Edit if needed) → Publish",
        )
        .set_start_executor(writer)
        .add_edge(writer, reviewer)
        .add_edge(
            reviewer, publisher, condition=is_approved
        )  # Direct to publish if good
        .add_edge(reviewer, editor, condition=needs_editing)  # Edit if needs work
        .add_edge(editor, publisher)  # Editor output goes to publisher
        .build()
    )

    print("\nWorkflow built:")
    print("  DocWriter → DocReviewer")
    print("  DocReviewer → DocPublisher (if score >= 80)")
    print("  DocReviewer → DocEditor → DocPublisher (if score < 80)")

    # Run the workflow
    print("\n" + "-" * 40)
    print("Running workflow...")
    print("-" * 40)

    task = f"Document this code:\n\n```python\n{code_to_document}\n```"
    print("\nTask: Document the fetch_with_retry function")

    result = await workflow.run(task)

    # Get outputs
    outputs = result.get_outputs()
    final_output = outputs[-1] if outputs else "No output"

    print("\n" + "-" * 40)
    print("Workflow Complete!")
    print("-" * 40)
    print(f"\nFinal documentation:\n{str(final_output)[:800]}...")

    # Cleanup
    print("\nFlushing traces...")
    DakoraIntegration.force_flush()
    await dakora.close()

    print("\n✅ Done! Check Dakora Studio to see:")
    print("   - Complete workflow execution path")
    print("   - Which route was taken (approved vs edited)")
    print("   - Each agent's contribution to the pipeline")
    print("   - Template: technical_documentation linked to writer")


if __name__ == "__main__":
    asyncio.run(main())
