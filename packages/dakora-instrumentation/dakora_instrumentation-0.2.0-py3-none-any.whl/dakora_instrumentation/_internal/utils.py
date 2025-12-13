"""Shared OTEL utilities for Dakora integrations."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

from packaging.version import InvalidVersion
from packaging.version import parse as parse_version

logger = logging.getLogger(__name__)

# Default timeout for force_flush operations (seconds)
DEFAULT_FLUSH_TIMEOUT = 5

# Minimum required versions for key dependencies
MINIMUM_VERSIONS = {
    "dakora-client": "0.1.0",
    "opentelemetry-api": "1.20.0",
    "opentelemetry-sdk": "1.20.0",
    "opentelemetry-exporter-otlp-proto-http": "1.20.0",
}


class DakoraOTELUtils:
    """Common OpenTelemetry utility operations."""

    @staticmethod
    def force_flush(timeout_seconds: int = DEFAULT_FLUSH_TIMEOUT) -> bool:
        """
        Force flush all pending OTEL spans to exporters.

        Useful before application shutdown to ensure all traces are exported.

        Args:
            timeout_seconds: Maximum time to wait for flush (default: 5)

        Returns:
            True if flush succeeded within timeout, False otherwise

        Example:
            >>> # After completing work
            >>> DakoraOTELUtils.force_flush()
            >>> await dakora.close()
        """
        try:
            from opentelemetry import trace

            tracer_provider = trace.get_tracer_provider()
            if hasattr(tracer_provider, "force_flush"):
                result = tracer_provider.force_flush(timeout_seconds * 1000)  # type: ignore
                logger.info(f"OTEL force_flush completed: {result}")
                return result
            else:
                logger.warning("TracerProvider does not support force_flush")
                return False
        except Exception as e:
            logger.error(f"Failed to force flush OTEL spans: {e}")
            return False

    @staticmethod
    def suppress_otel_console_logging() -> None:
        """
        Suppress verbose OTEL console logs.

        Reduces noise from OpenTelemetry internal logging during normal operation.
        """
        # Suppress verbose OTEL console metrics logs
        logging.getLogger("opentelemetry.sdk.trace.export").setLevel(logging.WARNING)
        logging.getLogger("opentelemetry.sdk.metrics.export").setLevel(logging.WARNING)
        logging.getLogger("opentelemetry.exporter.otlp").setLevel(logging.WARNING)

    @staticmethod
    def check_dependency_versions(strict: bool = False) -> list[str]:
        """
        Check if installed dependency versions meet minimum requirements.

        This follows best practices by validating versions at startup to prevent
        runtime failures due to incompatible dependencies.

        Args:
            strict: If True, raise ImportError on version mismatches.
                   If False, only log warnings (default).

        Returns:
            List of warning messages for any version issues found.

        Raises:
            ImportError: If strict=True and version requirements not met.

        Example:
            >>> from dakora_instrumentation._internal.utils import DakoraOTELUtils
            >>> warnings = DakoraOTELUtils.check_dependency_versions()
            >>> if warnings:
            ...     for warning in warnings:
            ...         print(warning)
        """
        issues = []

        for package, min_version in MINIMUM_VERSIONS.items():
            try:
                installed_version = get_version(package)

                # Use packaging.version for robust comparison (handles pre-releases, metadata, etc.)
                installed_parsed = parse_version(installed_version)
                required_parsed = parse_version(min_version)

                if installed_parsed < required_parsed:
                    message = (
                        f"{package}>={min_version} required, but {installed_version} is installed. "
                        f"Upgrade with: pip install --upgrade '{package}>={min_version}'"
                    )
                    issues.append(message)
                    logger.warning(message)
                else:
                    logger.debug(
                        f"{package} version check passed: {installed_version}>={min_version}"
                    )

            except PackageNotFoundError:
                # Package not installed - this is expected for optional dependencies
                logger.debug(f"{package} not installed (may be optional)")
            except InvalidVersion as e:
                # Version parsing error (rare, but possible with non-PEP-440 versions)
                message = f"Could not parse version for {package}: {e}"
                issues.append(message)
                logger.debug(message)

        if strict and issues:
            raise ImportError(
                "Dependency version requirements not met:\n"
                + "\n".join(f"  - {issue}" for issue in issues)
            )

        return issues
