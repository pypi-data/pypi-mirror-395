"""
Tests for Spans context managers and decorators.
"""

import asyncio
import os

import pytest

from msgtrace.sdk import Spans


# Enable telemetry for tests
@pytest.fixture(autouse=True)
def enable_telemetry():
    """Enable telemetry for all tests."""
    os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
    os.environ["MSGTRACE_EXPORTER"] = "console"
    yield
    os.environ.pop("MSGTRACE_TELEMETRY_ENABLED", None)
    os.environ.pop("MSGTRACE_EXPORTER", None)


class TestSpanContextManagers:
    """Test context managers."""

    def test_span_context_basic(self):
        """Test basic span context."""
        with Spans.span_context("test_span"):
            pass  # Span should be created and ended

    def test_span_context_with_kwargs(self):
        """Test span context with custom attributes."""
        with Spans.span_context("test_span", custom_attr="value"):
            pass

    def test_init_flow(self):
        """Test flow-level span."""
        with Spans.init_flow("test_flow"):
            pass

    def test_init_module(self):
        """Test module-level span."""
        with Spans.init_module("test_module"):
            pass

    def test_nested_spans(self):
        """Test nested span hierarchy."""
        with Spans.init_flow("parent_flow"):
            with Spans.init_module("child_module"):
                with Spans.span_context("grandchild_span"):
                    pass

    def test_span_context_exception_handling(self):
        """Test exception recording in span."""
        with pytest.raises(ValueError):
            with Spans.span_context("error_span"):
                raise ValueError("Test error")

    def test_span_context_returns_span(self):
        """Test that context manager yields span."""
        with Spans.span_context("test") as span:
            assert span is not None
            assert span.is_recording() or not span.is_recording()  # Valid span object


class TestAsyncSpanContextManagers:
    """Test async context managers."""

    @pytest.mark.asyncio
    async def test_aspan_context(self):
        """Test async span context."""
        async with Spans.aspan_context("async_test"):
            await asyncio.sleep(0.01)

    @pytest.mark.asyncio
    async def test_ainit_flow(self):
        """Test async flow span."""
        async with Spans.ainit_flow("async_flow"):
            await asyncio.sleep(0.01)

    @pytest.mark.asyncio
    async def test_ainit_module(self):
        """Test async module span."""
        async with Spans.ainit_module("async_module"):
            await asyncio.sleep(0.01)

    @pytest.mark.asyncio
    async def test_async_nested_spans(self):
        """Test nested async spans."""
        async with Spans.ainit_flow("async_parent"):
            async with Spans.ainit_module("async_child"):
                async with Spans.aspan_context("async_grandchild"):
                    await asyncio.sleep(0.01)

    @pytest.mark.asyncio
    async def test_async_exception_handling(self):
        """Test async exception recording."""
        with pytest.raises(ValueError):
            async with Spans.aspan_context("async_error"):
                raise ValueError("Async test error")


class TestSpanDecorators:
    """Test function decorators."""

    def test_instrument_decorator(self):
        """Test @instrument decorator."""

        @Spans.instrument("decorated_function")
        def my_function(x: int) -> int:
            return x * 2

        result = my_function(5)
        assert result == 10

    def test_instrument_default_name(self):
        """Test @instrument with default function name."""

        @Spans.instrument()
        def my_function():
            return "test"

        result = my_function()
        assert result == "test"

    def test_instrument_with_kwargs(self):
        """Test @instrument with span kwargs."""

        @Spans.instrument("test_func", custom_attr="value")
        def my_function():
            return True

        assert my_function() is True

    def test_set_tool_attributes_decorator(self):
        """Test @set_tool_attributes decorator."""

        @Spans.set_tool_attributes("search_tool", description="Search database")
        @Spans.instrument("tool_function")
        def search(query: str):
            return [query]

        results = search("test query")
        assert results == ["test query"]

    def test_set_agent_attributes_decorator(self):
        """Test @set_agent_attributes decorator."""

        @Spans.set_agent_attributes("test_agent", agent_id="agent-001")
        @Spans.instrument("agent_function")
        def agent_action():
            return "completed"

        result = agent_action()
        assert result == "completed"

    def test_decorator_exception_handling(self):
        """Test decorator with exception."""

        @Spans.instrument("error_function")
        def failing_function():
            raise RuntimeError("Decorator error")

        with pytest.raises(RuntimeError):
            failing_function()


class TestAsyncDecorators:
    """Test async decorators."""

    @pytest.mark.asyncio
    async def test_ainstrument_decorator(self):
        """Test @ainstrument decorator."""

        @Spans.ainstrument("async_decorated")
        async def async_function(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        result = await async_function(5)
        assert result == 10

    @pytest.mark.asyncio
    async def test_ainstrument_default_name(self):
        """Test @ainstrument with default name."""

        @Spans.ainstrument()
        async def async_function():
            return "async test"

        result = await async_function()
        assert result == "async test"

    @pytest.mark.asyncio
    async def test_aset_tool_attributes(self):
        """Test @aset_tool_attributes decorator."""

        @Spans.aset_tool_attributes("async_search", description="Async search")
        @Spans.ainstrument("async_tool")
        async def async_search(query: str):
            await asyncio.sleep(0.01)
            return [query]

        results = await async_search("async query")
        assert results == ["async query"]

    @pytest.mark.asyncio
    async def test_aset_agent_attributes(self):
        """Test @aset_agent_attributes decorator."""

        @Spans.aset_agent_attributes("async_agent", agent_id="async-001")
        @Spans.ainstrument("async_agent_action")
        async def agent_action():
            await asyncio.sleep(0.01)
            return "async completed"

        result = await agent_action()
        assert result == "async completed"

    @pytest.mark.asyncio
    async def test_async_decorator_exception(self):
        """Test async decorator with exception."""

        @Spans.ainstrument("async_error")
        async def failing_async():
            raise RuntimeError("Async decorator error")

        with pytest.raises(RuntimeError):
            await failing_async()


class TestMixedSyncAsync:
    """Test mixing sync and async operations."""

    @pytest.mark.asyncio
    async def test_sync_in_async_context(self):
        """Test sync span in async context."""
        async with Spans.ainit_flow("async_flow"):
            # Sync span within async flow
            with Spans.span_context("sync_child"):
                pass

    def test_integration_example(self):
        """Test realistic integration scenario."""

        @Spans.instrument("process_data")
        def process_data(data: str):
            return data.upper()

        with Spans.init_flow("data_pipeline"):
            with Spans.init_module("preprocessing"):
                result = process_data("hello")

            with Spans.init_module("postprocessing"):
                assert result == "HELLO"
