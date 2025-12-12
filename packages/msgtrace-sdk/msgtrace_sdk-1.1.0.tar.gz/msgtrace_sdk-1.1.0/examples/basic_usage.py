"""
Basic usage examples for msgtrace SDK.

Demonstrates:
- Context managers (sync and async)
- Decorators
- Attributes (unified MsgTraceAttributes)
- Drop-in replacement for msgflux telemetry
"""

import asyncio
import os

from msgtrace.sdk import MsgTraceAttributes, Spans

# ========== Configuration ==========
# Enable telemetry
os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
os.environ["MSGTRACE_OTLP_ENDPOINT"] = "http://localhost:8000/api/v1/traces/export"
os.environ["MSGTRACE_SERVICE_NAME"] = "example-app"


# ========== Example 1: Basic Context Manager ==========


def example_basic_context():
    """Basic span with context manager."""
    with Spans.span_context("chat_completion"):
        # Set attributes
        MsgTraceAttributes.set_operation_name("chat")
        MsgTraceAttributes.set_model("gpt-5")
        MsgTraceAttributes.set_temperature(0.7)

        # Simulate AI operation
        print("Processing chat completion...")

        # Set usage
        MsgTraceAttributes.set_usage(input_tokens=100, output_tokens=50)

        # Set cost
        MsgTraceAttributes.set_cost(input_cost=0.003, output_cost=0.0015)


# ========== Example 2: Flow and Module Spans ==========


def example_flow_and_modules():
    """Hierarchical flow with modules."""
    with Spans.init_flow("user_query_flow"):
        MsgTraceAttributes.set_workflow_name("query_processing")

        # Module 1: Retrieve
        with Spans.init_module("vector_search"):
            MsgTraceAttributes.set_operation_name("embedding")
            MsgTraceAttributes.set_model("text-embedding-3-small")
            print("Searching vectors...")

        # Module 2: Generate
        with Spans.init_module("response_generation"):
            MsgTraceAttributes.set_operation_name("chat")
            MsgTraceAttributes.set_model("gpt-5")
            print("Generating response...")


# ========== Example 3: Function Decorators ==========


@Spans.instrument("process_query")
def process_query(query: str):
    """Instrumented function."""
    MsgTraceAttributes.set_operation_name("chat")
    MsgTraceAttributes.set_model("gpt-5")
    print(f"Processing: {query}")
    return f"Response to: {query}"


@Spans.set_tool_attributes("search_database", description="Search knowledge base")
@Spans.instrument("tool_search")
def search_database(query: str):
    """Tool with attributes."""
    print(f"Searching database for: {query}")
    return ["result1", "result2"]


# ========== Example 4: Async Operations ==========


@Spans.ainstrument("async_chat")
async def async_chat_completion(prompt: str):
    """Async chat completion."""
    MsgTraceAttributes.set_operation_name("chat")
    MsgTraceAttributes.set_model("gpt-5")
    MsgTraceAttributes.set_prompt(prompt)

    # Simulate async API call
    await asyncio.sleep(0.1)

    MsgTraceAttributes.set_completion("Here's the response")
    MsgTraceAttributes.set_usage(input_tokens=50, output_tokens=30)

    return "Response"


async def example_async_flow():
    """Async flow with context managers."""
    async with Spans.ainit_flow("async_user_flow"):
        MsgTraceAttributes.set_workflow_name("async_processing")

        async with Spans.ainit_module("async_retrieval"):
            print("Async retrieval...")
            await asyncio.sleep(0.05)

        async with Spans.ainit_module("async_generation"):
            result = await async_chat_completion("What is AI?")
            print(f"Result: {result}")


# ========== Example 5: Tool Calling ==========


def example_tool_calling():
    """Example with tool calls."""
    with Spans.span_context("agent_execution"):
        MsgTraceAttributes.set_operation_name("agent")
        MsgTraceAttributes.set_agent_name("research_agent")

        # Set tool call
        MsgTraceAttributes.set_tool_name("search_web")
        MsgTraceAttributes.set_tool_call_id("call_001")
        MsgTraceAttributes.set_tool_call_arguments(
            {"query": "latest AI research", "num_results": 5}
        )

        # Simulate tool execution
        print("Calling tool: search_web")

        # Set tool response
        MsgTraceAttributes.set_tool_response({"results": ["result1", "result2", "result3"]})

        # Set msgtrace-specific tool metadata
        MsgTraceAttributes.set_tool_callings(
            [
                {
                    "id": "call_001",
                    "name": "search_web",
                    "arguments": {"query": "latest AI research", "num_results": 5},
                }
            ]
        )

        MsgTraceAttributes.set_tool_responses([{"id": "call_001", "content": "Found 3 results..."}])


# ========== Example 6: Error Handling ==========


def example_error_handling():
    """Automatic exception recording."""
    try:
        with Spans.span_context("risky_operation"):
            MsgTraceAttributes.set_operation_name("chat")
            raise ValueError("Something went wrong!")
    except ValueError as e:
        print(f"Caught error: {e}")
        # Exception automatically recorded in span


# ========== Example 7: Custom Attributes ==========


def example_custom_attributes():
    """Using custom msgtrace attributes."""
    with Spans.span_context("custom_operation"):
        # Standard GenAI
        MsgTraceAttributes.set_operation_name("chat")
        MsgTraceAttributes.set_model("gpt-5")

        # MsgTrace custom
        MsgTraceAttributes.set_user_id("user_123")
        MsgTraceAttributes.set_session_id("session_456")
        MsgTraceAttributes.set_environment("production")
        MsgTraceAttributes.set_version("1.0.0")
        MsgTraceAttributes.set_cache_hit(True)
        MsgTraceAttributes.set_retry_count(2)

        # Fully custom
        MsgTraceAttributes.set_custom("business_metric", 42.5)
        MsgTraceAttributes.set_custom("metadata", {"key1": "value1", "key2": "value2"})


# ========== Example 8: Drop-in Replacement for msgflux ==========


def example_msgflux_replacement():
    """
    Drop-in replacement for msgflux telemetry.

    Just change imports:
    FROM: from msgflux.telemetry import Spans, MsgTraceAttributes
    TO:   from msgtrace.sdk import Spans, MsgTraceAttributes
    """
    # Exactly same API as msgflux
    with Spans.init_flow("my_flow"):
        MsgTraceAttributes.set_operation_name("chat")
        MsgTraceAttributes.set_model("gpt-5")

        with Spans.init_module("my_module"):
            MsgTraceAttributes.set_usage(input_tokens=100, output_tokens=50)


# ========== Run Examples ==========


def main():
    """Run all examples."""
    print("=" * 60)
    print("msgtrace SDK Examples")
    print("=" * 60)

    print("\n1. Basic context manager:")
    example_basic_context()

    print("\n2. Flow and modules:")
    example_flow_and_modules()

    print("\n3. Function decorators:")
    result = process_query("What is AI?")
    print(f"Result: {result}")

    print("\n4. Tool with decorators:")
    results = search_database("AI research")
    print(f"Results: {results}")

    print("\n5. Tool calling:")
    example_tool_calling()

    print("\n6. Error handling:")
    example_error_handling()

    print("\n7. Custom attributes:")
    example_custom_attributes()

    print("\n8. msgflux replacement:")
    example_msgflux_replacement()

    print("\n" + "=" * 60)
    print("Running async examples...")
    print("=" * 60)

    # Run async examples
    asyncio.run(example_async_flow())

    print("\n✅ All examples completed!")


if __name__ == "__main__":
    main()
