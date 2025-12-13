# Dakora Instrumentation

**OTLP backend for LLM observability**

[![PyPI version](https://badge.fury.io/py/dakora-instrumentation.svg)](https://pypi.org/project/dakora-instrumentation/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Dakora accepts OpenTelemetry traces via OTLP/HTTP. This package provides:

1. **Generic helper** - Thin wrapper to configure OTEL exporters pointing to Dakora
2. **Framework integrations** - Batteries-included support for Microsoft Agent Framework (MAF)
   - LangChain, CrewAI, and more coming soon

## Features

✅ **OTLP Backend** - Point your existing OTEL setup at Dakora  
✅ **Multi-Export** - Send traces to Dakora + Jaeger/Grafana/Azure Monitor  
✅ **BYO OpenTelemetry** - Use your own OTEL versions, no dependency conflicts  
✅ **Framework Integrations** - Batteries-included MAF support  
✅ **Template Linkage** - Track Dakora prompts used in executions  
✅ **Budget Enforcement** - Pre-execution checks with caching (MAF integration)

---

## Architecture

```
Your App → OTEL SDK → Instrumentation → OTLP Exporter → Dakora API
                                                    ↓
                                            /api/v1/traces
                                         (with X-API-Key header)
```

---

## Quick Start

### 1. With OpenTelemetry Collector (Recommended)

Already running a collector? Just add Dakora as an exporter:

```yaml
# otel-collector-config.yaml
exporters:
  otlphttp/dakora:
    endpoint: ${DAKORA_BASE_URL}/api/v1/traces
    headers:
      X-API-Key: ${DAKORA_API_KEY}

service:
  pipelines:
    traces:
      exporters: [otlphttp/dakora, jaeger, ...] # Multi-export!
```

### 2. Direct Integration (Python)

#### Step 1: Install OpenTelemetry + Instrumentations

```bash
# Core OTEL
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http

# Provider instrumentations (choose what you need)
pip install opentelemetry-instrumentation-openai
pip install opentelemetry-instrumentation-anthropic

# Dakora helper (optional convenience)
pip install dakora-instrumentation
```

#### Step 2: Instrument Your Providers

```python
# Do this once at application startup
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

OpenAIInstrumentor().instrument()
AnthropicInstrumentor().instrument()
```

#### Step 3: Configure Dakora Exporter

```python
from dakora import Dakora
from dakora_instrumentation import setup_instrumentation

dakora = Dakora(api_key="dk_proj_...")
setup_instrumentation(dakora, service_name="my-app")

# That's it! All instrumented SDKs now export to Dakora
```

### 2. With Microsoft Agent Framework (Batteries Included)

```bash
pip install 'dakora-instrumentation[maf]'
```

```python
from dakora import Dakora
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from agent_framework.azure import AzureOpenAIChatClient

# Initialize Dakora
dakora = Dakora(api_key="dk_proj_...")

# One-line OTEL setup
middleware = DakoraIntegration.setup(dakora)

# Use with any MAF client
azure_client = AzureOpenAIChatClient(
    endpoint=...,
    deployment_name=...,
    api_key=...,
    middleware=[middleware],
)

agent = azure_client.create_agent(
    id="chat-v1",
    name="ChatBot",
    instructions="You are helpful.",
)

response = await agent.run("Hello!")
```

---

## Package Structure

```text
dakora_instrumentation/
├── frameworks/maf/          # Microsoft Agent Framework integration
├── generic.py               # Generic OTEL setup helper
└── _internal/               # Internal utilities (private)
```

**Public API:**

```python
from dakora_instrumentation import setup_instrumentation
from dakora_instrumentation.frameworks.maf import DakoraIntegration
```

---

## Examples

See `examples/` directory for progressive examples:

- `01_quickstart/` - Start here: basic setup and template usage
- `02_providers/` - BYO OTEL patterns (OpenAI, Anthropic, multi-provider)
- `03_maf_agents/` - MAF agent patterns (simple, tools, templates)
- `04_maf_multi_agent/` - Multi-agent orchestration (sequential, parallel, workflows)
- `05_advanced/` - Production patterns (dual export, budget checking, custom attributes)

---

## FAQ

**Q: Do I need to install `dakora-instrumentation`?**

No! If you already have OTEL configured, point your exporter at Dakora's OTLP endpoint:
`${DAKORA_BASE_URL}/api/v1/traces` with `X-API-Key` header.
This package provides convenience helpers.

**Q: How do I install provider instrumentations?**

Install them directly from the opentelemetry-instrumentation packages:

```bash
pip install opentelemetry-instrumentation-openai
pip install opentelemetry-instrumentation-anthropic
```

**Q: When should I use which integration?**

- **Generic `setup_instrumentation()`** - For direct SDK calls (OpenAI, Anthropic, etc.)
- **MAF Integration** - For Microsoft Agent Framework agents (batteries included)

**Q: Do I need to instrument providers manually?**

Yes, OpenTelemetry instrumentation is global:

```python
OpenAIInstrumentor().instrument()  # Do once at startup
```

**Q: Can I send traces to multiple backends?**

Yes! Use `additional_exporters` parameter:

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

jaeger_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
setup_instrumentation(dakora, additional_span_exporters=[jaeger_exporter])
```

**Q: Does this work with LangChain/CrewAI?**

Not yet, but support is coming! Use generic `setup_instrumentation()` for now.

---

## Links

- **Documentation**: https://docs.dakora.io
- **GitHub**: https://github.com/dakora-labs/dakora
- **Issues**: https://github.com/dakora-labs/dakora/issues
- **Support**: support@dakora.io

---

## License

Apache License 2.0
