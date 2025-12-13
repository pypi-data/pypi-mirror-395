"""Generic OpenTelemetry instrumentation setup for Dakora.

Configures OpenTelemetry to export traces to Dakora's OTLP endpoint at
`/api/v1/traces` with authentication via X-API-Key header.

**Installation:**
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    pip install opentelemetry-instrumentation-openai  # for OpenAI
    pip install opentelemetry-instrumentation-anthropic  # for Anthropic

**Usage:**
    >>> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
    >>> from dakora import Dakora
    >>> from dakora_instrumentation import setup_instrumentation
    >>>
    >>> # Instrument globally (do once at startup)
    >>> OpenAIInstrumentor().instrument()
    >>>
    >>> # Configure Dakora exporter
    >>> dakora = Dakora(api_key="dk_proj_...")
    >>> setup_instrumentation(dakora, service_name="my-app")
    >>>
    >>> # Use SDK as normal - automatically traced
    >>> from openai import OpenAI
    >>> client = OpenAI()
    >>> response = client.chat.completions.create(...)

For framework-specific integrations (MAF, LangChain, etc.), see the
`dakora_instrumentation.frameworks` subpackage.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:  # pragma: no cover - optional dependencies
    from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
    from opentelemetry.sdk.trace.export import SpanExporter

    from dakora import Dakora

logger = logging.getLogger(__name__)

__all__ = ["setup_instrumentation", "InstrumentationHelper"]


def setup_instrumentation(
    dakora_client: "Dakora",
    *,
    service_name: str = "dakora",
    span_source: str = "generic",
    auto_detect_providers: bool = False,
    exporter_endpoint: str | None = None,
    exporter_timeout: int = 30,
    headers: dict[str, str] | None = None,
    resource_attributes: dict[str, Any] | None = None,
    instrumentors: Sequence["BaseInstrumentor"] | None = None,
    additional_span_exporters: Sequence["SpanExporter"] | None = None,
    tracer_provider: Any | None = None,
) -> Any:
    """
    Configure OpenTelemetry to export traces to Dakora.

    Sets up an OTLP HTTP exporter that sends spans to Dakora's `/api/v1/traces`
    endpoint. Works with any OpenTelemetry-instrumented SDK or framework.

    Args:
        dakora_client: Initialized Dakora client with API key.
        service_name: OTEL resource service.name (default: dakora-client).
        span_source: Value to set on `dakora.span_source` for exported spans.
        auto_detect_providers: If True, automatically detect and instrument
            installed LLM providers (OpenAI, Anthropic). Default False.
        exporter_endpoint: Override OTLP endpoint (default: Dakora `/api/v1/traces`).
        exporter_timeout: Timeout for the OTLP HTTP exporter (seconds).
        headers: Additional headers for the OTLP exporter.
        resource_attributes: Extra OTEL resource attributes to attach.
        instrumentors: Custom instrumentor instances to run `.instrument()` on.
        additional_span_exporters: Extra OTEL span exporters for multi-export.
        tracer_provider: Custom TracerProvider. When omitted, creates and registers
            a default provider globally.

    Returns:
        The configured TracerProvider instance.

    Examples:
        Basic setup with OpenAI (manual instrumentation):
            >>> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
            >>> from dakora import Dakora
            >>> from dakora_instrumentation import setup_instrumentation
            >>>
            >>> # Instrument OpenAI globally (do this once)
            >>> OpenAIInstrumentor().instrument()
            >>>
            >>> # Setup Dakora exporter
            >>> dakora = Dakora(api_key="dk_proj_...")
            >>> setup_instrumentation(dakora, service_name="my-service")
            >>>
            >>> # Use OpenAI as normal - automatically traced
            >>> from openai import OpenAI
            >>> client = OpenAI()
            >>> response = client.chat.completions.create(...)

        Multiple providers:
            >>> from opentelemetry.instrumentation.openai import OpenAIInstrumentor
            >>> from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
            >>>
            >>> # Instrument both providers globally
            >>> OpenAIInstrumentor().instrument()
            >>> AnthropicInstrumentor().instrument()
            >>>
            >>> # Setup Dakora exporter (works for all instrumented providers)
            >>> setup_instrumentation(dakora)

        With custom TracerProvider:
            >>> from opentelemetry.sdk.trace import TracerProvider
            >>> from opentelemetry.sdk.resources import Resource
            >>>
            >>> # Create custom TracerProvider with extra resource attributes
            >>> resource = Resource.create({"deployment.environment": "production"})
            >>> custom_provider = TracerProvider(resource=resource)
            >>>
            >>> # Pass it to setup_instrumentation()
            >>> setup_instrumentation(dakora, tracer_provider=custom_provider)

        With additional exporters (Jaeger + Dakora):
            >>> from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            >>>
            >>> jaeger_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
            >>> setup_instrumentation(
            ...     dakora,
            ...     additional_span_exporters=[jaeger_exporter]
            ... )

        Auto-detection (quick setup):
            >>> # Automatically instruments all installed providers
            >>> setup_instrumentation(dakora, auto_detect_providers=True)

    Note:
        Instrumentation is global and applies to all instances of the instrumented
        SDK. For example, once you call OpenAIInstrumentor().instrument(), all
        OpenAI API calls in your application will be traced.
    """
    return InstrumentationHelper.setup(
        dakora_client=dakora_client,
        service_name=service_name,
        span_source=span_source,
        auto_detect_providers=auto_detect_providers,
        exporter_endpoint=exporter_endpoint,
        exporter_timeout=exporter_timeout,
        headers=headers,
        resource_attributes=resource_attributes,
        instrumentors=instrumentors,
        additional_span_exporters=additional_span_exporters,
        tracer_provider=tracer_provider,
    )


class InstrumentationHelper:
    """
    Helper class for configuring OpenTelemetry instrumentations.

    Provides utilities for setting up Dakora OTLP exporters and
    instrumenting LLM providers.
    """

    @staticmethod
    def _detect_and_instrument_providers() -> list[str]:
        """
        Detect installed LLM provider SDKs and instrument them.

        Checks sys.modules for common LLM provider packages and instruments
        them automatically if found.

        Returns:
            List of provider names that were successfully instrumented.
        """
        import sys

        detected_providers = []
        failed_providers = []

        # Check for OpenAI
        if "openai" in sys.modules:
            try:
                from opentelemetry.instrumentation.openai import OpenAIInstrumentor

                OpenAIInstrumentor().instrument()
                detected_providers.append("openai")
                logger.info("Successfully instrumented OpenAI SDK")
            except ImportError:
                logger.warning(
                    "openai SDK detected but instrumentation not installed. "
                    "Install with: pip install opentelemetry-instrumentation-openai"
                )
                failed_providers.append("openai")
            except RuntimeError as e:
                # Already instrumented or other runtime error
                if "already instrumented" in str(e).lower():
                    logger.debug("OpenAI SDK already instrumented")
                    detected_providers.append("openai")
                else:
                    logger.error(
                        "Failed to instrument OpenAI: %s. "
                        "This may cause telemetry gaps for OpenAI calls.",
                        e,
                        exc_info=True,
                    )
                    failed_providers.append("openai")
            except Exception as e:
                logger.error(
                    "Unexpected error instrumenting OpenAI: %s. "
                    "This may cause telemetry gaps for OpenAI calls.",
                    e,
                    exc_info=True,
                )
                failed_providers.append("openai")

        # Check for Anthropic
        if "anthropic" in sys.modules:
            try:
                from opentelemetry.instrumentation.anthropic import (
                    AnthropicInstrumentor,
                )

                AnthropicInstrumentor().instrument()
                detected_providers.append("anthropic")
                logger.info("Successfully instrumented Anthropic SDK")
            except ImportError:
                logger.warning(
                    "anthropic SDK detected but instrumentation not installed. "
                    "Install with: pip install opentelemetry-instrumentation-anthropic"
                )
                failed_providers.append("anthropic")
            except RuntimeError as e:
                if "already instrumented" in str(e).lower():
                    logger.debug("Anthropic SDK already instrumented")
                    detected_providers.append("anthropic")
                else:
                    logger.error(
                        "Failed to instrument Anthropic: %s. "
                        "This may cause telemetry gaps for Anthropic calls.",
                        e,
                        exc_info=True,
                    )
                    failed_providers.append("anthropic")
            except Exception as e:
                logger.error(
                    "Unexpected error instrumenting Anthropic: %s. "
                    "This may cause telemetry gaps for Anthropic calls.",
                    e,
                    exc_info=True,
                )
                failed_providers.append("anthropic")

        # Log summary
        if detected_providers:
            logger.info(
                "Auto-instrumented %d provider(s): %s",
                len(detected_providers),
                ", ".join(detected_providers),
            )

        if failed_providers:
            logger.warning(
                "Failed to instrument %d provider(s): %s. "
                "Install missing packages or use manual instrumentation.",
                len(failed_providers),
                ", ".join(failed_providers),
            )

        if not detected_providers and not failed_providers:
            logger.warning(
                "auto_detect_providers=True but no LLM providers detected in sys.modules. "
                "Ensure provider SDKs are imported before calling setup_instrumentation()."
            )

        return detected_providers

    @staticmethod
    def setup(
        dakora_client: "Dakora",
        *,
        service_name: str = "dakora-client",
        span_source: str = "generic",
        auto_detect_providers: bool = False,
        exporter_endpoint: str | None = None,
        exporter_timeout: int = 30,
        headers: dict[str, str] | None = None,
        resource_attributes: dict[str, Any] | None = None,
        instrumentors: Sequence["BaseInstrumentor"] | None = None,
        additional_span_exporters: Sequence["SpanExporter"] | None = None,
        tracer_provider: Any | None = None,
    ) -> Any:
        """
        Configure a Dakora OTLP exporter for OpenTelemetry.

        See setup_instrumentation() for full documentation.
        """
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise ImportError(
                "opentelemetry-sdk and opentelemetry-exporter-otlp-proto-http "
                "are required for setup_instrumentation(). "
                "Install with: pip install opentelemetry-sdk "
                "opentelemetry-exporter-otlp-proto-http"
            ) from exc

        # Use shared internal utilities
        from ._internal.exporter import DakoraOTLPExporterFactory
        from ._internal.processors import DakoraSpanSourceProcessor
        from ._internal.setup import DakoraOTELSetup
        from ._internal.utils import DakoraOTELUtils

        # Check dependency versions (non-strict - warnings only)
        DakoraOTELUtils.check_dependency_versions(strict=False)

        # Create OTLP exporter using shared factory
        dakora_exporter = DakoraOTLPExporterFactory.create_span_exporter(
            dakora_client=dakora_client,
            endpoint=exporter_endpoint,
            timeout=exporter_timeout,
            additional_headers=headers,
        )

        # Create tracer provider using shared setup
        if tracer_provider is None or not isinstance(tracer_provider, TracerProvider):
            tracer_provider = DakoraOTELSetup.create_tracer_provider(
                service_name=service_name,
                service_namespace="dakora",
                resource_attributes=resource_attributes,
            )
            DakoraOTELSetup.set_global_tracer_provider(tracer_provider)
        else:
            logger.debug("Using caller-provided TracerProvider for Dakora exporter")

        tracer_provider.add_span_processor(DakoraSpanSourceProcessor(span_source))
        tracer_provider.add_span_processor(BatchSpanProcessor(dakora_exporter))

        if additional_span_exporters:
            for exporter in additional_span_exporters:
                tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

        # Auto-detect and instrument providers if requested
        if auto_detect_providers:
            detected = InstrumentationHelper._detect_and_instrument_providers()
            if detected:
                logger.info(
                    "Auto-detected and instrumented providers: %s",
                    ", ".join(detected),
                )
            else:
                logger.warning(
                    "auto_detect_providers=True but no providers detected in sys.modules"
                )

        # Instrument custom instrumentors if provided
        if instrumentors:
            for inst in instrumentors:
                inst.instrument()
                logger.info("Instrumented custom instrumentor: %s", type(inst).__name__)

        return tracer_provider
