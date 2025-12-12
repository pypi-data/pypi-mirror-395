# CLAUDE.md - msgtrace-sdk Project Context

This file provides context for Claude Code sessions working on the msgtrace-sdk project.

## Project Overview

**msgtrace-sdk** is a standalone OpenTelemetry-based tracing SDK for AI applications. It provides a drop-in replacement for msgflux telemetry with the same API, enabling developers to instrument AI operations (chat, tool calls, agents, embeddings) with minimal code changes.

**Key Features**:
- OpenTelemetry Gen AI semantic conventions (`gen_ai.*` attributes)
- Unified `MsgTraceAttributes` class with 60+ attributes
- Context managers and decorators for sync/async operations
- Thread-safe lazy initialization with zero overhead when disabled
- OTLP HTTP export to msgtrace backend

## Project Structure

```
msgtrace-sdk/
├── src/msgtrace/
│   ├── sdk/
│   │   ├── __init__.py         # Public API exports
│   │   ├── attributes.py       # MsgTraceAttributes class
│   │   ├── spans.py            # Spans context managers & decorators
│   │   └── tracer.py           # TracerManager singleton
│   ├── version.py              # Single source of truth for version
│   └── __init__.py
├── tests/                       # 69 tests (pytest)
├── examples/
│   └── basic_usage.py          # Executable examples
├── .github/workflows/           # CI/CD automation
│   ├── ci.yml                  # Lint, format, test
│   ├── validate-version-bump.yml
│   ├── auto-tag.yml            # Auto-tag on version changes
│   └── publish.yml             # Auto-publish to PyPI
├── README.md                    # Complete documentation (consolidated)
├── CONTRIBUTING.md              # Developer workflow
├── CHANGELOG.md                 # Version history
├── ROADMAP.md                   # Future features (v0.2.0+)
├── pyproject.toml               # Package config (dynamic versioning)
└── CLAUDE.md                    # This file
```

## Technology Stack

- **Python**: 3.10+ (tested on 3.10, 3.11, 3.12, 3.13)
- **Package Manager**: uv (modern, fast alternative to pip)
- **Build Backend**: hatchling (dynamic versioning from version.py)
- **Linter/Formatter**: ruff (10-100x faster than black/pylint)
- **Testing**: pytest (69 tests, 100% passing)
- **CI/CD**: GitHub Actions (xAI-inspired workflow)
- **OpenTelemetry**: SDK core (tracer, spans, attributes)

## Important Configuration

