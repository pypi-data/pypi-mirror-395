"""Shared span processor for tagging spans with dakora.span_source."""

from __future__ import annotations

from typing import TYPE_CHECKING

from opentelemetry.sdk.trace import SpanProcessor

if TYPE_CHECKING:
    from opentelemetry.context import Context
    from opentelemetry.sdk.trace import ReadableSpan, Span


class DakoraSpanSourceProcessor(SpanProcessor):
    """
    Span processor that tags spans with dakora.span_source attribute.

    This attribute identifies which integration created the span (e.g., "maf", "otel").
    """

    def __init__(self, span_source: str) -> None:
        """
        Initialize the processor.

        Args:
            span_source: Value to set for dakora.span_source attribute (e.g., "maf")
        """
        self._span_source = span_source

    def on_start(self, span: "Span", parent_context: "Context | None" = None) -> None:
        """
        Called when a span is started.

        Adds dakora.span_source attribute if span is recording and attribute not already set.

        Args:
            span: The span being started
            parent_context: Optional parent context
        """
        if self._span_source and span.is_recording():
            if "dakora.span_source" not in span.attributes:
                span.set_attribute("dakora.span_source", self._span_source)

    def on_end(self, span: "ReadableSpan") -> None:
        """
        Called when a span ends.

        No-op for this processor.

        Args:
            span: The span that ended
        """
        pass

    def shutdown(self) -> None:
        """
        Cleanup resources.

        No-op for this processor.
        """
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """
        Force flush (no-op for this processor).

        Args:
            timeout_millis: Timeout in milliseconds (unused)

        Returns:
            Always returns True
        """
        return True
