"""
Attributes - MsgTrace attribute helpers.

Based on OpenTelemetry Gen AI semantic conventions and msgflux telemetry.
Provides 60+ attributes for AI/GenAI tracing, all in a single convenient class.
"""

import json
from typing import Any

from opentelemetry import trace


class MsgTraceAttributes:
    """
    Unified attribute class for all tracing attributes.

    Includes:
    - OpenTelemetry Gen AI semantic conventions (gen_ai.*)
    - Generic observability attributes (workflow.*, user.*, session.*, tool.*, etc.)
    - SDK-specific extensions (msgtrace.custom.*)
    - Operation metadata (chat, tool, agent)
    - Model information
    - Token usage and costs (gen_ai.usage.*)
    - Tool calls and responses
    - Agent workflows
    - Custom business metrics
    """

    # ========== Operation Attributes (GenAI) ==========

    @staticmethod
    def set_operation_name(operation: str):
        """
        Set the operation name.

        Args:
            operation: Operation type (e.g., 'chat', 'tool', 'agent', 'embedding')

        Example:
            MsgTraceAttributes.set_operation_name("chat")
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.operation.name", operation)

    @staticmethod
    def set_system(system: str):
        """
        Set the GenAI system.

        Args:
            system: System name (e.g., 'openai', 'anthropic', 'langchain')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.system", system)

    # ========== Request Attributes (GenAI) ==========

    @staticmethod
    def set_model(model: str):
        """
        Set the model name.

        Args:
            model: Model identifier (e.g., 'gpt-4', 'claude-3-opus')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.model", model)

    @staticmethod
    def set_temperature(temperature: float):
        """Set model temperature parameter."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.temperature", temperature)

    @staticmethod
    def set_top_p(top_p: float):
        """Set model top_p parameter."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.top_p", top_p)

    @staticmethod
    def set_max_tokens(max_tokens: int):
        """Set max tokens parameter."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.max_tokens", max_tokens)

    @staticmethod
    def set_frequency_penalty(penalty: float):
        """Set frequency penalty parameter."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.frequency_penalty", penalty)

    @staticmethod
    def set_presence_penalty(penalty: float):
        """Set presence penalty parameter."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.presence_penalty", penalty)

    # ========== Response Attributes (GenAI) ==========

    @staticmethod
    def set_response_id(response_id: str):
        """Set response ID from API."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.response.id", response_id)

    @staticmethod
    def set_response_model(model: str):
        """Set actual model used in response."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.response.model", model)

    @staticmethod
    def set_finish_reason(reason: str):
        """
        Set finish reason.

        Args:
            reason: Reason (e.g., 'stop', 'length', 'tool_calls', 'content_filter')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.response.finish_reasons", [reason])

    # ========== Usage Attributes (GenAI) ==========

    @staticmethod
    def set_usage(
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
    ):
        """
        Set token usage.

        Args:
            input_tokens: Input/prompt tokens
            output_tokens: Output/completion tokens
            total_tokens: Total tokens (if not provided, calculated)
        """
        span = trace.get_current_span()
        if span.is_recording():
            if input_tokens is not None:
                span.set_attribute("gen_ai.usage.input_tokens", input_tokens)

            if output_tokens is not None:
                span.set_attribute("gen_ai.usage.output_tokens", output_tokens)

            # Calculate total if not provided
            if total_tokens is None and input_tokens and output_tokens:
                total_tokens = input_tokens + output_tokens

            if total_tokens is not None:
                span.set_attribute("gen_ai.usage.total_tokens", total_tokens)

    # ========== Prompt Attributes (GenAI) ==========

    @staticmethod
    def set_prompt(prompt: str | list[dict[str, Any]]):
        """
        Set prompt content.

        Args:
            prompt: Prompt as string or messages array
        """
        span = trace.get_current_span()
        if span.is_recording():
            if isinstance(prompt, str):
                span.set_attribute("gen_ai.prompt", prompt)
            else:
                # Serialize messages to JSON
                span.set_attribute("gen_ai.prompt", json.dumps(prompt))

    @staticmethod
    def set_completion(completion: str):
        """Set completion/response text."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.completion", completion)

    # ========== Tool Attributes (GenAI) ==========

    @staticmethod
    def set_tool_name(name: str):
        """Set tool name."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.tool.name", name)

    @staticmethod
    def set_tool_description(description: str):
        """Set tool description."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.tool.description", description)

    @staticmethod
    def set_tool_call_id(call_id: str):
        """Set tool call ID."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.tool.call.id", call_id)

    @staticmethod
    def set_tool_call_arguments(arguments: str | dict[str, Any]):
        """
        Set tool call arguments.

        Args:
            arguments: Arguments as string or dict
        """
        span = trace.get_current_span()
        if span.is_recording():
            if isinstance(arguments, str):
                span.set_attribute("gen_ai.tool.call.arguments", arguments)
            else:
                span.set_attribute("gen_ai.tool.call.arguments", json.dumps(arguments))

    @staticmethod
    def set_tool_response(response: str | dict[str, Any]):
        """
        Set tool response.

        Args:
            response: Response as string or dict
        """
        span = trace.get_current_span()
        if span.is_recording():
            if isinstance(response, str):
                span.set_attribute("gen_ai.tool.response", response)
            else:
                span.set_attribute("gen_ai.tool.response", json.dumps(response))

    # ========== Agent Attributes (GenAI) ==========

    @staticmethod
    def set_agent_name(name: str):
        """Set agent name."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.agent.name", name)

    @staticmethod
    def set_agent_id(agent_id: str):
        """Set agent ID."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.agent.id", agent_id)

    @staticmethod
    def set_agent_type(agent_type: str):
        """Set agent type (e.g., 'conversational', 'task', 'autonomous')."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.agent.type", agent_type)

    @staticmethod
    def set_agent_goal(goal: str):
        """Set agent goal/objective."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.agent.goal", goal)

    # ========== Provider-Specific Attributes (GenAI) ==========

    @staticmethod
    def set_provider_name(provider: str):
        """
        Set provider name.

        Args:
            provider: Provider (e.g., 'openai', 'anthropic', 'google', 'cohere')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.provider.name", provider)

    @staticmethod
    def set_endpoint(endpoint: str):
        """Set API endpoint URL."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.request.endpoint", endpoint)

    # ========== Embedding Attributes (GenAI) ==========

    @staticmethod
    def set_embedding_dimensions(dimensions: int):
        """Set embedding vector dimensions."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.embedding.dimensions", dimensions)

    @staticmethod
    def set_embedding_format(format: str):
        """Set embedding format (e.g., 'float', 'base64')."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.embedding.format", format)

    # ========== Cost Attributes (GenAI) ==========

    @staticmethod
    def set_cost(
        input_cost: float | None = None,
        output_cost: float | None = None,
        currency: str = "USD",
    ):
        """
        Set cost information.

        Args:
            input_cost: Input/prompt cost (cost per input tokens)
            output_cost: Output/completion cost (cost per output tokens)
            currency: Currency code (default: USD)
        """
        span = trace.get_current_span()
        if span.is_recording():
            if input_cost is not None:
                span.set_attribute("gen_ai.usage.cost.input_tokens", input_cost)

            if output_cost is not None:
                span.set_attribute("gen_ai.usage.cost.output_tokens", output_cost)

            span.set_attribute("gen_ai.usage.cost.currency", currency)

    # ========== Tool Calling Metadata ==========

    @staticmethod
    def set_tool_callings(callings: list[dict[str, Any]]):
        """
        Set tool callings array.

        Args:
            callings: List of tool call objects with id, name, arguments
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("tool.callings", json.dumps(callings))

    @staticmethod
    def set_tool_responses(responses: list[dict[str, Any]]):
        """
        Set tool responses array.

        Args:
            responses: List of tool response objects
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("tool.responses", json.dumps(responses))

    # ========== Workflow Attributes ==========

    @staticmethod
    def set_workflow_name(name: str):
        """Set workflow/flow name."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("workflow.name", name)

    @staticmethod
    def set_workflow_id(workflow_id: str):
        """Set workflow ID."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("workflow.id", workflow_id)

    @staticmethod
    def set_workflow_step(step: str):
        """Set current workflow step."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("workflow.step", step)

    # ========== User/Session Attributes ==========

    @staticmethod
    def set_user_id(user_id: str):
        """Set user ID."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("user.id", user_id)

    @staticmethod
    def set_session_id(session_id: str):
        """Set session ID."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("session.id", session_id)

    # ========== Custom Metrics ==========

    @staticmethod
    def set_latency(latency_ms: float):
        """
        Set custom latency metric.

        Args:
            latency_ms: Latency in milliseconds
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("latency.ms", latency_ms)

    @staticmethod
    def set_retry_count(count: int):
        """Set retry count."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("retry.count", count)

    @staticmethod
    def set_cache_hit(hit: bool):
        """Set cache hit/miss."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("cache.hit", hit)

    # ========== Environment Attributes ==========

    @staticmethod
    def set_environment(env: str):
        """
        Set environment.

        Args:
            env: Environment (e.g., 'dev', 'staging', 'prod')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("environment", env)

    @staticmethod
    def set_version(version: str):
        """Set application version."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("version", version)

    # ========== Module Attributes ==========

    @staticmethod
    def set_module_name(name: str):
        """
        Set module name.

        Args:
            name: Module name (e.g., 'vector_search', 'intent_classifier')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("module.name", name)

    @staticmethod
    def set_module_type(module_type: str):
        """
        Set module type for specialized visualizations.

        Args:
            module_type: Type (e.g., 'Agent', 'Tool', 'LLM', 'Transcriber', 'Retriever')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("module.type", module_type)

    # ========== Extended Tool Attributes ==========

    @staticmethod
    def set_tool_execution_type(execution_type: str):
        """
        Set tool execution type.

        Args:
            execution_type: Execution type (e.g., 'local', 'remote')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.tool.execution.type", execution_type)

    @staticmethod
    def set_tool_protocol(protocol: str):
        """
        Set tool protocol.

        Args:
            protocol: Protocol (e.g., 'mcp', 'a2a', 'http', 'grpc')
        """
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("gen_ai.tool.protocol", protocol)

    # ========== Extended Agent Attributes ==========

    @staticmethod
    def set_agent_response(response: str | dict[str, Any]):
        """
        Set agent response content.

        Args:
            response: Agent response as string or dict
        """
        span = trace.get_current_span()
        if span.is_recording():
            if isinstance(response, str):
                span.set_attribute("gen_ai.agent.response", response)
            else:
                span.set_attribute("gen_ai.agent.response", json.dumps(response))

    # ========== Generic Custom Attributes (MsgTrace) ==========

    @staticmethod
    def set_custom(key: str, value: Any):
        """
        Set custom attribute with user-defined key.

        Args:
            key: Attribute key (used as-is, no prefix)
            value: Attribute value (dicts/lists are JSON-serialized)
        """
        span = trace.get_current_span()
        if span.is_recording():
            # Handle different types
            if isinstance(value, (dict, list)):
                span.set_attribute(key, json.dumps(value))
            else:
                span.set_attribute(key, value)
