# Dakora Instrumentation Examples

Progressive examples for learning Dakora instrumentation, from basic setup to production patterns.

## Quick Start

```bash
# Choose your integration style:

# Option A: BYO OpenTelemetry (full control)
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-instrumentation-openai openai
pip install dakora dakora-instrumentation

# Option B: MAF Integration (batteries included)
pip install 'dakora-instrumentation[maf]'
```

## Example Organization

Examples are organized by complexity and use case. Start with `01_quickstart` and progress through as needed.

### 📁 01_quickstart/ - Start Here

The simplest possible examples to get traces flowing to Dakora.

| File                  | Description                   | Dependencies      |
| --------------------- | ----------------------------- | ----------------- |
| `01_hello_world.py`   | Single LLM call with tracing  | BYO OTEL + OpenAI |
| `02_with_template.py` | Add Dakora template rendering | BYO OTEL + OpenAI |

```bash
python 01_quickstart/01_hello_world.py
```

### 📁 02_providers/ - BYO OpenTelemetry Patterns

Manual instrumentation for different LLM providers.

| File                      | Description                 | Dependencies           |
| ------------------------- | --------------------------- | ---------------------- |
| `01_openai_basic.py`      | OpenAI without tools        | OpenAI instrumentor    |
| `02_openai_with_tools.py` | OpenAI with tool calls      | OpenAI instrumentor    |
| `03_anthropic_basic.py`   | Anthropic Claude            | Anthropic instrumentor |
| `04_multi_provider.py`    | OpenAI + Anthropic together | Both instrumentors     |

```bash
python 02_providers/01_openai_basic.py
```

### 📁 03_maf_agents/ - MAF Agent Framework

Higher-level agent patterns with Microsoft Agent Framework.

| File                        | Description               | Dependencies  |
| --------------------------- | ------------------------- | ------------- |
| `01_simple_agent.py`        | Basic MAF agent           | `[maf]` extra |
| `02_agent_with_tools.py`    | Agent with tool functions | `[maf]` extra |
| `03_agent_with_template.py` | Template-driven agent     | `[maf]` extra |
| `04_conversation.py`        | Multi-turn conversation   | `[maf]` extra |

```bash
python 03_maf_agents/01_simple_agent.py
```

### 📁 04_maf_multi_agent/ - Multi-Agent Orchestration

Complex workflows with multiple agents.

| File                      | Description                  | Dependencies  |
| ------------------------- | ---------------------------- | ------------- |
| `01_sequential_agents.py` | Research → Writer pipeline   | `[maf]` extra |
| `02_parallel_agents.py`   | Concurrent agent execution   | `[maf]` extra |
| `03_workflow_builder.py`  | Conditional routing workflow | `[maf]` extra |

```bash
python 04_maf_multi_agent/01_sequential_agents.py
```

### 📁 05_advanced/ - Production Patterns

Advanced patterns for production deployments.

| File                      | Description                     | Dependencies     |
| ------------------------- | ------------------------------- | ---------------- |
| `01_dual_export.py`       | Export to Dakora + Jaeger       | `[maf]` + Jaeger |
| `02_budget_checking.py`   | Pre-execution budget validation | `[maf]` extra    |
| `03_custom_attributes.py` | Custom span attributes          | `[maf]` extra    |

```bash
python 05_advanced/01_dual_export.py
```

### 📁 shared/ - Common Utilities

Shared templates and utilities used across examples.

| File           | Description                          |
| -------------- | ------------------------------------ |
| `templates.py` | Standard Dakora template definitions |

## Environment Setup

Create a `.env` file in this directory (copy from `.env.example`):

```bash
# Required
DAKORA_API_KEY=dk_proj_...
OPENAI_API_KEY=sk-...

# Optional
DAKORA_BASE_URL=http://localhost:8000
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
JAEGER_ENDPOINT=http://localhost:4317
```

## Templates Used

These examples use Dakora's standard sample templates:

| Template ID               | Use Case                 | Complexity   |
| ------------------------- | ------------------------ | ------------ |
| `faq_responder`           | FAQ/support responses    | Starter      |
| `research_synthesizer`    | Multi-source research    | Intermediate |
| `technical_documentation` | Code documentation       | Intermediate |
| `social_media_campaign`   | Multi-platform content   | Intermediate |
| `simple_assistant`        | Basic agent instructions | Starter      |
| `weather_agent`           | Agent with tools         | Starter      |
| `research_agent`          | Multi-agent workflows    | Intermediate |
| `writer_agent`            | Content creation         | Intermediate |
| `reviewer_agent`          | Quality review           | Intermediate |

Templates are automatically created if they don't exist when running examples.

## Running with uv

If using uv for development:

```bash
# BYO OTEL examples
cd packages/instrumentation
uv run python examples/01_quickstart/01_hello_world.py

# MAF examples
uv run --extra maf python examples/03_maf_agents/01_simple_agent.py
```

## Troubleshooting

### ModuleNotFoundError: opentelemetry.instrumentation

Install the required OpenTelemetry packages:

```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-instrumentation-openai
```

### ModuleNotFoundError: agent_framework

Install the MAF extra:

```bash
pip install 'dakora-instrumentation[maf]'
```

### API Key Errors

Ensure your `.env` file contains valid API keys and is in the examples directory.

### Template Not Found

Templates are auto-created on first run. Ensure your Dakora server is running:

```bash
cd server
uv run uvicorn dakora_server.main:app --reload --port 8000
```

## Support

- [Documentation](https://docs.dakora.io)
- [GitHub Issues](https://github.com/dakora-labs/dakora/issues)