### pyproject.toml
- **Dynamic versioning**: `dynamic = ["version"]` + `[tool.hatch.version]` reads from `src/msgtrace/version.py`
- **Dependencies**: Use `[dependency-groups]` (uv's modern approach), NOT `[project.optional-dependencies]`
- **Build system**: hatchling with `packages = ["src/msgtrace"]`

### src/msgtrace/sdk/tracer.py (Line 110-111)
```python
# IMPORTANT: Backend expects this exact endpoint (Jaeger/OTLP standard)
endpoint = os.getenv("MSGTRACE_OTLP_ENDPOINT", "http://localhost:8000/api/v1/traces/export")
```

### src/msgtrace/sdk/attributes.py
```python
# IMPORTANT: set_custom() uses user keys directly (no prefix)
def set_custom(key: str, value: Any):
    # Uses key as-is, NOT 'msgtrace.custom.' prefix
    span.set_attribute(key, value)
```

## CI/CD Workflow (xAI-Inspired)

The project uses an **automated CI/CD pipeline** inspired by xAI's Python SDK:

1. **On PR**: Run tests + validate version bump in `src/msgtrace/version.py`
2. **On merge to main**: Auto-tag when version changes detected
3. **On tag push**: Auto-publish to TestPyPI then PyPI

**Key files**:
- `.github/workflows/ci.yml` - Lint (ruff), format check, pytest on Python 3.10-3.13
- `.github/workflows/validate-version-bump.yml` - Ensures version bumps on PRs
- `.github/workflows/auto-tag.yml` - Creates git tags on version changes
- `.github/workflows/publish.yml` - Publishes to PyPI on tag push

**Local testing**:
```bash
act -j test  # Requires Docker + act CLI
```

## Common Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --group dev

# Add new dependency
uv add <package>

# Add dev dependency
uv add <package> --group dev
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/msgtrace --cov-report=term-missing

# Run specific test
uv run pytest tests/test_attributes.py -v
```

### Linting and Formatting
```bash
# Check formatting
uv run ruff format --check .

# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .
```

### Version Management
```bash
# Update version (ONLY file to change)
vim src/msgtrace/version.py

# Bump patch: 0.1.0 -> 0.1.1 (bug fixes)
# Bump minor: 0.1.0 -> 0.2.0 (new features, backward compatible)
# Bump major: 0.1.0 -> 1.0.0 (breaking changes)
```

### Git Workflow
```bash
# IMPORTANT: NEVER use 'git add -A'
# Always stage files individually
git add file1.py file2.py file3.py

# Create feature branch
git checkout -b feat/your-feature

# Commit with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"

# Push and create PR
git push -u origin feat/your-feature
gh pr create --title "feat: add new feature" --body "Description"
```

## Key Design Decisions

### 1. Documentation Consolidation (All in README.md)
- **Decision**: Keep all documentation in README.md instead of separate docs/ directory
- **Rationale**: Project is small enough that separate documentation adds maintenance overhead
- **User quote**: "ótimo, nesse caso remova por inteiro a documentação"

### 2. Custom Attributes Without Prefix
- **Decision**: `set_custom(key, value)` uses user keys directly (no `msgtrace.custom.` prefix)
- **Rationale**: Maximum flexibility for users to define their own namespaces
- **User quote**: "em 'set_custom' metodo em attributes tem um prefix de custom msgtrace, retire, use a key do usuario direto"

### 3. Dynamic Versioning
- **Decision**: Use hatchling to read version from `src/msgtrace/version.py`
- **Rationale**: Single source of truth, auto-tag workflow reads same file
- **Configuration**: `dynamic = ["version"]` in pyproject.toml

### 4. OTLP Endpoint Standard
- **Decision**: Use `/api/v1/traces/export` as default endpoint
- **Rationale**: Matches Jaeger/OTLP standard and msgtrace backend implementation
- **User quote**: "no outro projeto o msgtrace, lá eu pedi a uma outra instância do claude para olhar os padrões de como o jaeger e outros definem o endpoint de export"

### 5. Executable Examples
- **Decision**: All code examples must include mock functions and be fully executable
- **Rationale**: Reproducibility and ease of testing for users
- **User quote**: "eu só mudaria o quickstart e demais onde tem 'chat_completion(...)' escreva uma fn mock para isso, é importante que tudo seja executável"

### 6. Span Naming Conventions
- **Decision**: Document `module.type` and `module.name` conventions for frontend visualizations
- **Common types**: Agent, Tool, LLM, Transcriber, Retriever, Embedder, Custom
- **Rationale**: Enables msgtrace frontend to render specialized visualizations
- **User quote**: "pode adicionar no readme sobre as convenções de uso de module name e module type, eles são usadas principalmente para gerar visualizações específicas no frontend"

## GenAI Semantic Conventions

The SDK follows OpenTelemetry GenAI semantic conventions:

### Standard Attributes (`gen_ai.*`)
- `gen_ai.operation.name` - Operation type (chat, tool, agent, embedding)
- `gen_ai.request.model` - Model name (e.g., gpt-5, claude-3-opus)
- `gen_ai.usage.input_tokens` / `output_tokens` / `total_tokens`
- `gen_ai.usage.cost.input_tokens` / `output_tokens` / `currency`
- `gen_ai.agent.name` / `agent.id` / `agent.type`
- `gen_ai.tool.name` / `tool.description` / `tool.call.id`
- `gen_ai.prompt` / `gen_ai.completion`

### Generic Observability Attributes
- `workflow.name` / `workflow.id` / `workflow.step`
- `user.id` / `session.id`
- `environment` / `version`
- `cache.hit` / `retry.count` / `latency.ms`

### Module Type Conventions (Frontend Visualizations)
Use `MsgTraceAttributes.set_custom("module.type", "Agent")` to categorize spans:

| Module Type | Description | Visualization |
|------------|-------------|---------------|
| Agent | Autonomous decision-making agents | Agent graph, workflow diagram |
| Tool | External tool calls (API, search, calculator) | Tool execution timeline |
| LLM | Large language model calls (chat, completion) | Token usage, cost analysis |
| Transcriber | Audio/video transcription | Transcription duration, word count |
| Retriever | Vector search, database queries | Retrieval metrics, relevance |
| Embedder | Text embedding generation | Embedding dimensions, batch size |
| Custom | Application-specific operations | Generic span view |

## Important Notes for Future Claude Sessions

### What to NEVER Do
1. **NEVER use `git add -A`** - Always stage files individually by name
2. **NEVER add `msgtrace.custom.` prefix** to custom attributes (removed in current implementation)
3. **NEVER use outdated model names** - Use `gpt-5` (not gpt-4, gpt-4o)
4. **NEVER forget imports in examples** - All code blocks must be fully executable
5. **NEVER create non-executable examples** - Add mock functions where needed

### What to ALWAYS Do
1. **ALWAYS stage files individually**: `git add file1.py file2.py`
2. **ALWAYS use `/api/v1/traces/export` for OTLP endpoint** (not `/v1/traces`)
3. **ALWAYS make code examples executable** with mock functions
4. **ALWAYS include all necessary imports** in code examples
5. **ALWAYS update CHANGELOG.md** when making changes
6. **ALWAYS run tests** before committing: `uv run pytest`
7. **ALWAYS use conventional commits**: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

### Testing Before Commits
```bash
# Run full test suite
uv run pytest

# Run with coverage
uv run pytest --cov=src/msgtrace --cov-report=term-missing

# Check formatting
uv run ruff format --check .

# Check linting
uv run ruff check .

# Test example files
uv run python examples/basic_usage.py
```

### User Preferences
- **Separate code blocks** for different installation methods (easier to copy-paste)
- **Executable examples** with mock functions (reproducibility)
- **Individual file staging** (NOT `git add -A`)
- **Uppercase filenames** when specified (e.g., API.md not api.md)
- **Modern model references** (gpt-5, not gpt-4)
- **Complete imports** in all code examples

## Related Projects

- **msgtrace**: OpenTelemetry observability platform for AI applications (backend + frontend)
  - Location: `/home/vilson-neto/Documents/msg-projects/msgtrace`
  - Backend: FastAPI on port 8000
  - Frontend: React + TypeScript
  - Database: SQLite with WAL mode
  - OTLP endpoint: `http://localhost:8000/api/v1/traces/export`

## Current Status (as of last conversation)

- **Branch**: `feat/improve-ci-workflow`
- **Commits**: 21 commits ready for PR
- **Tests**: 69 tests, 100% passing (0.46s)
- **Documentation**: Fully consolidated in README.md
- **CI/CD**: xAI-inspired workflows configured
- **Version**: 0.1.0 (dynamic versioning via hatchling)
- **Next Step**: Create PR when user confirms

## Future Roadmap (v0.2.0)

See `ROADMAP.md` for detailed implementation plans:

- **Trace Sampling**: `MSGTRACE_TRACE_SAMPLE_RATE` environment variable
- **Batch Export Configuration**: Fine-tune batch processor settings
- **Custom Samplers**: Parent-based, rate limiting, attribute-based
- **Metrics Support**: Token usage, cost, latency histograms
- **Log Correlation**: Inject trace context into logs

## References

- OpenTelemetry Gen AI Semantic Conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- xAI Python SDK (CI/CD inspiration): https://github.com/xai-org/xai-sdk-python
- uv documentation: https://docs.astral.sh/uv/
- hatchling versioning: https://hatch.pypa.io/latest/version/
- GitHub Actions act tool: https://github.com/nektos/act

---

**Last Updated**: 2025-11-24 (continuation from previous session that ran out of context)
**Branch**: main
