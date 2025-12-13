"""Pytest configuration and fixtures for dakora-agents tests."""

import sys
import types
from dataclasses import dataclass
from enum import Enum
from unittest.mock import AsyncMock, MagicMock

import pytest

# Provide a lightweight stub for agent_framework when the dependency isn't installed.
try:  # pragma: no cover - exercised implicitly during import
    import agent_framework  # type: ignore
except ImportError:  # pragma: no cover - exercised only in test envs without dependency

    class Role(str, Enum):
        USER = "user"
        ASSISTANT = "assistant"
        TOOL = "tool"

    @dataclass
    class ChatMessage:
        role: Role
        text: str | None = None

    @dataclass
    class ChatResponse:
        messages: list[ChatMessage]

    class ChatOptions:
        """Placeholder chat options."""

    class ChatContext:
        def __init__(
            self,
            messages: list[ChatMessage] | None = None,
            metadata: dict | None = None,
            chat_client: MagicMock | None = None,
            chat_options: ChatOptions | None = None,
        ):
            self.messages = messages or []
            self.metadata = metadata or {}
            self.chat_client = chat_client
            self.chat_options = chat_options or ChatOptions()
            self.terminate = False
            self.result: ChatResponse | None = None

    class ChatMiddleware:
        async def process(self, context, next_func):
            await next_func(context)

    # Create a dummy agent_framework module to satisfy imports
    agent_framework = types.ModuleType("agent_framework")
    agent_framework.Role = Role
    agent_framework.ChatMessage = ChatMessage
    agent_framework.ChatContext = ChatContext
    agent_framework.ChatMiddleware = ChatMiddleware
    agent_framework.ChatResponse = ChatResponse
    agent_framework.ChatOptions = ChatOptions
    sys.modules["agent_framework"] = agent_framework


# Mock OpenTelemetry dependencies globally for all tests (at import time)
# This ensures that imports in test files don't fail during collection
otel_module = sys.modules.setdefault("opentelemetry", types.ModuleType("opentelemetry"))
# Make it a package
if not hasattr(otel_module, "__path__"):
    otel_module.__path__ = []

if not hasattr(otel_module, "trace"):
    otel_module.trace = types.SimpleNamespace(get_current_span=lambda: MagicMock())

# Ensure opentelemetry.sdk exists
if "opentelemetry.sdk" not in sys.modules:
    sdk_module = types.ModuleType("opentelemetry.sdk")
    sdk_module.__path__ = []
    sys.modules["opentelemetry.sdk"] = sdk_module
    otel_module.sdk = sdk_module

# Ensure opentelemetry.sdk.trace exists
if "opentelemetry.sdk.trace" not in sys.modules:
    trace_module = types.ModuleType("opentelemetry.sdk.trace")
    sys.modules["opentelemetry.sdk.trace"] = trace_module
    sys.modules["opentelemetry.sdk"].trace = trace_module

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

    trace_module.SpanProcessor = FakeSpanProcessor
    trace_module.TracerProvider = MagicMock()

# Ensure opentelemetry.sdk.trace.export exists
if "opentelemetry.sdk.trace.export" not in sys.modules:
    export_module = types.ModuleType("opentelemetry.sdk.trace.export")
    sys.modules["opentelemetry.sdk.trace.export"] = export_module
    sys.modules["opentelemetry.sdk.trace"].export = export_module
    export_module.BatchSpanProcessor = MagicMock()
    export_module.SpanExporter = MagicMock()


@pytest.fixture
def mock_dakora_client():
    """Mock Dakora client for testing"""
    client = MagicMock()
    client.base_url = "http://localhost:8000"
    client.project_id = "test-project-123"
    client._Dakora__api_key = "test-api-key"  # Private attribute
    client.get = AsyncMock(
        return_value=MagicMock(
            status_code=200,
            json=lambda: {"exceeded": False, "status": "ok"},
            raise_for_status=lambda: None,
        )
    )
    client.prompts = MagicMock()
    client.prompts.render = AsyncMock(
        return_value=MagicMock(
            text="Test prompt text",
            version="1.0",
            prompt_id="test-prompt",
            inputs={"key": "value"},
            metadata={},
        )
    )
    return client


@pytest.fixture
def sample_chat_context():
    """Sample ChatContext for testing"""
    from agent_framework import ChatContext, ChatMessage, ChatOptions, Role

    # Create a mock chat client
    mock_chat_client = MagicMock()
    mock_chat_client.complete = AsyncMock(
        return_value=ChatMessage(role=Role.ASSISTANT, text="Mock response")
    )

    context = ChatContext(
        messages=[
            ChatMessage(role=Role.USER, text="Hello"),
        ],
        metadata={},
        chat_client=mock_chat_client,
        chat_options=ChatOptions(),
    )
    return context


@pytest.fixture
def sample_render_result():
    """Sample RenderResult for testing to_message()"""
    result = MagicMock()
    result.text = "Rendered template text"
    result.version = "1.0"
    result.prompt_id = "test-prompt"
    result.inputs = {"user": "Alice"}
    result.metadata = {"category": "greeting"}
    return result


@pytest.fixture
def project_id():
    """Test project ID"""
    return "test-project-123"


@pytest.fixture
def agent_id():
    """Test agent ID"""
    return "test-agent"


@pytest.fixture
def session_id():
    """Test session ID"""
    return "test-session-456"


@pytest.fixture(scope="session", autouse=True)
def mock_opentelemetry():
    """Mock OpenTelemetry dependencies for all tests."""
    # Ensure opentelemetry namespace exists
    otel_module = sys.modules.setdefault(
        "opentelemetry", types.ModuleType("opentelemetry")
    )
    # Make it a package
    if not hasattr(otel_module, "__path__"):
        otel_module.__path__ = []

    if not hasattr(otel_module, "trace"):
        otel_module.trace = types.SimpleNamespace(get_current_span=lambda: MagicMock())

    # Ensure opentelemetry.sdk exists
    if "opentelemetry.sdk" not in sys.modules:
        sdk_module = types.ModuleType("opentelemetry.sdk")
        sdk_module.__path__ = []
        sys.modules["opentelemetry.sdk"] = sdk_module
        otel_module.sdk = sdk_module

    # Ensure opentelemetry.sdk.trace exists
    if "opentelemetry.sdk.trace" not in sys.modules:
        trace_module = types.ModuleType("opentelemetry.sdk.trace")
        sys.modules["opentelemetry.sdk.trace"] = trace_module
        sys.modules["opentelemetry.sdk"].trace = trace_module

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

        trace_module.SpanProcessor = FakeSpanProcessor
        trace_module.TracerProvider = MagicMock()

    # Ensure opentelemetry.sdk.trace.export exists
    if "opentelemetry.sdk.trace.export" not in sys.modules:
        export_module = types.ModuleType("opentelemetry.sdk.trace.export")
        sys.modules["opentelemetry.sdk.trace.export"] = export_module
        sys.modules["opentelemetry.sdk.trace"].export = export_module
        export_module.BatchSpanProcessor = MagicMock()
        export_module.SpanExporter = MagicMock()
