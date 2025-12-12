# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-12-04

### Added

#### Module Attributes
- `MsgTraceAttributes.set_module_name(name)` - Set module name for better organization (e.g., 'vector_search', 'intent_classifier')
- `MsgTraceAttributes.set_module_type(module_type)` - Set module type for specialized visualizations in msgtrace frontend
  - Supported types: 'Agent', 'Tool', 'LLM', 'Transcriber', 'Retriever', 'Embedder', 'Custom'
  - Enables automatic grouping and type-specific analytics

#### Extended Tool Attributes
- `MsgTraceAttributes.set_tool_execution_type(execution_type)` - Track how tools are executed
  - Values: 'local' (in-process), 'remote' (external service)
  - Useful for performance analysis and debugging
- `MsgTraceAttributes.set_tool_protocol(protocol)` - Track communication protocol used
  - Values: 'mcp' (Model Context Protocol), 'a2a' (Agent-to-Agent), 'http', 'grpc', etc.
  - Enables protocol-specific debugging and monitoring

#### Extended Agent Attributes
- `MsgTraceAttributes.set_agent_response(response)` - Capture agent response content
  - Accepts string or dict (automatically JSON-serialized)
  - Useful for debugging agent behavior and outputs
  - Can be used alongside existing `set_agent_name`, `set_agent_id`, `set_agent_type`

### Benefits
- Better categorization of AI operations by module type
- Enhanced tool execution tracking with protocol and execution type metadata
- Improved agent debugging with response content capture
- Enables specialized visualizations in msgtrace frontend
- Full compatibility with OpenTelemetry GenAI semantic conventions

### Migration Notes
All new attributes follow the same patterns as existing methods:
- Thread-safe through OpenTelemetry's span API
- Only record when span is recording (zero overhead when disabled)
- Automatic JSON serialization for complex types
- Consistent naming with GenAI semantic conventions

## [1.0.0] - 2025-11-26

## [0.1.0] - TBD

### Added
- Initial release
- OpenTelemetry-based tracing for AI applications
- Support for Gen AI semantic conventions
- Automatic token counting and cost calculation
- Tool call tracking and execution monitoring
- Comprehensive test suite
- Full CI/CD automation
- Automated release workflow
- Security validation for releases

[Unreleased]: https://github.com/msgflux/msgtrace-sdk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/msgflux/msgtrace-sdk/releases/tag/v0.1.0
