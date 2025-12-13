# Provider Examples (BYO OpenTelemetry)

These examples show how to instrument different LLM providers using the
"Bring Your Own OpenTelemetry" pattern. You manually install and configure
OTEL dependencies, giving you full control over the setup.

## Examples

| File                      | Description                 | What You Learn                 |
| ------------------------- | --------------------------- | ------------------------------ |
| `01_openai_basic.py`      | OpenAI without tools        | Basic provider instrumentation |
| `02_openai_with_tools.py` | OpenAI with tool calls      | Tool execution tracing         |
| `03_anthropic_basic.py`   | Anthropic Claude            | Multi-provider support         |
| `04_multi_provider.py`    | OpenAI + Anthropic together | Combined instrumentation       |

## Prerequisites

```bash
# Core OpenTelemetry
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http

# Provider instrumentations (choose what you need)
pip install opentelemetry-instrumentation-openai openai
pip install opentelemetry-instrumentation-anthropic anthropic

# Dakora
pip install dakora-client dakora-instrumentation
```

## Key Concepts

### Global Instrumentation

Provider instrumentors work globally - call `.instrument()` once at startup:

```python
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
OpenAIInstrumentor().instrument()  # Patches ALL OpenAI clients
```

### Manual Spans

Create parent spans to group related calls:

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-workflow"):
    # All LLM calls here become child spans
    response = client.chat.completions.create(...)
```

### Tool Call Tracing

When using tools, both the initial call and tool response continuation
are captured as separate spans, linked in the trace hierarchy.
