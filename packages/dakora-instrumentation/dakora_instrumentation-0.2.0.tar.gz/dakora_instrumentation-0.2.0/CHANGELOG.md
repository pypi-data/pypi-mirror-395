# Changelog

All notable changes to Dakora Instrumentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-XX

### 🎉 Initial Release

Dakora Instrumentation provides OpenTelemetry integration for LLM observability.
Dakora acts as an OTLP backend - point your instrumented applications at Dakora's `/api/v1/traces` endpoint.

### Added

- **Generic OTLP Setup**
  - `setup_instrumentation()` helper for configuring OTLP export to Dakora
  - Works with any OTEL-instrumented SDK (OpenAI, Anthropic, etc.)
  - Multi-export support (send traces to multiple backends simultaneously)
  - Optional auto-detection of installed providers

- **Framework Integrations**
  - Microsoft Agent Framework (MAF) with `DakoraIntegration` helper
  - Budget enforcement with configurable caching
  - Template linkage with Dakora prompts
  - Context manager support for automatic span flushing

- **Automatic Tracking**
  - Agent ID and conversation context (MAF)
  - Token usage and cost calculation
  - Latency and performance metrics
  - Full conversation history (configurable)

- **Package Structure**
  - `frameworks/maf/` - Microsoft Agent Framework integration
  - `generic.py` - Generic OTEL setup helper
  - `_internal/` - Shared internal utilities

- **Examples**
  - MAF integration examples
  - OpenAI/Anthropic with manual instrumentation
  - Multi-provider examples
  - Diagnostic verification script

- **Quality**
  - Comprehensive test suite (24 tests)
  - Type hints throughout
  - Detailed documentation and docstrings

### Installation

```bash
# Generic (BYO OTEL)
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-instrumentation-openai  # or anthropic, etc.
pip install dakora-instrumentation

# MAF (batteries included)
pip install 'dakora-instrumentation[maf]'
```

---

[1.0.0]: https://github.com/dakora-labs/dakora/releases/tag/dakora-instrumentation-v1.0.0
