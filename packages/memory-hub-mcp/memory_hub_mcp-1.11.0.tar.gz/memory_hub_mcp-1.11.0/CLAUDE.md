# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Memory Hub MCP Server is a local memory system for AI agents using the Model Context Protocol (MCP). It provides vector-based storage and retrieval through:
- **stdio transport**: For local MCP clients (ZenCoder, Claude Code)
- **HTTP REST API**: For remote agents with authenticated access (v1.8.0+)

## Essential Commands

### Development Setup
```bash
# Setup development environment
uv venv
source .venv/bin/activate
uv pip install -e .

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Running the Server

**stdio MCP Server (for local clients):**
```bash
# Run with default settings
memory-hub-mcp

# Run with custom configuration
memory-hub-mcp --log-level DEBUG --qdrant-url http://localhost:6333 --lm-studio-url http://localhost:1234/v1

# Run with UVX (recommended for distribution)
uvx memory-hub-mcp
```

**HTTP REST API Server (for remote agents):**
```bash
# Run with default settings (port 8080)
memory-hub-http

# Run with custom configuration
memory-hub-http --port 8080 \
  --qdrant-url http://192.168.12.239:6333 \
  --lm-studio-url http://192.168.12.239:1234/v1 \
  --users-config config/users.yaml \
  --log-level INFO

# API documentation available at http://localhost:8080/docs
# Logs written to /tmp/memory-hub-http.log
```

### Development and Testing
```bash
# Code formatting and linting
black src/
ruff check src/

# Build distribution
uv build

