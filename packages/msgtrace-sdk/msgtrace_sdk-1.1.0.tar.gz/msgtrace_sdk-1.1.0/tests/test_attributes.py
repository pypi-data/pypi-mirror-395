"""
Tests for GenAI and MsgTrace attributes.
"""

import os

import pytest

from msgtrace.sdk import MsgTraceAttributes, Spans


@pytest.fixture(autouse=True)
def enable_telemetry():
    """Enable telemetry for all tests."""
    os.environ["MSGTRACE_TELEMETRY_ENABLED"] = "true"
    os.environ["MSGTRACE_EXPORTER"] = "console"
    yield
    os.environ.pop("MSGTRACE_TELEMETRY_ENABLED", None)
    os.environ.pop("MSGTRACE_EXPORTER", None)


class TestMsgTraceAttributes:
    """Test GenAI semantic convention attributes."""

    def test_set_operation_name(self):
        """Test setting operation name."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_operation_name("chat")
            # No exception = success

    def test_set_system(self):
        """Test setting GenAI system."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_system("openai")

    def test_set_model(self):
        """Test setting model name."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_model("gpt-5")

    def test_request_parameters(self):
        """Test setting request parameters."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_temperature(0.7)
            MsgTraceAttributes.set_top_p(0.9)
            MsgTraceAttributes.set_max_tokens(1000)
            MsgTraceAttributes.set_frequency_penalty(0.5)
            MsgTraceAttributes.set_presence_penalty(0.3)

    def test_response_attributes(self):
        """Test setting response attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_response_id("resp_123")
            MsgTraceAttributes.set_response_model("gpt-5-0613")
            MsgTraceAttributes.set_finish_reason("stop")

    def test_set_usage_all_fields(self):
        """Test setting token usage with all fields."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_usage(input_tokens=100, output_tokens=50, total_tokens=150)

    def test_set_usage_auto_total(self):
        """Test automatic total calculation."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_usage(
                input_tokens=100,
                output_tokens=50,
                # total_tokens should be calculated
            )

    def test_set_usage_partial(self):
        """Test setting partial usage."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_usage(input_tokens=100)
            MsgTraceAttributes.set_usage(output_tokens=50)

    def test_set_prompt_string(self):
        """Test setting prompt as string."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_prompt("What is AI?")

    def test_set_prompt_messages(self):
        """Test setting prompt as messages array."""
        with Spans.span_context("test"):
            messages = [
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "What is AI?"},
            ]
            MsgTraceAttributes.set_prompt(messages)

    def test_set_completion(self):
        """Test setting completion text."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_completion("AI is artificial intelligence")

    def test_tool_attributes(self):
        """Test tool-related attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_tool_name("search_web")
            MsgTraceAttributes.set_tool_description("Search the web")
            MsgTraceAttributes.set_tool_call_id("call_123")

    def test_tool_call_arguments_dict(self):
        """Test setting tool arguments as dict."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_tool_call_arguments({"query": "test", "limit": 5})

    def test_tool_call_arguments_string(self):
        """Test setting tool arguments as string."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_tool_call_arguments('{"query": "test"}')

    def test_tool_response_dict(self):
        """Test setting tool response as dict."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_tool_response({"results": ["a", "b", "c"]})

    def test_tool_response_string(self):
        """Test setting tool response as string."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_tool_response("Success")

    def test_agent_attributes(self):
        """Test agent attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_agent_name("research_agent")
            MsgTraceAttributes.set_agent_id("agent_001")
            MsgTraceAttributes.set_agent_type("autonomous")
            MsgTraceAttributes.set_agent_goal("Research topic")

    def test_provider_attributes(self):
        """Test provider attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_provider_name("openai")
            MsgTraceAttributes.set_endpoint("https://api.openai.com/v1/chat")

    def test_embedding_attributes(self):
        """Test embedding attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_embedding_dimensions(1536)
            MsgTraceAttributes.set_embedding_format("float")

    def test_complete_chat_scenario(self):
        """Test complete chat completion scenario."""
        with Spans.span_context("chat_completion"):
            # Request
            MsgTraceAttributes.set_operation_name("chat")
            MsgTraceAttributes.set_system("openai")
            MsgTraceAttributes.set_provider_name("openai")
            MsgTraceAttributes.set_model("gpt-5")
            MsgTraceAttributes.set_temperature(0.7)
            MsgTraceAttributes.set_max_tokens(1000)
            MsgTraceAttributes.set_prompt("What is AI?")

            # Response
            MsgTraceAttributes.set_response_id("resp_123")
            MsgTraceAttributes.set_response_model("gpt-5-0613")
            MsgTraceAttributes.set_finish_reason("stop")
            MsgTraceAttributes.set_completion("AI is...")
            MsgTraceAttributes.set_usage(input_tokens=10, output_tokens=50)


