"""Tests for DakoraTraceMiddleware with OTLP architecture"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from agent_framework import ChatContext, ChatMessage, Role
from dakora_instrumentation.frameworks.maf import DakoraTraceMiddleware

# Ensure internal modules are loaded for patching


@pytest.mark.asyncio
class TestDakoraTraceMiddleware:
    """Test suite for DakoraTraceMiddleware"""

    async def test_middleware_initialization(self, mock_dakora_client):
        """Test middleware can be initialized"""
        middleware = DakoraTraceMiddleware(
            dakora_client=mock_dakora_client,
            budget_check_cache_ttl=30,
        )

        assert middleware.dakora == mock_dakora_client
        assert middleware.budget_check_cache_ttl == 30

    async def test_middleware_initialization_validates_client(self):
        """Test middleware validates dakora_client is not None"""
        with pytest.raises(ValueError, match="dakora_client cannot be None"):
            DakoraTraceMiddleware(dakora_client=None)

    async def test_middleware_initialization_validates_cache_ttl(
        self, mock_dakora_client
    ):
        """Test middleware validates cache TTL is positive"""
        with pytest.raises(ValueError, match="budget_check_cache_ttl must be positive"):
            DakoraTraceMiddleware(
                dakora_client=mock_dakora_client, budget_check_cache_ttl=0
            )

        with pytest.raises(ValueError, match="budget_check_cache_ttl must be positive"):
            DakoraTraceMiddleware(
                dakora_client=mock_dakora_client, budget_check_cache_ttl=-1
            )

    async def test_middleware_initialization_validates_client_methods(self):
        """Test middleware validates client has required methods"""
        invalid_client = MagicMock()
        delattr(invalid_client, "get")  # Remove get method

        with pytest.raises(TypeError, match="must have a 'get' method"):
            DakoraTraceMiddleware(dakora_client=invalid_client)

    async def test_budget_check_allows_execution_when_under_budget(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that execution proceeds when budget is not exceeded"""
        # Mock budget check to return under budget
        mock_dakora_client.get = AsyncMock(
            return_value=MagicMock(
                status_code=200, json=lambda: {"exceeded": False, "status": "ok"}
            )
        )

        middleware = DakoraTraceMiddleware(dakora_client=mock_dakora_client)

        executed = False

        async def mock_next(ctx: ChatContext) -> None:
            nonlocal executed
            executed = True
            ctx.messages.append(ChatMessage(role=Role.ASSISTANT, text="Response"))

        await middleware.process(sample_chat_context, mock_next)

        assert executed is True
        assert len(sample_chat_context.messages) == 2

    async def test_budget_check_blocks_execution_when_exceeded_strict(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that execution is blocked when budget exceeded in strict mode"""
        # Mock budget check to return exceeded with strict enforcement
        mock_dakora_client.get = AsyncMock(
            return_value=MagicMock(
                status_code=200,
                json=lambda: {
                    "exceeded": True,
                    "enforcement_mode": "strict",
                    "budget_usd": 10.0,
                    "current_spend_usd": 12.0,
                },
            )
        )

        middleware = DakoraTraceMiddleware(
            dakora_client=mock_dakora_client, enable_budget_check=True
        )

        executed = False

        async def mock_next(ctx: ChatContext) -> None:
            nonlocal executed
            executed = True

        await middleware.process(sample_chat_context, mock_next)

        assert executed is False  # Should not execute
        assert sample_chat_context.terminate is True  # Should terminate
        assert sample_chat_context.result is not None  # Should have error response

    async def test_budget_check_allows_execution_when_exceeded_alert(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that execution proceeds when budget exceeded in alert mode"""
        # Mock budget check to return exceeded with alert enforcement
        mock_dakora_client.get = AsyncMock(
            return_value=MagicMock(
                status_code=200,
                json=lambda: {
                    "exceeded": True,
                    "enforcement_mode": "alert",
                    "budget_usd": 10.0,
                    "current_spend_usd": 12.0,
                },
            )
        )

        middleware = DakoraTraceMiddleware(dakora_client=mock_dakora_client)

        executed = False

        async def mock_next(ctx: ChatContext) -> None:
            nonlocal executed
            executed = True
            ctx.messages.append(ChatMessage(role=Role.ASSISTANT, text="Response"))

        await middleware.process(sample_chat_context, mock_next)

        assert executed is True  # Should execute despite budget exceeded
        assert len(sample_chat_context.messages) == 2

    async def test_budget_check_uses_cache(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that budget check uses TTL cache"""
        # Mock budget check
        mock_dakora_client.get = AsyncMock(
            return_value=MagicMock(
                status_code=200, json=lambda: {"exceeded": False, "status": "ok"}
            )
        )

        middleware = DakoraTraceMiddleware(
            dakora_client=mock_dakora_client,
            enable_budget_check=True,
            budget_check_cache_ttl=30,
        )

        async def mock_next(ctx: ChatContext) -> None:
            ctx.messages.append(ChatMessage(role=Role.ASSISTANT, text="Response"))

        # First call - should hit API
        await middleware.process(sample_chat_context, mock_next)
        assert mock_dakora_client.get.call_count == 1

        # Second call - should use cache
        await middleware.process(sample_chat_context, mock_next)
        assert mock_dakora_client.get.call_count == 1  # Still 1, didn't call again

    async def test_budget_check_fail_open(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that budget check fails open when API call fails"""
        # Mock budget check to raise exception
        mock_dakora_client.get = AsyncMock(side_effect=Exception("API Error"))

        middleware = DakoraTraceMiddleware(dakora_client=mock_dakora_client)

        executed = False

        async def mock_next(ctx: ChatContext) -> None:
            nonlocal executed
            executed = True

        await middleware.process(sample_chat_context, mock_next)

        assert executed is True  # Should execute despite error (fail-open)

    async def test_handles_no_otel_gracefully(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that middleware works even if OTEL is not available"""
        # Mock the import to raise ImportError
        import builtins

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "opentelemetry" or name.startswith("opentelemetry."):
                raise ImportError("OTEL not available")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            middleware = DakoraTraceMiddleware(dakora_client=mock_dakora_client)

            executed = False

            async def mock_next(ctx: ChatContext) -> None:
                nonlocal executed
                executed = True

            # Should not raise error
            await middleware.process(sample_chat_context, mock_next)
            assert executed is True

    async def test_context_manager_support(self, mock_dakora_client):
        """Test that middleware can be used as async context manager"""
        async with DakoraTraceMiddleware(
            dakora_client=mock_dakora_client
        ) as middleware:
            assert middleware is not None
            assert isinstance(middleware, DakoraTraceMiddleware)
        # Should exit cleanly and flush spans

    async def test_context_manager_flushes_on_exit(self, mock_dakora_client):
        """Test that context manager flushes OTEL spans on exit"""
        # Import the module and patch the class method directly
        from dakora_instrumentation._internal import utils as otel_utils

        with patch.object(otel_utils.DakoraOTELUtils, "force_flush") as mock_flush:
            mock_flush.return_value = True

            async with DakoraTraceMiddleware(dakora_client=mock_dakora_client):
                pass

            # Should have called force_flush
            mock_flush.assert_called_once_with(timeout_seconds=5)

    async def test_context_manager_propagates_exceptions(self, mock_dakora_client):
        """Test that context manager doesn't suppress exceptions"""
        with pytest.raises(ValueError, match="test error"):
            async with DakoraTraceMiddleware(dakora_client=mock_dakora_client):
                raise ValueError("test error")

    async def test_budget_warning_logged_once(
        self, mock_dakora_client, sample_chat_context
    ):
        """Test that budget disabled warning is only logged once"""
        middleware = DakoraTraceMiddleware(
            dakora_client=mock_dakora_client, enable_budget_check=False
        )

        executed_count = 0

        async def mock_next(ctx: ChatContext) -> None:
            nonlocal executed_count
            executed_count += 1

        with patch(
            "dakora_instrumentation.frameworks.maf.middleware.logger"
        ) as mock_logger:
            # First call - should log warning
            await middleware.process(sample_chat_context, mock_next)

            # Second call - should NOT log warning again
            await middleware.process(sample_chat_context, mock_next)

            # Third call - should NOT log warning again
            await middleware.process(sample_chat_context, mock_next)

            assert executed_count == 3

            # Check that info was only called once for budget warning
            info_calls = [
                call
                for call in mock_logger.info.call_args_list
                if "Budget enforcement is disabled" in str(call)
            ]
            assert len(info_calls) == 1