# Publish to PyPI (requires token)
UV_PUBLISH_TOKEN=<token> uv publish dist/*
```

### Docker Environment
```bash
# Start Qdrant dependency
docker-compose up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up
```

## Architecture

### Core Components

**Server Implementations:**
1. **stdio MCP Server** (`src/memory_hub/mcp_server.py`): Local MCP protocol over stdio
2. **HTTP REST API** (`src/memory_hub/http_server.py`): Remote FastAPI server with authentication (v1.8.0+)
3. **stdio CLI** (`src/memory_hub/cli.py`): Entry point for stdio MCP server
4. **HTTP CLI** (`src/memory_hub/http_cli.py`): Entry point for HTTP REST API server

**Core Services:**
5. **Core Services** (`src/memory_hub/core/services.py`): Qdrant client and LM Studio integration
6. **Authentication** (`src/memory_hub/core/auth.py`): User-based auth with hierarchical path authorization
7. **Handlers** (`src/memory_hub/core/handlers/`): Business logic (shared by both transports)
8. **Models** (`src/memory_hub/core/models.py`): Pydantic data models

### Key Design Patterns

- **Dual transport**: stdio MCP for local clients, HTTP REST API for remote agents
- **Shared handlers**: Same business logic for both transports
- **Hierarchical memory**: 4-level structure: app_id → project_id → ticket_id → run_id
- **Path-based authorization**: Wildcard patterns for flexible access control (HTTP only)
- **Hybrid search**: Vector similarity + keyword matching + LLM synthesis
- **Async-first**: All operations use async/await patterns

### External Dependencies

- **Qdrant**: Vector database for embeddings storage
- **LM Studio**: Provides embeddings and chat completions
- **MCP Protocol**: stdio transport for client communication

## MCP Tools Available

1. **add_memory**: Store content with hierarchical metadata
2. **search_memories**: Semantic search with keyword enhancement
3. **get_project_memories**: Retrieve ALL memories for a specific app_id/project_id without search queries
4. **update_memory**: Update existing memories with automatic version incrementing
5. **get_recent_memories**: Retrieve memories from the last N hours (perfect for resuming work)
6. **list_app_ids**: List all application identifiers
7. **list_project_ids**: List all project identifiers
8. **list_ticket_ids**: List all ticket identifiers
9. **list_memory_types**: List memory types currently in use (with counts and metadata)
10. **get_memory_type_guide**: Get the recommended memory type conventions
11. **health_check**: Server health verification
12. **delete_run_memories**: Delete all memories for a specific run_id (requires exact 4-level match)
13. **get_version**: Get current server version
14. **session_resume**: Get full context for starting/resuming work (session state + handoff + recent memories)
15. **session_handoff**: Store comprehensive handoff and update session atomically
16. **session_update**: Quick checkpoint for commits, decisions, or focus changes

## Session Management (v1.10.0+)

Memory Hub provides atomic session management endpoints that handle all session logic server-side. Agents only need to know `app_id` and `project_id` - Memory Hub handles everything else.

**Core Rule**: One session per project (`app_id` + `project_id` = unique session)

### Session State Schema

```json
{
  "active_ticket": "smart-actions-testing",
  "focus": "Current work focus",
  "decisions": ["decision 1", "decision 2"],
  "blockers": [],
  "next_steps": ["next step 1", "next step 2"],
  "last_commits": ["abc123: Fix auth bug", "def456: Add tests"],
  "last_handoff_at": "2025-12-05T22:00:00Z",
  "ticket_history": {
    "smart-actions-testing": "2025-12-06T14:00:00Z",
    "auth-flow": "2025-12-05T10:00:00Z"
  },
  "created_at": "2025-12-05T10:00:00Z",
  "updated_at": "2025-12-06T14:00:00Z"
}
```

### Session Workflows

**1. Starting Work (session_resume)**
```python
session_resume(app_id="covenant", project_id="portal", handoff_limit=1)
# Returns:
# - session_state: Current session state (includes ticket_history)
# - handoffs: List of recent handoffs from ALL tickets (not just active_ticket)
# - recent_memories: Recent memories from active_ticket (24h, limit 10)
# - is_new_session: True if session was just created
#
# handoff_limit: Number of handoffs to retrieve (default 1, max 10)
```

**Key behavior:** Handoffs are retrieved from ALL tickets in the project, so even if the last handoff was stored at a different ticket, you'll still get it.

**2. Ending Work (session_handoff)**
```python
session_handoff(
    app_id="covenant",
    project_id="portal",
    summary="Completed JWT auth. Tests passing. Next: add refresh tokens.",
    session_updates={
        "focus": "JWT refresh tokens",
        "next_steps": ["Add refresh endpoint", "Update docs"],
        "decisions": ["Use RS256 for signing"]
    }
)
# Atomically: stores handoff memory + updates session state
```

**3. Quick Checkpoint (session_update)**
```python
session_update(
    app_id="covenant",
    project_id="portal",
    updates={
        "last_commits": ["a1b2c3d: Fix JWT expiry"],
        "decisions": ["Store refresh tokens in Redis"]
    }
)
# Partial update - only specified fields are changed
```

### When to Use Each

| Scenario | Tool | Example |
|----------|------|---------|
| Agent starting work | `session_resume` | Load context at conversation start |
| After 3+ git commits | `session_update` | Save commit history |
| Making key decisions | `session_update` | Record architectural choices |
| Switching tickets | `session_update` | Change `active_ticket` |
| Context about to clear | `session_handoff` | Comprehensive end-of-session save |

### Allowed Session Update Fields

`session_update` only allows these fields:
- `active_ticket` - Currently active ticket_id
- `focus` - Current work focus (free-form text)
- `decisions` - Key decisions made (list of strings)
- `blockers` - Current blockers (list of strings)
- `next_steps` - Planned next actions (list of strings)
- `last_commits` - Recent commits (list of strings, max 5)

## Memory Retrieval Optimization

### Return Format Control

Both `get_project_memories` and `get_recent_memories` support a `return_format` parameter for optimizing token usage:

**Options:**
- `summary_only`: AI-generated summary only (~80% token reduction)
- `chunks_only`: Raw memory chunks without summarization
- `both`: Summary + chunks (default, backward compatible)

### Agent Usage Patterns

**1. Starting New Work** (use `summary_only`):
```python
get_project_memories(
    app_id="crossroads",
    return_format="summary_only"
)
# Returns: Concise overview, ~500-800 tokens vs ~3,000 tokens
```

**2. Deep Implementation** (use `chunks_only`):
```python
get_project_memories(
    app_id="crossroads",
    project_id="auth",
    return_format="chunks_only"
)
# Returns: Exact content, no LLM interpretation
# Use when extracting specific data, code, or facts
```

**3. Exploration/Debugging** (use `both`):
```python
get_project_memories(
    app_id="crossroads",
    return_format="both"
)
# Returns: Summary + full chunks for reference
```

### Token Efficiency Examples

| Memories | Format | Approx Tokens |
|----------|--------|---------------|
| 10 app-level | both | ~3,000 |
| 10 app-level | summary_only | ~600 |
| 50 project-level | both | ~15,000 |
| 50 project-level | summary_only | ~2,000 |

**Best Practice:** Default to `summary_only` for initial context loading, then request `chunks_only` when you need specific details.

## Chunking Control (v1.6.0+)

The `chunking` parameter on `add_memory` controls whether content is semantically chunked or stored as a single unit.

### When to Disable Chunking (`chunking=false`)

Use `chunking=false` for:
- **AutoStack plans**: Large markdown documents that should be retrieved as complete units
- **Specifications**: Technical documents that need to be read in full
- **Structured data**: JSON/YAML configs that should remain intact
- **Long-form content**: Articles, reports, or documentation that don't benefit from semantic chunking

### Performance Benefits

- **20-30x fewer embedding calls**: Single embedding vs 20-30 chunks
- **Faster storage**: Skip chunking overhead (~100ms saved)
- **Simpler retrieval**: No reassembly needed, single chunk returned

### Usage Example

```python
# AutoStack planning agent storing a plan
add_memory(
    content=full_plan_markdown,  # e.g., 2000-token plan
    metadata={
        "app_id": "covenant",
        "project_id": "portal",
        "ticket_id": "auth-flow",
        "type": "plan"
    },
    chunking=False  # ← Store as single unit
)
# Result: 1 chunk stored instead of 25 chunks
```

### Default Behavior (`chunking=true`)

Most memories should use default chunking for optimal semantic search:
```python
# Normal memory (code changes, decisions, etc.)
add_memory(
    content="Implemented JWT authentication with refresh tokens...",
    metadata={
        "app_id": "covenant",
        "project_id": "auth",
        "type": "feature_implementation"
    }
    # chunking=True by default - will create ~5-10 chunks
)
```

**Tradeoff**: Large single embeddings are less semantically precise for search, but perfect for documents that need to be retrieved whole.

## Configuration

### Environment Variables
- `QDRANT_URL`: Qdrant server URL (default: http://localhost:6333)
- `LM_STUDIO_BASE_URL`: LM Studio base URL (default: http://localhost:1234/v1)
- `MIN_SCORE_THRESHOLD`: Minimum similarity score for results (default: 0.60)
- `ENABLE_GEMMA_SUMMARIZATION`: Enable LLM summarization (default: true)

### CLI Arguments
- `--qdrant-url`: Override Qdrant URL
- `--lm-studio-url`: Override LM Studio URL
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `--users-config`: Path to users YAML file (HTTP server only, default: config/users.yaml)
- `--host`: HTTP server bind address (default: 0.0.0.0)
- `--port`: HTTP server port (default: 8080)

## HTTP Authentication & Authorization (v1.8.0+)

### User Configuration

HTTP server requires authentication via `config/users.yaml`:

```yaml
users:
  manus:
    status: active  # active | blocked | suspended
    is_admin: false
    allowed_paths:
      - ["manus-autostack", "buildout", "*", "*"]  # All tickets/runs in this project
    allowed_tools:
      - add_memory
      - get_project_memories
      - search_memories
      - update_memory
      - get_recent_memories

  matt:
    status: active
    is_admin: true
    allowed_paths: []  # Empty = all access (admin only)
    allowed_tools: []  # Empty = all tools (admin only)
```

### Path Authorization Patterns

**Pattern syntax:**
- `["app"]` - App-level only (no projects/tickets/runs)
- `["app", "*"]` - App + all projects (no deeper)
- `["app", "proj", "*"]` - App + project + all tickets (no runs)
- `["app", "proj", "ticket", "*"]` - Specific ticket + all runs
- `["app", "*", "*", "*"]` - Everything under app

**Matching rules:**
- Trailing wildcards are optional (requests can stop before reaching them)
- Pattern `["app", "proj", "*", "*"]` matches:
  - ✅ `["app", "proj"]` (app + project)
  - ✅ `["app", "proj", "ticket"]` (+ ticket)
  - ✅ `["app", "proj", "ticket", "run"]` (all 4 levels)

### HTTP Authentication

All endpoints (except `/api/health` and `/api/version`) require authentication:

```bash
# Include user handle in X-Memory-Hub-User header
curl -H "X-Memory-Hub-User: manus" http://localhost:8080/api/add_memory
```

**Authorization checks:**
1. User exists and status is `active`
2. Tool is in user's `allowed_tools` list
3. Requested path matches user's `allowed_paths` patterns

### Admin Users

Admin users (`is_admin: true`) bypass all authorization:
- Can access all paths (empty `allowed_paths`)
- Can use all tools (empty `allowed_tools`)
- See all results from list endpoints

### Exposing HTTP Server for Remote Access

Use LocalCan or ngrok to expose the HTTP server:

```bash
# Using LocalCan
localcan http 8080

# Using ngrok
ngrok http 8080
```

Remote agents can then access via the public URL:
```bash
curl -H "X-Memory-Hub-User: manus" \
  https://memory-hub-http-09.beta.localcan.dev/api/add_memory \
  -d '{"content": "...", "metadata": {...}}'
```

## Development Notes

### Important File Locations
- `src/memory_hub/mcp_server.py`: stdio MCP server implementation
- `src/memory_hub/http_server.py`: HTTP REST API server (v1.8.0+)
- `src/memory_hub/cli.py`: stdio server CLI entry point
- `src/memory_hub/http_cli.py`: HTTP server CLI entry point (v1.8.0+)
- `src/memory_hub/core/auth.py`: Authentication & authorization (v1.8.0+)
- `src/memory_hub/core/config.py`: Configuration constants and environment variables
- `src/memory_hub/core/chunking.py`: Semantic text chunking implementation
- `src/memory_hub/core/utils/search_utils.py`: Search enhancement utilities
- `config/users.yaml`: User authentication config for HTTP server
- `pyproject.toml`: Package configuration and dependencies

### Testing Considerations
- No formal test suite currently exists
- Manual testing requires running Qdrant and LM Studio locally
- Debug script available: `debug_memory_hub.py`

### Version Management
- Version defined in `pyproject.toml`
- Must increment for PyPI publishing
- Semantic versioning: MAJOR.MINOR.PATCH

## Hierarchical Memory Structure

Memory Hub enforces a strict 4-level hierarchy with validation:

**Hierarchy Levels:**
1. `app_id` (Application/Product level)
2. `project_id` (Feature area within app)
3. `ticket_id` (Specific feature/task, maps to git branch in AutoStack)
4. `run_id` (Individual execution, maps to git commit in AutoStack)

**Rules:**
- `app_id` is always required
- `project_id` requires `app_id` (cannot specify project without app)
- `ticket_id` requires both `app_id` AND `project_id` (cannot specify ticket without both)
- `run_id` requires `app_id` + `project_id` + `ticket_id` (cannot specify run without all three parents)

**Children Depth Control:**

Both `get_project_memories` and `get_recent_memories` support `children_depth` to control how many levels of children to include:

| children_depth | Behavior |
|----------------|----------|
| `0` (default) | Only memories at the exact level specified |
| `1` | This level + immediate children |
| `2` | This level + 2 levels down |
| `-1` | All children (unlimited depth) |

**Examples at project_id level:**
- `children_depth=0` → Project-level memories only
- `children_depth=1` → Project + tickets (no runs)
- `children_depth=2` or `-1` → Project + tickets + runs

**Examples at app_id level:**
- `children_depth=0` → App-level memories only
- `children_depth=1` → App + projects (no tickets/runs)
- `children_depth=2` → App + projects + tickets (no runs)
- `children_depth=-1` → Everything in the app

## Agent Usage Patterns

### For Agents Saving Progress
When an agent needs to save work progress:
```
1. Use add_memory with:
   - app_id: Your application/domain (e.g., "eatzos", "motiv")
   - project_id: Specific project/feature (e.g., "next", "enhanced-chat")
   - ticket_id: Optional ticket/task identifier (e.g., "auth-flow")
   - run_id: Optional run identifier for multi-run scenarios (e.g., "initial-impl", "fix-validation")
   - type: Type of memory (e.g., "progress", "code_changes", "decisions")
   - content: Detailed progress, decisions, code changes, etc.

2. For updates to existing memories:
   - Use update_memory to increment version automatically
   - Specify app_id, project_id, ticket_id, run_id, and optionally memory_type
   - Provide new_content with the updated information

3. Hierarchy validation:
   - VALID: {app_id: "crossroads"}
   - VALID: {app_id: "crossroads", project_id: "auth"}
   - VALID: {app_id: "crossroads", project_id: "auth", ticket_id: "TICK-123"}
   - VALID: {app_id: "crossroads", project_id: "auth", ticket_id: "TICK-123", run_id: "initial-impl"}
   - INVALID: {project_id: "auth"} ← Missing required app_id
   - INVALID: {ticket_id: "TICK-123"} ← Missing required app_id and project_id
   - INVALID: {run_id: "initial-impl"} ← Missing required app_id, project_id, and ticket_id
```

### For Agents Resuming Work
When an agent needs to continue previous work:
```
1. Use get_project_memories to retrieve ALL context:
   - Specify app_id, project_id, and optionally ticket_id/run_id
   - No need to guess search terms!
   - Automatically gets latest versions
   - Use run_id to retrieve specific execution context (AutoStack multi-run scenarios)

2. Use get_recent_memories to see what changed:
   - Optionally filter by app_id/project_id/ticket_id/run_id
   - Default: last 24 hours
   - Includes AI-generated summary

3. Use search_memories only when:
   - Looking for specific concepts across projects
   - Need keyword-enhanced semantic search
```

### Best Practices for Agent Continuity
1. **Consistent Naming**: Use consistent app_id and project_id across sessions
2. **Meaningful Types**: Use descriptive memory types (e.g., "api_design", "bug_fix", "feature_implementation")
3. **Regular Updates**: Update memories as work progresses, not just at the end
4. **Version Awareness**: The system handles versioning automatically - just update when needed

## AutoStack Usage Patterns

AutoStack is a formalized AI-First development methodology that uses Memory Hub as its state management backbone. Each AutoStack workflow (plan → build → wrap) stores execution state and artifacts at predictable memory addresses.

### Checkpoint Pattern with children_depth=0

AutoStack orchestrators use **exact address matching** to check if work has been done at a specific checkpoint:

```python
# Orchestrator checks if planning is complete
get_project_memories({
  app_id: "covenant",
  project_id: "portal",
  ticket_id: "auth-flow",
  children_depth: 0,  # CRITICAL: Only return ticket-level memories
  memory_types: ["plan"],
  return_format: "chunks_only"  # Skip AI summarization
})

# Returns 0 results if no plan exists → Start planning phase
# Returns plan document if it exists → Skip to build phase
```

**Why children_depth=0 is critical:**
- With `children_depth=-1`: Query returns ticket + all runs → too much data
- With `children_depth=0`: Query returns ONLY ticket-level data → 0 results if checkpoint is empty
- Enables lightweight "does this address have data?" checks

### AutoStack Memory Address Structure

AutoStack uses predictable `ticket_id` + `type` combinations:

```python
# State tracking (orchestrator writes this)
{
  app_id: "covenant",
  project_id: "portal",
  ticket_id: "auth-flow",
  type: "state",
  content: JSON.stringify({ phase: "build", plan_approved: true })
}

# Plan document (planner agent writes this)
{
  ticket_id: "auth-flow",
  type: "plan",
  content: "# Auth Flow Implementation Plan\n..."
}

# Backend results (backend agent writes this)
{
  ticket_id: "auth-flow",
  type: "backend-result",
  content: JSON.stringify({ files_created: [...], tests_passing: true })
}

# Frontend results (frontend agent writes this)
{
  ticket_id: "auth-flow",
  type: "frontend-result",
  content: JSON.stringify({ components: [...], playwright_passed: true })
}

# Wrap results (wrap agent writes this)
{
  ticket_id: "auth-flow",
  type: "wrap-result",
  content: JSON.stringify({ commit_message: "...", staged_files: [...] })
}
```

### Token Optimization for Structured Data

AutoStack stores structured JSON/YAML data that agents need to parse:

```python
# Retrieve plan without AI summarization
get_project_memories({
  app_id: "covenant",
  project_id: "portal",
  ticket_id: "auth-flow",
  children_depth: 0,
  memory_types: ["plan"],
  return_format: "chunks_only"  # Returns verbatim chunks, no LLM processing
})

# Agent concatenates chunks and parses JSON
plan_chunks = response.retrieved_chunks
plan_text = "".join(chunk.text_chunk for chunk in plan_chunks)
plan_data = JSON.parse(plan_text)
```

### Including Children for Context Retrieval

When agents need full project context (including all tickets and runs), use children_depth:

```python
# Planner agent gathering historical context
get_recent_memories({
  app_id: "covenant",
  project_id: "portal",
  children_depth: -1,  # Include all children (tickets + runs)
  hours: 168,  # Last week
  return_format: "summary_only"  # AI summary for quick overview
})
```

### AutoStack Tool Selection Guide

| Use Case | Tool | children_depth | return_format |
|----------|------|----------------|---------------|
| Check if checkpoint exists | `get_project_memories` | `0` | `chunks_only` |
| Retrieve structured artifact | `get_project_memories` | `0` | `chunks_only` |
| Get full project context | `get_project_memories` | `-1` | `summary_only` |
| Resume after interruption | `get_recent_memories` | `-1` | `both` |
| Find specific pattern | `search_memories` | N/A | `both` |

### Complete AutoStack Example

```python
# 1. Orchestrator checks current state
state_result = get_project_memories({
  app_id: "covenant",
  project_id: "portal",
  ticket_id: "auth-flow",
  children_depth: 0,  # Only ticket-level, not runs
  memory_types: ["state"],
  return_format: "chunks_only"
})

if state_result.total_results == 0:
  # No state exists, start from planning
  invoke_agent("autostack-planner")
else:
  # Parse state and resume from checkpoint
  state = JSON.parse(state_result.retrieved_chunks[0].text_chunk)
  if state.phase == "build":
    invoke_agent("autostack-backend")

# 2. Backend agent retrieves plan
plan_result = get_project_memories({
  app_id: "covenant",
  project_id: "portal",
  ticket_id: "auth-flow",
  children_depth: 0,
  memory_types: ["plan"],
  return_format: "chunks_only"
})
plan_text = concatenate_chunks(plan_result.retrieved_chunks)

# 3. Backend agent writes results
add_memory({
  content: JSON.stringify({
    files_created: ["routes/auth.ts"],
    tests_passing: true
  }),
  metadata: {
    app_id: "covenant",
    project_id: "portal",
    ticket_id: "auth-flow",
    type: "backend-result"
  }
})
```

## Troubleshooting

### Common Issues
1. **Qdrant connection errors**: Verify Qdrant is running and accessible
2. **LM Studio timeout**: Check LM Studio is running with appropriate models loaded
3. **Context length errors**: Reduce chunk size or query complexity
4. **Import errors**: Ensure all dependencies installed with `uv pip install -e .`

### Debugging
- Use `--log-level DEBUG` for verbose output
- Check logs:
  - stdio MCP: `/tmp/memory-hub-mcp.log`
  - HTTP server: `/tmp/memory-hub-http.log`
- Check `docker-compose.yml` for service configuration
- HTTP API docs: `http://localhost:8080/docs` (interactive testing)