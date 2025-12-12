"""
Spans - Context managers and decorators for tracing.

Based on msgflux telemetry API with drop-in replacement compatibility.
"""

import functools
from collections.abc import Callable
from contextlib import asynccontextmanager, contextmanager

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from msgtrace.sdk.tracer import tracer_manager


class Spans:
    """
    Context managers and decorators for creating spans.

    Features:
    - Sync and async context managers
    - Function decorators
    - Automatic exception recording
    - Flow and module-level spans
    - Tool and agent attribute helpers
    """

    @staticmethod
    @contextmanager
    def span_context(name: str, **kwargs):
        """
        Create a basic span context.

        Args:
            name: Span name
            **kwargs: Additional span attributes

        Example:
            with Spans.span_context("chat_completion"):
                # Your code here
                pass
        """
        span = tracer_manager.tracer.start_span(name)

        # Set custom attributes
        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            # Record exception and re-raise
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    @staticmethod
    @contextmanager
    def init_flow(flow_name: str, **kwargs):
        """
        Create a flow-level span (top-level operation).

        Args:
            flow_name: Flow name
            **kwargs: Additional attributes

        Example:
            with Spans.init_flow("user_query_flow"):
                # Your flow logic
                pass
        """
        span = tracer_manager.tracer.start_span(
            flow_name,
            kind=trace.SpanKind.SERVER,  # Flow is a server-level operation
        )

        span.set_attribute("span.type", "flow")

        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    @staticmethod
    @contextmanager
    def init_module(module_name: str, **kwargs):
        """
        Create a module-level span.

        Args:
            module_name: Module name
            **kwargs: Additional attributes

        Example:
            with Spans.init_module("vector_search"):
                # Your module logic
                pass
        """
        span = tracer_manager.tracer.start_span(module_name, kind=trace.SpanKind.INTERNAL)

        span.set_attribute("span.type", "module")

        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    # ========== Async Context Managers ==========

    @staticmethod
    @asynccontextmanager
    async def aspan_context(name: str, **kwargs):
        """
        Create an async span context.

        Args:
            name: Span name
            **kwargs: Additional attributes

        Example:
            async with Spans.aspan_context("async_chat"):
                # Your async code
                pass
        """
        span = tracer_manager.tracer.start_span(name)

        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    @staticmethod
    @asynccontextmanager
    async def ainit_flow(flow_name: str, **kwargs):
        """
        Create an async flow-level span.

        Args:
            flow_name: Flow name
            **kwargs: Additional attributes

        Example:
            async with Spans.ainit_flow("async_user_flow"):
                # Your async flow
                pass
        """
        span = tracer_manager.tracer.start_span(flow_name, kind=trace.SpanKind.SERVER)

        span.set_attribute("span.type", "flow")

        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    @staticmethod
    @asynccontextmanager
    async def ainit_module(module_name: str, **kwargs):
        """
        Create an async module-level span.

        Args:
            module_name: Module name
            **kwargs: Additional attributes

        Example:
            async with Spans.ainit_module("async_vector_search"):
                # Your async module logic
                pass
        """
        span = tracer_manager.tracer.start_span(module_name, kind=trace.SpanKind.INTERNAL)

        span.set_attribute("span.type", "module")

        if kwargs:
            for key, value in kwargs.items():
                span.set_attribute(key, value)

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    # ========== Sync Decorators ==========

    @staticmethod
    def instrument(name: str | None = None, **span_kwargs):
        """
        Decorator to instrument a sync function.

        Args:
            name: Span name (defaults to function name)
            **span_kwargs: Additional span attributes

        Example:
            @Spans.instrument("process_query")
            def process(query: str):
                return result
        """

        def decorator(func: Callable) -> Callable:
            span_name = name or func.__name__

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with Spans.span_context(span_name, **span_kwargs):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def set_tool_attributes(tool_name: str, description: str | None = None, **extra_attrs):
        """
        Decorator to set tool attributes on a function.

        Args:
            tool_name: Tool name
            description: Tool description
            **extra_attrs: Additional attributes

        Example:
            @Spans.set_tool_attributes("search_db", description="Search database")
            def search(query: str):
                return results
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                span = trace.get_current_span()

                if span.is_recording():
                    span.set_attribute("gen_ai.tool.name", tool_name)
                    if description:
                        span.set_attribute("gen_ai.tool.description", description)

                    for key, value in extra_attrs.items():
                        span.set_attribute(f"gen_ai.tool.{key}", value)

                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def set_agent_attributes(agent_name: str, agent_id: str | None = None, **extra_attrs):
        """
        Decorator to set agent attributes on a function.

        Args:
            agent_name: Agent name
            agent_id: Agent ID
            **extra_attrs: Additional attributes

        Example:
            @Spans.set_agent_attributes("research_agent", agent_id="agent-001")
            def research(topic: str):
                return findings
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                span = trace.get_current_span()

                if span.is_recording():
                    span.set_attribute("gen_ai.agent.name", agent_name)
                    if agent_id:
                        span.set_attribute("gen_ai.agent.id", agent_id)

                    for key, value in extra_attrs.items():
                        span.set_attribute(f"gen_ai.agent.{key}", value)

                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def ainstrument(name: str | None = None, **span_kwargs):
        """
        Decorator to instrument an async function.

        Args:
            name: Span name (defaults to function name)
            **span_kwargs: Additional span attributes

        Example:
            @Spans.ainstrument("async_process_query")
            async def process(query: str):
                return result
        """

        def decorator(func: Callable) -> Callable:
            span_name = name or func.__name__

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                async with Spans.aspan_context(span_name, **span_kwargs):
                    return await func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def aset_tool_attributes(tool_name: str, description: str | None = None, **extra_attrs):
        """
        Async decorator to set tool attributes.

        Args:
            tool_name: Tool name
            description: Tool description
            **extra_attrs: Additional attributes

        Example:
            @Spans.aset_tool_attributes("async_search_db")
            async def search(query: str):
                return results
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                span = trace.get_current_span()

                if span.is_recording():
                    span.set_attribute("gen_ai.tool.name", tool_name)
                    if description:
                        span.set_attribute("gen_ai.tool.description", description)

                    for key, value in extra_attrs.items():
                        span.set_attribute(f"gen_ai.tool.{key}", value)

                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def aset_agent_attributes(agent_name: str, agent_id: str | None = None, **extra_attrs):
        """
        Async decorator to set agent attributes.

        Args:
            agent_name: Agent name
            agent_id: Agent ID
            **extra_attrs: Additional attributes

        Example:
            @Spans.aset_agent_attributes("async_research_agent")
            async def research(topic: str):
                return findings
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                span = trace.get_current_span()

                if span.is_recording():
                    span.set_attribute("gen_ai.agent.name", agent_name)
                    if agent_id:
                        span.set_attribute("gen_ai.agent.id", agent_id)

                    for key, value in extra_attrs.items():
                        span.set_attribute(f"gen_ai.agent.{key}", value)

                return await func(*args, **kwargs)

            return wrapper

        return decorator
