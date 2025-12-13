"""Observability middleware for Microsoft Agent Framework agents."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from agent_framework import ChatContext, ChatMessage, ChatMiddleware, ChatResponse, Role

if TYPE_CHECKING:
    from dakora import Dakora

__all__ = ["DakoraTraceMiddleware"]

logger = logging.getLogger(__name__)

# Budget check configuration constants
DEFAULT_BUDGET_CACHE_TTL = 30  # seconds
DEFAULT_BUDGET_CHECK_MAX_RETRIES = 3
DEFAULT_BUDGET_CHECK_RETRY_BASE_DELAY = 1.0  # seconds
DEFAULT_BUDGET_CHECK_RETRY_MAX_DELAY = 10.0  # seconds
DEFAULT_FLUSH_TIMEOUT = 5  # seconds


class DakoraTraceMiddleware(ChatMiddleware):
    """
    Lightweight middleware that integrates Dakora with MAF's OTEL tracing.

    Responsibilities:
    - Check budget before execution (blocking if exceeded)

    OTEL handles everything else:
    - Agent ID tracking (gen_ai.agent.id)
    - Token tracking (gen_ai.usage.input_tokens/output_tokens)
    - Message capture (gen_ai.input.messages/output.messages)
    - Latency tracking (span duration)
    - Export to Dakora API via standard OTLP exporter
    """

    def __init__(
        self,
        dakora_client: Dakora,
        enable_budget_check: bool = False,
        budget_check_cache_ttl: int = DEFAULT_BUDGET_CACHE_TTL,
        budget_check_max_retries: int = DEFAULT_BUDGET_CHECK_MAX_RETRIES,
    ) -> None:
        """
        Configure the middleware.

        Args:
            dakora_client: Dakora client instance with API key configured.
            enable_budget_check: Enable pre-execution budget checks (default: False).
                                When enabled, blocks execution if budget exceeded in strict mode.
                                Warning: Adds latency to every agent call.
            budget_check_cache_ttl: Cache TTL for budget checks in seconds (default: 30).
                                   Only used when enable_budget_check=True.
            budget_check_max_retries: Maximum retries for budget API calls with exponential
                                     backoff (default: 3). Only used when enable_budget_check=True.

        Raises:
            ValueError: If dakora_client is None or budget_check_cache_ttl is invalid.
            TypeError: If dakora_client doesn't have required methods.
        """
        # Validate inputs
        if dakora_client is None:
            raise ValueError("dakora_client cannot be None")

        if budget_check_cache_ttl <= 0:
            raise ValueError(
                f"budget_check_cache_ttl must be positive, got {budget_check_cache_ttl}"
            )

        # Validate dakora_client has required methods
        if not hasattr(dakora_client, "get"):
            raise TypeError(
                f"dakora_client must have a 'get' method for API calls, "
                f"got {type(dakora_client).__name__}"
            )

        if not hasattr(dakora_client, "base_url"):
            raise TypeError(
                f"dakora_client must have a 'base_url' attribute, "
                f"got {type(dakora_client).__name__}"
            )

        self.dakora = dakora_client
        self.enable_budget_check = enable_budget_check
        self.budget_check_cache_ttl = budget_check_cache_ttl
        self.budget_check_max_retries = budget_check_max_retries
        self._budget_cache: dict[str, Any] | None = None
        self._budget_cache_time: datetime | None = None
        self._budget_cache_lock = asyncio.Lock()
        self._has_logged_budget_warning = False

    async def _check_budget_with_cache(self, project_id: str) -> dict[str, Any]:
        """
        Check budget with TTL-based caching to reduce latency.

        Cache prevents excessive API calls for high-frequency agents.
        Thread-safe implementation prevents race conditions when multiple
        concurrent requests check budget simultaneously.

        Args:
            project_id: Project identifier

        Returns:
            Budget status dictionary with at minimum:
                - exceeded (bool): Whether budget is exceeded
                - status (str): Status message
        """
        now = datetime.now(timezone.utc)

        # Fast path: Return cached result if still valid (no lock needed)
        if (
            self._budget_cache is not None
            and self._budget_cache_time is not None
            and (now - self._budget_cache_time).total_seconds()
            < self.budget_check_cache_ttl
        ):
            logger.debug(
                "Using cached budget status",
                extra={
                    "cache_age_seconds": (
                        now - self._budget_cache_time
                    ).total_seconds(),
                    "project_id": project_id,
                },
            )
            return self._budget_cache

        # Slow path: Acquire lock to fetch fresh data
        async with self._budget_cache_lock:
            # Re-check cache after acquiring lock (another request may have updated it)
            now = datetime.now(timezone.utc)
            if (
                self._budget_cache is not None
                and self._budget_cache_time is not None
                and (now - self._budget_cache_time).total_seconds()
                < self.budget_check_cache_ttl
            ):
                logger.debug(
                    "Using cached budget status (acquired after lock)",
                    extra={"project_id": project_id},
                )
                return self._budget_cache

            # Fetch fresh budget status with retry logic
            budget_status = await self._fetch_budget_with_retry(project_id)

            if budget_status is not None:
                # Cache the result
                self._budget_cache = budget_status
                self._budget_cache_time = datetime.now(timezone.utc)

                logger.debug(
                    "Fetched fresh budget status",
                    extra={
                        "project_id": project_id,
                        "exceeded": budget_status.get("exceeded"),
                        "status": budget_status.get("status"),
                    },
                )

                return budget_status
            else:
                # All retries failed - fail open
                logger.warning(
                    "All budget check retries exhausted - allowing execution (fail-open)",
                    extra={"project_id": project_id},
                )
                return {"exceeded": False, "status": "check_failed"}

    async def _fetch_budget_with_retry(self, project_id: str) -> dict[str, Any] | None:
        """
        Fetch budget status with exponential backoff retry.

        Implements exponential backoff: 1s, 2s, 4s, etc., capped at max delay.

        Args:
            project_id: Project identifier

        Returns:
            Budget status dict if successful, None if all retries failed
        """
        for attempt in range(self.budget_check_max_retries):
            try:
                response = await self.dakora.get(f"/api/projects/{project_id}/budget")
                response.raise_for_status()
                budget_status = response.json()

                # Validate response structure
                if not isinstance(budget_status, dict):
                    raise ValueError(
                        f"Expected dict response from budget API, got {type(budget_status)}"
                    )

                # Ensure required fields exist with safe defaults
                budget_status.setdefault("exceeded", False)
                budget_status.setdefault("status", "ok")

                return budget_status

            except (ValueError, KeyError, json.JSONDecodeError) as e:
                logger.warning(
                    "Budget API returned invalid response format",
                    extra={
                        "project_id": project_id,
                        "attempt": attempt + 1,
                        "max_retries": self.budget_check_max_retries,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    },
                )
                # Don't retry on validation errors - fail immediately
                return {"exceeded": False, "status": "check_failed", "error": str(e)}

            except Exception as e:
                logger.warning(
                    "Budget check attempt failed",
                    extra={
                        "project_id": project_id,
                        "attempt": attempt + 1,
                        "max_retries": self.budget_check_max_retries,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    },
                    exc_info=(
                        attempt == self.budget_check_max_retries - 1
                    ),  # Log full trace on last attempt
                )

                # If not the last attempt, wait with exponential backoff
                if attempt < self.budget_check_max_retries - 1:
                    delay = min(
                        DEFAULT_BUDGET_CHECK_RETRY_BASE_DELAY * (2**attempt),
                        DEFAULT_BUDGET_CHECK_RETRY_MAX_DELAY,
                    )
                    logger.debug(
                        f"Retrying budget check after {delay:.1f}s",
                        extra={"attempt": attempt + 1, "delay_seconds": delay},
                    )
                    await asyncio.sleep(delay)

        # All retries exhausted
        return None

    def _format_budget_error(self, budget_status: dict[str, Any]) -> ChatResponse:
        """
        Format user-friendly budget exceeded message.

        Args:
            budget_status: Budget status dictionary

        Returns:
            ChatResponse with error message
        """
        error_message = (
            f"❌ Budget Limit Reached\n\n"
            f"Your project has reached its monthly budget limit.\n\n"
            f"Budget: ${budget_status.get('budget_usd', 0):.2f}\n"
            f"Current Spend: ${budget_status.get('current_spend_usd', 0):.2f}\n\n"
            f"To continue:\n"
            f"1. Increase your budget in Dakora Studio Settings\n"
            f"2. Switch to 'alert' mode to allow executions with warnings\n"
            f"3. Wait until next month (budget resets on the 1st)"
        )

        return ChatResponse(
            messages=[
                ChatMessage(
                    role=Role.ASSISTANT,
                    text=error_message,
                )
            ]
        )

    async def process(
        self,
        context: ChatContext,
        next: Callable[[ChatContext], Awaitable[None]],
    ) -> None:
        """
        Execute the downstream pipeline while checking budget and adding project context.

        OTEL (via MAF) automatically handles:
        - Creating span with agent_id, tokens, messages, etc.
        - Parent/child relationships for multi-agent scenarios
        - Exporting to configured OTEL backends
        """
        logger.debug("DakoraTraceMiddleware.process() called")

        # Log warning if budget checks are disabled (once per instance)
        if not self.enable_budget_check and not self._has_logged_budget_warning:
            logger.info(
                "Budget enforcement is disabled. Enable with enable_budget_check=True to enforce budget limits.",
                extra={
                    "middleware": "DakoraTraceMiddleware",
                    "feature": "budget_check",
                },
            )
            self._has_logged_budget_warning = True

        # Check budget BEFORE execution (optional feature)
        if self.enable_budget_check:
            project_id = self.dakora.project_id

            if project_id:
                budget_status = await self._check_budget_with_cache(project_id)

                if budget_status.get("exceeded", False):
                    enforcement_mode = budget_status.get("enforcement_mode", "strict")

                    if enforcement_mode == "strict":
                        # STRICT MODE: Block execution
                        context.terminate = True
                        context.result = self._format_budget_error(budget_status)
                        logger.warning(
                            "Execution BLOCKED: Budget exceeded",
                            extra={
                                "project_id": project_id,
                                "current_spend_usd": budget_status.get(
                                    "current_spend_usd", 0
                                ),
                                "budget_usd": budget_status.get("budget_usd", 0),
                                "enforcement_mode": "strict",
                                "action": "blocked",
                                "agent_id": getattr(context, "agent_id", None),
                            },
                        )
                        return  # Exit early - no LLM call

                    elif enforcement_mode == "alert":
                        # ALERT MODE: Log warning but allow execution
                        logger.warning(
                            "Budget EXCEEDED but allowing execution (alert mode)",
                            extra={
                                "project_id": project_id,
                                "current_spend_usd": budget_status.get(
                                    "current_spend_usd", 0
                                ),
                                "budget_usd": budget_status.get("budget_usd", 0),
                                "enforcement_mode": "alert",
                                "action": "allowed",
                                "agent_id": getattr(context, "agent_id", None),
                            },
                        )

                elif budget_status.get("status") == "warning":
                    # At warning threshold
                    logger.info(
                        "Budget WARNING: Approaching budget limit",
                        extra={
                            "project_id": project_id,
                            "current_spend_usd": budget_status.get(
                                "current_spend_usd", 0
                            ),
                            "budget_usd": budget_status.get("budget_usd", 0),
                            "percentage_used": budget_status.get("percentage_used", 0),
                            "status": "warning",
                        },
                    )

        # Set dakora.* attributes on the current span (invoke_agent span)
        # This is simpler than creating a wrapper span and searching for it later
        try:
            from opentelemetry import trace

            current_span = trace.get_current_span()

            if current_span and current_span.is_recording():
                current_span.set_attribute("dakora.span_source", "maf")

        except ImportError:
            # OTEL not available
            logger.debug("OpenTelemetry not available")

        # Execute agent
        await next(context)

        # OTEL automatically:
        # - Captures tokens (gen_ai.usage.input_tokens, output_tokens)
        # - Captures messages (gen_ai.input.messages, output.messages)
        # - Captures agent_id (gen_ai.agent.id)
        # - Calculates latency (span duration)
        # - Exports to Dakora API via standard OTLP exporter

    async def __aenter__(self) -> "DakoraTraceMiddleware":
        """Context manager entry - returns self for use in async with statements."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """
        Context manager exit - ensures OTEL spans are flushed on exit.

        This guarantees that all telemetry data is exported before the context exits,
        which is important for short-lived applications or scripts.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred

        Returns:
            False to propagate any exception that occurred
        """
        from ..._internal.utils import DakoraOTELUtils

        logger.debug("Flushing OTEL spans before context exit")
        flush_success = DakoraOTELUtils.force_flush(
            timeout_seconds=DEFAULT_FLUSH_TIMEOUT
        )

        if not flush_success:
            logger.warning(
                "Failed to flush all OTEL spans within timeout. Some telemetry may be lost."
            )

        return False  # Don't suppress exceptions
