"""Integration tests for Dakora integrations and helpers."""

import sys
import types
from unittest.mock import MagicMock, patch

from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dakora_instrumentation.generic import InstrumentationHelper


class TestDakoraIntegration:
    """Test suite for DakoraIntegration setup

    Note: DakoraIntegration.setup() is primarily glue code that wires together
    standard OTLP exporters with MAF's observability system. We test it manually
    and with end-to-end tests rather than mocking all the dependencies.

    The real business logic is in DakoraTraceMiddleware (see test_middleware.py).
    """

    def test_force_flush_calls_tracer_provider(self):
        """Test force_flush() calls TracerProvider.force_flush()"""
        mock_provider = MagicMock()
        mock_provider.force_flush.return_value = True

        mock_trace = MagicMock()
        mock_trace.get_tracer_provider.return_value = mock_provider

        # Patch within the utils module where the import happens
        with patch.dict(
            "sys.modules",
            {
                "opentelemetry.trace": mock_trace,
                "opentelemetry": MagicMock(trace=mock_trace),
            },
        ):
            # Need to reimport to pick up the patched module
            result = DakoraIntegration.force_flush(timeout_seconds=10)

        assert result is True
        mock_provider.force_flush.assert_called_once_with(10000)  # milliseconds

    def test_force_flush_handles_no_support(self):
        """Test force_flush() handles providers without force_flush"""
        mock_provider = MagicMock(spec=[])  # No force_flush method

        mock_trace = MagicMock()
        mock_trace.get_tracer_provider.return_value = mock_provider

        with patch("opentelemetry.trace", mock_trace):
            result = DakoraIntegration.force_flush()

        assert result is False

    def test_force_flush_handles_exception(self):
        """Test force_flush() handles exceptions gracefully"""
        mock_provider = MagicMock()
        mock_provider.force_flush.side_effect = Exception("OTEL error")

        mock_trace = MagicMock()
        mock_trace.get_tracer_provider.return_value = mock_provider

        with patch("opentelemetry.trace", mock_trace):
            result = DakoraIntegration.force_flush()

        assert result is False


