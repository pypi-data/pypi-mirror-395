"""
Dakora Instrumentation - OpenTelemetry instrumentation for LLM applications

Provides automatic observability for:
- Agent frameworks (Microsoft Agent Framework, LangChain, CrewAI)
Key features:
- Microsoft Agent Framework (MAF) integration with middleware and helpers
- Generic OTEL instrumentation setup for any Python application
- LLM providers (OpenAI, Anthropic)
- Automatic trace export to Dakora backend
- Generic OpenTelemetry setup

Quick Start:
    # Framework integration (MAF)
    >>> from dakora_instrumentation.frameworks.maf import DakoraIntegration
    >>> middleware = DakoraIntegration.setup(dakora_client)
    
    # Generic instrumentation
    >>> from dakora_instrumentation import setup_instrumentation
    >>> setup_instrumentation(dakora_client, service_name="my-app")
"""

from importlib import metadata as _metadata

# Top-level re-exports for convenience
from .generic import setup_instrumentation

try:
    __version__ = _metadata.version("dakora-instrumentation")
except _metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "__version__",
    "setup_instrumentation",
]
