"""Shared OTLP exporter factory for Dakora integrations."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opentelemetry.sdk.trace.export import SpanExporter

    from dakora import Dakora

logger = logging.getLogger(__name__)

# Default OTLP exporter timeout (seconds)
DEFAULT_OTLP_TIMEOUT = 30


class DakoraOTLPExporterFactory:
    """Factory for creating standardized OTLP exporters pointing to Dakora API."""

    @staticmethod
    def create_span_exporter(
        dakora_client: "Dakora",
        endpoint: str | None = None,
        timeout: int = DEFAULT_OTLP_TIMEOUT,
        additional_headers: dict[str, str] | None = None,
    ) -> "SpanExporter":
        """
        Create an OTLP HTTP span exporter configured for Dakora.

        Args:
            dakora_client: Dakora client instance with API key and base URL
            endpoint: Override OTLP endpoint (default: {base_url}/api/v1/traces)
            timeout: Timeout for the OTLP HTTP exporter in seconds (default: 30)
            additional_headers: Extra headers to include in OTLP requests

        Returns:
            Configured OTLPSpanExporter instance

        Raises:
            ImportError: If opentelemetry-exporter-otlp-proto-http is not installed
        """
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )
        except ImportError as exc:
            raise ImportError(
                "opentelemetry-exporter-otlp-proto-http is required. "
                "Install with: pip install opentelemetry-exporter-otlp-proto-http"
            ) from exc

        # Extract API key from Dakora client using protected method
        # Falls back to name-mangled attribute for backward compatibility
        api_key = None
        if hasattr(dakora_client, "_get_api_key_for_telemetry"):
            api_key = dakora_client._get_api_key_for_telemetry()
        elif hasattr(dakora_client, "_Dakora__api_key"):
            # Backward compatibility with older dakora-client versions
            api_key = getattr(dakora_client, "_Dakora__api_key")
            logger.debug(
                "Using legacy API key extraction. Consider upgrading dakora-client to >=1.0.1"
            )

        if not api_key:
            raise ValueError(
                "Dakora client must have an API key configured. "
                "Initialize with: Dakora(api_key='dk_proj_...') or set DAKORA_API_KEY environment variable."
            )

        # Determine endpoint
        if endpoint is None:
            base_url = dakora_client.base_url.rstrip("/")
            endpoint = f"{base_url}/api/v1/traces"

        # Validate HTTPS in production environments
        if not endpoint.startswith(
            ("https://", "http://localhost", "http://127.0.0.1")
        ):
            logger.warning(
                "SECURITY WARNING: Using non-HTTPS endpoint '%s'. "
                "API keys should only be transmitted over HTTPS in production environments.",
                endpoint,
            )

        # Build headers
        headers = {"X-API-Key": api_key}
        if additional_headers:
            headers.update(additional_headers)

        logger.info(f"Creating OTLP span exporter for Dakora: {endpoint}")

        return OTLPSpanExporter(
            endpoint=endpoint,
            headers=headers,
            timeout=timeout,
        )
