# Quickstart Examples

The simplest way to get started with Dakora instrumentation.

## Examples

| File                  | Description            | What You Learn                         |
| --------------------- | ---------------------- | -------------------------------------- |
| `01_hello_world.py`   | Absolute minimum setup | Single LLM call with OTEL tracing      |
| `02_with_template.py` | Add Dakora templates   | Template rendering + automatic linking |

## Prerequisites

```bash
# Install OpenTelemetry + OpenAI instrumentation
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-instrumentation-openai openai

# Install Dakora
pip install dakora-client dakora-instrumentation
```

## Running

```bash
# Set your API keys
export DAKORA_API_KEY=dk_proj_...
export OPENAI_API_KEY=sk-...

# Run examples
python 01_quickstart/01_hello_world.py
python 01_quickstart/02_with_template.py
```

## Key Concepts

1. **OpenTelemetry Instrumentation**: Automatically captures LLM calls
2. **Dakora Exporter**: Sends traces to Dakora for analysis
3. **Template Rendering**: Use managed prompts with automatic version tracking
