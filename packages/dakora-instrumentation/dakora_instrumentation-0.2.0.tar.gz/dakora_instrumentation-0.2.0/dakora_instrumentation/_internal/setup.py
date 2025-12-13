"""Shared OTEL setup helpers for Dakora integrations."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider

logger = logging.getLogger(__name__)

# Default OTEL resource attribute values
DEFAULT_SERVICE_NAME = "dakora-client"
DEFAULT_SERVICE_NAMESPACE = "dakora"


class DakoraOTELSetup:
    """Helper for common OpenTelemetry setup operations."""

    @staticmethod
    def create_tracer_provider(
        service_name: str = DEFAULT_SERVICE_NAME,
        service_namespace: str = DEFAULT_SERVICE_NAMESPACE,
        resource_attributes: dict[str, Any] | None = None,
    ) -> "TracerProvider":
        """
        Create and configure a TracerProvider with Dakora resource attributes.

        Args:
            service_name: Service name for OTEL resource (default: dakora-client)
            service_namespace: Service namespace (default: dakora)
            resource_attributes: Additional resource attributes to include

        Returns:
            Configured TracerProvider instance

        Raises:
            ImportError: If opentelemetry-sdk is not installed
        """
        try:
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
        except ImportError as exc:
            raise ImportError(
                "opentelemetry-sdk is required. "
                "Install with: pip install opentelemetry-sdk"
            ) from exc

        resource_dict = {
            "service.name": service_name,
            "service.namespace": service_namespace,
        }
        if resource_attributes:
            resource_dict.update(resource_attributes)

        resource = Resource.create(resource_dict)
        tracer_provider = TracerProvider(resource=resource)

        logger.info(f"Created TracerProvider with service.name={service_name}")
        return tracer_provider

    @staticmethod
    def set_global_tracer_provider(tracer_provider: "TracerProvider") -> None:
        """
        Set the given tracer provider as the global default.

        Args:
            tracer_provider: The TracerProvider to set globally

        Raises:
            ImportError: If opentelemetry-api is not installed
        """
        try:
            from opentelemetry import trace
        except ImportError as exc:
            raise ImportError(
                "opentelemetry-api is required. "
                "Install with: pip install opentelemetry-api"
            ) from exc

        trace.set_tracer_provider(tracer_provider)
        logger.debug("Set global TracerProvider")