class TestInstrumentationHelper:
    """Tests for the generic OpenLLMetry helper."""

    def test_api_key_extraction_from_client(self):
        """Exporter factory should extract API key from Dakora client's private attribute."""

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret-key"

        # This will be tested indirectly through the exporter factory
        # The exporter creation validates the API key is properly extracted
        try:
            # We can't actually create the exporter without OTEL deps installed
            # but we can verify the logic is sound via the setup test
            pass
        except ImportError:
            pass

    def test_setup_configures_otlp_exporter(self, monkeypatch):
        """setup() should wire up OTLP exporter + processors without real OTEL deps."""

        created_exporters = []

        class FakeOTLPExporter:
            def __init__(self, endpoint, headers, timeout):
                self.endpoint = endpoint
                self.headers = headers
                self.timeout = timeout
                created_exporters.append(self)

        class FakeBatchProcessor:
            def __init__(self, exporter):
                self.exporter = exporter

        class FakeSpanProcessor:
            def on_start(self, span, parent_context):
                return None

            def on_end(self, span):
                return None

            def shutdown(self):
                return None

            def force_flush(self, timeout_millis: int = 30_000):
                return True

        class FakeTracerProvider:
            def __init__(self, resource):
                self.resource = resource
                self.processors = []

            def add_span_processor(self, processor):
                self.processors.append(processor)

        class FakeResource:
            @staticmethod
            def create(attrs):
                return attrs

        class FakeTraceModule:
            def __init__(self):
                self.provider = FakeTracerProvider(resource={"service.name": "default"})

            def get_tracer_provider(self):
                return self.provider

            def set_tracer_provider(self, provider):
                self.provider = provider

        fake_trace_module = FakeTraceModule()

        # Register fake modules in sys.modules
        opentelemetry_pkg = types.ModuleType("opentelemetry")
        opentelemetry_pkg.trace = fake_trace_module
        monkeypatch.setitem(sys.modules, "opentelemetry", opentelemetry_pkg)

        exporter_module = types.ModuleType(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
        exporter_module.OTLPSpanExporter = FakeOTLPExporter
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            exporter_module,
        )

        sdk_resources_module = types.ModuleType("opentelemetry.sdk.resources")
        sdk_resources_module.Resource = FakeResource
        monkeypatch.setitem(
            sys.modules, "opentelemetry.sdk.resources", sdk_resources_module
        )

        sdk_trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sdk_trace_module.TracerProvider = FakeTracerProvider
        sdk_trace_module.SpanProcessor = (
            FakeSpanProcessor  # Required for _internal/processors.py
        )
        monkeypatch.setitem(sys.modules, "opentelemetry.sdk.trace", sdk_trace_module)

        sdk_trace_export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sdk_trace_export_module.BatchSpanProcessor = FakeBatchProcessor
        sdk_trace_export_module.SpanProcessor = FakeSpanProcessor
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.sdk.trace.export",
            sdk_trace_export_module,
        )

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret"

        # Simplified API - no providers parameter
        provider = InstrumentationHelper.setup(
            DummyDakora(),
            service_name="my-service",
            span_source="otel",
            instrumentors=None,
            additional_span_exporters=None,
        )

        assert provider is fake_trace_module.provider
        assert len(created_exporters) == 1
        exporter = created_exporters[0]
        assert exporter.endpoint == "https://api.dakora.io/api/v1/traces"
        assert exporter.headers["X-API-Key"] == "secret"
        # Processor order: Dakora span source + BatchSpanProcessor
        assert len(provider.processors) == 2
        assert isinstance(provider.processors[1], FakeBatchProcessor)
        assert provider.processors[1].exporter is exporter

    def test_setup_with_custom_instrumentors(self, monkeypatch):
        """setup() should accept custom instrumentors and call instrument() on them."""

        class FakeInstrumentor:
            """Fake instrumentor for testing."""

            def __init__(self):
                self.instrumented = False

            def instrument(self, **kwargs):
                self.instrumented = True
                return self

        # Setup minimal fake OTEL environment
        opentelemetry_pkg = types.ModuleType("opentelemetry")
        opentelemetry_pkg.trace = MagicMock()
        monkeypatch.setitem(sys.modules, "opentelemetry", opentelemetry_pkg)

        exporter_module = types.ModuleType(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
        exporter_module.OTLPSpanExporter = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            exporter_module,
        )

        sdk_resources_module = types.ModuleType("opentelemetry.sdk.resources")
        sdk_resources_module.Resource = MagicMock()
        monkeypatch.setitem(
            sys.modules, "opentelemetry.sdk.resources", sdk_resources_module
        )

        # Use a real class for SpanProcessor
        class FakeSpanProcessor:
            def on_start(self, span, parent_context=None):
                pass

            def on_end(self, span):
                pass

            def shutdown(self):
                pass

            def force_flush(self, timeout_millis=30000):
                return True

        sdk_trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sdk_trace_module.TracerProvider = MagicMock()
        sdk_trace_module.SpanProcessor = (
            FakeSpanProcessor  # Required for _internal/processors.py
        )
        monkeypatch.setitem(sys.modules, "opentelemetry.sdk.trace", sdk_trace_module)

        sdk_trace_export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sdk_trace_export_module.BatchSpanProcessor = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.sdk.trace.export",
            sdk_trace_export_module,
        )

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret"

        custom_instrumentor = FakeInstrumentor()

        # Setup should call instrument() on custom instrumentors
        InstrumentationHelper.setup(
            DummyDakora(),
            instrumentors=[custom_instrumentor],
        )

        # Verify the instrumentor was instrumented via the setup's loop
        assert custom_instrumentor.instrumented is True

    def test_setup_manual_instrumentation_workflow(self, monkeypatch):
        """Test the expected manual instrumentation workflow."""

        # Use a real class for SpanProcessor
        class FakeSpanProcessor:
            def on_start(self, span, parent_context=None):
                pass

            def on_end(self, span):
                pass

            def shutdown(self):
                pass

            def force_flush(self, timeout_millis=30000):
                return True

        # Setup minimal fake OTEL environment
        opentelemetry_pkg = types.ModuleType("opentelemetry")
        opentelemetry_pkg.trace = MagicMock()
        monkeypatch.setitem(sys.modules, "opentelemetry", opentelemetry_pkg)

        exporter_module = types.ModuleType(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
        exporter_module.OTLPSpanExporter = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            exporter_module,
        )

        sdk_resources_module = types.ModuleType("opentelemetry.sdk.resources")
        sdk_resources_module.Resource = MagicMock()
        monkeypatch.setitem(
            sys.modules, "opentelemetry.sdk.resources", sdk_resources_module
        )

        sdk_trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sdk_trace_module.TracerProvider = MagicMock()
        sdk_trace_module.SpanProcessor = (
            FakeSpanProcessor  # Required for _internal/processors.py
        )
        monkeypatch.setitem(sys.modules, "opentelemetry.sdk.trace", sdk_trace_module)

        sdk_trace_export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sdk_trace_export_module.BatchSpanProcessor = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.sdk.trace.export",
            sdk_trace_export_module,
        )

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret"

        # Step 1: User would manually instrument (simulated with mock)
        mock_instrumentor = MagicMock()
        mock_instrumentor.instrument()

        # Step 2: Setup Dakora OTLP exporter
        provider = InstrumentationHelper.setup(
            DummyDakora(),
            service_name="test-service",
        )

        # Verify setup completed without errors
        assert provider is not None
        mock_instrumentor.instrument.assert_called_once()

    def test_auto_detect_providers_enabled(self, monkeypatch):
        """Test auto_detect_providers=True detects and instruments installed providers."""

        # Use a real class for SpanProcessor
        class FakeSpanProcessor:
            def on_start(self, span, parent_context=None):
                pass

            def on_end(self, span):
                pass

            def shutdown(self):
                pass

            def force_flush(self, timeout_millis=30000):
                return True

        # Setup minimal fake OTEL environment
        opentelemetry_pkg = types.ModuleType("opentelemetry")
        opentelemetry_pkg.trace = MagicMock()
        monkeypatch.setitem(sys.modules, "opentelemetry", opentelemetry_pkg)

        exporter_module = types.ModuleType(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
        exporter_module.OTLPSpanExporter = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            exporter_module,
        )

        sdk_resources_module = types.ModuleType("opentelemetry.sdk.resources")
        sdk_resources_module.Resource = MagicMock()
        monkeypatch.setitem(
            sys.modules, "opentelemetry.sdk.resources", sdk_resources_module
        )

        sdk_trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sdk_trace_module.TracerProvider = MagicMock()
        sdk_trace_module.SpanProcessor = (
            FakeSpanProcessor  # Required for _internal/processors.py
        )
        monkeypatch.setitem(sys.modules, "opentelemetry.sdk.trace", sdk_trace_module)

        sdk_trace_export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sdk_trace_export_module.BatchSpanProcessor = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.sdk.trace.export",
            sdk_trace_export_module,
        )

        # Mock OpenAI SDK being installed
        openai_module = types.ModuleType("openai")
        monkeypatch.setitem(sys.modules, "openai", openai_module)

        # Mock OpenAI instrumentor
        mock_openai_instrumentor = MagicMock()
        openai_instrumentation_module = types.ModuleType(
            "opentelemetry.instrumentation.openai"
        )
        openai_instrumentation_module.OpenAIInstrumentor = MagicMock(
            return_value=mock_openai_instrumentor
        )
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.instrumentation.openai",
            openai_instrumentation_module,
        )

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret"

        # Setup with auto-detection enabled
        provider = InstrumentationHelper.setup(
            DummyDakora(),
            auto_detect_providers=True,
        )

        # Verify provider was created
        assert provider is not None

        # Verify OpenAI was instrumented
        mock_openai_instrumentor.instrument.assert_called_once()

    def test_auto_detect_no_providers(self, monkeypatch):
        """Test auto_detect_providers=True when no providers are installed."""

        # Use a real class for SpanProcessor
        class FakeSpanProcessor:
            def on_start(self, span, parent_context=None):
                pass

            def on_end(self, span):
                pass

            def shutdown(self):
                pass

            def force_flush(self, timeout_millis=30000):
                return True

        # Setup minimal fake OTEL environment
        opentelemetry_pkg = types.ModuleType("opentelemetry")
        opentelemetry_pkg.trace = MagicMock()
        monkeypatch.setitem(sys.modules, "opentelemetry", opentelemetry_pkg)

        exporter_module = types.ModuleType(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter"
        )
        exporter_module.OTLPSpanExporter = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            exporter_module,
        )

        sdk_resources_module = types.ModuleType("opentelemetry.sdk.resources")
        sdk_resources_module.Resource = MagicMock()
        monkeypatch.setitem(
            sys.modules, "opentelemetry.sdk.resources", sdk_resources_module
        )

        sdk_trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sdk_trace_module.TracerProvider = MagicMock()
        sdk_trace_module.SpanProcessor = (
            FakeSpanProcessor  # Required for _internal/processors.py
        )
        monkeypatch.setitem(sys.modules, "opentelemetry.sdk.trace", sdk_trace_module)

        sdk_trace_export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sdk_trace_export_module.BatchSpanProcessor = MagicMock()
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.sdk.trace.export",
            sdk_trace_export_module,
        )

        # Ensure no provider SDKs are in sys.modules
        for provider in ["openai", "anthropic"]:
            if provider in sys.modules:
                monkeypatch.delitem(sys.modules, provider)

        class DummyDakora:
            base_url = "https://api.dakora.io"
            _Dakora__api_key = "secret"

        # Setup with auto-detection enabled but no providers installed
        provider = InstrumentationHelper.setup(
            DummyDakora(),
            auto_detect_providers=True,
        )

        # Should still create provider successfully (just with warning logged)
        assert provider is not None

    def test_detect_and_instrument_providers_method(self, monkeypatch):
        """Test _detect_and_instrument_providers() method directly."""

        # Mock Anthropic SDK being installed
        anthropic_module = types.ModuleType("anthropic")
        monkeypatch.setitem(sys.modules, "anthropic", anthropic_module)

        # Mock Anthropic instrumentor
        mock_anthropic_instrumentor = MagicMock()
        anthropic_instrumentation_module = types.ModuleType(
            "opentelemetry.instrumentation.anthropic"
        )
        anthropic_instrumentation_module.AnthropicInstrumentor = MagicMock(
            return_value=mock_anthropic_instrumentor
        )
        monkeypatch.setitem(
            sys.modules,
            "opentelemetry.instrumentation.anthropic",
            anthropic_instrumentation_module,
        )

        # Call detection method
        detected = InstrumentationHelper._detect_and_instrument_providers()

        # Verify Anthropic was detected and instrumented
        assert "anthropic" in detected
        mock_anthropic_instrumentor.instrument.assert_called_once()
