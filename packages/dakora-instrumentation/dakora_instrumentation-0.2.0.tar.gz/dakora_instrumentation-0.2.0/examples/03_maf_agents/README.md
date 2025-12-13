# MAF Agent Examples

Examples using Microsoft Agent Framework (MAF) with Dakora instrumentation.
MAF provides a higher-level abstraction for building AI agents.

## Examples

| File                        | Description                  | What You Learn               |
| --------------------------- | ---------------------------- | ---------------------------- |
| `01_simple_agent.py`        | Basic agent without tools    | MAF + Dakora setup           |
| `02_agent_with_tools.py`    | Agent with tool functions    | Tool execution tracing       |
| `03_agent_with_template.py` | Agent using Dakora templates | Template-driven instructions |
| `04_conversation.py`        | Multi-turn conversation      | Conversation tracking        |

## Prerequisites

```bash
# MAF integration bundles OTEL dependencies
pip install 'dakora-instrumentation[maf]'
```

## Key Concepts

### DakoraIntegration Middleware

The MAF integration provides middleware that automatically:

- Configures OpenTelemetry exporters
- Captures agent metadata (ID, name)
- Tracks token usage and latency
- Links templates to executions

```python
from dakora_instrumentation.frameworks.maf import DakoraIntegration

middleware = DakoraIntegration.setup(dakora)
agent = ChatAgent(
    ...,
    middleware=[middleware],  # One line to add observability
)
```

### Template-Driven Agents

Use Dakora templates for agent instructions:

```python
instructions = await dakora.prompts.render(
    "weather_agent",
    {"region": "Pacific Northwest"}
)
agent = ChatAgent(instructions=instructions.text, ...)
```