class TestMsgTraceCustomAttributes:
    """Test MsgTrace custom attributes."""

    def test_set_cost_all_fields(self):
        """Test setting cost with all fields."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_cost(input_cost=0.003, output_cost=0.002, currency="USD")

    def test_set_cost_partial(self):
        """Test setting partial cost."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_cost(input_cost=0.003)

    def test_set_cost_default_currency(self):
        """Test default currency."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_cost(input_cost=0.003, output_cost=0.002)
            # Should use USD by default

    def test_set_tool_callings(self):
        """Test setting tool callings array."""
        with Spans.span_context("test"):
            callings = [{"id": "call_1", "name": "search", "arguments": {"query": "test"}}]
            MsgTraceAttributes.set_tool_callings(callings)

    def test_set_tool_responses(self):
        """Test setting tool responses array."""
        with Spans.span_context("test"):
            responses = [{"id": "call_1", "content": "Results..."}]
            MsgTraceAttributes.set_tool_responses(responses)

    def test_workflow_attributes(self):
        """Test workflow attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_workflow_name("user_query")
            MsgTraceAttributes.set_workflow_id("wf_123")
            MsgTraceAttributes.set_workflow_step("retrieval")

    def test_user_session_attributes(self):
        """Test user and session attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_user_id("user_456")
            MsgTraceAttributes.set_session_id("session_789")

    def test_custom_metrics(self):
        """Test custom metrics."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_latency(123.45)
            MsgTraceAttributes.set_retry_count(3)
            MsgTraceAttributes.set_cache_hit(True)

    def test_environment_attributes(self):
        """Test environment attributes."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_environment("production")
            MsgTraceAttributes.set_version("1.0.0")

    def test_set_custom_primitive(self):
        """Test setting custom primitive values."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_custom("counter", 42)
            MsgTraceAttributes.set_custom("ratio", 0.95)
            MsgTraceAttributes.set_custom("enabled", True)
            MsgTraceAttributes.set_custom("name", "test")

    def test_set_custom_dict(self):
        """Test setting custom dict."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_custom("metadata", {"key1": "value1", "key2": "value2"})

    def test_set_custom_list(self):
        """Test setting custom list."""
        with Spans.span_context("test"):
            MsgTraceAttributes.set_custom("tags", ["tag1", "tag2"])

    def test_complete_msgtrace_scenario(self):
        """Test complete scenario with MsgTrace attributes."""
        with Spans.span_context("agent_execution"):
            # Workflow
            MsgTraceAttributes.set_workflow_name("research_flow")
            MsgTraceAttributes.set_workflow_id("wf_001")

            # User/session
            MsgTraceAttributes.set_user_id("user_123")
            MsgTraceAttributes.set_session_id("session_456")

            # Environment
            MsgTraceAttributes.set_environment("production")
            MsgTraceAttributes.set_version("2.1.0")

            # Metrics
            MsgTraceAttributes.set_latency(250.5)
            MsgTraceAttributes.set_retry_count(0)
            MsgTraceAttributes.set_cache_hit(False)

            # Cost
            MsgTraceAttributes.set_cost(input_cost=0.005, output_cost=0.003)

            # Tools
            MsgTraceAttributes.set_tool_callings([{"id": "call_1", "name": "search"}])

            # Custom
            MsgTraceAttributes.set_custom("business_metric", 99.9)


class TestCombinedUsage:
    """Test combining GenAI and MsgTrace attributes."""

    def test_combined_attributes(self):
        """Test using both attribute classes together."""
        with Spans.span_context("combined_test"):
            # GenAI attributes
            MsgTraceAttributes.set_operation_name("chat")
            MsgTraceAttributes.set_model("gpt-5")
            MsgTraceAttributes.set_usage(input_tokens=100, output_tokens=50)

            # MsgTrace attributes
            MsgTraceAttributes.set_cost(input_cost=0.003, output_cost=0.002)
            MsgTraceAttributes.set_user_id("user_123")
            MsgTraceAttributes.set_environment("prod")

    def test_realistic_agent_workflow(self):
        """Test realistic agent workflow with all attributes."""
        with Spans.init_flow("agent_research"):
            # Flow-level attributes
            MsgTraceAttributes.set_workflow_name("research_agent")
            MsgTraceAttributes.set_user_id("user_789")

            with Spans.init_module("tool_execution"):
                # Tool call
                MsgTraceAttributes.set_operation_name("tool")
                MsgTraceAttributes.set_tool_name("search_web")
                MsgTraceAttributes.set_tool_call_arguments({"query": "AI"})

                # Metrics
                MsgTraceAttributes.set_latency(120.0)
                MsgTraceAttributes.set_tool_callings([{"id": "t1", "name": "search_web"}])

            with Spans.init_module("llm_processing"):
                # LLM call
                MsgTraceAttributes.set_operation_name("chat")
                MsgTraceAttributes.set_model("gpt-5")
                MsgTraceAttributes.set_usage(input_tokens=200, output_tokens=100)

                # Cost
                MsgTraceAttributes.set_cost(input_cost=0.006, output_cost=0.003)
